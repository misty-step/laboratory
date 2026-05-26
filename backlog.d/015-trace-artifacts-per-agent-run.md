---
acceptance:
    - Live experiment harnesses can write trace-level JSONL artifacts for model calls, tool calls, verifier decisions, and policy checks.
    - Run data includes stable pointers to trace artifacts.
    - Analysis and publication artifacts can reference the trace artifacts for at least one completed live experiment.
evidence_required:
    - trace artifact sample
    - validation output
    - publication artifact reference
id: 015-trace-artifacts-per-agent-run
lifecycle_stage: Evidence
status: ready
title: Capture trace artifacts for live agent runs
---

## Goal

Move beyond CSV-only evidence by recording trace-level artifacts for live agent
experiments.

## Scope

Start with local JSONL traces beside experiment data. Do not build a hosted trace
backend yet. If the contract proves useful, upstream only the reusable harness
primitive to Spellbook.

## Minimum Trace Events

- model request metadata
- model response metadata
- tool call request
- tool call result
- verifier/scorer decision
- policy gate decision
- budget/cost update
