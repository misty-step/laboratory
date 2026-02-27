# Round 8 Executive Summary

**Date:** 2026-02-13

## Key Finding

Prompt-injection defenses that work against direct user input are weaker when attacks arrive through retrieved documents. In simulated trials (N=1,980), intermediate defenses showed 4.5--7.1 percentage points higher injection rates in the retrieval channel vs. direct input. Full-stack defense (system instruction + nonce tags + tool-call filter) eliminated the gap, achieving 0% injection across all 9 models and 396 retrieval-channel trials.

| Defense | Direct | Retrieval | Gap |
|---|---:|---:|---:|
| Tags only | 9.1% | 16.2% | +7.1pp |
| Instruction only | 5.3% | 9.8% | +4.5pp |
| Full stack | 0.0% | 0.0% | 0.0pp |

## Implication

RAG agents are more vulnerable than direct-input chatbots at intermediate defense levels. Retrieved documents carry implicit trust ("the system fetched this") that weakens partial defenses. Organizations testing defenses only against direct input are underestimating their RAG exposure. Reasoning budget adjustments (low vs. high) provide no substitute -- Gemini 3 Flash actually performed worse with higher reasoning budget.

## Recommendation

Deploy full-stack defense for any RAG agent handling untrusted retrieval sources. "Tags only" or "instruction only" configurations that pass direct-input testing will underperform by 5-7pp on retrieval-channel attacks. If output text can reach untrusted channels, add secret redaction as an additional layer beyond tool-call filtering.

**Caveat:** These findings are from deterministic simulation, not live API calls. Validate with live model testing before making production security decisions.
