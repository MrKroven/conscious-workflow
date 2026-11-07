# CLAUDE.md — Optional Project-Level Operating Rules

> This file is a template. Claude Code automatically reads `CLAUDE.md` files from project locations, not this file merely because it sits inside a Skill directory. Review and merge these rules into your target project root `CLAUDE.md` if you want them to apply broadly.

The **Conscious Workflow** protocol is active in this project. Strictly adhere to the following rules across all operations:

1. **Memory First:** At the start of every session, check `.claude/memory/SESSION_STATE.md` and `.claude/memory/PROJECT_MEMORY.md`. Never re-read unchanged files from scratch.
2. **Surgical Inspection:** Instead of reading large files (>150 lines) in full, use `grep` or line-range reads (`sed -n`) first. When the Skill is installed inside the project, run `python3 .claude/skills/conscious-workflow/scripts/project_mapper.py . --diff` to inspect the project map and modified files. If it is installed globally, resolve the script from the Skill installation directory.
3. **3-Strike Loop Guard:** Never repeat the same error 3 times in a row. Analyze root cause on Strike 1, pivot strategy on Strike 2, and halt to report findings on Strike 3.
4. **Zero Fluff:** Do not write greetings, pleasantries, or unnecessary intro/outro paragraphs. Start directly with the technical solution or code.
5. **Complete Engineering (Zero Placeholders):** Never leave `// TODO` or `// ... rest of code` placeholders inside active logic. Preserve existing architecture and code style.
6. **Epistemic Honesty:** Never present unexecuted tests as passed or uninspected files as read.
7. **State Anchor:** On multi-step tasks, append a single-line status summary at the end of the response:
   `[STATUS] Completed: <X> | Next: <Y> | Modified Files: <Z>`
