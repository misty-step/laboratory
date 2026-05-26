---
name: ship
description: |
  Final mile for a merge-ready Laboratory branch: verify landability, preserve
  backlog closure, merge through PR or git-native flow, update docs, reflect,
  and monitor evidence. Trigger: /ship.
argument-hint: "[branch-or-pr]"
---

# /ship

Land merge-ready Laboratory work without losing scientific provenance or backlog
closure. `/ship` assumes `/settle` already proved the branch clean; if review,
QA, or `make ci-smoke` has not run for the current HEAD, route back to
`/settle`.

## Preconditions

- Current branch is not `master` or `main`.
- Working tree is clean unless the user explicitly asks for a local-only final
  pass.
- The branch has a PR or a clear git-native merge path.
- Current HEAD has landability evidence: green PR checks or local `make
  ci-smoke` plus review/QA receipts from this session.
- Closing backlog IDs are known from branch name, commit trailers, PR body, or
  explicit user instruction.

## Process

1. Inspect branch, PR state, `git status --short`, and recent verification
   evidence.
2. Refuse if simulated data is being published as live evidence.
3. Archive closed `backlog.d/<id>-*.md` items to `backlog.d/_done/` on the
   shipping branch when the closure is proven.
4. Ensure touched docs accurately describe the shipped experiment, analysis,
   report, or harness behavior.
5. Merge by PR when available. Use git-native squash only when there is no PR
   route and the user wants local landing.
6. Preserve `Closes-backlog:` trailers in the merge/squash message.
7. Run `/reflect` for the shipped work and route any new work into backlog or a
   follow-up branch.
8. Run `/monitor` for the relevant signal: CI, experiment artifact integrity,
   publication provenance, or Spellbook bridge health.

## Refuse Conditions

- Default-branch direct shipping without explicit user instruction.
- Dirty worktree whose changes are not part of the intended shipment.
- Missing or stale landability evidence.
- Missing live traces for publishable live claims.
- Backlog closure cannot be associated with a concrete item or explicit user
  decision.

## Output

Report:

- shipped branch or PR
- backlog IDs closed or referenced
- merge method
- verification evidence
- reflect/monitor outcome
- residual risk
