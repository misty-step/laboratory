# Archived Artifacts

These artifacts were retired on 2026-02-27 because they mixed simulated and live data
without disclosure.

## What's here

- `report/` — Cross-round synthesis deliverables (paper, findings, blog post, executive
  summary, social thread, data card, charts, peer review). This synthesis combined R7 live
  data with R8 simulated data and presented the result as empirical evidence.

- `rounds/round8/report/` — All 6 R8 deliverables. R8 used seeded RNG with hard-coded
  defense multipliers throughout. No live API calls were made. The findings merely reflected
  the multiplier ordering, not model behavior.

## What's valid

- `../rounds/round7/` — R7 (N=1,200, 9 models, live API calls, defense ablation) is solid
  science. Per-round R7 findings remain in place.
- `../rounds/round7/data/` — The underlying R7 CSVs are real data.

## What went wrong

R8's harness defaulted to `--simulate` and no live data was collected. The publication
pipeline wrote deliverables anyway. The cross-round synthesis then combined R7 live data
with R8 simulated data in result tables without disclosing the data collection discrepancy.

The peer review caught this. The experiment program is being restarted with simulation
integrity rules in place.

## See also

- `CLAUDE.md` "Simulation integrity" section — the codified rule that prevents recurrence.
- `AGENTS.md` "Simulation integrity (blocking)" — enforced in agent workflows.
- `.claude/agents/publication-writer.md` — GATE check added as first constraint.
