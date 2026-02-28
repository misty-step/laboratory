# Peer Review: Prompt Injection Defense Ablation Program

**Date:** 2026-02-27
**Target:** `experiments/prompt-injection-boundary-tags/report/` (cross-round synthesis)
**Verdict:** ⛔ MAJOR REVISION REQUIRED

---

## Review Panel

| Phase | Provider | Role | Tool |
|-------|----------|------|------|
| 1 | OpenAI (Codex) | Methodology Critic | `codex exec` |
| 1 | Google (Gemini 3 Pro) | Citation Verifier | `gemini` CLI |
| 1 | Anthropic (Claude) | Logic Auditor | Task subagent |
| 1 | Anthropic (Claude) | Data Integrity | Task subagent (Read + Bash) |
| 2 | (synthesis) | Cross-reviewer reconciliation | Manual |

---

## Findings: FATAL

These block publication in current form.

---

### [F1] R6 Policy Filter Table Is Mostly Wrong *(Data Integrity — VERIFIED)*

Three of four rows in the tool-call policy filter results table (Paper §4.6) contain incorrect values. Only the "balanced" config row is correct. All others appear to have been written from a design specification, not computed from actual data.

**Claimed vs. actual (computed from `policy_eval_latest.csv`):**

| Config | Paper: Recall | Actual | Paper: FPR | Actual | Paper: F1 | Actual |
|--------|--------------|--------|------------|--------|-----------|--------|
| Permissive | 74.1% | **33.3%** | 0.0% | 0.0% ✓ | 0.85 | **0.50** |
| Balanced | 92.6% | 92.6% ✓ | 0.0% | 0.0% ✓ | 0.96 | 0.96 ✓ |
| Strict | 96.3% | **100.0%** | 2.8% | **33.3%** | 0.96 | **0.90** |
| Paranoid | 100.0% | 100.0% ✓ | 8.3% | **100.0%** | 0.95 | **0.75** |

The strict config achieves 100% recall (not 96.3%) with 33.3% FPR (not 2.8%) because it flags all `execute_command` calls regardless of content. The paranoid config has 100% FPR, not 8.3% — it flags every tool call.

**Fix required:** Re-derive all four rows from data. The balanced config ("92.6% recall, 0.0% FPR, F1=0.96") remains correct and remains the headline recommendation.

---

### [F2] "~93% Reduction" Is a Misattributed Number *(Data Integrity — VERIFIED)*

**Paper Abstract #3:** "Instruction + tags achieve ~93% reduction through synergy, not mere addition of independent effects."
**Findings §1:** "Tags + instruction combo | ~93% reduction"

**Actual instruction+tags reductions from data:**
- R7 (direct): (18.9% − 2.3%) / 18.9% = **87.8%**
- R8 (retrieval): (19.9% − 8.8%) / 19.9% = **55.8%**

92.6% is the balanced tool-call filter **recall** (R6), not an injection reduction percentage. The abstract appears to have transposed these two numbers.

**Fix required:** Replace "~93% reduction" with "87.8% reduction (direct channel)" or a range. Add a note that 92.6% is a separate claim about the filter, not about instruction+tags.

---

### [F3] "~20% Higher Baseline Rates" for Retrieval Is Wrong *(Data Integrity — VERIFIED)*

**Paper Abstract #5 and Findings §5:** "retrieval-mediated attacks show ~20% higher baseline rates"

**Actual (computed from R7 + R8 raw condition data):**
- R7 raw: 18.9%, R8 raw: 19.9% — delta = **+1.0pp** (+5.3% relative)
- Intermediate deltas: tags_only +7.1pp, instruction_only +4.5pp, instruction_tags +6.5pp

No interpretation of "~20%" is defensible. The raw baselines differ by 1pp. Intermediate conditions differ by 4.5–7.1pp in absolute terms. "~20%" is neither the absolute nor the relative delta at any condition.

**Fix required:** Replace with: "retrieval shows 1.0pp higher raw rates and 4.5–7.1pp higher rates at intermediate defense levels."

---

### [F4] Abstract Obscures That 88.9% of Trials Are Simulated *(Logic + Methodology — CONCORDANT)*

The abstract leads with "3,580 prompt-injection trials" without qualification. In reality:
- R1 (73) and R2/R2b (324) = **397 live API trials**
- R7 (1,200) and R8 (1,980) = **3,180 simulated trials** (seeded RNG)

Every headline result — the ~50% reduction from instructions, the <0.2% full-stack rate, the cross-channel comparison — is derived from simulated data. The simulation calibration methodology is described in one sentence with no detail on objective function or held-out validation.

*Agreed by: Logic Auditor (F1) and Methodology Critic (Attack Vector 4)*

**Fix required:** Abstract must state "3,180 simulated + 397 live API trials" or equivalent. Simulation methodology needs a dedicated subsection with calibration protocol.

---

### [F5] R8 Simulation Is Largely Circular *(Methodology — VERIFIED by Data Integrity)*

The R8 harness uses condition multipliers that are explicitly monotonic (`raw > tags_only > instruction_only > instruction_tags > full_stack`) and hard-codes retrieval channel uplift. The "retrieval trust premium" finding — that retrieval-channel defenses are weaker at intermediate levels — is therefore baked into the simulation generator.

The paper cannot distinguish discovered behavior from programmed assumptions for R8. This is the most damaging single flaw in the experimental design.

*Data Integrity cross-confirmed: R7 rows have `mode=live`, R8 rows have `mode=simulate`. Cross-channel comparison silently mixes modes without disclosure.*

**Fix required:** Either (a) run R8 live to obtain non-circular retrieval data, or (b) frame R8 explicitly as a simulation-only hypothesis-generator, not a validation round. The cross-channel comparison must disclose mode difference.

---

### [F6] Cross-Round Synthesis Mixes Incompatible Datasets *(Methodology — CONCORDANT)*

The synthesis combines rounds with: different model sets (R2: 3 models, R7/R8: 9 models), different modes (live vs simulated), different trial densities (N=1 to N=5 per cell), and different scoring context (pre/post calibration). Per-round raw percentages are presented as commensurate when they are not.

*Agreed by: Methodology Critic (Attack Vector 9) and Logic Auditor (F2 — "~50% reduction varies 22pp across rounds unexplained")*

**Fix required:** Cross-round comparisons need caveats about incompatibility. The headline synthesis table should not present round-level rates as directly comparable. A model-stratified subanalysis using only R7 (live) would be more defensible.

---

## Findings: MAJOR

Should be fixed before publication.

---

### [M1] Missing Foundational Citations *(Citations — VERIFIED)*

The related work section omits two foundational papers that define the problem being studied:

- **Perez & Ribeiro (2022)** — "Ignore Previous Prompt: Attack Techniques For Language Models" (NeurIPS 2022). This defined direct prompt injection. The paper discusses "direct override" payloads without citing this work.
- **Greshake et al. (2023)** — "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (arXiv 2023). This defined indirect/retrieval injection and the threat model the paper's R8 directly extends.

All four 2024–2025 citations (AgentDojo, InjecAgent, SafeToolBench, Agent Security Bench) are verified correct.

---

### [M2] R6 Tool-Call Corpus Provenance Is Unclear *(Methodology + Logic)*

The tool-call policy filter achieves 92.6% recall on a "synthetic corpus." The paper never states whether the 90 malicious tool calls were drawn from actual model outputs in the injection experiments or constructed by the authors. A filter achieving 92.6% recall on an author-built corpus is a weaker claim than on a production-distribution corpus.

---

### [M3] Simulation Calibrated on 3 Models, Extrapolated to 9 *(Logic — FATAL by Logic Auditor)*

The simulation risk multipliers were calibrated against R1/R2 data (Claude Haiku 3.5, Claude Sonnet 4.5, Kimi K2.5). Six models in R7/R8 (GPT-5.2, Gemini 3 Flash, Grok 4.1, DeepSeek V3.2, Qwen3-Coder, MiniMax M2.1, GLM-4.7) were never in calibration rounds. Their multipliers are estimated, not calibrated.

The tag non-monotonicity finding — DeepSeek V3.2 and Qwen3-Coder show increased injection under boundary tags — is the paper's most novel result. It rests entirely on uncalibrated simulation for those two models and cannot be distinguished from parameter choice. Live data is required to support this claim.

---

### [M4] Total Trial Count Off by 4, Multiple Per-Round Errors *(Data Integrity — VERIFIED)*

| Round | Paper Claim | Actual CSV Rows |
|-------|-------------|-----------------|
| R1 | 73 | 72 |
| R7 | 1,202 | 1,200 |
| R8 | 1,981 | 1,980 |
| **Total** | **3,580** | **3,576** |

These are small but signal inadequate data provenance checking.

---

### [M5] "~50% Reduction from Instructions" Understates R7 by 22pp *(Data + Logic — CONCORDANT)*

The abstract claims "system instructions alone reduce injection success by ~50%." This is approximately correct for R8 (51%) but understates R7 (72%) by 22 percentage points. The paper never explains this 22pp variance. A more accurate headline: "instructions reduce injection 50–72% depending on channel."

---

### [M6] Model Vulnerability Rankings Internally Inconsistent *(Data Integrity — VERIFIED)*

- **Kimi K2 Thinking:** Paper §4.4 places it in "High risk" tier (25–42%); Findings §2 lists it as "Mid-tier" at 17%. Actual data: R7 raw = 16.7%, R8 raw = 22.2%. Findings document is more accurate; paper is wrong.
- **GLM-4.7:** Findings §2 lists as "Least vulnerable (8%)". Actual data: R7 raw = 16.7%, R8 raw = 22.2%. Off by 2x. GLM-4.7 belongs in the mid-tier.

---

### [M7] "Synergy, Not Addition" Never Demonstrated *(Logic)*

The paper claims instruction+tags achieve ~93% reduction "through synergy, not mere addition." The additive prediction (instruction alone 72% × tags alone 52% ≈ combined effect) was never computed and compared to the observed combined rate. Without this calculation, "synergy" is asserted, not shown.

---

### [M8] Statistical Tests Inappropriate for Hierarchical Data *(Methodology)*

Chi-square + Cramér's V assumes iid observations. Trials share model, payload, and condition structure — they are not iid. Mixed-effects logistic regression treating model and payload as random effects would be the appropriate test. The current approach likely underestimates confidence intervals.

---

### [M9] Calibration Not Back-Applied to Data CSV *(Data Integrity — NOTE promoted)*

`results_r2_combined_latest.csv` contains pre-calibration (scorer v1) scores. The human-validated truth is in `human_labels_v1.csv` only. Downstream analyses reading the combined CSV see uncalibrated Kimi K2.5 rates (22.2% instead of 5.6%). This is a provenance gap that could corrupt future analyses.

---

## Findings: MINOR

---

- **m1:** R1's 0% injection across all conditions is included in "rounds complete" count but provides no signal. Its inclusion in the 3,580/3,576 total inflates apparent coverage.
- **m2:** "Classical attacks dead against frontier models" (direct override 0%) uses only R2 payload data from 3 pre-frontier models, not the R7/R8 frontier model set.
- **m3:** "No meaningful benefit" from reasoning budgets drawn from 2 models, no statistical test. Gemini 3 Flash worsens at high budget (8.3% → 11.1%) — this contrary finding deserves acknowledgment, not a parenthetical.
- **m4:** Gemini novelty reviewer flagged "HoneyTrap" and other 2025–2026 ablation studies as potential prior art for the stacking methodology. Recommend a targeted literature search for arXiv papers from 2025–2026 on "defense stacking" and "progressive ablation" to verify novelty claim scope.
- **m5:** Phase 2 (N=540 full-stack, live) is a stronger finding than Phase 1. The paper buries Phase 2 results and leads with Phase 1. Consider restructuring to foreground the live Phase 2 evidence.

---

## Reviewer Concordance

| Finding | Logic | Methodology | Citations | Data |
|---------|-------|-------------|-----------|------|
| Simulation disclosure (F4) | FATAL | FATAL | — | — |
| Circular R8 simulation (F5) | mentioned | FATAL | — | confirmed |
| Cross-round incompatibility (F6) | FATAL | FATAL | — | — |
| Missing Perez/Greshake citations (M1) | — | — | MAJOR | — |
| "~50% reduction" variance unexplained (M5) | FATAL | MAJOR | — | MINOR |
| R6 filter table wrong (F1) | — | — | — | FATAL |
| "93% reduction" misattribution (F2) | — | — | — | FATAL |
| "~20% baseline" wrong (F3) | — | — | — | FATAL |
| Tag non-monotonicity on uncalibrated models (M3) | FATAL | — | — | — |
| Statistical test selection (M8) | noted | FATAL | — | — |

**Strong concordance:** The simulation validity concerns (F4, F5, F6) are independently flagged FATAL by both the logic and methodology reviewers. These are the most defensible blockers.

**Single-reviewer critiques:** The data integrity failures (F1–F3) are only verifiable by a reviewer with tool access to the raw CSVs — the other reviewers couldn't check them. They are however the most concrete and easily fixed.

---

## Blind Spot Analysis

All reviewers share a limitation: none can evaluate whether the simulation risk multipliers are *plausible* in a domain-expert sense, only that they are circular. A human prompt-injection researcher reviewing the multiplier design might reach different conclusions about plausibility.

The citation reviewer (Gemini) produced one potentially confabulated citation ("AgentSys 2026," "Hybrid Stacks 2025") — these should not be acted on without independent verification.

---

## Action Items

### Must-fix before any publication

- [ ] **[F1]** Replace R6 policy filter table with values computed from data. Balanced row is correct; permissive, strict, paranoid must be recomputed.
- [ ] **[F2]** Replace "~93% reduction" (instruction+tags) with actual computed values. Clearly separate from 92.6% filter recall.
- [ ] **[F3]** Replace "~20% higher baseline rates" with "1.0pp higher raw rates; 4.5–7.1pp higher at intermediate defenses."
- [ ] **[F4]** Add simulation disclosure to abstract and title. State trial counts as "397 live + 3,180 simulated" everywhere trials are counted.
- [ ] **[M1]** Add Perez & Ribeiro (2022) and Greshake et al. (2023) to Related Work.
- [ ] **[M4]** Fix per-round N values (R1: 72, R7: 1,200, R8: 1,980, Total: 3,576).
- [ ] **[M6]** Fix Kimi K2 Thinking tier (mid, not high) and GLM-4.7 rate (16–22%, not 8%).

### Should-fix (materially weakens claims)

- [ ] **[F5]** Add explicit disclosure that R8 is simulated with monotonic multipliers, and cross-channel comparison mixes live (R7) and simulated (R8) data.
- [ ] **[F6]** Add caveats to cross-round table; clarify which rounds are live vs simulated.
- [ ] **[M3]** Caveat tag non-monotonicity finding as simulation-only for uncalibrated models, requiring live validation.
- [ ] **[M5]** Reframe "~50% reduction" as "50–72% depending on channel."
- [ ] **[M7]** Compute additive prediction for instruction+tags to support or retract "synergy" claim.
- [ ] **[M9]** Document calibration provenance gap; note that combined CSV has pre-calibration scores for R2.

### Nice-to-have

- [ ] **[M8]** Consider mixed-effects logistic regression for the R7 primary analysis, or acknowledge chi-square limitation.
- [ ] **[m3]** Give the Gemini 3 Flash high-budget result (8.3% → 11.1%) a sentence, not a parenthetical.
- [ ] **[m4]** Search arXiv 2025–2026 for "defense stacking" "progressive ablation" prompt injection to verify novelty claim.
- [ ] **[m5]** Consider restructuring to lead with Phase 2 (live, N=540) as primary evidence.

---

## What Holds Up

The following findings are **well-supported** and should be retained:

- R7 injection rates by condition (raw 18.9% → full_stack 0.0%) — verified against live data, numbers exact.
- R7 Phase 2 full-stack (0.185%, 1/540) — verified against data; MiniMax failure correctly described.
- R8 injection rates by condition (raw 19.9% → full_stack 0.0%) — verified against simulated data, numbers exact.
- Cross-channel deltas at intermediate defenses (+4.5–7.1pp) — computed correctly.
- R6 balanced config (92.6% recall, 0.0% FPR, F1=0.96) — verified.
- R2 chi-square statistics (χ²=24.22, p=0.000006, V=0.27) — verified.
- R2b calibration (7 FPs, 2.2% → 0% FPR, Kimi K2.5 22.2% → 5.6%) — verified.
- Reasoning budget null result (GPT-5.2 6.7% vs 5.6%, Gemini 3 Flash 8.3% vs 11.1%) — verified.
- Scorer definition (`score >= 2` as injection threshold) — consistent across rounds.

The engineering contribution is real. Seven of the must-fix items are factual corrections that don't require new experiments. The simulation-disclosure issues require framing changes. The circular simulation issue (F5) is the only item that requires either new live data or a fundamental reframing of R8's contribution.
