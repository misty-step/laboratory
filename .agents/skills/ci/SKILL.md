---
name: ci
description: |
  Laboratory CI gate audit and verification workflow. Use when checking whether
  experiment, harness, analysis, docs, or Spellbook harness changes are safe to
  ship. Trigger: /ci, /gates.
argument-hint: "[--audit-only|--run-only] [paths]"
---

# /ci

`make ci-smoke` is the load-bearing gate in this repository. It runs Python
compile checks, compatibility-wrapper checks, unit tests, and analysis smoke
commands over committed datasets.

Do not invent a second CI owner here. If the current change needs a new
executable path verified, add that path to `make ci-smoke` or name it
explicitly as unverified.

## Modes

- Default: audit changed surfaces, then run `make ci-smoke`.
- `--audit-only`: inspect gate coverage and report gaps; do not run commands.
- `--run-only`: run `make ci-smoke` and report the result.

## Audit

1. Inspect `git status --short` and the changed paths.
2. Classify the change:
   - experiment harness
   - analysis script
   - shared scorer/budget/preflight utility
   - docs/backlog/design
   - Spellbook harness skill/agent/bridge
   - website/content
3. Confirm the matching gate exists:
   - Python executable path: included in `make check` or covered by tests.
   - Compatibility wrapper: covered by `make check-wrappers`.
   - Analysis behavior: covered by `make smoke-analyze` or a focused test.
   - New harness: has a deterministic simulate mode and a test.
   - Docs-only/harness-only: `make ci-smoke` plus link/path sanity is enough.
4. For live-data or publication changes, verify simulation integrity:
   simulated data cannot support findings.

## Run

```bash
make ci-smoke
```

If it fails, diagnose the first failing gate from the output. Fix mechanical
format/import/path issues directly when the cause is clear. Do not lower a gate
or remove a test to get green.

## Report

Return:

- verdict: `PASS`, `FAIL`, or `UNVERIFIED`
- commands run
- changed surfaces covered by the gate
- any executable path or publication claim not exercised
