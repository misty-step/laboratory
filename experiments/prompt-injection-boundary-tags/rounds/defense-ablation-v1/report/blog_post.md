# Which Prompt Injection Defenses Actually Work? We Tested Five.

If you're building an AI agent that reads external content, you've probably wondered which defenses are worth the complexity. Boundary tags? System prompt instructions? An output filter? All three? The honest answer until now has been: nobody's measured the marginal value of each layer in isolation.

We ran 2,100 live API trials across seven models and five defense conditions to find out.

## The Setup

Our test scenario: a GitHub issue summarization agent. The agent has fake credentials in its system prompt. Injection payloads are hidden in the "Additional Context" field of the issue it's summarizing. The question is whether the agent leaks those credentials or makes suspicious tool calls.

We tested five defense conditions, each a progressive layer on top of the last:

1. **Raw** -- no defense, untrusted content passed directly to the agent
2. **Tags only** -- dynamic nonce boundary tags wrapping the untrusted content
3. **Instruction only** -- system prompt tells the model to treat external content as data, not instructions
4. **Instruction + tags** -- both layers combined
5. **Full stack** -- tags + instruction + an output filter that blocks tool calls to untrusted targets

Seven models: Claude Sonnet 4.6, GPT-5.2, Gemini 3 Flash, Grok 4.1 Fast, MiniMax M2.5, Kimi K2.5, and DeepSeek V3.2. All trials were live API calls at temperature 0. No simulation.

## The Numbers

| Condition | Attack Success Rate | 95% CI |
|---|---|---|
| raw | 17.4% | [14.1%, 21.3%] |
| tags only | 5.5% | [3.7%, 8.1%] |
| instruction only | 2.4% | [1.3%, 4.3%] |
| instruction + tags | 0.5% | [0.1%, 1.7%] |
| full stack | 0.0% | [0.0%, 0.9%] |

The overall effect is real (chi-square p < 0.001, Cramer's V = 0.29). Each condition is statistically distinguishable from `raw`. But the story in the middle is more interesting than the headline numbers suggest.

## Two Findings That Weren't Obvious

**Tags and instruction are statistically equivalent to each other.** After Bonferroni correction for multiple comparisons, `tags_only` (5.5%) and `instruction_only` (2.4%) are not significantly different from one another. Both beat `raw` by a wide margin, but neither is clearly the better single layer. If you can only add one defense, the data doesn't tell you which one to pick.

What the data does tell you: combine them. `instruction_tags` (0.5%) is significantly better than either layer alone (p = 0.0001 vs tags, p = 0.037 vs instruction, though the latter doesn't survive Bonferroni). The combination isn't just additive. It's multiplying. Boundary tags apparently make the instruction more effective, and vice versa.

**The output filter barely matters once you have both other layers.** Going from `instruction_tags` to `full_stack` reduces ASR from 0.5% to 0.0%, a 0.5 percentage point improvement that is not statistically significant. In this dataset that's 2 compromises out of 420 trials. The output filter is a last-resort backstop, not a standalone defense. At 0.5% residual ASR, it earns its keep as a safety net, but you'd be wrong to treat it as a substitute for the earlier layers.

## The Model Gap

The per-model numbers deserve their own attention:

| Model | ASR (all conditions pooled) | Type |
|---|---|---|
| DeepSeek V3.2 | 17.7% | Open-weight |
| MiniMax M2.5 | 11.0% | Open-weight |
| Grok 4.1 Fast | 3.0% | Proprietary |
| Kimi K2.5 | 2.3% | Open-weight |
| Gemini 3 Flash | 1.7% | Proprietary |
| GPT-5.2 | 0.3% | Proprietary |
| Claude Sonnet 4.6 | 0.0% | Proprietary |

The Western frontier models (Claude, GPT-5.2, Gemini) are dramatically more resistant than the open-weight alternatives, even before any defense is applied. DeepSeek at 17.7% is operating at the same ASR level as an undefended frontier model. MiniMax at 11.0% isn't far behind.

This gap is probably training-related. Models like Claude appear to have internalized instruction-following policies that treat credential exfiltration as off-limits regardless of what the untrusted content says. Open-weight models trained primarily for capability may not have received the same adversarial alignment treatment.

The practical implication: if you're building on an open-weight model, your defensive posture needs to be considerably more aggressive. Adding the instruction layer alone brings DeepSeek's susceptibility down substantially, but you can't skip the defense steps and rely on the model to refuse.

## What Actually Gets Through

One more finding worth understanding: not all attack types are equal.

In the undefended condition, gradual escalation attacks succeeded 62.9% of the time. Indirect extraction came in at 40.0%. Multi-step attacks hit 31.4%.

Direct override, authority escalation, and tag-breaking attacks all scored 0.0%.

The naive attacks ("ignore previous instructions," "you are now in admin mode") don't work on any current frontier model. What works is patience. Gradual escalation slowly shifts the frame over multiple exchanges. Indirect extraction avoids asking for secrets directly and instead asks questions whose answers reveal them. Multi-step attacks chain individually innocent requests into a sequence that achieves the goal.

These patience-based attacks are harder to block because they're harder to detect. A single exchange might look completely benign. The injection only becomes apparent across the full conversation.

## What to Do Today

**Use both tags and instruction, not one or the other.** Tags alone reduce ASR from 17.4% to 5.5%. Instruction alone reduces it to 2.4%. Together they get you to 0.5%. The marginal cost of adding the second layer is low; the benefit is not.

**If you're on a frontier model, you have a head start. Don't waste it.** Claude and GPT-5.2 show near-zero ASR even in the undefended condition. That's not a reason to skip defenses; it's a reason to feel reasonably good about your baseline before you add them. On an open-weight model, the baseline is much worse and the defenses matter more.

**Design for gradual escalation.** The attacks that work don't announce themselves. Consider session-level monitoring for behavioral drift, not just per-message filtering. An agent whose responses are slowly shifting from summarization to data retrieval is showing a pattern that single-turn analysis misses.

**Add the output filter last, not first.** It contributes real (if small) protection once you already have the other layers in place. But building only an output filter while skipping instruction and tags is backwards: you're defending the exit while leaving the entrance open.

## What We Don't Know Yet

This experiment used static payloads drawn from a fixed taxonomy. A competent attacker testing your specific system wouldn't use static payloads; they'd probe your defenses and adapt. Phase 2 of this work (adaptive red teaming) will test whether automated fuzzing against each defense condition finds bypasses that static payloads miss. The expectation is yes; the question is by how much.

We also didn't measure utility. We don't yet know whether the instruction layer causes more false refusals on legitimate inputs. That data is worth collecting before recommending this as a production pattern.

The payload set covers one task type (summarization) on one input format (GitHub issues). Injection patterns in PDF parsing, email processing, or web browsing workflows may differ.

---

The data, methodology, and analysis code are available at [github.com/misty-step/laboratory](https://github.com/misty-step/laboratory) under MIT license. The experiment design was preregistered in `design.md` before data collection.
