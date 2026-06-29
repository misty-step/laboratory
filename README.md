# Laboratory

Misty Step's computational laboratory for reproducible software-engineering experiments.

## Philosophy

Every claim should be testable. Every run should be reproducible. Every result should be preserved with context.

**Observe -> Hypothesize -> Test -> Document -> Share**

## Repository Structure

```text
laboratory/
├── docs/                 # schemas, labels, ADRs
├── experiments/
│   ├── prompt-injection-boundary-tags/
│   │   ├── rounds/
│   │   │   ├── round1/   # baseline (single-model, 72 trials)
│   │   │   ├── round2/   # alternate harness (432 trials)
│   │   │   ├── round2b/  # realistic harness + analysis (324 trials)
│   │   │   ├── round3/   # defense-ablation matrix
│   │   │   ├── round4/   # single-turn vs multi-turn benchmark
│   │   │   ├── round5/   # security vs utility tradeoff
│   │   │   ├── round6/   # tool-call policy gate eval
│   │   │   └── round7/   # cross-model defense validation
│   │   └── shared/       # reusable assets (e.g., wrappers)
│   └── opencode-agent-models/  # coding-agent benchmark harness
│   └── glance-context-ablations/ # Glance context-packaging ablation harness
├── templates/            # new experiment skeletons
├── tools/                # shared utilities
├── .agents/              # Spellbook-backed repo-local skills and agents
└── papers/               # finalized publications
```

Each round has its own `design.md`, `harness/`, `analysis/` (when present), `data/`, and `report/`.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

This repo is Spellbook-backed. The repo-local harness lives in `.agents/`;
Claude, Codex, and Pi entrypoints are bridges back to that shared root.

```bash
make ci-smoke
```

For live runs, set API keys via env vars (see `.env.example`).

Run canonical Round 2B workflow:

```bash
make run-r2b analyze-r2b calibrate-r2b
```

Normalize and analyze cross-round historical data with one schema:

```bash
make normalize-runs analyze-runs
```

Back-compat entrypoints remain available at repo root:

```bash
python3 run_experiment_r2.py
python3 analyze_r2.py
```

## Docs

- `docs/ARCHITECTURE.md`
- `docs/RUN_SCHEMA.md`
- `docs/ISSUE_LABELS.md`
- `docs/experiment-ideas.md`
- `docs/inspiration-studies.md`
- `docs/adr/0000-template.md`

## Agent Harness

Spellbook is the active harness substrate. Keep shared skill content under
`.agents/skills/`; keep `.claude/skills/`, `.codex/skills/`, and `.pi/skills/`
as symlink bridges. Repo-specific lab skills such as `brainstorm` and
`peer-review` live alongside the selected Spellbook workflow skills.

The load-bearing repo gate is:

```bash
make ci-smoke
```

Use Spellbook workflow skills for repo work: `/groom`, `/shape`, `/deliver`,
`/code-review`, `/ci`, `/qa`, `/settle`, and `/ship`.

## CI Smoke Checks

GitHub Actions workflow: `.github/workflows/ci.yml`

It runs on each pull request and each push to `master`:

- `make check` (compile check for harnesses, analyzers, wrappers, tools)
- `make check-wrappers` (compat wrapper run-path sanity)
- `make test` (unit tests)
- `make smoke-analyze` (analysis smoke run on committed datasets)

Run the same gate locally:

```bash
make ci-smoke
```

To block merges on failures, set branch protection to require these hosted checks:

- `ci-smoke`: runs the same `make ci-smoke` gate documented above.
- `trufflehog`: repository secret scan.

## Experiments

| Experiment | Status | Summary |
|---|---|---|
| [prompt-injection-boundary-tags](experiments/prompt-injection-boundary-tags/) | R1-R7 implemented | Tests boundary-tagging, defense layering, multi-turn escalation risk, policy filtering, and cross-model defense validation. |
| [glance-context-ablations](experiments/glance-context-ablations/) | Scaffolded (pilot harness + analyzer) | Measures causal impact of Glance context strategy (`C0`-`C4`) on coding-task success, readiness, runtime, and token/cost frontier. |

## Contributing

See `CONTRIBUTING.md`.

## License

MIT
