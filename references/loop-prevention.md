# Loop Prevention & Root-Cause Control System

This module prevents infinite retry loops, circular reasoning, scope creep, and blind trial-and-error.

---

## 1. THE 3-STRIKE CIRCUIT BREAKER

Track every error by its **Error Signature** (`<ErrorType>:<File>:<Line>` or command exit reason):

| Strike | Required Action | Prohibited Behavior |
| :--- | :--- | :--- |
| **Strike 1** (First Occurrence) | Read full error output + inspect exact line window (±20 lines). Identify root cause before touching code. | Blindly tweaking syntax or re-running the identical command. |
| **Strike 2** (Second Occurrence of Same/Derived Error) | **STOP coding.** Log the failed attempt in `SESSION_STATE.md` under `Failed Attempts`. Verify library versions, config, and data types. Switch to an alternative architectural approach. | Applying a minor variation of Strike 1's fix. |
| **Strike 3** (Third Occurrence) | **CIRCUIT BREAKER TRIGGERED.** Halt execution immediately. Report findings to the user and request direction or missing environment context. | Starting a 4th attempt or rewriting unrelated project files. |

You can automate this check using:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/memory_guard.py" log-error "<error_signature>" "<attempted_fix>"
```

---

## 2. ROOT-CAUSE ANALYSIS (RCA) PROTOCOL

When any build, test, or runtime command fails, execute this sequence before writing code:

1. **Isolate the First Failure:** Ignore cascading downstream errors; locate the **very first** exception or compiler error in the log.
2. **Verify Assumptions:**
   - Is the file path/import resolving to the file you think it is?
   - Are environment variables, dependency versions, and types matching the actual runtime?
3. **Minimal Reproduction:** If the cause is unclear, test the failing function/query in isolation rather than running the entire application stack repeatedly.

---

## 3. ANTI-SCOPE-CREEP & TASK BOUNDARY GUARDS

- **No Unsolicited Refactoring:** If asked to fix a bug in `login()`, do not rename variables in `register()` or upgrade unrelated dependencies.
- **No Infinite Task Chains:** Complete the requested deliverable first. If you discover secondary improvements during inspection, note them in 1–2 bullets at the end under `[Suggested Improvements]` rather than executing them unprompted.
- **Explicit Blocker Declaration:** If a task requires missing credentials, external network access unavailable in the sandbox, or corrupted binary assets, state the exact blocker immediately on Turn 1 instead of attempting workarounds that cannot succeed.
