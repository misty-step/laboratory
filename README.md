# Laboratory

Misty Step's open science laboratory. Where hypotheses are tested, experiments are run, and knowledge is forged.

## Philosophy

We believe in scientific rigor for software engineering. Every claim should be testable. Every experiment should be reproducible. Every result should be documented.

**Observe → Hypothesize → Test → Document → Share**

## Structure

```
laboratory/
├── experiments/          # Individual experiments, each self-contained
│   └── <experiment>/
│       ├── HYPOTHESIS.md # What we're testing and why
│       ├── README.md     # Setup, methodology, how to reproduce
│       ├── results/      # Raw data and outputs
│       └── report/       # Analysis, findings, papers
├── tools/                # Shared experiment infrastructure
├── papers/               # Published findings and write-ups
└── templates/            # Experiment templates
```

## Running an Experiment

Each experiment is self-contained in its own directory under `experiments/`. To start a new one:

1. Copy `templates/experiment/` to `experiments/<your-experiment-name>/`
2. Write your `HYPOTHESIS.md` — what you're testing and what you expect
3. Build your experiment tooling
4. Run it, collect results
5. Write up findings in `report/`

## Experiments

| Experiment | Status | Summary |
|-----------|--------|---------|
| [prompt-injection-boundary-tags](experiments/prompt-injection-boundary-tags/) | Complete (Round 1 & 2) | Does wrapping CLI output in security boundary tags reduce prompt injection success rates against LLM agents? |

## Contributing

New experiment ideas welcome. File an issue with:
- **Hypothesis**: What do you want to test?
- **Why it matters**: What decision does this inform?
- **Methodology**: How would you test it?

## License

MIT
