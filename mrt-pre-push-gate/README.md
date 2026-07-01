# mrt-pre-push-gate

## Overview

Audits staged and unstaged git diffs against a specific Laravel multi-tenant project's subsystem docs, and reports only the required test/doc hygiene actions before a push.

## Value Proposition

Catches "missing tests for a changed subsystem" and "stale docs" before they reach a PR, with minimal output — no fluff, no preambles, at most one clarifying question.

## Who It Is For

Mertcan's Laravel multi-tenant project workflow specifically — this skill hard-codes that project's subsystem doc filenames (`CHECKOUT-ORDER-SYSTEM.md`, `PAYMENT-SYSTEM.md`, etc.) and conventions (`ShopScope`, `getCacheKey()`).

## Technical Overview

- Frontmatter: `name: mrt-pre-push-gate`.
- Trigger: `/pre-push`, "pre-push check", "before push", "check tests docs", "gate check" — deliberately narrow ("Use ONLY when...").
- No bundled scripts — pure `git diff` / `git diff --cached` inspection plus a fixed subsystem-to-doc mapping.
- Never runs `git push` itself; never writes tests directly, only asks whether to.

## Status

Working, unchanged from the original Codex skill. No Codex-specific mechanics were found.

## Project Memory

No external state; reads the current repo's diff and the target project's own `*-SYSTEM.md` docs (must exist at that repo's root for the subsystem mapping to mean anything).

## Next Steps

Run `/pre-push` (or say "gate check") inside the Laravel multi-tenant project before pushing.
