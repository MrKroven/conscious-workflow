#!/usr/bin/env python3
"""
Conscious Workflow — Memory & 3-Strike Loop Guard CLI (memory_guard.py)
Provides deterministic helpers for:
1. Initializing .claude/memory/ files (`init`)
2. Checking whether a file actually changed before re-reading (`check-file`)
3. Recording error signatures and enforcing the 3-Strike Circuit Breaker (`log-error`)
"""

import os
import sys
import json
import hashlib
import argparse
from datetime import datetime


def get_memory_dir(root_path: str = ".") -> str:
    mem_dir = os.path.join(os.path.abspath(root_path), ".claude", "memory")
    os.makedirs(mem_dir, exist_ok=True)
    return mem_dir


def get_state_json_path(root_path: str = ".") -> str:
    return os.path.join(get_memory_dir(root_path), ".guard_state.json")


def load_guard_state(root_path: str = ".") -> dict:
    path = get_state_json_path(root_path)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"read_cache": {}, "error_strikes": {}}


def save_guard_state(state: dict, root_path: str = "."):
    path = get_state_json_path(root_path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def compute_hash(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()[:12]


def cmd_init(root_path: str):
    mem_dir = get_memory_dir(root_path)
    pm_path = os.path.join(mem_dir, "PROJECT_MEMORY.md")
    ss_path = os.path.join(mem_dir, "SESSION_STATE.md")

    if not os.path.exists(pm_path):
        with open(pm_path, "w", encoding="utf-8") as f:
            f.write("# PROJECT MEMORY\n\n## 1. Tech Stack\n- TBD\n\n## 2. File Index\n- TBD\n")
    if not os.path.exists(ss_path):
        with open(ss_path, "w", encoding="utf-8") as f:
            f.write("# SESSION STATE\n\n## 1. Active Task\n- Initialized\n\n## 2. Read Cache\n\n## 3. Failed Attempts\n")

    save_guard_state(load_guard_state(root_path), root_path)
    print(f"[OK] Memory system initialized at: {mem_dir}")


def cmd_check_file(filepath: str, summary: str = "", root_path: str = "."):
    if not os.path.exists(filepath):
        print(f"[MISSING] File not found: {filepath}")
        sys.exit(1)

    state = load_guard_state(root_path)
    rel = os.path.relpath(filepath, root_path).replace("\\", "/")
    current_hash = compute_hash(filepath)
    cached = state["read_cache"].get(rel)

    if cached and cached.get("hash") == current_hash and not summary:
        print(f"[CACHE HIT — DO NOT RE-READ!] `{rel}` has not changed since last read (hash: {current_hash}).")
        print(f"Cached Summary: {cached.get('summary', 'No summary recorded')}")
        return

    state["read_cache"][rel] = {
        "hash": current_hash,
        "summary": summary or (cached.get("summary") if cached else "Inspected"),
        "updated_at": datetime.now().isoformat(timespec="seconds")
    }
    save_guard_state(state, root_path)
    print(f"[CACHE UPDATED] `{rel}` (hash: {current_hash}) stored in read cache.")


def cmd_log_error(signature: str, attempted_fix: str, root_path: str = "."):
    state = load_guard_state(root_path)
    entry = state["error_strikes"].get(signature, {"count": 0, "attempts": []})
    entry["count"] += 1
    entry["attempts"].append({
        "strike": entry["count"],
        "fix": attempted_fix,
        "time": datetime.now().isoformat(timespec="seconds")
    })
    state["error_strikes"][signature] = entry
    save_guard_state(state, root_path)

    count = entry["count"]
    if count == 1:
        print(f"[STRIKE 1/3] `{signature}` logged. Analyze root cause and apply a targeted fix.")
    elif count == 2:
        print(f"[STRIKE 2/3 — WARNING] `{signature}` occurred a 2nd time! Stop incremental guessing and pivot strategy.")
    else:
        print(f"[STRIKE {count}/3 — CIRCUIT BREAKER TRIGGERED!] `{signature}` failed 3 times!")
        print("HALT: Do not retry the same operation. Report root cause and the 3 attempted approaches to the user.")
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description="Conscious Workflow Memory & Loop Guard")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize .claude/memory structure")
    p_init.add_argument("--root", default=".", help="Project root path")

    p_check = sub.add_parser("check-file", help="Check or update file read cache by SHA-256 hash")
    p_check.add_argument("filepath", help="File path to check/cache")
    p_check.add_argument("--summary", default="", help="Short summary to store in cache")
    p_check.add_argument("--root", default=".", help="Project root path")

    p_err = sub.add_parser("log-error", help="Record an error signature and check 3-strike loop breaker")
    p_err.add_argument("signature", help="Error identifier (e.g. TypeError:auth.ts:42)")
    p_err.add_argument("attempted_fix", help="Brief description of what was tried")
    p_err.add_argument("--root", default=".", help="Project root path")

    args = parser.parse_args()
    if args.command == "init":
        cmd_init(args.root)
    elif args.command == "check-file":
        cmd_check_file(args.filepath, args.summary, args.root)
    elif args.command == "log-error":
        cmd_log_error(args.signature, args.attempted_fix, args.root)


if __name__ == "__main__":
    main()
