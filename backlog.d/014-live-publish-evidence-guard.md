---
acceptance:
    - Publish-oriented analysis fails when source data contains `mode=simulate`.
    - Publish-oriented analysis fails when source data lacks enough provenance to distinguish live from simulated runs.
    - Existing smoke-analysis commands still work for non-publish historical summaries.
evidence_required:
    - tests
    - validation output
    - affected command examples
id: 014-live-publish-evidence-guard
lifecycle_stage: Policy/Eval
status: ready
title: Add live-data publish guard for lab analyses
---

## Goal

Prevent simulated or provenance-poor data from becoming publishable findings.

## Rationale

The repository already has a simulation-integrity policy, but enforcement is
inconsistent across analyzers and historical data. This should be a shared guard
with explicit non-publish escape hatches for smoke tests and archived summaries.

## First Targets

- `tools/analyze_prompt_injection_runs.py`
- `tools/analyze_prompt_injection_with_ci.py`
- Current active experiment analyzers
