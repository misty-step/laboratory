# Glance Context Ablations

Experiment track for issue `#48`: measure whether Glance context packaging improves coding-task outcomes,
and which injection strategy wins on quality/cost frontier.

## Layout

- `design.md`: hypotheses, novelty statement, experiment matrix, and adoption gates.
- `tasks/task_suite_v1.json`: canonical task suite (balanced by task tier and repo archetype).
- `harness/run_experiment.py`: deterministic simulation harness for `C0`-`C4` conditions.
- `analysis/analyze.py`: aggregates run data and writes decision-ready report artifacts.
- `data/`: immutable timestamped run CSVs plus `runs_latest.csv`.
- `report/`: generated findings + publication deliverable stubs.

## Run

```bash
python3 experiments/glance-context-ablations/harness/run_experiment.py
python3 experiments/glance-context-ablations/analysis/analyze.py
```

Or via `make`:

```bash
make run-glance-context
make analyze-glance-context
```

## Notes

- `--mode simulate` is the default and produces deterministic runs with a fixed seed.
- `--mode live` is reserved for follow-up integration with a real coding-agent runner.
