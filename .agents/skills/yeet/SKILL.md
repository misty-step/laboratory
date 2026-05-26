---
name: yeet
description: |
  Turn Laboratory worktree changes into coherent commits and push when
  appropriate. Classifies every path, keeps experiment/data boundaries clear,
  and refuses secrets or default-branch pushes. Trigger: /yeet, /ship-local.
argument-hint: "[--dry-run] [--single-commit] [--no-push]"
---

# /yeet

Turn the current worktree into reviewable commits. This is not a blind git
wrapper. It classifies every changed path, preserves user work, and keeps
experiment data separate from code/docs.

## Process

1. Read:
   - `git status --short --untracked-files=all`
   - `git diff --stat`
   - `git log -10 --oneline`
   - current branch name
2. Classify every path:
   - `experiment`: design, harness, analyzer, tests
   - `analysis`: analysis scripts or statistical utilities
   - `data`: immutable run artifacts
   - `report`: findings, paper, blog, summaries, charts
   - `docs`: README, architecture, backlog, plans
   - `infra`: CI, Makefile, wrappers, Spellbook harness
   - `debris`: caches, logs, scratch output
   - `secret-risk`: env files or plausible credentials
3. Run the relevant verification. Default is `make ci-smoke`.
4. Split commits by concern and by the repo's commit prefixes:
   `experiment:`, `data:`, `analysis:`, `report:`, `infra:`, `docs:`,
   `refactor:`, or `fix:`.
5. Push only from a non-default branch, unless the user explicitly asks for a
   local-only commit flow.

## Safety

- Never force-push.
- Never use `git add -A` before classification.
- Never mix generated live data with code in the same commit.
- Never commit secrets.
- Never delete untracked user work unless it is unambiguous debris.
- Never push directly to `master`.

## Output

Report commits created, paths deliberately left unstaged or ignored, commands
run, push target, and final worktree status.
