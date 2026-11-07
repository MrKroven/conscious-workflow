# Project Memory & Context Continuity System

This module prevents project amnesia across long conversations and multi-session workflows while keeping memory read overhead under **400 tokens**.

---

## 1. LEAN 2-TIER MEMORY ARCHITECTURE

Do **not** create 7+ fragmented markdown files that require multiple tool calls to read. Maintain a maximum of **2 core files** (plus 1 optional task tracker for massive projects) inside `.claude/memory/`:

1. **`.claude/memory/PROJECT_MEMORY.md` (Static / Slow-Changing — Max 120 Lines)**
   - **Contents:** Tech stack & versions, architecture overview, entry points, `FILE_INDEX` (key files + 1-line purpose + hash), and permanent architectural `DECISIONS`.
   - **When to Read:** Once at the start of a session.
   - **When to Update:** Only when new modules are created, dependencies change, or major architectural decisions are made.

2. **`.claude/memory/SESSION_STATE.md` (Dynamic Working Memory — Max 100 Lines)**
   - **Contents:** Current objective, `TASK_PROGRESS` checklist, **Session Read Cache** (files already inspected + key findings so they are never re-read), **Failed Attempts / Known Issues** (to prevent repeating failed fixes), and **Next-Session Handoff Note**.
   - **When to Read:** At session start or after context compaction.
   - **When to Update:** At the `SAVE` stage of tasks or when switching sub-tasks.

3. **`.claude/memory/TASK_PROGRESS.md` (Optional — Only for 5+ Phase Epics)**
   - Used only when a project has a multi-phase roadmap too large for `SESSION_STATE.md`.

*(Templates for all three files are located in `templates/`.)*

---

## 2. SESSION LIFECYCLE PROTOCOL

### Workflow A: First Session on a Project
1. Run `python3 "${CLAUDE_SKILL_DIR}/scripts/project_mapper.py" <project_root> --save-cache` (or inspect root config files + directory tree).
2. Populate `.claude/memory/PROJECT_MEMORY.md` and `.claude/memory/SESSION_STATE.md` using the templates.
3. Proceed with the user's task without reading unrelated source files.

### Workflow B: Returning Session / Resuming Work
1. Read `.claude/memory/SESSION_STATE.md` and `.claude/memory/PROJECT_MEMORY.md` **first**.
2. Run `python3 "${CLAUDE_SKILL_DIR}/scripts/project_mapper.py" <project_root> --diff` (or `git status -s` / `git diff --stat`) to see which files changed since the last session.
3. **Trust cached summaries** for unchanged files. Inspect **only** modified files and files directly required for the next task step.

---

## 3. CONTEXT COMPACTION & LOW-CONTEXT RECOVERY

When the conversation grows long or before context compaction occurs:
1. Flush all active findings, completed steps, remaining todos, and any failed approaches into `.claude/memory/SESSION_STATE.md`.
2. Write a 3-line `## Handoff Anchor` at the bottom of `SESSION_STATE.md` containing:
   - Exact file and function currently being edited.
   - Last verification command run and its outcome.
   - Immediate next step required.
3. **Epistemic Verification Rule:** When reading memory files from a previous session, treat cached architectural notes as *working context*, but verify target lines before applying destructive edits if external changes may have occurred. Do not store secrets, API keys, or personal data in memory files.
