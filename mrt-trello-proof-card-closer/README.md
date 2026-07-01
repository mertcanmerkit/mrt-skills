# mrt-trello-proof-card-closer

## Overview

Attaches audit-proof screenshots to matching Trello cards, ticks completion markers, and moves verified cards to a done list.

## Value Proposition

Closes the loop from "I verified this feature with screenshots" (via `mrt-feature-proof-auditor`) to "the Trello card reflects that" — without manually hunting for the right card and re-uploading files.

## Who It Is For

Mertcan's Trello-based task tracking, wherever a board tracks feature/audit work with waiting → done style lists.

## Technical Overview

- Frontmatter: `name: mrt-trello-proof-card-closer`.
- No bundled scripts — operates via a Trello MCP/API connector when available, or Chrome browser control as a fallback.
- Normalizes card titles vs. audit titles/screenshot slugs (Turkish/ASCII, punctuation, hyphens) to find safe matches; skips ambiguous matches rather than guessing.
- Hard safety rules: never deletes cards/attachments/lists, never invents checklist items, never moves rows that aren't cleanly complete.

## Status

Working. Adapted from Codex: only the description wording changed ("asks Codex" → "asks Claude").

## Project Memory

No local state. It mutates a live Trello board directly — the board itself is the "memory."

## Next Steps

Trigger with "close these Trello cards", "move verified cards to done", or by pointing it at an audit matrix produced by `mrt-feature-proof-auditor`.
