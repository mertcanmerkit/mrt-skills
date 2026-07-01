# mrt-ui-polish-sourcing

## Overview

Keeps UI work source-aware: inspects existing project conventions first, then selectively pulls in third-party UI libraries, themes, or inspiration only when they solve a concrete, specific design gap.

## Value Proposition

Prevents both failure modes at once — reinventing UI from scratch when a good existing token/component already covers it, and reflexively bolting on component libraries the project doesn't need.

## Who It Is For

UI/frontend work (fixing, redesigning, polishing) where the goal is to avoid "generic AI-looking UI."

## Technical Overview

- Frontmatter: `name: mrt-ui-polish-sourcing`.
- `references/ui-sources.md`: loaded only when actually choosing or comparing outside UI sources, libraries, fonts, or motion tools.
- Coordinates with two sibling skills: `mrt-ui-design-guardrails` for deeper product/design interviewing, and `motion-design` (a third-party skill, not part of this collection) for motion-craft specifics.

## Status

Working. Adapted from Codex: only the description wording changed ("Use when Codex works on..." → "Use when Claude works on...").

## Project Memory

No external state; operates on whatever repo/project it's invoked in.

## Next Steps

Trigger during any frontend/UI polish, redesign, or "make it look professional" request.
