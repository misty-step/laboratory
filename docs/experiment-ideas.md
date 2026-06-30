# Experiment Ideas Backlog

**Purpose:** maintain more experiment ideas than the lab can run. This is
deliberately a pile: ideas can be practical, strange, exploratory, or obviously
too large today, as long as they can eventually be sharpened into falsifiable,
computational experiments.

## Selection Criteria

- **Novelty:** measures a causal variable or domain not already done to death.
- **Tractability:** can run with bounded API spend and deterministic scoring.
- **Publishability:** produces useful evidence for builders, researchers, or
  practitioners.
- **Scaffold value:** exercises or improves the lab's design -> run -> evidence
  -> publish loop.
- **Safety:** avoids real-world manipulation, real financial action, real user
  targeting, or uncontrolled external side effects.

## Near-Term Candidates

| Idea | Question | Why It Matters | First Useful Run |
|---|---|---|---|
| [MCP tool-schema entropy](../experiments/mcp-tool-schema-entropy/design.md) | Do larger, noisier, more ambiguous tool catalogs make agents choose wrong tools or bad arguments? | Builders are rapidly adopting MCP and function tools; schema design is an actionable scaffold variable. | Synthetic local MCP-style server, 3 entropy levels, 2 catalog sizes, 3 cheap models. |
| Tool retrieval vs execution failure | Do agents fail because they cannot find the right tool, parameterize it, or plan across tools? | Separates discovery failures from tool-call failures; useful after MCP entropy MVP. | Full catalog vs routed subset vs gold shortlist. |
| Stateful tool-use traps | How often do agents fail when state is stale, ambiguous, or prerequisite-dependent? | Real workflows are stateful; final database-state scoring is deterministic. | Toy CRM/order/calendar environment with stale IDs and reversible writes. |
| Authority-gradient prompt injection | Does attacker authority framing change compliance with unsafe instructions? | Extends the injection program into a clean behavioral factor. | Same payloads under coworker, manager, vendor, security-team, and system-mimic framing. |
| Reflection budget frontier | Does reflection improve agent success enough to justify extra tokens and latency? | Converts "let the agent think/retry" into a cost-quality frontier. | Coding or tool-use tasks with no reflection, terse reflection, full postmortem. |
| Multi-agent cascade/conformity | Do planner/reviewer/implementer setups dampen or amplify an early wrong assumption? | Multi-agent workflows are common but can launder mistakes. | Seed one incorrect premise; compare solo, independent review, and visible-prior review. |
| Context packaging and injection susceptibility | Does better context packaging also increase trust in poisoned context? | Bridges Glance ablations and prompt-injection work. | Same coding task with C0-C4 context and benign vs poisoned context packets. |
| Benchmark honeytoken integrity | Do agents exploit exposed gold files, labels, or validator hints? | Measures benchmark hacking and evidence hygiene. | Local sandbox with audited file reads and hidden validator. |
| Budget-aware tool use | Do agents choose rational verification when tools have explicit cost/latency? | Real agents operate under budgets; success alone is incomplete. | Tool suite with cheap noisy tools, expensive reliable tools, and optimal scripted baseline. |
| Content workflow quality decay | How much factual drift appears through transformations like paper -> blog -> thread -> script? | Useful for publication pipelines and content agents. | Frozen source docs, deterministic citation checker, drift taxonomy. |
| [Rampart on-device PII red-team](brainstorms/2026-06-30-tiny-models-and-prime-intellect.md) | How far below its claimed ~98.4% recall can an open-weight, on-device .gov PII filter be driven by *imperceptible* input perturbations? | First independent adversarial stress-test of a shipped on-device government privacy model; deterministic ΔRecall scoring; reproducible open weights; coordinated-disclosure public good. | Reproduce baseline recall on a clean seed corpus, then paired clean-vs-perturbed ΔRecall for two perturbation classes (homoglyph/confusables; Unicode/spelled digits) with Wilson CIs and per-layer attribution. |
| Homoglyph / Unicode NER-evasion robustness | How much do imperceptible Unicode perturbations (homoglyphs, confusables, full-width/zero-width) degrade small NER/PII encoders, and which classes hurt most? | Generalizes the Rampart finding into a clean factor; informs defenses (NFKC normalization, confusable folding) for any on-device classifier. | Frozen small encoder + labeled entity set; sweep perturbation classes at fixed rates; recall delta per class with CIs. |
| [InjectHunter (verifiers RL env)](brainstorms/2026-06-30-tiny-models-and-prime-intellect.md) | Can adversarial self-play discover novel layered-defense-bypassing injection payloads beyond a handcrafted set? | Turns the lab's 0–3 scorer into a reusable Prime Intellect Hub environment; the best attacks can't be hand-written. | Wrap the existing scorer + one frozen target as a `verifiers` `Environment.rollout()` over a 20-task slice; reward = score + novelty bonus − literal-pattern discount, rotating defense condition. |

## Left-Field Candidates

| Idea | Question | Safe Framing |
|---|---|---|
| Synthetic double-auction market agents | Do LLM agents herd, overreact, or respect risk limits in a toy market? | Synthetic order book only; no real trading advice or execution. |
| Game cooperation without persuasion optimization | What memory/reputation scaffolds improve cooperation in repeated games? | Simulated agents only; no human persuasion. |
| Persona/religious frame effects on epistemic humility | Do worldview/persona frames change uncertainty, citation behavior, or omissions? | No conversion, persuasion, or targeting; measure fidelity and humility only. |
| Agent compute economy | How do agents allocate scarce context, tool budget, and queue priority? | Artificial economy; no real money. |
| Local civic workflow simulation | Can agents summarize and route zoning/public-comment workflows without losing minority concerns? | Synthetic civic records; no real political targeting. |
| Formation/memory tutor eval | Which tutoring scaffolds improve recall without hallucinated doctrine or facts? | Fixed corpus, objective quiz scoring, no pastoral advice claims. |
| [Active experiment design (Falsifier)](brainstorms/2026-06-30-tiny-models-and-prime-intellect.md) | Can an agent recover a hidden causal DAG faster by choosing `do(X)` interventions than by observation alone? | Synthetic causal world only; reward is structural recovery under a sampling budget; no real-world action. |

## Current Recommendation

Start with **MCP tool-schema entropy**. It is cheap, deterministic to score, close
to Misty Step's agent-grade-primitives thesis, and forces the lab to implement
the right next scaffold: manifest, live guard, trace artifacts, and publish
checks. The current preregistration draft lives at
`experiments/mcp-tool-schema-entropy/design.md`.
