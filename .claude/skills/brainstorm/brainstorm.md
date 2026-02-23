# /brainstorm

Generate novel experiment hypotheses for the Misty Step Laboratory.

Explores existing results, searches current literature, identifies gaps, and produces
3-5 scored hypothesis proposals. Optionally scaffolds a `design.md` for the selected one.

## When to use

- You want to know what to run next
- You have a vague direction and need it sharpened into a falsifiable hypothesis
- You want to check whether an idea is novel before investing in it
- You've just completed an experiment and want to identify natural follow-ups

## Process

### Phase 1: Load existing knowledge

Read the following (all exist in this repo):

1. `project.md` — vision, active focus, experiment families
2. All `design.md` files: `find experiments -name design.md`
3. Available `report/findings.md` files for completed experiments
4. `canonical/runs_v1.csv` if cross-round context is relevant

Build a summary of:
- What has been confirmed / refuted / inconclusive
- Which hypotheses remain open or partially answered
- What interaction effects haven't been tested
- What conditions or models are missing from existing designs

### Phase 2: Literature search

Search for current prior art. Do NOT rely on training data — web search explicitly.

Queries to run:
- `prompt injection LLM agent defense 2024 2025 site:arxiv.org`
- `LLM coding agent benchmark tool use 2024 2025`
- `context window agent performance ablation 2024 2025`
- Specific venues: NeurIPS 2024, ACL 2024, EMNLP 2025, USENIX Security 2025

Compare each idea against:
- **AgentDojo** (Debenedetti et al., NeurIPS 2024)
- **InjecAgent** (Zhan et al., ACL 2024)
- **SafeToolBench** (EMNLP 2025)
- **CalypsoAI CASI** vulnerability leaderboard
- **Gray Swan SHADE** adversarial platform

For each candidate idea: "Does this already exist? What's the gap?"

### Phase 3: Identify gaps

Categories to scan:

**Unexplored variables** — What hasn't been manipulated in existing rounds?
- Defense conditions not yet tested
- Payload categories not yet covered
- Models not yet benchmarked
- Task tiers or repo archetypes not yet included

**Follow-ups from confirmed findings** — What do our results predict should happen?
- If full_stack reduces injection, what's the ceiling? Does it hold against adaptive attackers?
- If C2 (explicit discovery) outperforms C1 (silent), what instruction phrasing matters?

**Cross-domain** — Where do findings from one family apply to another?
- Do injection defense lessons apply to coding agent eval?
- Does context packaging affect injection susceptibility?

**Replications** — Which published findings should we verify independently?
- Are AgentDojo's results stable across frontier models in 2025/2026?

### Phase 4: Generate proposals

Produce 3-5 candidate hypotheses. For each:

```markdown
## [N]. [Hypothesis Name]

**Statement**: [Falsifiable: "Condition X produces outcome Y compared to Z in context W."]

**Novelty**: This produces new information because [specific gap]. Existing work covers [Y]
but not [Z].

**Connection to our findings**: [Which of our results motivates or enables this?]

**Factor matrix**:
- Independent variable: [what varies]
- Dependent variable: [what we measure]
- Controls: [what stays fixed]

**Expected information gain**: High / Medium / Low
[Why: what decision does this inform?]

**Effort**: S / M / L / XL
[Why: simulation feasibility, data complexity, API cost]

**Risk**: [What could make this inconclusive? What would invalidate the result?]

**Prior art checked**: [Specific papers/benchmarks that don't cover this exact ground]

**Score**: [Novelty 1-5] × [Info Gain 1-5] × [Effort Efficiency 1-5] = [total/75]
```

### Phase 5: Recommend

After all proposals, explicitly state:

```markdown
## Recommendation

**Best next experiment: [Name]** (Score: X/75)

Reason: [Why this produces the most value per unit effort, given current project focus]
```

### Phase 6: Scaffold design.md (if user selects a hypothesis)

Once the user picks a hypothesis, generate a pre-filled `design.md`:

```markdown
# Experiment Design: [Name]

## Problem
[Why this matters]

## Novelty Statement
This experiment produces new information because [X]. Existing work covers [Y] but not [Z].

## Prior Art
- [Paper 1] (venue, year) — covers [X], does not cover [Z]
- [Paper 2] ...

## Hypotheses
- H1: [Falsifiable statement]
- H2: [...]

## Factor Matrix

### [Independent variable]
- [Level 1]: [description]
- [Level 2]: [description]

### Controls
- [Control 1]: [value held fixed]

## Methodology
[How trials will be run, sample sizes, randomization]

## Success Criteria
[What a confirmed / refuted / inconclusive result looks like]

## Deliverables
All 7 artifacts in report/: findings, paper, blog_post, executive_summary, social_thread, data_card, charts/
```

Write this to `experiments/{family}/rounds/roundN/design.md` (propose the path).

## Output

```markdown
# Brainstorm Session — [date]

## Existing Knowledge Summary
[3-5 sentences: what we know, what's open]

## Literature Gaps Found
[Bullet list from Phase 2 search]

## Proposals

[3-5 full proposal blocks]

## Recommendation
[Single best next experiment with rationale]
```

Then ask: "Would you like me to scaffold a design.md for any of these?"
