# Spellbook Laboratory Loop Plan

## Decision

Gradient is retired for this repository. Spellbook is the active agent harness
substrate. Laboratory keeps experiment semantics local: manifests, harnesses,
trace artifacts, live-data guards, and publication deliverables exist to support
computational science, not a generic governance platform.

## Operating Loop

1. Maintain a large backlog of experiment ideas and inspiration studies.
2. Select one cheap, useful, publishable experiment.
3. Write a preregistered `design.md` and a thin `experiment.yaml`.
4. Build only the scaffold needed to run that experiment well.
5. Run deterministic simulate mode for harness QA.
6. Run bounded live smoke before approving full live spend.
7. Analyze only trace-backed live data for publishable findings.
8. Publish all required deliverables.
9. Feed scaffold pain back into either this repo or Spellbook, depending on
   whether it is lab-specific or reusable agent-harness infrastructure.

## What Belongs In Laboratory

- Experiment manifests and validators.
- Domain harnesses, analyzers, and report generators.
- Live-data publication guards.
- Trace contracts for computational experiments.
- Experiment idea and prior-art surfaces.

## What Belongs In Spellbook

- Reusable skills, agents, and workflow guidance.
- Cross-harness bridge conventions.
- Generic backlog, review, CI, QA, and delivery primitives.
- Shared shell helpers used by workflow skills.

## Current Next Experiment

MCP tool-schema entropy remains the recommended next experiment. Its design
lives at `experiments/mcp-tool-schema-entropy/design.md`; the next build step is
`backlog.d/017-build-mcp-tool-schema-entropy-harness.md`.
