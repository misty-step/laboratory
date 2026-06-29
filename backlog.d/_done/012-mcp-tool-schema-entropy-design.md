---
acceptance:
    - A preregistered design exists for an MCP tool-schema entropy experiment.
    - The design includes novelty, prior art, factor matrix, power/sample rationale, budget estimate, and live-smoke plan.
    - The design explicitly states which scaffold changes are required before running.
evidence_required:
    - design.md
    - literature review
    - budget estimate
id: 012-mcp-tool-schema-entropy-design
lifecycle_stage: Feedback
status: done
title: Preregister MCP tool-schema entropy experiment
---

## Goal

Design the next low-cost, publishable laboratory experiment: how MCP-style tool
catalog shape affects agent behavior.

## Hypothesis Candidate

As tool catalogs become larger, more verbose, and semantically overlapping,
agents will show lower task success, higher wrong-tool-call rates, higher token
cost, and slower completion compared with compact, disjoint tool catalogs.

## Why This Experiment

It keeps the lab focused on agentic workflows while avoiding another generic
benchmark ranking. The expected output is actionable for builders: how to shape
tool schemas and tool catalogs so agents make fewer mistakes.

## Notes

Use current prior art around WebArena, WorkArena, tau-bench, MCP-Bench, MCPMark,
and tool-use evaluation, but focus the novelty statement on causal ablation of
tool catalog design rather than aggregate agent performance.
