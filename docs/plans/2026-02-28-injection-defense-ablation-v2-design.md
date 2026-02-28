# Injection Defense Ablation v2 — Design Summary

**Date:** 2026-02-28
**Issue:** TBD (will be created after design approval)
**Directory:** experiments/prompt-injection-boundary-tags/rounds/defense-ablation-v1/

## What we're building

A clean-restart prompt injection defense experiment with:
- 7 current frontier models (4 proprietary, 3 open-weight)
- 5 progressive defense conditions (ablation study)
- 12 static + automated adaptive payloads
- Utility measurement on clean inputs
- Formal power analysis and statistical rigor exceeding field standard
- ~$75 estimated budget, $100 hard cap
- Live API calls only. Zero simulation data.

## Why this matters

No published paper tests incremental defense stacking. Everyone tests defenses
in isolation or as a complete stack. Our ablation progression isolates each
layer's marginal contribution — the most actionable information for practitioners
deciding which defenses to implement.

## Key design decisions

1. **Single scenario** (GitHub issue summarization) — maximizes statistical power per cell
2. **7 models** — Claude Sonnet 4.6, GPT-5.2, Gemini 3 Flash, Grok 4.1 Fast, MiniMax M2.5, Kimi K2.5, DeepSeek V3.2
3. **Two-phase structure** — static payloads first, then adaptive red teaming
4. **Paired utility measurement** — clean inputs through each defense condition
5. **Preregistered analysis** — statistical plan locked before data collection

## Implementation scope

- New harness in `round9/harness/run_experiment.py` (reuses shared infra)
- Adaptive fuzzing module (attacker LLM iterates payloads per defense condition)
- LLM-judge utility scorer
- Analysis script in `round9/analysis/analyze.py`
- Full deliverable pipeline

## Full design

See `experiments/prompt-injection-boundary-tags/rounds/round9/design.md`
