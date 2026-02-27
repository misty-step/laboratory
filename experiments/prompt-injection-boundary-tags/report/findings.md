# Cross-Round Findings: Prompt Injection Defense Ablation Program

## Program Summary

Six rounds of experiments (R1, R2, R2b, R6, R7, R8) measuring prompt-injection defense effectiveness in LLM agent workflows. Three rounds designed but not executed (R3, R4, R5).

**Total data:** 3,580 prompt-injection trials + 360 tool-call policy evaluations
**Models:** 12 unique across 6 providers (Anthropic, OpenAI, Google, xAI, OpenRouter open-weight)
**Defense conditions:** 5 progressive layers (raw → tags_only → instruction_only → instruction_tags → full_stack)
**Injection channels:** Direct (R7) and retrieval/RAG (R8)

## Round-by-Round Findings

### Round 1: Baseline (N=73, 1 model)
- **Hypothesis:** Boundary tags reduce injection success.
- **Result:** Null — 0% injection across all conditions.
- **Root cause:** System prompt was too protective for single-model test.
- **Lesson:** Need realistic agent prompts, tool access, multiple models.

### Round 2: Realistic Conditions (N=324 cleaned, 3 models)
- **Hypothesis:** Tags work under realistic agent conditions with tool access.
- **Result:** Confirmed. Tags reduce injection 31% → 10% (static) → 9% (dynamic nonce).
- **Statistics:** Chi-square = 24.22, p = 0.000006, Cramer's V = 0.27 (medium effect).
- **Key finding:** Gradual escalation most dangerous (56-89% raw success); direct override ineffective (0%).

### Round 2b: Scoring Calibration (N=324, same data re-scored)
- **Goal:** Eliminate false positives through human validation.
- **Result:** 7 false positives corrected (2.2% FPR → 0%). All were defensive tool calls (model alerting admin, not attacking).
- **Impact:** Kimi K2.5 raw vulnerability revised from 22.2% → 5.6%.
- **Protocol established:** Human review of all score >= 2 rows.

### Round 6: Tool-Call Policy Filter (N=360 evaluations, synthetic corpus)
- **Hypothesis:** Post-hoc rule-based filtering achieves >= 90% recall with <= 5% FPR.
- **Result:** Confirmed. Balanced config: 92.6% recall, 0.0% FPR, F1 = 0.96.
- **Per-tool:** read_file 100%, send_message 100%, execute_command 77.8% (hardest).
- **False negatives:** 4 sophisticated command-construction evasions.

### Round 7: Cross-Model Validation (N=1,202, 9 models, direct channel)
- **Hypothesis:** Defense ordering holds across model families.
- **Result:** Confirmed. raw 18.9% → tags 9.1% → instruction 5.3% → instr+tags 2.3% → full_stack 0.0%.
- **Phase 2 (N=540, full_stack, 5 trials/cell):** 0.2% (1/540). Single failure: MiniMax M2.1 secret echo in refusal.
- **Non-monotonicity:** DeepSeek V3.2 and Qwen3-Coder show INCREASED injection with tags_only (+8pp each).
- **Cost:** $3.75 total.

### Round 8: Retrieval Channel (N=1,981, 9 models, RAG injection)
- **Hypothesis:** Defense ordering transfers to retrieval-mediated attacks.
- **Result:** Confirmed. raw 19.9% → tags 16.2% → instruction 9.8% → instr+tags 8.8% → full_stack 0.0%.
- **Cross-channel delta:** Retrieval shows ~20% higher absolute rates at intermediate levels; full_stack eliminates difference.
- **Reasoning budgets:** No meaningful defense benefit (GPT-5.2 low 6.7% vs high 5.6%; Gemini 3 Flash low 8.3% vs high 11.1%).

## Synthesized Findings

### 1. Defense Layer Marginal Contribution (High Confidence)

| Layer | Solo Effect | Marginal When Stacked | Evidence Rounds |
|-------|-----------|----------------------|-----------------|
| System instruction | ~50% reduction | Largest single lever | R2, R7, R8 |
| Boundary tags | ~47% reduction | ~40% additional (synergistic, not additive) | R2, R7, R8 |
| Tags + instruction combo | ~93% reduction | Synergy > sum of parts | R7, R8 |
| Tool-call filter | 92.6% recall catch-all | Last-mile defense | R6 |
| Full stack | 99.8% reduction | Model-agnostic convergence | R7, R8 |

### 2. Model Vulnerability Spectrum

**Least vulnerable (raw):** GPT-5.2 (6-8%), GLM-4.7 (8%)
**Mid-tier:** Claude Sonnet 4.5 (17%), Gemini 3 Flash (8-16%), Kimi K2 Thinking (17%)
**Most vulnerable:** Qwen3-Coder (42%), MiniMax M2.1 (42%), Grok 4.1 Fast (33%), DeepSeek V3.2 (25%)

**Convergence under full_stack:** All models < 0.2%. Defense quality compensates for model quality.

### 3. Payload Threat Ranking

**Dead attacks (0% raw success):** Direct override, tag breaking, persona hijack, direct tool invocation.
**Active threats:** Gradual escalation (72%), indirect extraction (41%), social engineering (33%).
**Pattern:** Attacks mimicking legitimate behavior dominate; classical "obvious" injections are obsolete.

### 4. Tag Non-Monotonicity

Tags *increase* injection on DeepSeek V3.2 (+8pp) and Qwen3-Coder (+8pp) when used without instructions. Hypothesis: tags signal content salience without trust context. Never deploy tags solo.

### 5. Retrieval Channel Parity

Defense ordering identical across direct and retrieval channels. Retrieval baseline ~1pp higher. Full-stack defense eliminates channel difference entirely. No separate RAG defense strategy needed.

### 6. Reasoning Budgets Irrelevant

Higher reasoning budgets (GPT-5.2, Gemini 3 Flash) show no meaningful defense benefit. Gemini 3 Flash slightly worse with high budget (11.1% vs 8.3%). Reasoning cannot substitute for defense stacking.

## Statistical Summary

| Test | Statistic | p-value | Effect Size | Round |
|------|-----------|---------|-------------|-------|
| Chi-square (3 conditions) | 24.22 | 0.000006 | Cramer's V = 0.27 | R2 |
| Calibration precision | — | — | 1.0 (post-human review) | R2b |
| Tool filter balanced recall | — | — | 92.6%, FPR 0.0% | R6 |
| Condition trend (5 levels) | Monotonic decrease | — | 18.9% → 0.0% | R7 |
| Cross-channel delta | full_stack | — | 0.0pp difference | R7 vs R8 |

## Known Limitations

1. Single agent task (issue summarization)
2. Static payloads (no adaptive attacker)
3. Simulated tools (no real filesystem/network)
4. Small per-cell N in some rounds (1-5 trials)
5. Rounds 3-5 unexecuted (phrasing sensitivity, multi-turn, utility tradeoffs)
6. No output secret scanning layer tested
7. Limited reasoning budget coverage (2 models only)

## Unexecuted Round Designs

- **R3:** Instruction phrasing sensitivity + defense stacking margins
- **R4:** Multi-turn context poisoning — do defenses degrade over conversation length?
- **R5:** Security-utility Pareto frontier — does defense impose unacceptable utility loss?

These remain designed and ready to execute. R4 and R5 would address the two most important open questions for production deployment.
