# Token Optimization Protocol

This module defines practical mechanics for reducing unnecessary input and output token usage without degrading engineering quality. Actual savings depend on task complexity, project structure, tool availability, and model behavior.

---

## 1. FILE INSPECTION HIERARCHY (CHEAPEST TO MOST EXPENSIVE)

Never read a whole file when a cheaper operation answers the question:

1. **Level 0 — Memory Cache (0 File Tokens):**
   - Check `SESSION_STATE.md` (Read Cache section) and `PROJECT_MEMORY.md` (`FILE_INDEX`).
   - If the file was already summarized in the current session and not modified, **do not re-read it**.
2. **Level 1 — Metadata & Tree Map (~50–150 Tokens):**
   - Run `python3 "${CLAUDE_SKILL_DIR}/scripts/project_mapper.py" <dir>` or `ls -la` to see file sizes, line counts, and changed hashes.
3. **Level 2 — Symbol & Pattern Search (~100–300 Tokens):**
   - Use `grep -n "functionName" <file>` or `rg` to locate exact line numbers before opening a large file.
4. **Level 3 — Surgical Window Read (~200–500 Tokens):**
   - For files >150 lines, read only the relevant 40–80 line window (`sed -n '120,180p' <file>`).
5. **Level 4 — Full File Read (Last Resort):**
   - Only read 100% of a file if it is <150 lines OR requires a complete structural rewrite.

---

## 2. DIFF-ONLY VERIFICATION & EDITING

- **Surgical Edits:** When modifying existing files >150 lines in chat output, provide only the modified function/block with 2–3 lines of surrounding context unless the user explicitly asks for the full file.
- **No Full-Project Re-scans:** After editing `fileA.ts`, never re-read `fileB.ts` or re-run directory tree listings unless `fileA.ts` changed an exported interface used by `fileB.ts`.
- **Targeted Test Execution:** Run only the unit test file corresponding to the modified module (`pytest tests/test_auth.py` instead of `pytest` across 200 test files). Run the full suite only at final verification.

---

## 3. SUB-AGENT & TOOL DISCIPLINE

- **No Sub-Agent Spawning for Simple Lookups:** Never spawn a sub-agent to read 1–2 files or run a single grep search; sub-agent initialization duplicates system prompt tokens.
- **Batch Related Operations:** Combine related shell checks or file inspections into a single command where safe (e.g., `grep -rn "API_URL" src/ config/`) instead of 5 separate tool turns.

---

## 4. OUTPUT COMPRESSION RULES

- **Forbidden Phrases:** Never output filler openings/closings (*"Certainly, I can help with that"*, *"Great point"*, *"To summarize"*, *"Let me know if you have any other questions"*).
- **Code Over Prose:** Let clean, self-documenting code and exact diff blocks speak for themselves. Limit prose explanations to:
  1. Root cause of a bug (1–2 sentences).
  2. Architectural trade-offs or breaking changes (bulleted, 1 line each).
  3. Verification result (exact test/command output status).
