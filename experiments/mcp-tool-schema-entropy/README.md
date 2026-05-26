# MCP Tool Schema Entropy

This experiment asks whether the shape of an MCP-style tool catalog changes how
reliably an agent chooses tools, fills arguments, and completes a task.

The design is preregistered in [design.md](design.md). The draft manifest is
[experiment.yaml](experiment.yaml). No live data has been collected yet.

## Status

- Design: draft
- Harness: not implemented
- Data: none
- Publishable evidence: none

## Intended Run Modes

- `--simulate`: deterministic harness smoke only. Simulated rows are not
  scientific evidence.
- `--live`: provider-native tool-calling runs against a local, harmless,
  in-memory MCP-style environment.

