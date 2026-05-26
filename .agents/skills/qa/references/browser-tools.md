# Site And Browser QA

Most Laboratory QA is CLI and artifact inspection. Use browser automation only
when the touched surface is the Astro site or a publication page whose rendered
state matters.

## When To Use

- `site/src/**`, `site/public/**`, or site build/config changed.
- A report/chart/content sync changed a rendered publication page.
- The user explicitly asks for browser verification.

## Minimum Evidence

- Build or sync command that produces the rendered artifact.
- Browser screenshot or accessibility snapshot of the changed route.
- Console/network errors if the page is interactive.
- Confirmation that chart/image assets referenced by the page render.

For pure harness, analyzer, data, backlog, or Spellbook changes, prefer direct
commands and artifact inspection over browser tooling.
