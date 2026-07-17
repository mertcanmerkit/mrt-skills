# mrt-pre-push-gate

## Overview

Audits staged and unstaged git diffs against the project's own subsystem docs (discovered from the repo), and reports only the required test/doc hygiene actions before a push.

## Value Proposition

Catches "missing tests for a changed subsystem" and "stale docs" before they reach a PR, with minimal output — no fluff, no preambles, at most one clarifying question.

## Who It Is For

Any repo that keeps subsystem-level docs (root `*-SYSTEM.md` files or `docs/subsystems/`) and wants a cheap tests/docs gate before pushing. Degrades to folder-level grouping when no subsystem docs exist.

## Technical Overview

- Frontmatter: `name: mrt-pre-push-gate`, `disable-model-invocation: true` — user-invoked only.
- Trigger: type `/mrt-pre-push-gate` before pushing.
- No bundled scripts — pure `git diff` / `git diff --cached` inspection plus a discovered subsystem-to-doc mapping (root `*-SYSTEM.md` → `docs/subsystems/` → `CLAUDE.md`/`AGENTS.md` map → folder grouping).
- Never runs `git push` itself; never writes tests directly, only asks whether to.

## Status

Working.

## Project Memory

No external state; reads the current repo's diff and the project's own subsystem docs when they exist.

## Next Steps

Run `/mrt-pre-push-gate` in any project before pushing.
