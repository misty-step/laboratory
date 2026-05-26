---
name: flywheel
description: |
  Outer loop for Laboratory research work. Picks a backlog item, shapes it,
  delivers it, settles it, ships it through PR, monitors evidence, and reflects.
  Trigger: /flywheel.
argument-hint: "[--max-cycles N]"
---

# /flywheel

Run bounded Laboratory research cycles. This repository ships experiments,
analysis, reports, and harness improvements; it does not deploy an app by
default.

## Cycle

1. Pick the next ready item from `backlog.d/`.
2. `/shape` if the item lacks a falsifiable oracle.
3. `/deliver` the item to merge-ready.
4. `/yeet` only when the user requested commits/pushes.
5. `/settle` until review, `make ci-smoke`, refactor, and QA are clean.
6. `/ship` through the repo's branch/PR workflow when the user asked to land.
7. `/monitor` the relevant evidence surface after shipping or a run.
8. `/reflect` and capture any follow-up backlog or harness changes.

## Laboratory Invariants

- Scientific workflow is the product: hypothesis, harness, data, analysis,
  traces, and deliverables.
- Simulated data is QA evidence only. It never supports publishable claims.
- Live runs require explicit `--live`, provider preflight, budget cap, and
  trace artifacts.
- `make ci-smoke` is the default gate unless a touched surface names a narrower
  additional command.
- Spellbook owns workflow primitives. Laboratory owns experiment semantics.

## Non-Goals

- No semantic workflow engine or hidden scheduler.
- No deployment phase unless the user points at an actual site/service change.
- No live API spend merely because a cycle reached an experiment item.
- No backlog archival without file or command evidence.

## Output

For each cycle, report the item, phase verdicts, commands run, artifacts
inspected, residual risk, and the next concrete step.
