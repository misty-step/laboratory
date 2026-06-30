# Brainstorm — Tiny Local Models & the Prime Intellect Agentic Plane

**Date:** 2026-06-30
**Type:** Research-direction brainstorm (exploratory ideation, **not** measurement)
**Methods:** `creative-ideation` (Jobs-to-be-Done, Analogy & Blending, Defamiliarization, First Principles), `research` (multi-source grounded fan-out)
**Companion artifact:** [`2026-06-30-tiny-models-and-prime-intellect.html`](./2026-06-30-tiny-models-and-prime-intellect.html) — interactive, progressive-disclosure version of this record (also served at `https://serenity.tail5f5eb4.ts.net:8810/` during the session)
**Status:** Captured for the idea pile. One candidate (Rampart red-team) is a strong near-term lab fit; see [`../experiment-ideas.md`](../experiment-ideas.md).

---

## Why this session happened

Two theses collided and turned out to be one:

1. **Tiny single-purpose local models.** The US National Design Studio shipped **Rampart** — a ~14.7 MB ML model that redacts PII *in the browser* before anything reaches a server. Not a chatbot; one narrow job, done client-side. Adjacent viral sentiment: tiny models doing one thing well, trained on a single GPU, are a new monetizable software category.
2. **Prime Intellect's "every company becomes an AI research lab."** Environments Hub + the `verifiers` spec (dataset + harness + reward) + prime-rl + distributed training. RL "trades compute for expertise"; the bet is that specialized post-trained small models proliferate.

The session brief: react to both, then ideate creatively — first anchored to the lab's injection work, then deliberately **unshackled** from it across unrelated domains, then re-focused onto the three directions the user wanted to lean into.

## The strategic spine (the one finding worth keeping)

The two planes are not separate bets. The lab's existing **0–3 injection scorer** (`experiments/.../shared/scoring/scorer.py`) is already `verifiers`-shaped, so it is the shared reward across a single coherent program:

> **Rampart red-team → "Misty Step Verified" cert → InjectHunter (RL env on the PI Hub)**

One body of work yields a paper (Rampart), a product/benchmark (Verified), and a flagship open-source environment that plants the lab's flag in Prime Intellect's ecosystem (InjectHunter) — all on infrastructure the lab already owns.

---

## Grounded research findings

### Rampart (National Design Studio)
- Architecture inferred: **regex** (SSNs/structured IDs) + a **MiniLM-class encoder** (names/addresses). Open-weight, on-device (WebGPU/WASM), claims ~98.4% recall.
- Verdict: **almost certainly breakable to well below 98.4%, cheaply, imperceptibly, reproducibly.** Novel not because the attack primitives are new, but because the *target* is — it would be the first independent adversarial stress-test of a publicly-shipped, open-weight, on-device **.gov** PII filter against its own published number.

### Prime Intellect
- Environments Hub + `verifiers` (an `Environment.rollout()` returning a reward), prime-rl, distributed training, INTELLECT-N lineage. Strategy thesis: lower the cost of producing *many* specialized small models; the Hub is the distribution substrate.
- Intersection with the tiny-model thesis: **enabler/beneficiary**, not orthogonal. The lab can publish an environment that is simultaneously research and a public good.

---

## The three deep-dives (honest tractability verdicts)

These were the directions the user asked to lean into. Each is reported with the honest "why it's *not* already solved," not a pitch.

### ❄️ Beat-the-freeze (Parkinson's freezing-of-gait)
- **Already solved:** detecting a freeze *in progress* from one IMU (sub-1MB CNNs, ~F1 0.90 subject-independent). Latency is a red herring — freezes last seconds.
- **Unsolved frontier:** *pre-onset prediction in free-living conditions at a tolerable false-positive rate.* Lab numbers (~84% sens / 86% spec) collapse in the wild. Akinetic freezes have no prodrome; akinetic stillness ≈ sitting/standing → FP floods; huge inter/intra-patient variability × ON/OFF med state.
- **Why no breakout** despite Path Finder / DeFOG / CUE1 / Cue2Walk: open-loop continuous cueing often matches closed-loop (gutting the value prop); RCTs underwhelm (DeFOG: no significant between-group difference); habituation; SaMD load; no reimbursement; compliance.
- **Where a team wins:** per-patient on-device personalization (the variability that sinks population models becomes the moat); own the false-positive frontier honestly (publish free-living FP/hour); the scarce asset is a curated longitudinal *free-living* dataset, not the model.

### 😴 Sleep apnea — the partner problem deleted by physics
- The "distinguish target from sleeping partner" problem is an *airborne-acoustics* problem. Any **body-coupled** sensor (PPG, in-ear/chest accelerometer, ballistocardiogram) physically cannot see a partner — so you don't separate, you choose a contact modality and the partner vanishes from the signal. The comfortable wearable is *what makes it tractable*, not a nice-to-have.
- **Works today:** Belun Ring (finger PPG) REI-vs-PSG r≈0.91; Withings BCG AUC≈0.93; PranaQ in-ear PPG+accel FDA-cleared 2025. Cautionary tale: Apple Watch wrist accel ~66% sensitivity.
- **Real moats (not separation):** hypopnea sensitivity from one comfortable site; nightly compliance; the notification-vs-diagnosis wall (single-night AHI misclassifies 20–50%; error stabilizes only after ~14 nights, Lechat 2022 — the exact multi-night lane Apple/Samsung are legally walled off from).

### 🛡️ Red-teaming Rampart — the strongest near-term *research* bet
- **Per layer:** the regex falls to Unicode/full-width digits (`１２３`, `١٢٣`), spelled-out numbers, locale ID formats; the MiniLM encoder inherits small-NER pathologies — name-recall disparity on non-Western names (Mishra 2020), boundary fragility (RockNER), tokenizer destruction from imperceptible chars (Boucher et al., *Bad Characters*, IEEE S&P 2022).
- **Expected kill shot:** homoglyph + Unicode-digit substitution drives name/ID recall from ~98% to single digits **with zero visible change to the rendered text and no latency cost.**
- **Paper *and* product:** package as **"Misty Step Verified"** — a *moving* adversarial perturbation suite (rotated quarterly so vendors can't overfit), a public post-evasion-recall leaderboard, a cert. External tamper-evident measurement = the lab's doctrine as a product.
- **First experiment (this week):** (1) pull weights + WebGPU runtime, reproduce 98.4% on a clean seed corpus; (2) two perturbation classes only — homoglyph/confusables (encoder) + Unicode/spelled digits & near-miss (regex); (3) paired clean-vs-perturbed ΔRecall per class with Wilson CIs + per-layer attribution; (4) if the kill shot lands, freeze the harness as v0 "Verified" and draft **coordinated disclosure** to NDS with a fix menu (NFKC + confusable folding + digit canonicalization before regex; encoder adversarial augmentation). Frame: *hardening a privacy-protective public good.*

---

## Faves (pitched harder)

- **📉 Relationship Seismograph** — zero ML needed for the first jaw-drop: export an iMessage thread, compute inter-message latency/length/who-initiated, run change-point detection (PELT/BOCPD), point at the week a relationship started dying months before either person knew. The most private possible data, processed where it can never leak. Highest surprise-per-line-of-code object in the set. Risk is taste, not tech — ship as a local "look once and delete" artifact.
- **🦠 Acoustic Antibody** — Apple's Sound Recognition ships ~15 fixed categories; a deaf person's life isn't 15 categories. Few-shot keyword-spotting (MatchboxNet/BC-ResNet, sub-MB, on a watch) lets a user enroll *their* alarm / kid's cry / buzzer from 5 examples, patrol offline. The immune-system framing is the literal architecture. Real moat: personalization the cloud can't economically do. Risk: false-tap trust erosion → the enroll UX + per-user threshold are the whole game.
- **📟 Phrasebook-Index Codec** — the only idea in the corpus that isn't a smaller version of something that already exists. Meaning travels as a 2-byte index into a shared codebook, expanded in the receiver's own language on the far end — translation with *no text on the wire*, fitting a 20-byte LoRa packet. Off-grid crisis comms; the codebook already exists (Translators Without Borders). Ceiling: out-of-vocab maps to the nearest wrong phrase — a constrained-domain primitive, not general MT.

---

## Teeny-model plane — fresh territories

Each binds to a *triple lock* (privacy + latency + no-signal) that forces the model on-device:

- **🔢 7-segment display reader for the blind** *(grounded)* — speaks your microwave/glucose-meter/thermostat aloud, in-browser, offline. ANPR OCR × household 7-seg. Lock: meds-privacy + at-the-beeping-appliance latency + basement-no-signal.
- **🐝 Varroa mite counter** — pathology cell-counting × beekeeping, phone + $15 macro lens, hive-side in a dead-zone field.
- **🌡️ Per-orchard-row frost nowcaster** — $3 ESP32 trained on one season of *that hollow's* microclimate; fires the frost-fan where the NWS grid never sees.
- **🥚 Egg candling viability at day 7** — obstetric-triage × backyard candling; keep/pull/recheck in the dark.
- **🔥 Blacksmith temper-color → temperature** — astronomy blackbody color-temp × oxide hue; pull the blade at the right window.
- **🚲 Pothole memory from your bike's shake** — seismology STA/LTA event detection × road surface; a private map that buzzes the bars before a known crater.

> Note: these are **product/device** ideas, not computational AI-behavior experiments — they belong in this session record, not the lab's experiment pile.

---

## Prime Intellect agentic plane

### RL environments worth building (for the Hub)
- **🎯 InjectHunter** *(grounded — the bridge)* — adversarial self-play that *discovers* novel prompt-injection payloads bypassing layered defenses. Reward = the lab's `score_response()` 0–3 scorer + novelty bonus + literal-pattern discount + rotating defense condition. **First step:** wrap the scorer + one frozen target as a `verifiers` `Environment.rollout()` over a 20-task slice. Same program as the Rampart red-team.
- **🔬 Falsifier** — *active experiment design over a hidden causal world*: the agent chooses `do(X)` interventions under a budget to recover a causal DAG. Observational-only policies provably plateau, so the reward *forces* real experimentation — the literal data engine for "every company becomes a research lab."
- **🗄️ MigrationSurgeon** — zero-downtime DB schema evolution; reward = target schema (hard gate) × workload-green across *every* intermediate state.
- **📟 Pager** — incident diagnosis in a fault-injected microservice sim; a *recurrence probe* distinguishes a true root-cause fix from a mask.
- **🤝 SurplusEngine** — multi-issue negotiation self-play rewarding Pareto-efficiency (gap-to-LP-optimal), not extraction.
- **📚 Legible** — teach a frozen weaker student; reward = comprehension delta − answer-leakage.

### Products / "every company a lab" wedges
Each passes the honest test (proprietary signal + hard verifiable reward + frontier plateau):
- **🏥 Healthcare revenue-cycle coder** — payer adjudication rules are tacit/undocumented; RL extracts the hidden rule from accept/reject remittance outcomes; HIPAA forces local hosting; every claim is a free labeled reward.
- **🌐 Network change-safety agent** *(grounded)* — drafts a config change; **Batfish** (real, open-source formal analyzer) scores reachability/loops/blast-radius. Reward harness exists off the shelf today.
- **🧰 Verifier-from-Exhaust** *(picks-and-shovels)* — instrument a stack, mine implicit accept/reject events (CI logs, PR approvals, ticket closes, 👍/👎), emit a Hub-ready verifier. Siblings: a reward-hacking red team ("CVE database for reward functions") and Model CI (continuous post-training gated like code).

---

## What the lab should actually pursue

Most of the above are products/devices outside this lab's charter (computational, falsifiable experiments on **AI system behavior**). The genuinely lab-fitting, near-term candidates were promoted into [`../experiment-ideas.md`](../experiment-ideas.md):

1. **Rampart on-device PII red-team** — the standout. Extends the lab's injection/defense program from "attack a prompt" to "attack an on-device classifier," with deterministic ΔRecall scoring, bounded cost, reproducible open weights, and a coordinated-disclosure safety frame.
2. **Homoglyph / Unicode NER-evasion robustness** — the generalizable mechanism behind (1): how imperceptible perturbations degrade small encoders, as a clean factor.
3. **InjectHunter** — the lab's scorer as a `verifiers` RL environment; a Hub artifact.
4. **Falsifier** — active-experiment-design RL env; on-thesis for "every company a research lab."

## Provenance & integrity notes

- This is **exploratory ideation**, not measurement. No numbers here are lab results. The cited external figures (Belun r≈0.91, DeFOG RCT, Lechat 2022, Boucher S&P 2022, etc.) are from published work and should be re-verified before any deliverable cites them.
- Product/device ideas (FOG, apnea, the faves, the teeny territories) are recorded for completeness but are **out of scope** for the computational lab; they are not experiment candidates.
- Safe framing for the lab candidates: Rampart work is *hardening a public good* via coordinated disclosure; InjectHunter is synthetic self-play over the lab's own scorer. No real-world targeting, no real financial/user action.
