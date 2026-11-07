# Debugging and Verification

## Evidence-First Debugging

1. Capture the exact error, stack trace, command, environment, and reproduction steps.
2. Identify the failing layer: input, configuration, dependency, application logic, storage, network, or runtime.
3. Find the first relevant frame or failing assertion; do not guess from the final line alone.
4. Form one testable hypothesis.
5. Make the smallest diagnostic check that can confirm or reject it.
6. Apply a focused fix only after the cause is supported by evidence.
7. Run the narrow regression test, then relevant broader checks.

## Test Discipline

- Check available scripts and documented test commands before inventing commands.
- Prefer deterministic, targeted tests.
- Distinguish test failure from environment/setup failure.
- Record exact command and concise result.
- If tests cannot run, explain why and what was inspected instead.
- Do not claim full verification when only a partial check was run.

## Failure Classification

- **Code Defect:** Reproduce and fix the implementation.
- **Configuration Defect:** Inspect effective config and defaults.
- **Dependency/Version Mismatch:** Verify lockfile and supported version range.
- **Environment Defect:** Report missing tool, permission, service, or variable.
- **Flaky/Transient:** Retry only with a plausible transient cause and bounded attempts.
- **Insufficient Evidence:** Gather targeted evidence; do not patch speculatively.

## Regression Review

After the fix, inspect related call sites, tests, configuration, and persisted data assumptions. Verify that the fix does not merely hide the symptom.
