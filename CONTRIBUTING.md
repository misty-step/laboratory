# Contributing

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

## Quality gate (run before PR)
```bash
make ci-smoke
```

## Data + Repro Invariants
- Treat `data/` as immutable run artifacts.
- Add new runs as new timestamped files.
- Keep a `*_latest.csv` pointer (symlink or copied file).

## Rounds
- New work: add a new `roundN/` (do not mutate old harness logic).
- Each round owns: `design.md`, `harness/`, `analysis/`, `data/`, `report/`.

## Live runs
- Default is `--simulate`.
- For `--live`, set API keys via env vars (see `.env.example`).

## Tests
- Tests: `tests/test_*.py` (`unittest`).
- Add tests for deterministic logic (scoring, parsing, classification).

## Git + Issues
- Commit prefixes: `docs:`, `experiment:`, `data:`, `refactor:`, `fix:`, `infra:`.
- Issue templates: `.github/ISSUE_TEMPLATE/`.
- Label taxonomy: `docs/ISSUE_LABELS.md`.
