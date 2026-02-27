# Executive Summary: Prompt Injection Defense Stacking Study

## Key Finding

Stacking five defense layers reduces prompt injection success from ~20-31% to <0.2% across all tested models and injection channels. Each layer contributes measurably; the full stack is model-agnostic — defense quality compensates for model quality.

## What We Tested

3,580 injection trials across 12 models (Anthropic, OpenAI, Google, xAI, open-weight), 12 payload categories, 2 injection channels (direct input, retrieved documents). Six rounds of experiments, each isolating different aspects of the defense stack.

## Defense Layer Effectiveness

| Layer | Marginal Reduction | Cumulative |
|-------|-------------------|------------|
| System instruction | ~50% | ~50% |
| Boundary tags (with instruction) | ~40% additional | ~93% |
| Tool-call policy filter | Catches residual | ~99.8% |

## Recommendation

Deploy all layers. The cost is negligible (20-50 tokens of system prompt, <1ms for tool-call filtering). One additional layer — output secret scanning — would address the single failure mode observed (a model leaking a secret value inside its refusal text).

## Implications

- **Model selection is less important than defense selection.** Baseline vulnerability varies 6x across models; under full defense, all converge to <0.2%.
- **RAG pipelines don't need separate defense strategies.** The same stack works on retrieval-mediated injection.
- **Classical injection attacks are obsolete.** "IGNORE ALL PREVIOUS INSTRUCTIONS" achieves 0% success. Real threats are gradual escalation and social engineering.
- **Tags without instructions can increase vulnerability.** Never deploy boundary markers without an accompanying system instruction.

## Status

Open source, MIT licensed, fully reproducible without API keys. Published by Misty Step Laboratory, February 2026.
