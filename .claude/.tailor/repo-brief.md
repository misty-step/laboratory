# Laboratory Repo Brief

## Vision And Purpose

Laboratory is Misty Step's computational science workspace for reproducible,
hypothesis-driven experiments on AI system behavior. Code exists to serve the
science loop: design experiments, run bounded simulations or live trials,
analyze data, and publish results with enough evidence for other builders to
inspect or reproduce the claim.

## Stack And Boundaries

- Python experiment harnesses, analyzers, and shared utilities are the product.
- `experiments/` owns experiment families and their local `design.md`,
  `harness/`, `analysis/`, `data/`, and `report/` surfaces.
- `tools/` owns cross-round normalization and analysis.
- `docs/` owns architecture, run schema, issue labels, study inspiration, and
  experiment idea backlog.
- `.agents/` owns the Spellbook-backed agent harness. Harness-specific
  directories are bridges, not canonical content.

## Load-Bearing Gate

`make ci-smoke` IS the repository gate. It runs compile checks, compatibility
wrapper checks, unit tests, and analysis smoke commands.

## Invariants

- Never publish findings from simulated data. Simulation validates harness
  machinery only.
- Live runs require explicit `--live`, API key preflight, model/config
  documentation, and budget control.
- Data files under experiment `data/` are immutable. Add timestamped outputs;
  do not rewrite evidence.
- Every completed experiment produces findings, paper, blog post, executive
  summary, social thread, data card, and charts.
- Branch work happens off `master`; PRs must include goal, changes, commands,
  data paths, and a linked issue or backlog item.

## Known Debts

- MCP tool-schema entropy has a design and manifest, but no runnable harness.
- The lab needs a first-class experiment manifest validator and trace-backed
  publish guard.
- Some historical backlog items and docs came from retired Gradient work and
  should be treated as migration context, not active platform truth.

## Terminology

- Experiment: a hypothesis-driven computational study.
- Harness: code that generates trials and writes data.
- Analysis: deterministic code that reads data and emits report artifacts.
- Live data: provider/API-backed empirical rows.
- Simulated data: deterministic QA rows, never publication evidence.

## Session Signal

- The operator wants thin harnesses tied to real experiments, not a large
  platform scaffold that delays research.
- Repo-specific tailoring matters more than generic generated governance.
- Evidence must be non-optional and inspectable.
- Spellbook is the active harness substrate; Gradient is retired.
