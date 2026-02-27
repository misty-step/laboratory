# Social Thread: Defense Stacking Study

## Post 1 (Hook)

We ran 3,580 prompt injection trials across 12 LLMs to answer one question:

Which defenses actually work, and do they stack?

Short answer: yes. Full-stack defense drops injection success from ~20% to <0.2%.

The longer answer is more interesting. Thread:

## Post 2 (Surprising finding)

Boundary tags ALONE can backfire.

On DeepSeek and Qwen, adding `<<<UNTRUSTED>>>` markers WITHOUT a system instruction actually INCREASED injection rates by 8pp.

Tags signal "look at this" without saying "don't trust it."

Always pair tags with an instruction. Never use them solo.

## Post 3 (Key data)

Defense stacking, quantified:

- No defense: 19-31% injection success
- System instruction only: 5-10% (-50%)
- Instruction + tags: 2-9% (-93%)
- Full stack + tool filter: <0.2% (-99.8%)

A single sentence in your system prompt is the highest-leverage defense available. 20 tokens. Zero latency.

## Post 4 (Practical takeaway)

The attacks that work in 2026 aren't "IGNORE ALL PREVIOUS INSTRUCTIONS."

Those have 0% success even with no defense.

What works: gradual escalation (56-89% raw success), social engineering (33%), indirect extraction (41%).

Subtle attacks that mimic legitimate requests. Defenses need to match.

## Post 5 (CTA)

Full paper, all data, reproduction scripts:
github.com/misty-step/laboratory

All experiments reproducible via --simulate (no API keys needed).

MIT licensed. Use it.
