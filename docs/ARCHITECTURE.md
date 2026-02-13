# Architecture

Misty Step's lab for reproducible software-engineering experiments.

## Layout
- `docs/`: repo docs (schemas, labels, ADRs).
- `experiments/prompt-injection-boundary-tags/`: main experiment family.
- `experiments/opencode-agent-models/`: coding-agent benchmark harness (OpenCode CLI).
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
