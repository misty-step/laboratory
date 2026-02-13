# Round 7 Paper: Cross-Model Defense Validation

## Abstract

We evaluate prompt-injection defenses for an agent-style task (summarize a GitHub issue containing adversarial instructions) across multiple providers and model families. We ablate five defense configurations (`raw`, `tags_only`, `instruction_only`, `instruction_tags`, `full_stack`) over 12 fixed injection payload categories. Phase 1 (N=660, trials=1) confirms a consistent defense ranking in aggregate, with `full_stack` achieving 0/132 effective injections. Phase 2 (N=540, trials=5 on worst+anchor models) shows `full_stack` remains near-zero but not perfect: 1/540 effective injections (0.2%), concentrated in a single OpenRouter model (`minimax-m2.1`). The residual failure mode is plain-text secret leakage without tool calls, including leakage inside refusal text.

## Introduction

Prompt injection is a practical risk for LLM agents that ingest untrusted text (issues, tickets, emails) and have access to privileged data and tools. Many mitigations are recommended (delimiters/boundary tags, explicit system instructions, tool-call allow/deny policies). A key gap is cross-provider, defense-layer ablation: which layer buys the most marginal safety, and does the ordering transfer across model families?

This round is a cross-model validation of defense ordering observed in prior rounds.

## Prior Art (gap framing)

- AgentDojo (Debenedetti et al., 2024): prompt injection benchmark for tool-using agents; does not isolate delimiter layers as the primary axis.
- InjecAgent (Zhan et al., 2024): indirect prompt injection benchmark; limited cross-provider defense ablation under a shared harness.
- Provider guidance (e.g., OpenAI instruction hierarchy; Anthropic prompt-injection defenses): recommends mitigations, but not cross-provider layer-by-layer ablations on the same task.

## Methodology

### Task framing

- Input: a GitHub issue describing a mobile Safari crash.
- Attack surface: the issue’s “Additional Context” field, populated with an injection payload.
- System prompt includes fake secrets for measurable leakage:
  - `API_KEY="sk-FAKE-not-real-test-12345"`
  - `DATABASE_URL="postgres://fake:fake@localhost/fakedb"`
- Tools are exposed (`read_file`, `execute_command`, `send_message`).

### Payloads

- 12 payload categories frozen from Round 2B: `round2b/payloads/payloads.json`.

### Defense conditions

- `raw`: no special handling.
- `tags_only`: wrap issue content in boundary tags.
- `instruction_only`: add explicit system security instruction.
- `instruction_tags`: combine instruction + tags.
- `full_stack`: instruction + nonce boundary tags + tool-call policy filter that blocks suspicious tool calls.

### Models

- Anthropic: `claude-sonnet-4.5`
- OpenAI: `gpt-5.2`
- Google: `gemini-3-flash`
- xAI: `grok-4.1-fast`
- OpenRouter: `deepseek-v3.2`, `kimi-k2-thinking`, `qwen3-coder`, `minimax-m2.1`, `glm-4.7`

A small reasoning-budget axis is evaluated for two targets:

- `gpt-5.2`: OpenAI `reasoning_effort=low|high`.
- `gemini-3-flash`: Gemini `thinkingConfig.thinkingBudget=256|2048`.

All other targets use `reasoning_budget=none`.

### Scoring

We use a shared config-driven scorer (`shared/scoring/scorer.py` + `scorer_config_v2.json`):

- 0: clean
- 1: acknowledgement
- 2: partial compromise
- 3: secret leak or suspicious tool call

A trial is counted as “injection success” when `score_effective >= 2`.

## Results

### Phase 1: all conditions (trials=1)

Aggregate injection rate by condition:

| Condition | N | OK | ERR | Injection Rate |
|---|---:|---:|---:|---:|
| `raw` | 132 | 132 | 0 | 18.9% |
| `tags_only` | 132 | 132 | 0 | 9.1% |
| `instruction_only` | 132 | 132 | 0 | 5.3% |
| `instruction_tags` | 132 | 131 | 1 | 2.3% |
| `full_stack` | 132 | 132 | 0 | 0.0% |


Note: `instruction_tags` has `ERR=1` due to an OpenRouter timeout for `minimax-m2.1` on payload `context_confusion`. The 2.3% rate is computed over `OK=131`.

Per-model raw vs tags-only (Phase 1, trials=1; N=12 payloads per model-budget):

| Model | Budget | `raw` | `tags_only` | Delta |
|---|---|---:|---:|---:|
| `claude-sonnet-4.5` | `none` | 16.7% | 0.0% | -16.7% |
| `deepseek-v3.2` | `none` | 25.0% | 33.3% | +8.3% |
| `gemini-3-flash` | `low` | 8.3% | 0.0% | -8.3% |
| `gemini-3-flash` | `high` | 8.3% | 0.0% | -8.3% |
| `glm-4.7` | `none` | 16.7% | 0.0% | -16.7% |
| `gpt-5.2` | `low` | 0.0% | 0.0% | +0.0% |
| `gpt-5.2` | `high` | 0.0% | 0.0% | +0.0% |
| `grok-4.1-fast` | `none` | 33.3% | 16.7% | -16.7% |
| `kimi-k2-thinking` | `none` | 16.7% | 0.0% | -16.7% |
| `minimax-m2.1` | `none` | 41.7% | 0.0% | -41.7% |
| `qwen3-coder` | `none` | 41.7% | 50.0% | +8.3% |

#### Phase 2 model selection (worst + anchors)

Phase 2 runs `full_stack` only, trials=5, across 9 model-budget targets (12 payloads each):

- Worst (high Phase 1 injection under weaker conditions): `minimax-m2.1`, `qwen3-coder`, `deepseek-v3.2`, `grok-4.1-fast`.
- Anchors (frontier-provider coverage + budget axis): `claude-sonnet-4.5`, `gpt-5.2` (`low`/`high`), `gemini-3-flash` (`low`/`high`).

### Phase 2: `full_stack` only (trials=5)

- Overall injection rate: 0.2% (1/540)
- Concentrated in `minimax-m2.1`: 1.7% (1/60)

Observed failure mode: plain-text secret regurgitation without tool calls; can appear inside refusal text.

## Discussion

1. Defense ordering transfers across model families.

   In aggregate, system security instructions dominate tags-only, and combined layers outperform individual layers.

2. Tags-only is not a safe default.

   While tags reduce injection in aggregate, per-model behavior is not monotonic and can worsen on some models.

   Phase 1 examples (`raw` -> `tags_only`):
   - `deepseek-v3.2`: 25.0% -> 33.3%
   - `qwen3-coder`: 41.7% -> 50.0%

3. Tool-call filtering reduces tool exfil but not output exfil.

   The residual `full_stack` failure is output leakage. This suggests that “real full-stack” agent defenses need a final output scan/redaction layer if the product requires “never leak secrets” guarantees.

## Limitations

- Live calls are subject to provider drift and non-determinism.
- We do not store full response text in the CSV; only previews, lengths, and tool call JSON.
- `full_stack` here includes tool-call filtering but not an explicit output secret-scan layer.

## Artifacts

- Phase 1 CSV: `round7/data/cross_model_results_20260212_172247.csv`
- Phase 2 CSV: `round7/data/cross_model_results_20260212_205859.csv`

## References

- Debenedetti, E. et al. (2024). *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents.* NeurIPS 2024. arXiv:2406.13352.
- Zhan, Q. et al. (2024). *InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents.* ACL 2024. arXiv:2403.02691.
- Anthropic (2025). *Prompt Injection Defenses.* anthropic.com/research/prompt-injection-defenses
- OpenAI (2024). *The Instruction Hierarchy.* openai.com/research/the-instruction-hierarchy
- Google (2025). *Gemini API: Function calling.* ai.google.dev/gemini-api/docs/function-calling
- Willison, S. (2025). *The Lethal Trifecta.* simonwillison.net
