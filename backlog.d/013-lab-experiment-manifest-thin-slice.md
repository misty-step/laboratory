---
acceptance:
    - A minimal `experiment.yaml` contract is documented and used by the next active experiment.
    - The manifest captures hypothesis id, preregistration status, factors, data mode, budget, model/provider list, scorer version, output paths, and trace paths.
    - Validation fails clearly when required manifest fields are missing for an active live experiment.
evidence_required:
    - manifest schema or documented contract
    - validator output
    - example manifest
id: 013-lab-experiment-manifest-thin-slice
lifecycle_stage: Shape
status: ready
title: Add thin local experiment manifest contract
---

## Goal

Introduce the smallest useful first-class experiment manifest in Laboratory
without building a full experiment platform.

## Scope

Keep this repo-local until one or two experiments prove the shape. If the
contract generalizes, upstream the reusable primitive to Spellbook; keep
experiment semantics owned by the laboratory repo.

## Fields To Consider

- `experiment_id`
- `hypothesis_id`
- `preregistration_status`
- `data_mode`
- `factors`
- `models`
- `budget`
- `scorer_version`
- `run_outputs`
- `trace_outputs`
- `publication_status`
