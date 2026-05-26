---
name: code-review
description: |
  Parallel multi-agent review for Laboratory changes. Prioritizes correctness,
  scientific validity, provenance, tests, and harness fit. Trigger:
  /code-review, /review, /critique.
argument-hint: "[branch|diff|files]"
---

# /code-review

Review the diff as a Laboratory artifact. Findings lead; summaries are
secondary. Block on bugs, invalid scientific claims, missing tests, broken
simulate/live separation, missing trace/provenance, and runtime paths that were
not exercised.

## Scope

Default scope is `git diff <base>...HEAD`, where base is `master` unless the
user names another base. Include uncommitted changes when the user asks for a
working-tree review.

Classify touched surfaces:

- experiment design or manifest
- harness runner
- analysis/statistics
- data artifact
- report/publication artifact
- site/content
- Spellbook harness/skill/agent surface
- repository infra

## Review Lanes

Use fresh reviewers for substantive reviews:

- correctness and runtime behavior
- scientific methodology and provenance
- simplicity and harness fit

Use Thinktank or cross-harness review when the diff is broad, high-risk, or
touches experiment conclusions. Provider output is evidence, not authority; the
lead synthesizes and verifies.

## Blocking Checks

- New or changed executable paths were directly exercised: harness CLI,
  analyzer, Make target, script entrypoint, site build, or wrapper.
- Harnesses preserve deterministic `--simulate` behavior and require explicit
  `--live` for API calls.
- Live paths have provider preflight, budget controls, model/config logging,
  and trace artifacts.
- Analysis refuses simulated or trace-missing data for publishable findings.
- Reports cite live/provenance-backed data and do not overclaim.
- Tests cover new deterministic logic.
- Spellbook harness changes preserve shared `.agents` roots and bridge links.

## Verdicts

- `ship`: no blocking findings and required executable paths were exercised.
- `conditional`: only clearly bounded follow-up remains and the user can accept
  the risk.
- `dont-ship`: any correctness, scientific-validity, provenance, safety, or
  unverified-runtime blocker remains.

## Output

Return findings first, ordered by severity with file/line references. Then list
open questions, commands or artifacts reviewed, and the verdict.
