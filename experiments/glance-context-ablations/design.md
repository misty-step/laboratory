# Experiment Design: Glance Context Ablations

## Problem

We need causal evidence for whether Glance context packaging improves coding-agent outcomes, and whether
full inline context (`C3`) is worth its runtime/token overhead vs summary+retrieval (`C4`).

## Novelty Statement

This experiment produces new information because it isolates **Glance artifact presence + injection
strategy** as explicit factors in coding-agent performance, across repository archetypes and task
complexity tiers. Existing work in this repository covers prompt-injection defenses and coding-agent model
comparison, but not Glance-specific context packaging ablations.

## Hypotheses

- `H1`: Glance improves end-to-end coding task quality vs `C0` (no Glance).
- `H2`: "Files present + explicit discovery instruction" (`C2`) outperforms "files present but silent"
  (`C1`).
- `H3`: Full inline root context (`C3`) improves complex-task planning (`T3`) but risks efficiency regressions
  on simple tasks (`T1`).
- `H4`: Inline summary + retrieval (`C4`) outperforms full inline (`C3`) on quality/cost frontier.
- `H5`: Effect sizes vary by repo type and task tier (interaction effects).

## Factor Matrix

### Context condition

- `C0`: No Glance files.
- `C1`: Glance files exist, no instruction.
- `C2`: Glance files + explicit discovery instruction.
- `C3`: `C2` + full root `glance.md` inline in agent instructions.
- `C4`: `C2` + compact root summary (`<=400 tokens`) inline; full root retrievable on demand.

### Repository archetype

- `library_cli`
- `service_backend`
- `fullstack_app`
- `monorepo`

### Task complexity tier

- `T1`: small bug fix (single module)
- `T2`: medium feature (multi-file + tests)
- `T3`: high-complexity cross-module refactor/feature

### Agent/model

- `claude-sonnet-4.5`
- `codex-gpt-5`

## Controlled Variables

- Identical task spec text per cell.
- Fixed seed and deterministic simulation for pilot.
- Shared acceptance rubric and judge dimensions per row:
  - correctness
  - maintainability
  - architectural fit
  - test quality
  - minimality

## Task Suite

Canonical suite is stored in `tasks/task_suite_v1.json`:

- 12 tasks total
- 4 tasks per tier (`T1`, `T2`, `T3`)
- balanced across 4 repo archetypes
- includes Glance-local pointers (`../glance`, `misty-step/glance`) for full-stack tasks

## Data Contract

Harness output schema id: `glance_context_run_v1`

Each row captures:

- factor fields (`condition`, `task_tier`, `repo_type`, `model`)
- outcome fields (`task_success`, `tests_passed`, `pr_readiness_score`)
- efficiency fields (`runtime_seconds`, `tokens`, `estimated_cost_usd`)
- judge dimensions (`judge_*`)
- context usage fields (`context_utilized`, discovery/inline flags)

## Analysis Plan

- Aggregate condition-level metrics overall and by tier.
- Evaluate `C2`, `C3`, `C4` against `C0` baseline.
- Compute adoption gates from issue policy:
  - `>=10%` relative success lift on `T2+T3`
  - `<=15%` median runtime regression on `T1`
  - no meaningful maintainability/test-quality drop
  - cost increase justified by quality lift

## Adoption Rule

Recommend default condition from `C2/C3/C4` using gate count + frontier score.

Adopt only when all gates pass.

If `C3` underperforms `C4` on frontier, do not default to full inline root context.
