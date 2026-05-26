# Evidence Capture

QA evidence proves the changed scientific surface, not the existence of a
transcript.

## Capture By Surface

| Surface | Evidence |
|---|---|
| Harness | exact simulate command, output path, schema/provenance spot-check |
| Live path | preflight result, budget cap, model config, trace path, cost estimate |
| Analysis | exact analyzer command, input data path, generated report/chart path |
| Publication | live-data provenance, source data mode check, rendered artifact when relevant |
| Spellbook harness | bridge audit, skill/agent root check, `make ci-smoke` |
| Site | build/sync command plus screenshot or rendered route check |

## Storage

Transient logs and screenshots stay under `/tmp` or `.spellbook/` unless the
artifact is itself a report deliverable. Committed data/report artifacts must be
intentional outputs of the experiment workflow, not QA scratch.

## Failure Rule

If the evidence does not directly exercise the changed path, label the path
`UNVERIFIED`. Adjacent green tests are not runtime proof.
