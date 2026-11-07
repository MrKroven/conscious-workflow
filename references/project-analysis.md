# Advanced File, ZIP & Visual Project Analysis

Follow this strict inspection order whenever a user provides text, documents, screenshots, code files, or ZIP archives.

---

## 1. STRICT 7-STAGE INSPECTION ORDER

Always process inputs in this exact sequence to avoid wasted code scanning:

1. **User Prompt & Core Intent:** Identify the exact deliverable, target behavior, and success criteria.
2. **Explicit Constraints & Requirements:** Note stack limits, performance targets, forbidden libraries, or style rules.
3. **Documentation & Text Files (`.txt`, `.md`, `README`, specs):** Understand intended design before reading implementation code.
4. **Visuals & Screenshots (`.png`, `.jpg`, `.webp`):** Extract error messages, UI defects, file paths, and stack traces directly from images.
5. **Target Source Code:** Read entry points and specific modules linked to the user's request.
6. **ZIP Archives & Full Repositories:** Map structure and dependencies systematically (see Section 2).
7. **External Documentation:** Query official docs for any unfamiliar or version-sensitive APIs discovered in Steps 5–6.

---

## 2. ZIP ARCHIVE & REPOSITORY MAPPING PROTOCOL

When given a ZIP archive or project folder, **never** open source files randomly. Execute this 4-step funnel:

1. **Safe Archive Check & Tree Map:**
   - List archive contents and check for suspicious/traversal paths before extracting into a controlled directory.
   - Run `python3 "${CLAUDE_SKILL_DIR}/scripts/project_mapper.py" <project_dir>` (or list files excluding `node_modules`, `.git`, `venv`, `dist`, `build`, `__pycache__`, `bin`, `obj`).
2. **Fingerprint Stack & Dependencies:**
   - Inspect only manifest/config files first (`package.json`, `requirements.txt`, `pyproject.toml`, `*.csproj`, `Cargo.toml`, `pom.xml`, `tsconfig.json`, `.env.example`, `docker-compose.yml`).
   - Record exact framework and library versions.
3. **Locate Entry Points & Module Graph:**
   - Identify main entry points (`main.*`, `index.*`, `app.*`, `server.*`, `Program.cs`, routes/controllers) and trace how the target feature connects to them.
4. **Targeted Deep-Dive:**
   - Read **only** the files in the call path of the user's task + any error logs (`*.log`). Leave unrelated modules unread.

---

## 3. VISUAL & SCREENSHOT DIAGNOSTIC PROTOCOL

Treat every attached image as structured technical telemetry, not decorative media:

1. **Exact Text & Error Extraction:** Transcribe exact error codes, exception messages, line numbers, URLs, and terminal outputs visible in the screenshot.
2. **Path & Component Mapping:** Match visible window titles, URL routes, button labels, or component names to corresponding files in the codebase (`grep -rn "<UI_Text>" src/`).
3. **Layout & State Analysis:** For UI/frontend bugs, identify CSS/layout anomalies (overflow, z-index, alignment, missing state render) and correlate them directly with the component's styles and state logic.
