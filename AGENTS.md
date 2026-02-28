# Repository Guidelines

## What This Is

A computational science laboratory. The primary work is running reproducible, hypothesis-driven
experiments on AI system behavior and publishing findings. Code exists to serve science.

## Project Structure

```
experiments/
  prompt-injection-boundary-tags/    # Defense ablation program, rounds 1-8
    rounds/roundN/
      design.md                      # Hypothesis + methodology + novelty statement
      harness/run_experiment.py      # --simulate default, --live for API calls
      analysis/analyze.py            # Reads data/, produces report/
      data/                          # Immutable CSV artifacts
      report/                        # 7 deliverable artifacts (see below)
    shared/
      scoring/scorer.py              # score_response() → 0-3 severity
      budget/controller.py           # Cost control for live runs
      preflight/live.py              # API key validation
      wrapper/untrusted-exec.sh      # Sandboxed CLI output wrapper
  glance-context-ablations/          # Context packaging ablations (C0-C4)
  opencode-agent-models/             # Coding agent benchmarking via OpenCode CLI
canonical/                           # Cross-round normalized dataset
tools/                               # normalize_prompt_injection_runs.py, analyze_prompt_injection_runs.py
```

## Build & Test Commands

```bash
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -e .

make ci-smoke              # Full gate: check + check-wrappers + test + smoke-analyze
make test                  # unittest discover -s tests -p 'test_*.py'
make check                 # py_compile all harnesses, analyzers, tools

# Run a specific experiment
make run-r7 && make analyze-r7
make run-glance-context && make analyze-glance-context

# Cross-round analysis
make normalize-runs && make analyze-runs
```

## Coding Style

- Python 3.10+, 4-space indent, PEP 8, `ruff` at 100-char line length.
- `snake_case` for functions/variables; `UPPER_SNAKE_CASE` for constants.
- Keep modules focused: scoring, payload generation, provider calls, and analysis are separate concerns.
- New rounds: `rounds/roundN/` with explicit file names (`design.md`, `run_experiment.py`, `analyze.py`).

## Testing Guidelines

- Tests in `tests/test_<module>.py` using `unittest`. Focus on deterministic logic.
- Every harness has a corresponding test file. New harnesses get tests.
- Target ~80% patch confidence on new logic; don't chase global percentages.
- Never break simulate mode — it must run without API keys.

## Commit Conventions

Typed prefixes — use exactly one per commit:

| Prefix | When |
|--------|------|
| `experiment:` | New experiment rounds, harness changes, design.md |
| `data:` | Committed run artifacts (immutable CSVs) |
| `analysis:` | Analysis scripts, scoring changes, statistical work |
| `report:` | Deliverable artifacts (findings, paper, blog, charts) |
| `infra:` | Makefile, CI, shared tooling, harness infrastructure |
| `docs:` | README, CLAUDE.md, AGENTS.md, architecture docs |
| `refactor:` | Code improvement without behavior change |
| `fix:` | Bug fixes in harnesses, analysis, or tooling |

Keep commits single-purpose. Don't mix data + code in one commit.

## Pull Request Guidelines

Every PR must include:
- **Hypothesis/goal** — what question this addresses or what problem it fixes
- **What changed** — files touched, logic changes, new dependencies
- **Commands run** — exact commands used to test / verify
- **Data output paths** — if data was generated, where it lives
- **Linked issue** — every PR closes or references an issue

## Scientific Workflow

Every experiment follows: **Hypothesis → Methodology → Data → Analysis → Deliverables**.

**Before starting any experiment:**
1. Literature review (web search — don't trust training data for current benchmarks)
2. Gap analysis — what does this measure that existing work doesn't?
3. Novelty statement in `design.md`: "This produces new information because [X]. Existing work covers [Y] but not [Z]."

**Harness rules:**
- Always default to `--simulate` (deterministic, seeded, no API keys)
- `--live` requires explicit flag; document exact model + API config used
- Data files in `data/` are immutable — add timestamped copies, never overwrite
- **Simulation integrity (blocking):** Check `data/*_latest.csv` for `mode` column before
  writing any deliverable. `mode=simulate` means live data does not exist. Stop. Run `--live`
  first. Do not write findings from simulated data.
- Cross-round synthesis only combines rounds with matching `mode=live`. Simulated rounds
  are not evidence.

**Deliverable framework** — every completed experiment produces ALL of these in `report/`:

| File | Audience |
|------|----------|
| `findings.md` | Internal — raw results, tables, statistical tests |
| `paper.md` | Academic — abstract, intro, prior art, methodology, results, discussion |
| `blog_post.md` | Practitioners — 800-1500 words, what we tested, what it means |
| `executive_summary.md` | Leadership — 1-page TL;DR, key finding, recommendation |
| `social_thread.md` | Public — 3-5 post thread with hook + key finding |
| `data_card.md` | Researchers — schema, size, collection method, limitations, citation |
| `charts/` | All — PNG/SVG for every finding that can be visualized |

Deliverables are not optional polish. An experiment without deliverables is incomplete.

## Issue Labels

Use canonical org-wide labels:

**Priority** (exactly one): `p0` `p1` `p2` `p3`

**Type** (exactly one): `bug` `feature` `task` `refactor` `research` `epic`

**Horizon** (exactly one): `now` `next` `later` `blocked`

**Effort** (one): `effort/s` `effort/m` `effort/l` `effort/xl`

**Domain** (one or more): `domain/security` `domain/publication` `domain/experiment-design`
`domain/agent-eval` `domain/infra` `domain/data`

**Source**: `source/groom` `source/user` `source/agent`

Do NOT use `kind:*`, `area:*`, or `status:*` — these are legacy labels.

## Security & Configuration

- API keys via env vars only. See `.env.example`.
- Never commit secrets. Test fixtures must use fake data.
- `.env`, `.venv/`, `venv/`, and cache artifacts stay untracked.
