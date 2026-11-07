#!/usr/bin/env python3
"""
Conscious Workflow — Fast Project Mapper & Delta Detector (project_mapper.py)
Scans a directory or unpacked ZIP to produce a token-compact file index,
detect the tech stack, and identify modified files via SHA-256 hashes
so Claude never re-reads unchanged files.
"""

import os
import sys
import json
import hashlib
import argparse
from datetime import datetime

IGNORE_DIRS = {
    ".git", "node_modules", "venv", ".venv", "env", "__pycache__",
    "dist", "build", "out", "target", "bin", "obj", ".next", ".nuxt",
    ".idea", ".vscode", "coverage", ".pytest_cache", ".claude"
}

IGNORE_EXTS = {
    ".pyc", ".pyo", ".exe", ".dll", ".so", ".dylib", ".class",
    ".jpg", ".jpeg", ".png", ".gif", ".ico", ".pdf", ".zip", ".tar", ".gz", ".woff", ".woff2", ".ttf"
}

STACK_MARKERS = {
    "package.json": "Node.js / JavaScript / TypeScript",
    "tsconfig.json": "TypeScript",
    "requirements.txt": "Python",
    "pyproject.toml": "Python (Modern/Poetry/Hatch)",
    "Cargo.toml": "Rust",
    "go.mod": "Go",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java/Kotlin (Gradle)",
    "Dockerfile": "Docker Container",
    "docker-compose.yml": "Docker Compose"
}

ENTRY_PATTERNS = {
    "main.py", "app.py", "server.py", "manage.py", "index.js", "index.ts",
    "main.ts", "server.js", "server.ts", "Program.cs", "main.go", "main.rs", "App.tsx", "App.jsx"
}


def short_hash(filepath: str) -> str:
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()[:8]
    except Exception:
        return "unreadable"


def count_lines(filepath: str) -> int:
    try:
        with open(filepath, "rb") as f:
            return sum(1 for _ in f)
    except Exception:
        return -1


def scan_project(root_path: str):
    root_path = os.path.abspath(root_path)
    files_info = {}
    detected_stacks = set()
    entry_points = []
    config_files = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in sorted(dirnames) if d not in IGNORE_DIRS]
        for fname in sorted(filenames):
            ext = os.path.splitext(fname)[1].lower()
            rel_path = os.path.relpath(os.path.join(dirpath, fname), root_path).replace("\\", "/")
            full_path = os.path.join(dirpath, fname)

            if fname in STACK_MARKERS:
                detected_stacks.add(STACK_MARKERS[fname])
                config_files.append(rel_path)
            elif fname.endswith(".csproj") or fname.endswith(".sln"):
                detected_stacks.add("C# / .NET")
                config_files.append(rel_path)

            if fname in ENTRY_PATTERNS:
                entry_points.append(rel_path)

            if ext in IGNORE_EXTS:
                continue

            lines = count_lines(full_path)
            fhash = short_hash(full_path)
            files_info[rel_path] = {
                "lines": lines,
                "hash": fhash,
                "size": os.path.getsize(full_path)
            }

    return {
        "root": root_path,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "stacks": sorted(detected_stacks),
        "entry_points": entry_points,
        "config_files": config_files,
        "files": files_info
    }


def load_cached_index(root_path: str):
    cache_file = os.path.join(root_path, ".claude", "memory", ".file_cache.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def save_cached_index(root_path: str, scan_data: dict):
    mem_dir = os.path.join(root_path, ".claude", "memory")
    os.makedirs(mem_dir, exist_ok=True)
    cache_file = os.path.join(mem_dir, ".file_cache.json")
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(scan_data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Conscious Workflow Fast Project Mapper")
    parser.add_argument("path", nargs="?", default=".", help="Project root directory")
    parser.add_argument("--diff", action="store_true", help="Show only changed/added/deleted files since last scan")
    parser.add_argument("--save-cache", action="store_true", help="Save file hash snapshot to .claude/memory/.file_cache.json")
    parser.add_argument("--max-files", type=int, default=60, help="Max files to list in compact table")
    args = parser.parse_args()

    current = scan_project(args.path)
    previous = load_cached_index(args.path)

    if args.diff and previous:
        old_files = previous.get("files", {})
        new_files = current["files"]
        added = [p for p in new_files if p not in old_files]
        deleted = [p for p in old_files if p not in new_files]
        modified = [p for p in new_files if p in old_files and new_files[p]["hash"] != old_files[p]["hash"]]
        unchanged_count = len(new_files) - len(added) - len(modified)

        print(f"# DELTA REPORT ({current['timestamp']})")
        print(f"- Unchanged Files (DO NOT RE-READ): {unchanged_count}")
        print(f"- Modified: {len(modified)} | Added: {len(added)} | Deleted: {len(deleted)}\n")
        if modified:
            print("## Modified Files (Inspect Only These):")
            for p in modified:
                print(f"- `{p}` ({new_files[p]['lines']} lines, new hash: `{new_files[p]['hash']}`)")
        if added:
            print("\n## Added Files:")
            for p in added:
                print(f"- `{p}` ({new_files[p]['lines']} lines, hash: `{new_files[p]['hash']}`)")
        if deleted:
            print("\n## Deleted Files:")
            for p in deleted:
                print(f"- `{p}`")
        if not (modified or added or deleted):
            print("No files changed since the last scan. Memory cache is 100% valid.")
    else:
        print(f"# PROJECT MAP ({os.path.basename(current['root'])})")
        print(f"- **Tech Stack:** {', '.join(current['stacks']) or 'Undetermined'}")
        print(f"- **Entry Points:** {', '.join(current['entry_points']) or 'None detected'}")
        print(f"- **Config Files:** {', '.join(current['config_files']) or 'None detected'}")
        print(f"- **Total Source/Text Files:** {len(current['files'])}\n")
        print("| File Path | Lines | Hash |")
        print("| :--- | :---: | :--- |")
        for idx, (path, meta) in enumerate(current["files"].items()):
            if idx >= args.max_files:
                print(f"| *...and {len(current['files']) - args.max_files} more files* | - | - |")
                break
            print(f"| `{path}` | {meta['lines']} | `{meta['hash']}` |")

    if args.save_cache or args.diff:
        save_cached_index(args.path, current)


if __name__ == "__main__":
    main()
