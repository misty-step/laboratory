---
name: qa
description: |
  Verify laboratory experiment changes beyond "tests passed": simulate runs,
  analysis outputs, trace/provenance checks, and publication-readiness evidence.
  Use when: "QA this experiment", "verify this harness", "check publishability",
  "capture evidence", "smoke test this analysis". Trigger: /qa.
argument-hint: "[experiment-path|analysis-path|report-path]"
---

# /qa

QA in Laboratory means verifying the scientific workflow surface that changed.
`make ci-smoke` is necessary, but it is not always sufficient.

## Route By Surface

| Surface | QA Path |
|---|---|
| Experiment harness | Run deterministic simulate mode, inspect CSV schema, confirm no API keys are required. |
| Live harness path | Check explicit `--live`, provider preflight, budget cap, model/config logging, and trace output. |
| Analysis script | Run against fixture or committed data; verify output tables/charts match the data source. |
| Publication artifacts | Confirm source data is live, trace-backed, and not mixed with simulated rows. |
| Spellbook harness/docs | Check bridge links, repo brief, skill markers, and `make ci-smoke`. |
| Website/content | Run content sync/build if the touched files affect the site. |

## Procedure

1. Read `.spellbook/repo-brief.md`, `AGENTS.md`, and the touched experiment docs.
2. Identify the exact behavior the change claims to support.
3. Run the smallest direct command that exercises that behavior.
4. Inspect the generated artifact, not only the exit code.
5. For data/report work, check `mode` or equivalent provenance before accepting
   any publishable claim.
6. Record residual unverified paths explicitly.

## Simulation Integrity

Blocking rule: simulated rows are harness QA only. If a report, paper, blog post,
executive summary, social thread, or data card presents simulated rows as live
evidence, QA fails.

## Report

Return:

- verdict: `PASS`, `FAIL`, or `UNVERIFIED`
- commands run
- artifacts inspected
- provenance/live-data status
- remaining publication or runtime risk
