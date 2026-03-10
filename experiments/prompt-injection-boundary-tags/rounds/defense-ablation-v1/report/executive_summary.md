# Executive Summary: Defense Ablation v1

## Key Finding

Layering two cheap defenses — boundary tags and a plain-English instruction — nearly eliminates prompt-injection risk, dropping attack success from 17% to under 1%. The defenses multiply rather than add, so you need both.

## What We Tested

We ran 2,100 live API calls across seven production AI models to measure how different combinations of prompt-injection defenses affect attack success. The defenses tested ranged from no protection at all to a full stack of four controls. We also compared frontier models (Claude, GPT-5) against mid-tier and open-weight alternatives.

## Results

**The defense gradient is steep.** Without any protection, 17 in 100 attacks succeed. Adding boundary tags alone drops that to 6 in 100. Adding an instruction alone drops it to 2 in 100. Combining both drops it to 1 in 200. Adding an output filter on top of that adds no measurable benefit.

**The model gap is large and unexpected.** Claude and GPT-5 were essentially immune even with zero defenses in place. MiniMax and DeepSeek, both commercially available models, failed on 33% and 53% of undefended attacks respectively. If your product uses a mid-tier or open-weight model, defenses are not optional.

**Attack style matters more than payload content.** Gradual escalation — where the injected text slowly walks the model toward a harmful output — succeeded on 63% of undefended trials. Direct override commands succeeded on 0%. Attackers who understand this will use escalation. Defenders who don't know this will underestimate their exposure.

## Recommendation

**Ship tags + instruction today.** Both are zero-cost to implement: wrap untrusted content in labeled XML-style boundaries, and add one sentence to your system prompt telling the model to ignore instructions inside those boundaries. Together they reduce attack success by 97%. Do not rely on model choice alone — vendor lineups change, fine-tuned versions behave differently, and mid-tier models are genuinely more vulnerable.

If you are using any open-weight or non-frontier model in an agent workflow with tool access, treat defense as load-bearing infrastructure, not a nice-to-have.

## What's Next

Phase 2 will test adaptive attacks: payloads crafted specifically to defeat boundary tags and instruction-based defenses. We will also measure whether defenses reduce legitimate task utility, since a defense that breaks normal usage is not deployable.
