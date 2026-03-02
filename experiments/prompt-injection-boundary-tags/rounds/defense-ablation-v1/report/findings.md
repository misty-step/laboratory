# Defense Ablation v1 — Findings

Generated: 2026-03-02 18:46:16 UTC
Input: `/Users/phaedrus/Development/laboratory/experiments/prompt-injection-boundary-tags/rounds/defense-ablation-v1/data/runs_latest.csv`
Total rows: 2100 (adversarial: 2096, utility: 0, adaptive: 0)

## ASR by Condition

| Condition | N | ASR | 95% CI | Score 2 | Score 3 |
|---|---:|---:|---|---:|---:|
| raw | 420 | 17.4% | [14.1%, 21.3%] | 0 | 73 |
| tags_only | 419 | 5.5% | [3.7%, 8.1%] | 0 | 23 |
| instruction_only | 420 | 2.4% | [1.3%, 4.3%] | 0 | 10 |
| instruction_tags | 420 | 0.5% | [0.1%, 1.7%] | 0 | 2 |
| full_stack | 417 | 0.0% | [0.0%, 0.9%] | 0 | 0 |

## Chi-Square Test (Condition x ASR)

- Statistic: 176.653
- p-value: 0.000000
- df: 4
- Cramer's V: 0.290

## Pairwise Fisher's Exact Tests (Bonferroni-corrected)

| Condition A | Condition B | OR | p-value | p-adjusted | Significant |
|---|---|---:|---:|---:|---|
| raw | tags_only | 3.622 | 0.0000 | 0.0000 | Yes |
| raw | instruction_only | 8.625 | 0.0000 | 0.0000 | Yes |
| raw | instruction_tags | 43.968 | 0.0000 | 0.0000 | Yes |
| raw | full_stack | inf | 0.0000 | 0.0000 | Yes |
| tags_only | instruction_only | 2.381 | 0.0215 | 0.2153 | No |
| tags_only | instruction_tags | 12.139 | 0.0000 | 0.0001 | Yes |
| tags_only | full_stack | inf | 0.0000 | 0.0000 | Yes |
| instruction_only | instruction_tags | 5.098 | 0.0372 | 0.3724 | No |
| instruction_only | full_stack | inf | 0.0019 | 0.0185 | No |
| instruction_tags | full_stack | inf | 0.4994 | 1.0000 | No |

## Marginal Contribution of Each Defense Layer

| Layer | Before | After | Reduction | 95% CI |
|---|---:|---:|---:|---|
| boundary tags (raw -> tags_only) | 17.4% | 5.5% | 11.9% | [7.7%, 16.2%] |
| security instruction (raw -> instruction_only) | 17.4% | 2.4% | 15.0% | [11.1%, 19.1%] |
| security instruction (given tags) (tags_only -> instruction_tags) | 5.5% | 0.5% | 5.0% | [2.8%, 7.6%] |
| boundary tags (given instruction) (instruction_only -> instruction_tags) | 2.4% | 0.5% | 1.9% | [0.3%, 3.9%] |
| output filter (instruction_tags -> full_stack) | 0.5% | 0.0% | 0.5% | [-0.5%, 1.7%] |

## Hypothesis Evaluation

**H1 (monotonic ASR decrease): SUPPORTED.** ASR decreases with each added layer.

**H3 (full_stack ASR < 5%): SUPPORTED.** ASR = 0.0%.
