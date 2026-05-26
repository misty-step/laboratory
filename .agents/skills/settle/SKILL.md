---
name: settle
description: |
  Polish a Laboratory branch until it is merge-ready. Runs code review,
  make ci-smoke, refactor, and experiment QA. Stops before merge. Trigger:
  /settle, /pr-fix, /pr-polish.
argument-hint: "[PR-number|branch-name]"
---

# /settle

Take the current branch from "implemented" to merge-ready. This skill does not
merge, push, publish, or run live spend. It polishes the branch against the lab's
real evidence requirements.

## Preconditions

- Not on `master`.
- No merge/rebase/cherry-pick in progress.
- Working tree state is understood.
- The target branch has a clear base, normally `master`.

## Loop

1. Inspect `git status --short`, `git diff --stat`, and the full branch diff.
2. Run `/ci`; the command must be `make ci-smoke`.
3. Run `/code-review` and fix blockers.
4. Run `/refactor` for broad diffs or obvious simplification opportunities.
5. Run `/qa` for the touched surface:
   - harness changes: simulate mode and output schema
   - analysis changes: data-backed output inspection
   - docs/report changes: provenance and simulation-integrity checks
   - harness/skill changes: bridge and marker audit
6. Re-run `make ci-smoke` after any file change.

Exit only when the same pass has clean review, green CI, no further refactor
work, and QA evidence for the changed surface.

## Refuse Conditions

- Default branch direct work unless the user explicitly requested it.
- Unresolved conflict markers.
- A requested live run without explicit budget approval.
- Publication claims backed only by simulated data.

## Output

Report:

- verdict: `ship-ready`, `blocked`, or `not-ready`
- commands run
- review/QA findings fixed
- remaining risks
- exact next action, usually `/ship` or PR creation
