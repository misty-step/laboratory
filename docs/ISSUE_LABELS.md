# Issue Labels

Canonical label taxonomy for this repository. Use these; do not use legacy `kind:*`, `area:*`, or `status:*` labels.

## Priority (exactly one required)

| Label | When |
|-------|------|
| `p0` | Critical — blocks valid experiment execution or results trust |
| `p1` | Essential — foundation, fundamentals, current focus |
| `p2` | Important — useful, planned, not urgent |
| `p3` | Nice to have — polish, innovation, low-ROI research |

## Type (exactly one required)

| Label | When |
|-------|------|
| `bug` | Defect in harness, analysis, scoring, or tooling |
| `feature` | New capability or behavior |
| `task` | Implementation work item |
| `refactor` | Code improvement without behavior change |
| `research` | Investigation, spike, or experiment proposal |
| `epic` | Large multi-issue initiative |

## Horizon (exactly one required)

| Label | When |
|-------|------|
| `now` | Current sprint — actively being worked |
| `next` | Next sprint candidate |
| `later` | Backlog, not yet scheduled |
| `blocked` | Waiting on external dependency or decision |

## Effort (one required)

| Label | Estimate |
|-------|----------|
| `effort/s` | < 1 day |
| `effort/m` | 1–3 days |
| `effort/l` | 3–5 days |
| `effort/xl` | > 1 week |

## Domain (one or more required)

| Label | Covers |
|-------|--------|
| `domain/security` | Injection research, adversarial testing, vulnerability measurement |
| `domain/publication` | Papers, blog posts, visualizations, social content, deliverables |
| `domain/experiment-design` | Hypothesis design, novelty checks, methodology, literature review |
| `domain/agent-eval` | Agent behavior benchmarking, LLM tooling evaluation, OpenCode eval |
| `domain/infra` | CI, Makefile, shared tooling, harness infrastructure, reproducibility |
| `domain/data` | CSV schemas, data immutability, artifact management, normalization |

## Source (one required on groom-created issues)

| Label | When |
|-------|------|
| `source/groom` | Created by `/groom` skill |
| `source/user` | Reported by team member |
| `source/agent` | Created by AI agent |

## Legacy Labels (deprecated — do not use)

The following labels are retired. Migrate existing issues to canonical labels above:

- `kind:experiment` → use `research` type + `domain/experiment-design`
- `kind:bug` → use `bug` type
- `kind:infra` → use `task` type + `domain/infra`
- `area:prompt-injection` → use `domain/security`
- `area:tooling` → use `domain/infra`
- `area:data` → use `domain/data`
- `status:backlog` → use `later` horizon
- `status:active` → use `now` horizon
- `status:blocked` → use `blocked` horizon
- `priority:p0/p1/p2` → use `p0`/`p1`/`p2` directly
