# Architecture

Misty Step's lab for reproducible software-engineering experiments.

## Layout
- `docs/`: repo docs (schemas, labels, ADRs).
- `experiments/prompt-injection-boundary-tags/`: main experiment family.
- `experiments/opencode-agent-models/`: coding-agent benchmark harness (OpenCode CLI).
- `experiments/glance-context-ablations/`: context-packaging ablation harness for Glance integration strategy.
- `tools/`: shared utilities (normalization, analysis, calibration).
- `templates/`: new experiment skeletons.
- `papers/`: finalized publications.

## Prompt-Injection Boundary Tags
- Each round is isolated in `.../rounds/roundN/`.
- Round owns: `design.md`, `harness/run_experiment.py`, `analysis/analyze.py`, `data/`, `report/`.
- Harness defaults to deterministic `--simulate`. `--live` does real model calls + requires API keys.
- Shared modules in `experiments/prompt-injection-boundary-tags/shared/`:
  - scoring (`scorer.py` + `scorer_config_v2.json`)
  - budget controls (`shared/budget/`)
  - mandatory live preflight (`shared/preflight/`)
  - wrappers (`shared/wrapper/`)

## Data Contract
- `data/` is immutable.
- Write new run artifacts as timestamped files.
- Maintain a `*_latest.csv` pointer (symlink or copy) for current analysis.

## Cross-Round Analysis
- Canonical CSV schema: `docs/RUN_SCHEMA.md`.
- Build canonical dataset: `make normalize-runs`.
- Analyze canonical dataset: `make analyze-runs`.

## ADRs
- Architecture decisions live in `docs/adr/` (template: `docs/adr/0000-template.md`).

## Research Backlog
- `docs/experiment-ideas.md` is the living pile of candidate experiments.
- `docs/inspiration-studies.md` tracks external studies and classic experiments
  that can seed future lab work.
- Completed experiments should add follow-up ideas or explicitly record why no
  follow-up was generated.

## Spellbook Harness
- `.agents/skills/` is the canonical repo-local skill root.
- `.claude/skills/`, `.codex/skills/`, and `.pi/skills/` are symlink bridges
  back to `.agents/skills/`.
- `.agents/agents/` contains the shared agent definitions; harness-specific
  agent directories bridge to it where the runtime supports markdown agents.
- `.spellbook/repo-brief.md` records the durable tailoring brief for future
  skill rewrites and harness audits.
- `make ci-smoke` is the load-bearing repository gate.

Spellbook supplies the workflow primitives. The laboratory supplies the science
contract: hypothesis, methodology, data, analysis, and deliverables.

## Glance Context Ablations
- Canonical task suite lives in `tasks/task_suite_v1.json`.
- Harness in `harness/run_experiment.py` supports `C0`-`C4` condition toggles.
- Analyzer in `analysis/analyze.py` evaluates adoption gates against `C0` baseline.
