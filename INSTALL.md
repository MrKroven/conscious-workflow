# Conscious Workflow — Installation & Usage

Conscious Workflow is a modular Claude Skill with optional Python utilities. The Skill instructions work independently; the scripts add local project-mapping, memory-cache, loop-guard, and validation helpers when Python and filesystem access are available.

## Requirements

- Claude.ai with custom Skills enabled, or Claude Code.
- Python 3.8+ for the optional command-line utilities.
- Code execution enabled in Claude.ai when using uploaded Skills that need those capabilities.

## Package structure

```text
conscious-workflow/
├── SKILL.md
├── CLAUDE.md
├── INSTALL.md
├── README.md
├── README_TR.md
├── LICENSE
├── references/
│   ├── debugging.md
│   ├── loop-prevention.md
│   ├── memory-system.md
│   ├── project-analysis.md
│   ├── research-engine.md
│   ├── software-engineering.md
│   ├── task-execution.md
│   └── token-optimization.md
├── templates/
│   ├── PROJECT_MEMORY.md
│   ├── SESSION_STATE.md
│   └── TASK_PROGRESS.md
└── scripts/
    ├── memory_guard.py
    ├── project_mapper.py
    └── validate_skill.py
```

## 1. Claude.ai

1. Download `conscious-claude-en.zip` from the [GitHub Releases page](https://github.com/MrKroven/conscious-workflow/releases).
2. In Claude, open **Settings → Customize → Skills**.
3. Select **Add / Create skill → Upload a skill** (the label may vary by interface).
4. Upload the ZIP archive. It contains a top-level `conscious-workflow/` folder, matching the Skill metadata name.
5. Enable the Skill. Enable Code execution if you want Claude to use the bundled scripts where supported.
6. Ask Claude to use Conscious Workflow in a normal message. Claude.ai does not use the Claude Code slash command.

Example:

```text
Use the Conscious Workflow skill for this project. Inspect the existing project context first, focus on relevant files, avoid repeating unchanged reads, and verify changes before reporting completion.
```

## 2. Claude Code — global installation

**macOS / Linux**

```bash
git clone https://github.com/MrKroven/conscious-workflow.git "$HOME/.claude/skills/conscious-workflow"
```

**Windows PowerShell**

```powershell
git clone https://github.com/MrKroven/conscious-workflow.git "$env:USERPROFILE\.claude\skills\conscious-workflow"
```

Open a new Claude Code session and run:

```text
/skills
```

Confirm that `conscious-workflow` is listed. Invoke it directly by placing the command at the start of a message:

```text
/conscious-workflow Analyze this repository and explain its architecture. Do not modify files yet.
```

The directory name and frontmatter name are both `conscious-workflow`, so `/conscious-workflow` is the direct command in Claude Code. Claude Code may also invoke the Skill automatically when the task matches its description.

## 3. Project-specific installation

From the project root, add it as a Git submodule:

```bash
git submodule add https://github.com/MrKroven/conscious-workflow.git .claude/skills/conscious-workflow
```

Team members should clone the project with `git clone --recurse-submodules <your-project-repository>`.

If you do not want a submodule, download the repository ZIP and copy its contents (excluding `.git`) into `.claude/skills/conscious-workflow/`. Keep `SKILL.md` directly inside that directory.

You may also use the root `CLAUDE.md` as project-level guidance. Review it and merge it with any existing `CLAUDE.md` instead of overwriting project instructions blindly.

## 4. Optional command-line utilities

For a project-specific installation, run the following commands from your target project's root:

```bash
# Create a compact project map and save a SHA-256 snapshot.
python .claude/skills/conscious-workflow/scripts/project_mapper.py . --save-cache

# Show files changed since the previous saved snapshot.
python .claude/skills/conscious-workflow/scripts/project_mapper.py . --diff

# Initialize project-local memory and loop-guard state.
python .claude/skills/conscious-workflow/scripts/memory_guard.py init --root .

# Validate the installed Skill package.
python .claude/skills/conscious-workflow/scripts/validate_skill.py
```

If you installed the Skill globally, replace `.claude/skills/conscious-workflow/` with the global Skill path. Additional memory-guard commands:

```bash
# Store a concise summary after inspecting a file.
python .claude/skills/conscious-workflow/scripts/memory_guard.py check-file path/to/file.py --summary "Short file summary" --root .

# On a later check, omit --summary to allow a cache hit if unchanged.
python .claude/skills/conscious-workflow/scripts/memory_guard.py check-file path/to/file.py --root .

# Record an error signature and the attempted fix.
python .claude/skills/conscious-workflow/scripts/memory_guard.py log-error "TypeError:auth.py:42" "Updated input validation" --root .
```

Use `python3` instead of `python` on systems where that is the Python 3 command. On Windows, `py -3` may be available.

## Notes

- The Skill provides operating instructions; it does not guarantee a fixed percentage of token savings or eliminate every model error.
- Reference modules are intended to be loaded only when their trigger conditions apply.
- Helper scripts are optional. Their availability depends on Python, filesystem permissions, and the tools exposed by the Claude environment.
- Project memory is stored in ordinary files under `.claude/memory/`; inspect those files before sharing them.
- Review Skill files and scripts before installing or running them, especially when obtained from an unfamiliar fork.
