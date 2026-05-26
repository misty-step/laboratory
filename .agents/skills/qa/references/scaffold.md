# Laboratory QA Scaffold

Use this when a QA run needs a written checklist.

## Checklist

- What changed?
- Which executable path proves it?
- Which artifact should exist after the command?
- Is the artifact simulated, live, or derived from committed data?
- Does any publication claim depend on simulated data?
- Are traces/provenance present when claims require them?
- Did `make ci-smoke` pass after the final edit?

## Verdicts

- `PASS`: direct command and artifact inspection prove the changed path.
- `FAIL`: direct evidence contradicts the claim or violates simulation/live
  policy.
- `UNVERIFIED`: evidence is missing, indirect, or only adjacent.
