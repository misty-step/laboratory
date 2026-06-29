---
acceptance:
    - "docs/experiment-ideas.md contains a living backlog of candidate experiments."
    - "docs/inspiration-studies.md contains external studies and lab follow-up ideas."
    - "New completed experiments add at least one follow-up idea or explicitly state why none was generated."
evidence_required:
    - docs update
    - make ci-smoke
id: 016-maintain-experiment-idea-pile
lifecycle_stage: Intent
status: ready
title: Maintain large experiment and inspiration backlog
---

## Goal

Keep the laboratory stocked with more research ideas than it can execute.

## Rationale

The lab should continuously accumulate curious, useful, and left-field ideas.
Selection should happen from a large living surface, not from whatever idea was
most recently discussed in chat.

## Maintenance Rule

Every experiment closeout should update one of:

- `docs/experiment-ideas.md`
- `docs/inspiration-studies.md`
- a more specific future domain catalog, if this grows too large
