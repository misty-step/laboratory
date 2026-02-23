# Project: Misty Step Laboratory

## Vision

A computational science lab producing novel, reproducible findings on AI system behavior —
from prompt-injection defense to coding-agent tooling — with results that advance both
scientific understanding and engineering practice at Misty Step.

**North Star:** Established research program publishing peer-quality findings at the
intersection of AI security, agent tooling, and LLM behavior. Every completed experiment
flows through a publication pipeline; findings feed back into Misty Step's engineering
workflows.

**Target User:** Misty Step team as primary consumers; AI safety/security researchers
and practitioners building AI-powered workflows as secondary audience.

**Current Focus:** Complete glance context ablation experiment (run harness, collect data,
analyze, publish deliverables). Design publication sprint for rounds 1-7 injection findings.

**Key Differentiators:**
- Defense ablation methodology (not just vulnerability measurement — measuring each
  defense layer's independent contribution)
- Hypothesis-first, simulation-reproducible experiments (every result checkable without API keys)
- Full publication pipeline as a standard, not optional polish

## Domain Glossary

| Term | Definition |
|------|-----------|
| Round | One isolated experiment with design.md, harness, data, and report artifacts |
| Condition | A specific configuration being compared (e.g., `raw`, `tags_only`, `full_stack`) |
| Payload | An adversarial injection input used in prompt-injection experiments |
| Severity score | 0-3 scale: 0=clean, 1=acknowledged, 2=partial compromise, 3=full compromise |
| Harness | The experiment runner script (`harness/run_experiment.py`) |
| Simulate mode | Deterministic, seeded execution without API calls (default behavior) |
| Live mode | Real model API calls, requires explicit `--live` flag and API keys |
| Defense ablation | Systematic isolation of defense layers to measure each layer's contribution |
| Glance | Directory-level context summary artifacts (`.glance.md` files) for guiding coding agents |
| Context condition | In glance ablations: how context is packaged (C0=none, C1=silent, C2=explicit, C3=full inline, C4=summary+retrieval) |
| Deliverable framework | The 7 mandatory outputs per experiment: findings, paper, blog, exec summary, social thread, charts, data card |

## Experiment Families

| Family | Directory | Status | Description |
|--------|-----------|--------|-------------|
| Prompt-injection boundary tags | `experiments/prompt-injection-boundary-tags/` | Rounds 1-8 complete | Defense ablation across 5 conditions; 7 rounds of data |
| OpenCode agent model eval | `experiments/opencode-agent-models/` | Prototype complete | Bash harness measuring LLM coding-agent behavior via OpenCode CLI |
| Glance context ablations | `experiments/glance-context-ablations/` | Harness scaffolded, no data | Isolates Glance artifact presence + injection strategy as factors in coding-agent quality |

## Active Focus

- **Milestone:** Now: Current Sprint
- **In-flight:** Run glance ablation experiment (harness built, data collection pending)
- **Next:** Publication sprint — backfill all 7 deliverable artifacts for injection rounds 1-7
- **Theme:** From running experiments → publishing findings

## Quality Bar

Beyond "tests pass":
- [ ] Every completed experiment has all 7 deliverable artifacts (findings, paper, blog, exec summary, social thread, charts, data card)
- [ ] Experiments run reproducibly via `--simulate` (no API keys required)
- [ ] Every new experiment documents a novelty statement: "This produces new information because [X]"
- [ ] Hypotheses are falsifiable; conclusions address the hypothesis directly
- [ ] All backlog issues have readiness score >= 70 (agent-executable without clarification)
- [ ] Statistical significance reported where applicable

## Patterns to Follow

### Experiment directory structure
```
experiments/{family}/rounds/roundN/
├── design.md          # hypothesis + methodology + novelty statement
├── harness/
│   └── run_experiment.py  # --simulate default, --live for API
├── analysis/
│   └── analyze.py
├── data/              # immutable CSVs, timestamped
└── report/
    ├── findings.md
    ├── paper.md
    ├── blog_post.md
    ├── executive_summary.md
    ├── social_thread.md
    ├── data_card.md
    └── charts/
```

### Harness default
```python
# ALWAYS default to simulate; require explicit --live for API calls
parser.add_argument("--live", action="store_true", default=False)
```

### Data immutability
```bash
# Never overwrite existing data files; add timestamped copies
cp results.csv data/results_$(date +%Y%m%d_%H%M%S).csv
cp data/results_$(date +%Y%m%d_%H%M%S).csv data/results_latest.csv
```

## Lessons Learned

| Decision | Outcome | Lesson |
|----------|---------|--------|
| Closing model eval harness issues #19-24 | — | OpenCode experiment superseded feature-level harness issues; discrete hypothesis-driven experiments beat open-ended harness features |
| Defense ablation (rounds 1-7) | Validated that `full_stack` reduces injection rates significantly | Ablation > benchmark: measuring each layer separately is more useful than aggregate scores |
| Round-level isolation | Clean reproducibility | Don't share state between rounds; each round is self-contained |

---
*Last updated: 2026-02-23*
*Updated during: /groom session*
