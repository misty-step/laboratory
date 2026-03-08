# Social Thread: Defense Ablation v1

Post 1:
We told an AI "ignore all previous instructions" 2,100 times, across 7 models, with 5 different defenses active. The most dangerous attack pattern wasn't the direct override. It was gradual escalation — and it worked 63% of the time on undefended systems (among gradual escalation payloads; overall raw ASR was 17.4%). 🧵

Post 2:
The defense gradient, measured live across frontier and mid-tier models:

raw (no defense): 17.4% attack success
tags only: 5.5%
instruction only: 2.4%
tags + instruction: 0.5%
full stack: 0.0%

Two cheap controls, layered, cut risk by 97%.

Post 3:
The surprising part: tags alone and an instruction alone perform about the same. Neither is clearly better. But together they're multiplicatively stronger — not just additive. The output filter added nothing significant on top of that combination.

Post 4:
Practical takeaway: wrap untrusted content in labeled boundaries, add one sentence to your system prompt. That's it. But model choice matters too — Claude and GPT-5 were near-immune undefended; DeepSeek failed 53% of undefended trials. Know what you're running. #aisecurity

Post 5:
Full data, methodology, and findings: https://github.com/misty-step/laboratory/tree/master/experiments/prompt-injection-boundary-tags/rounds/defense-ablation-v1
