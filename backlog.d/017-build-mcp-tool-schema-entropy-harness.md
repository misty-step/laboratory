---
acceptance:
    - The MCP tool-schema entropy harness can generate seeded low, medium, and high entropy tool catalogs.
    - Simulate mode runs without API keys and writes non-publishable smoke artifacts.
    - Live mode requires an explicit flag, budget cap, and provider key preflight.
    - Every live trial writes a trace artifact matching the experiment design contract.
    - Analysis refuses to produce findings from simulated or trace-missing data.
evidence_required:
    - tests
    - simulate run
    - live smoke plan
id: 017-build-mcp-tool-schema-entropy-harness
lifecycle_stage: Intent
status: ready
title: Build MCP tool-schema entropy harness
---

## Goal

Implement the harness needed to run the 6-call live smoke and then the bounded
432-call MVP for `experiments/mcp-tool-schema-entropy`.

## Context

The experiment design is intentionally narrow: mutate MCP-style catalog entropy
while holding tasks and local stateful tools constant. The harness must preserve
the lab rule that simulation validates machinery but cannot support scientific
claims.

## Notes

Build the thin version first: one domain, generated catalogs, deterministic
validators, trace artifacts, and budget enforcement. Add more domains only after
the smoke path is verified.
