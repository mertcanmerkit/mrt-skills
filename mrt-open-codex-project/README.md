# mrt-open-codex-project

## Overview

A short reference note, not a functioning skill: explains that Claude Code has no equivalent to Codex Desktop's "Projects" registry.

## Value Proposition

Prevents wasted effort chasing a Claude Code "register this folder as a project" feature that doesn't exist. States the gap plainly and gives the closest available analogue instead of silently failing or fabricating a fake registration step.

## Who It Is For

Anyone migrating workflows from Codex Desktop to Claude Code who expects project-registration parity.

## Technical Overview

- Frontmatter: `name: mrt-open-codex-project`.
- No bundled scripts. The original `scripts/open_codex_project.sh` (which edited Codex's `.codex-global-state.json`) was dropped — it has no Claude Code target to act on.
- Content explains the gap and points to running `claude` inside a project folder — session context persists per folder automatically — as the closest analogue.

## Status

Adapted, not ported. This is the one skill in the collection with no working Claude Code equivalent. Kept as documentation rather than removed, so the limitation is discoverable instead of silently missing.

## Project Memory

None. It performs no actions and touches no files or state.

## Next Steps

Read it when Claude gives an unexpected answer to "open this as a project" or "show this folder under Projects" — it explains why. If you still use Codex Desktop, `codex app <path>` continues to work there.
