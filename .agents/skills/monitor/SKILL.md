---
name: monitor
description: |
  Watch Laboratory signals after a run, analysis change, publication update, CI
  change, or repeated agent workflow. Uses local files, CI status, data
  integrity checks, and experiment artifacts rather than deploy telemetry.
  Trigger: /monitor.
argument-hint: "[experiment-path|report-path|--ci]"
---

# /monitor

Laboratory has no production service to watch by default. Monitoring here means
watching the evidence surfaces that can drift after a change:

- CI failures
- flaky tests
- regenerated analysis outputs
- stale `*_latest.csv` pointers
- simulated data accidentally feeding publishable reports
- missing trace/provenance artifacts
- broken Spellbook harness bridges

## Procedure

1. Identify the watched surface: experiment, analysis tool, report, docs, or
   harness.
2. Pick the signal:
   - repo health: `make ci-smoke`
   - harness health: symlink/marker audit
   - experiment health: simulate run plus artifact inspection
   - publication health: data provenance and report consistency
3. Poll or re-run only as long as useful. This is a bounded local watch, not a
   daemon.
4. Escalate to `/diagnose` on a real regression.

## Output

Return `monitor.done` or `monitor.alert` with:

- commands run
- artifacts inspected
- signal result
- recommended next step
