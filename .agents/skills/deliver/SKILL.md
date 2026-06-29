---
name: deliver
description: |
  Take one Laboratory backlog item to merge-ready. Composes /shape,
  /implement, /code-review, /ci, /refactor, and /qa as needed. Stops before
  merge. Trigger: /deliver.
argument-hint: "[backlog-item]"
---

# /deliver

Deliver one shaped Laboratory work item to merge-ready state. This repository is
an experiment lab, not an app platform: delivery means the touched experiment,
harness, analysis, docs, or Spellbook harness surface is implemented,
reviewable, and verified by the repo's actual gate.

## Inputs

- A `backlog.d/<id>.md` item, experiment path, or explicit user request.
- Repo brief: `.spellbook/repo-brief.md`.
- Gate: `make ci-smoke`.

## Loop

1. Read the target item and the relevant repo anchors.
2. Shape any missing oracle before editing. The oracle must name the behavior,
   files, commands, and evidence that prove done.
3. Implement narrowly. For code changes, preserve simulate mode and add focused
   tests for new harness/analysis behavior.
4. Run `/code-review` for semantic issues.
5. Run `/ci`; it must execute `make ci-smoke`.
6. Run `/refactor` when the diff is broad or repeated logic appears.
7. Run `/qa` against the changed scientific surface:
   - simulate run for harnesses
   - fixture/committed-data analysis for analyzers
   - provenance check for report or publication artifacts
   - bridge/link audit for Spellbook harness changes

Loop back after any fix. Stop when review is clean, `make ci-smoke` passes, and
QA has inspected the relevant artifact.

## Non-Goals

- Do not merge, push, or publish.
- Do not run live API experiments unless the target item explicitly requires a
  bounded live smoke and the user has approved the spend.
- Do not archive backlog items without evidence in files or command output.
- Do not introduce platform scaffolding unrelated to the current experiment.

## Output

Return a concise delivery brief:

- target item
- what changed
- commands run
- artifacts inspected
- residual risk
- next step for merge or follow-up
