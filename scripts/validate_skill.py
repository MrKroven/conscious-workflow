#!/usr/bin/env python3
"""Validate required Skill metadata, referenced paths, and Python syntax."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
skill = ROOT / "SKILL.md"

if not skill.is_file():
    errors.append("Missing SKILL.md")
else:
    content = skill.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
    else:
        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append("Unclosed YAML frontmatter")
        else:
            frontmatter = parts[1]
            name_match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", frontmatter)
            desc_match = re.search(r"(?m)^description:\s*(.+)$", frontmatter)
            if not name_match:
                errors.append("Missing/invalid lowercase kebab-case name")
            elif len(name_match.group(1)) > 64 or any(x in name_match.group(1) for x in ("claude", "anthropic")):
                errors.append("Skill name violates current naming constraints")
            if not desc_match or not desc_match.group(1).strip():
                errors.append("Missing description")
            elif len(desc_match.group(1).strip()) > 200:
                errors.append("Description exceeds 200 characters")
        for target in re.findall(r"`((?:references|templates|scripts)/[a-zA-Z0-9_\-\.]+\.(?:md|py))`", content):
            if not (ROOT / target).exists():
                errors.append(f"Broken referenced path: {target}")

for script in (ROOT / "scripts").glob("*.py"):
    try:
        compile(script.read_text(encoding="utf-8"), str(script), "exec")
    except SyntaxError as exc:
        errors.append(f"Python syntax error in {script.name}: {exc}")

if errors:
    print("FAIL")
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)
print("PASS: frontmatter, required metadata, referenced paths, and Python syntax.")
