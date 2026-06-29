# MCP Tool Schema Entropy: Preregistered Design Draft

## Plain Summary

An agent with tools is like a child choosing from a drawer full of labeled
gadgets. If every label is short and distinct, the right gadget is easy to
choose. If the drawer has many gadgets with similar names, long confusing
instructions, and almost-identical buttons, the child may grab the wrong one or
press it incorrectly. This experiment measures how much that happens to AI
agents when their MCP-style tool catalogs get bigger, noisier, and more
ambiguous.

## Research Question

How does MCP-style tool catalog entropy affect model behavior under otherwise
identical tasks?

The experiment isolates catalog design variables: tool count, semantic overlap,
name similarity, description verbosity/noise, and argument-schema complexity. It
does not try to rank whole agents on realistic work. It asks a narrower builder
question: which catalog shapes make tool-using models fail?

## Prior Art And Gap

- The Model Context Protocol defines tool names, descriptions, input schemas,
  optional output schemas, annotations, and tool-use inputs. This makes the tool
  catalog a concrete object we can mutate and measure.
- BFCL evaluates function-calling capability across single-turn, live, and
  agentic API tasks, but it is primarily a benchmark of model/tool-call
  performance rather than a causal ablation of schema entropy.
- tau-bench evaluates dynamic user-agent-tool interactions and final database
  state reliability, but it focuses on realistic conversational domains rather
  than controlled catalog-shape mutations.
- ToolSandbox evaluates stateful, conversational, interactive tool-use
  capabilities. It motivates final-state and trajectory scoring, but it does not
  isolate tool schema entropy as the treatment.
- AgentDojo shows that tool-using agents fail in dynamic adversarial
  environments. This experiment is complementary: it studies non-adversarial
  schema design pressure before adding prompt injection or malicious tools.
- MCP-specific benchmarks such as MCP-Bench and MCPMark stress-test agents over
  MCP tasks. The complementary gap is a cheap, controlled, reproducible
  experiment that mutates one catalog variable at a time.

Novelty statement: this produces new information because it measures the causal
effect of MCP-style tool catalog entropy on wrong-tool calls, bad arguments,
extra calls, latency, and cost. Existing work establishes that tool agents are
brittle; this asks which schema/catalog choices create that brittleness.

## Hypotheses

H1: Success declines as catalog entropy increases, controlling for model, task,
domain, and catalog size.

H2: Semantic ambiguity among plausible tools harms success more than raw catalog
size alone.

H3: Name and description ambiguity mostly increases wrong-tool and extra-tool
errors; argument-schema complexity mostly increases schema-invalid and
semantic-argument errors.

H4: Strict/provider-native schema validation reduces syntactic JSON failures but
does not eliminate semantic wrong-tool or wrong-argument failures.

## Experimental Object

The harness exposes a local, harmless, in-memory MCP-style server. Each trial
contains:

- A synthetic domain: issue tracker, order desk, calendar, package registry, or
  CRM.
- A tool catalog generated from a seed and factor settings.
- A user task with a gold tool-call sequence and expected final state.
- Provider-native tool schema compiled from the same internal catalog.
- A validator that checks tool names, argument JSON, schema validity, semantic
  argument correctness, final state, extra calls, latency, and token usage.

No tool touches real external services. Mutating tools update only the in-memory
trial state.

## Entropy Definition

The primary independent variable is `schema_entropy_level`: `low`, `medium`, or
`high`. Each level is generated from measured components:

```text
E_total =
  0.20 * log2(tool_count)
+ 0.25 * target_distractor_similarity
+ 0.15 * name_collision_score
+ 0.15 * description_noise_score
+ 0.20 * argument_complexity_score
+ 0.05 * decoy_ratio
```

Component definitions:

- `tool_count`: number of tools exposed to the model.
- `target_distractor_similarity`: mean top-k lexical or embedding similarity
  between the gold tool and distractor tools.
- `name_collision_score`: normalized overlap among verb/object tokens in tool
  names.
- `description_noise_score`: fraction of description tokens that are irrelevant,
  redundant, contradictory, or shared with distractors.
- `argument_complexity_score`: normalized score from argument count, nesting
  depth, enum count, optional/required ratio, and cross-field constraints.
- `decoy_ratio`: fraction of catalog tools that are plausible but wrong for the
  task.

For MVP reproducibility, lexical similarity is acceptable. Embedding similarity
can be added in v2 if it is cached and deterministic by model/version.

## MVP Factor Matrix

| Factor | Levels |
|---|---|
| Catalog size | 8, 32 |
| Schema entropy | low, medium, high |
| Task type | single-call, two-call |
| Domain | issue tracker, order desk, calendar, package registry |
| Models | three cheap current tool-calling models, one each from OpenAI, Anthropic, and Google if keys are available |
| Repeats | 3 seeded repeats per cell |

MVP planned live calls:

```text
2 catalog sizes * 3 entropy levels * 2 task types * 4 domains *
3 models * 3 repeats = 432 calls
```

Live smoke before MVP:

```text
2 catalog sizes * 3 entropy levels * 1 domain * 1 task type *
1 model * 1 repeat = 6 calls
```

## Scoring

Each trial receives a deterministic 0-3 score:

- 3: exact gold tool sequence, schema-valid arguments, correct final state, no
  unnecessary risky calls.
- 2: correct final state with harmless extra read-only call or normalizable
  argument issue.
- 1: valid tool use but wrong tool, missing step, wrong order, or material
  semantic argument error.
- 0: invalid JSON, schema-invalid arguments, hallucinated tool, refusal, or
  wrong mutating action.

Primary outcome: `success = score >= 2`.

Secondary outcomes:

- wrong-tool rate
- schema-invalid argument rate
- semantic-argument error rate
- hallucinated-tool rate
- unnecessary-call rate
- final-state correctness
- latency
- input, output, and total tokens
- estimated cost

Error taxonomy:

- `wrong_tool`
- `missing_tool`
- `extra_tool`
- `invalid_json`
- `schema_invalid`
- `semantic_arg_error`
- `wrong_order`
- `refusal`
- `hallucinated_tool`
- `unsafe_mutation`

## Analysis Plan

Primary analysis:

- Report success rates by entropy level with Wilson confidence intervals.
- Report error-taxonomy rates by entropy level and catalog size.
- Estimate entropy effect with stratified bootstrap over task/domain/model cells.
- Plot cost and latency by entropy level.

Secondary analysis:

- Compare raw catalog-size effect against semantic-similarity effect.
- Compare single-call and two-call tasks for compounding failures.
- Compare models only as a robustness slice, not as a leaderboard headline.

Publishable claim threshold:

- The finding must reproduce directionally across at least two providers or be
  explicitly framed as provider-specific.
- The report must include all failed and successful live trials, not only
  examples.
- Simulated rows cannot appear in findings except as harness QA evidence.

## Trace Contract

Every live trial must write a JSON trace before analysis:

- run id, trial id, seed, mode, timestamp
- provider, model, temperature, tool-choice mode
- task text, domain, gold sequence, expected final state
- internal catalog JSON and hash
- provider-compiled schema JSON and hash
- entropy component scores
- raw request payload, with secrets redacted
- raw response payload
- parsed tool calls
- local tool execution results
- validation errors
- final state diff
- usage tokens, latency, and estimated cost
- retry count and error metadata

The CSV result row is an index over trace artifacts, not the full evidence.

## Cost Plan

The harness should calculate cost from provider pricing snapshots captured at
run time. As of May 24, 2026, cheap current tiers make the MVP comfortably
bounded:

- OpenAI `gpt-5.4-nano` is listed at $0.20/M input tokens and $1.25/M output
  tokens on standard processing.
- Anthropic `claude-haiku-4.5` is listed at $1/M input tokens and $5/M output
  tokens.
- Google `gemini-2.5-flash-lite` is listed at $0.10/M input tokens and $0.40/M
  output tokens.

Assume a conservative average trial of 8k input tokens and 1k output tokens,
including tool schemas:

```text
432 calls * 9k billed tokens ~= 3.9M total tokens
```

Approximate MVP spend should be under $10 on the cheapest mix, but the
registered budget cap should be $25 to absorb longer schemas, retries, and
provider overhead. The live smoke cap should be $2. A v2 with 4,608 calls and
larger catalogs should require explicit approval with a $100-$250 cap depending
on model mix.

## Design Variants Considered

1. **Microbench only:** ask models to emit one function call from a static
   catalog. Cheapest and cleanest, but less agent-relevant because there is no
   final-state verification.
2. **Stateful synthetic environment:** local MCP-style tools mutate an
   in-memory state and validators score final state. This is the recommended
   MVP because it is still cheap while measuring meaningful tool-use behavior.
3. **Real MCP marketplace catalogs:** sample real server schemas and write tasks
   against them. More ecological validity, but harder to control and more likely
   to produce messy, non-causal results.
4. **Security/adversarial entropy:** add prompt injection or malicious decoys.
   Interesting, but it should be v2 after the non-adversarial schema effect is
   measured.
5. **Router versus full catalog:** compare full catalog exposure against
   retrieval/routing. Useful follow-up, but it answers a mitigation question
   before measuring the underlying failure curve.

Recommended design: run variant 2 first, with variant 1 as a harness smoke and
variant 5 as the immediate follow-up.

## Scaffold Required Before Running

The repository is ready to design this experiment, but not ready to run and
publish it yet. Required scaffold:

- A first-class `experiment.yaml` validator for factor matrices, budget caps,
  run modes, trace contracts, and deliverable obligations.
- A harness for generating deterministic MCP-style catalogs from seed + entropy
  settings.
- Provider adapters that compile the internal catalog into OpenAI, Anthropic,
  and Google tool-call formats.
- A trace writer that persists raw request/response payloads, catalog artifacts,
  validation records, cost records, and final-state diffs per trial.
- A publish guard that blocks deliverables when result data is simulated or
  missing trace artifacts.
- A small analysis script that reads CSV rows plus trace JSON and emits the
  seven standard deliverables only for live data.

## Ready/Not Ready Decision

Ready:

- The research question is narrow, useful, and complementary to existing
  benchmarks.
- The live MVP is affordable.
- Deterministic scoring is possible.
- The experiment will force exactly the right next scaffold: manifest, trace,
  live guard, and publication discipline.

Not ready:

- No MCP entropy harness exists yet.
- No trace artifact contract is enforced by code.
- `experiment.yaml` is a draft manifest, not validated by the repo gate.
- The publication guard does not yet know how to require trace-backed live data
  for this experiment family.

Decision: build the thin manifest/trace/live-guard slice next, then implement a
6-call live smoke before approving the 432-call MVP.

