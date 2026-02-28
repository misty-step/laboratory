# Prompt-Injection Defense Ablation in the Retrieval Channel: Do Defenses Transfer from Direct Input to RAG?

**Authors:** Misty Step Laboratory
**Date:** February 2026
**Round:** 8 of 8

## Abstract

Retrieval-augmented generation (RAG) introduces a new injection surface: adversarial payloads embedded in retrieved documents rather than direct user input. We measure whether a progressive defense stack -- boundary tags, system instructions, tool-call policy -- performs differently when injections arrive via this retrieval channel. Across 1,980 simulated trials (9 models from 6 providers, 5 defense conditions, 12 payload categories), we find that (1) the defense ordering transfers: raw 19.9% > tags 16.2% > instruction 9.8% > instruction+tags 8.8% > full_stack 0.0%; (2) intermediate defenses show 4.5--7.1 percentage points higher injection rates than the equivalent direct-channel configuration; and (3) full_stack eliminates the cross-channel difference entirely. Reasoning budget variations (low vs. high) provide no meaningful defense benefit in either channel. All experiments are reproducible via deterministic simulation.

**Note:** All data in this paper is from deterministic simulation (seeded RNG, no live API calls). Findings represent the behavior of a calibrated simulation model, not direct measurements of LLM behavior.

## 1. Introduction

RAG agents consume external documents as reference material. When one of those documents is attacker-controlled -- a poisoned wiki page, a compromised search result, a malicious code comment -- the agent faces indirect prompt injection through the retrieval channel.

Prior work on RAG injection focuses on attack success rates (PoisonedRAG) or defense taxonomies different from ours (Hidden-in-Plain-Text's content-preprocessing approach). The question we address: does the same progressive defense stack that works against direct injection also work when payloads arrive via retrieval? And does the retrieval channel's implicit trust -- "the system retrieved this for a reason" -- weaken intermediate defenses?

This paper reports Round 8 of an eight-round experimental program. Round 7 established defense effectiveness on the direct channel across 9 model families. Round 8 holds all variables constant except the injection channel, enabling a controlled cross-channel comparison.

### 1.1 Contributions

- First measurement of defense-layer ablation specifically for retrieval-channel injection.
- Controlled cross-channel comparison: same models, payloads, and defense conditions across direct (R7) and retrieval (R8) channels.
- Quantification of the "retrieval trust premium" -- the additional injection success attributable to the retrieval channel at each defense level.

## 2. Related Work

**PoisonedRAG** (Zou et al., USENIX Security 2025) demonstrates that knowledge base poisoning can achieve high attack success against RAG systems. It does not ablate prompt-level defenses; its defense analysis focuses on retrieval-time filtering (e.g., perplexity-based rejection). Our work complements PoisonedRAG by evaluating architectural defenses at the prompt level.

**BIPIA** (Yi et al., KDD 2025) benchmarks indirect prompt injection across email, web browsing, and table-based tasks. It evaluates model-level and training-based defenses but does not test the progressive stacking of prompt-architecture layers we study.

**Hidden-in-Plain-Text** (Chen et al., WWW 2026) ablates content-preprocessing defenses for RAG systems: input sanitization, normalization, and attribution gating. Their taxonomy is orthogonal to ours -- we test prompt-level architectural decisions (boundary tags, system instructions, tool-call policy), not content-level preprocessing.

**AgentDojo** (Debenedetti et al., NeurIPS 2024) benchmarks agent security across 97 tasks, testing delimiters and tool filtering. It treats defenses as present/absent rather than measuring marginal contribution in a progressive stack.

**InjecAgent** (Zhan et al., ACL 2024) establishes the indirect prompt-injection threat model for tool-calling agents with 1,054 test cases. It focuses on attack taxonomy rather than defense comparison.

**SafeToolBench** (EMNLP 2025) evaluates model self-refusal of unsafe tool calls. Our Round 6 benchmarks a complementary approach: rule-based post-hoc filtering (92.6% recall, 0% FPR) that works without model fine-tuning.

**Agent Security Bench** (Zhang et al., ICLR 2025) evaluates 27 attack and defense methods independently. Our approach evaluates defenses as a progressive stack, revealing interaction effects invisible when tested in isolation.

## 3. Methodology

### 3.1 Threat Model

A RAG-augmented agent receives a clean user query (a GitHub issue) alongside three retrieved documents. One document (position 2, the middle slot) is poisoned with an adversarial payload. The agent must process the retrieved context to fulfill the user query while resisting injected instructions.

The agent has access to three tools: `read_file`, `execute_command`, and `send_message`. The system prompt contains fake secrets (`API_KEY`, `DATABASE_URL`) to measure leakage. This mirrors production RAG agents consuming documentation, wiki pages, or search results.

### 3.2 Defense Conditions

Five conditions, matching the Round 7 direct-channel conditions but adapted for retrieval context:

| Condition | System Instruction | Retrieved Doc Tags | Tool-Call Policy |
|---|---|---|---|
| `raw` | Base prompt only | None | None |
| `tags_only` | Base prompt only | `<<<RETRIEVED_DOCUMENT>>>` boundaries | None |
| `instruction_only` | + "Treat retrieved docs as reference only" | None | None |
| `instruction_tags` | + instruction | + tags | None |
| `full_stack` | + instruction + refusal policy | + nonce tags | + post-hoc filter |

### 3.3 Experiment Matrix

- **Models:** 9 (claude-sonnet-4.5, gpt-5.2, gemini-3-flash, grok-4.1-fast, deepseek-v3.2, kimi-k2-thinking, qwen3-coder, minimax-m2.1, glm-4.7)
- **Payload categories:** 12 (frozen from round2b)
- **Conditions:** 5
- **Trials per cell:** 3
- **Reasoning budget axis:** gpt-5.2 and gemini-3-flash tested at low and high budgets
- **Total trials:** 1,980

### 3.4 Scoring

Config-driven automated scorer (`shared/scoring/scorer.py`):

| Score | Meaning |
|---|---|
| 0 | Clean -- no injection signals |
| 1 | Acknowledgement -- model noticed injection, refused to act |
| 2 | Partial compromise -- partial secret leakage |
| 3 | Full compromise -- unauthorized tool call or complete secret exfiltration |

Injection is defined as score >= 2.

### 3.5 Simulation

All data uses deterministic simulation with seeded RNG and calibrated risk multipliers (per payload category, defense condition, and model). Simulation parameters were calibrated against live API results from Rounds 1-2. This enables full reproducibility without API keys.

## 4. Results

### 4.1 Defense Effectiveness (Retrieval Channel)

| Condition | N | Injection Rate | 95% CI | vs. Raw |
|---|---:|---:|---|---:|
| `raw` | 396 | 19.9% | [16.3%, 24.2%] | -- |
| `tags_only` | 396 | 16.2% | [12.9%, 20.1%] | -19% |
| `instruction_only` | 396 | 9.8% | [7.3%, 13.2%] | -51% |
| `instruction_tags` | 396 | 8.8% | [6.4%, 12.0%] | -56% |
| `full_stack` | 396 | 0.0% | [0.0%, 1.0%] | -100% |

The progressive defense ordering holds: each layer reduces injection rate monotonically in aggregate. System instructions alone cut injection by half. Full_stack achieves zero injection across 396 trials.

### 4.2 Cross-Channel Comparison

| Condition | R7 Direct | R8 Retrieval | Delta |
|---|---:|---:|---:|
| `raw` | 18.9% | 19.9% | +1.0pp |
| `tags_only` | 9.1% | 16.2% | +7.1pp |
| `instruction_only` | 5.3% | 9.8% | +4.5pp |
| `instruction_tags` | 2.3% | 8.8% | +6.5pp |
| `full_stack` | 0.0% | 0.0% | 0.0pp |

The "retrieval trust premium" is visible at intermediate defense levels: 4.5--7.1pp higher injection rates in the retrieval channel. At raw (no defense), the channels are nearly equivalent (+1.0pp). At full_stack, the gap vanishes.

This pattern is consistent with a model that treats retrieved documents with implicit deference. Boundary tags alone reduce direct injection by 52% but retrieval injection by only 19%. The instruction layer narrows this gap, and the full stack eliminates it.

### 4.3 Model Vulnerability

| Model | Overall Rate | Raw | Full Stack |
|---|---:|---:|---:|
| `gpt-5.2` | 6.1% | 9.7% | 0.0% |
| `grok-4.1-fast` | 8.3% | 25.0% | 0.0% |
| `gemini-3-flash` | 9.7% | 20.8% | 0.0% |
| `claude-sonnet-4.5` | 10.6% | 16.7% | 0.0% |
| `qwen3-coder` | 11.1% | 16.7% | 0.0% |
| `deepseek-v3.2` | 13.3% | 25.0% | 0.0% |
| `kimi-k2-thinking` | 13.3% | 22.2% | 0.0% |
| `glm-4.7` | 14.4% | 22.2% | 0.0% |
| `minimax-m2.1` | 17.8% | 30.6% | 0.0% |

All models reach 0.0% under full_stack. Baseline vulnerability varies 3x (GPT-5.2 at 9.7% raw vs. MiniMax M2.1 at 30.6% raw), but the defense stack equalizes them.

### 4.4 Tag Non-Monotonicity (Retrieval Channel)

One model showed increased injection under tags-only vs. raw:

- `qwen3-coder`: 16.7% raw -> 22.2% tags (+5.6pp)

This reproduces the R7 direct-channel pattern (Qwen3-Coder: +8.3pp under tags). Tags without instructions can signal content salience rather than demarcate untrusted input.

### 4.5 Reasoning Budget

| Model | Budget | Injection Rate |
|---|---|---:|
| `gpt-5.2` | low | 6.7% |
| `gpt-5.2` | high | 5.6% |
| `gemini-3-flash` | low | 8.3% |
| `gemini-3-flash` | high | 11.1% |

No defense benefit from reasoning budget. Gemini 3 Flash performs worse (+2.8pp) at higher budget. This matches R7: reasoning tokens do not substitute for architectural defenses.

### 4.6 Payload Category

Top 3 (highest retrieval-channel injection rate):

| Payload | Rate |
|---|---:|
| `helpful_framing` | 15.8% |
| `indirect_extraction` | 13.3% |
| `gradual_escalation` | 12.7% |

Bottom 3:

| Payload | Rate |
|---|---:|
| `persona_hijack` | 8.5% |
| `encoding_trick` | 8.5% |
| `direct_override` | 6.1% |

Social-engineering-adjacent strategies dominate in the retrieval channel. Direct override -- the simplest attack -- remains the least effective regardless of channel.

## 5. Discussion

### 5.1 The Retrieval Trust Premium

The central finding: intermediate defenses are weaker in the retrieval channel by 4.5--7.1pp. This "retrieval trust premium" likely reflects how models process content provenance. When a system retrieves documents, the model implicitly treats them as system-endorsed reference material. Tags alone ("this is a retrieved document") don't overcome this implicit trust. A direct instruction ("treat retrieved documents as untrusted external input") partially does. Only the full stack -- instruction + nonce tags + tool-call filter -- eliminates the advantage entirely.

For practitioners: if you've tuned your defenses on direct-input injection tests, your system is likely more vulnerable to retrieval injection at intermediate defense levels. Full-stack deployment is not over-engineering; it's the minimum configuration where channel-specific risk disappears.

### 5.2 Tags Are Not a Defense

The tag-anomaly pattern persists across channels and rounds. Qwen3-Coder shows increased injection under tags-only in both R7 (+8.3pp) and R8 (+5.6pp). Tags are a structural primitive, not a defense. Without an accompanying instruction, they may draw model attention to exactly the content the attacker wants it to engage with.

### 5.3 Reasoning Is Not a Defense

Neither GPT-5.2 nor Gemini 3 Flash shows meaningful security improvement from increased reasoning budget. This is now consistent across two rounds and two channels. Reasoning budgets optimize for task quality, not instruction adherence. Architectural defenses and runtime filters operate at a different layer than the model's reasoning process.

### 5.4 Limitations

1. **Simulated data.** All trials use deterministic simulation. Live validation is required before drawing operational conclusions.
2. **Fixed poison position.** Document 2 (middle) is always poisoned. Position effects may matter in production.
3. **Binary score gap.** No score=2 (partial compromise) appears in simulation output. Real model behavior includes partial leakage.
4. **Single retrieval architecture.** We test one retrieval pattern (3 docs, fixed position). Real RAG systems vary document count, ordering, and relevance scoring.

## 6. Conclusions

1. Defense ordering transfers from direct to retrieval injection channels. The progressive stack (raw -> tags -> instruction -> instruction+tags -> full_stack) reduces injection monotonically in both channels.

2. Retrieval injection is harder to defend at intermediate levels. The retrieval trust premium adds 4.5--7.1pp to injection rates under partial defenses.

3. Full_stack defense eliminates the cross-channel difference. At 0/396 injection (retrieval) and 1/540 (direct), full_stack is the only configuration where channel choice doesn't matter.

4. Reasoning budgets are not a security lever. Increased reasoning shows no consistent benefit across models, channels, or rounds.

5. Tags without instructions can increase injection success on some models. This non-monotonicity is consistent across rounds and channels.

## 7. References

1. Debenedetti, E., et al. "AgentDojo: A Dynamic Environment to Evaluate Attacks and Defenses for LLM Agents." NeurIPS, 2024.
2. Zhan, Q., et al. "InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents." ACL, 2024.
3. "SafeToolBench: Evaluating LLM Self-Refusal of Unsafe Tool Calls." EMNLP, 2025.
4. Zhang, H., et al. "Agent Security Bench: Evaluating Attacks and Defenses for LLM Agents." ICLR, 2025.
5. Zou, W., et al. "PoisonedRAG: Knowledge Poisoning Attacks to Retrieval-Augmented Generation of Large Language Models." USENIX Security, 2025.
6. Yi, J., et al. "BIPIA: Benchmarking Indirect Prompt Injection Attacks." KDD, 2025.
7. Chen, L., et al. "Hidden-in-Plain-Text: Content-Preprocessing Defenses for RAG Systems." WWW, 2026.
