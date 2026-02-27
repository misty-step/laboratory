# Round 8 Social Thread

1) Your prompt-injection defenses work differently when attacks come through RAG retrieval vs. direct input. We ran 1,980 simulated trials across 9 models to measure the gap.

2) Intermediate defenses are 5-7pp weaker in the retrieval channel. Tags-only: 9.1% direct vs 16.2% retrieval. Instruction-only: 5.3% vs 9.8%. Retrieved docs carry implicit trust that partial defenses can't overcome.

3) Full-stack defense (instruction + nonce tags + tool-call filter) eliminates the gap: 0% injection in both channels, across all 9 models. Defense architecture > model selection.

4) Reasoning budgets don't help. GPT-5.2 low=6.7% vs high=5.6%. Gemini 3 Flash actually got *worse* with more reasoning (8.3% -> 11.1%). Thinking harder is not a security strategy.

5) If you're building RAG agents: test defenses on retrieval injection, not just direct input. Ship full-stack or accept that your retrieval channel is your soft underbelly. Data + code: github.com/misty-step/laboratory (simulated data -- validate live before production decisions).
