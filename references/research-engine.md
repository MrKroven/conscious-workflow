# Deep Technical Research & Verification Engine

Never guess APIs, configuration keys, or library behaviors. When knowledge is uncertain or version-sensitive, execute disciplined verification.

---

## 1. RESEARCH PRIORITY HIERARCHY

1. **Project's Own Lockfiles & Installed Packages (Highest Truth):**
   - Check `package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `requirements.txt`, or local type definitions (`node_modules/.../index.d.ts`) to see the **exact version** installed in the project.
2. **Official Primary Documentation & Changelogs:**
   - Prioritize official vendor docs, RFCs, and migration guides over third-party blog posts or forum answers.
3. **Cross-Source Verification:**
   - When researching complex bugs or edge cases, cross-check at least 2 independent authoritative sources (e.g., official docs + canonical GitHub issue/release notes).

---

## 2. VERSION & DEPRECATION GUARDRAILS

Before writing code that uses external libraries/frameworks:
- **Verify Major Version Breaking Changes:**
  - *Examples:* `discord.js` v13 vs v14 (`MessageEmbed` → `EmbedBuilder`, intent flags), Next.js Pages vs App Router, React 18 vs 19, Pydantic v1 vs v2 (`.dict()` → `.model_dump()`), OpenAI SDK v0 vs v1+, `.NET` 6 vs 8.
- **No Deprecated Patterns:** Never suggest deprecated methods, legacy lifecycle hooks, or insecure crypto/auth patterns when modern equivalents exist for the project's target version.
- **Explicit Uncertainty Declaration:** If external search/docs are inaccessible in the current environment and you cannot 100% verify an obscure API signature, state the assumption in 1 clear sentence rather than presenting a guess as guaranteed fact.

---

## 3. ANTI-REDUNDANCY IN RESEARCH

- **Query Deduplication:** Record completed research conclusions in `SESSION_STATE.md`. Never run duplicate web/doc searches for the same library question within a session.
- **Refine, Don't Repeat:** If a search query returns irrelevant results, change the query structure (use exact error strings, method names, or version numbers) rather than repeating similar broad keywords.
