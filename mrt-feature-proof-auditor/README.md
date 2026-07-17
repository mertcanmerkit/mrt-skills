# mrt-feature-proof-auditor

## Overview

Produces browser-screenshot proof that a requested feature actually works, by building an audit matrix (requested / evidence / status) and capturing real browser screenshots against the running app.

## Value Proposition

Replaces "trust me, it works" with an evidence folder. Closes the loop between what was asked for (a feature request, a git diff, a chat thread) and what's actually visible in the running app.

## Who It Is For

Verifying implemented feature requests before reporting them done — to a boss/PM, to a Trello board (pairs with `mrt-trello-proof-card-closer`), or as a personal verification habit.

## Technical Overview

- Frontmatter: `name: mrt-feature-proof-auditor`.
- `scripts/capture-browser-evidence.mjs`: optional deterministic screenshot batch runner (Playwright-based), driven by a JSON manifest (`url`, `viewport`, `waitMs`, `scrollText`, `fullPage`).
- Workflow: build a request inventory → discover the app (README/package manifests/routes) → collect screenshots, preferring to reuse an existing dev server → handle state/blockers conservatively → return a compact table with screenshot paths.
- Status vocabulary: `Done` / `Missing` / `Uncertain` / `Blocked`.

## Status

Working.

## Project Memory

No persistent registry. Screenshots save outside the repo by default at `~/Desktop/feature-proof-audit-YYYY-MM-DD-HHMM/` and are never staged or committed.

## Next Steps

Trigger with "verify these changes with screenshots" or "prove this feature works". Requires a running or startable local dev server and a browser (in-app Browser tool, or Playwright + Chrome).
