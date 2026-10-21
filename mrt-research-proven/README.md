# mrt-research-proven

## Overview

Fact-checks advice or claims, usually the assistant's own earlier
recommendations, with a fixed three-track research method. The skill extracts
every checkable claim and groups the claims into three topic tracks. It then
runs one adversarial research subagent per track in parallel. The results are
merged into a single "what was said → verdict → what the evidence says" table
plus a corrected plan.

## Value Proposition

- Catches confident AI folklore before you act on it. Each agent must open its
  sources (no citing from memory) and search for evidence *against* each
  claim.
- Every claim gets one verdict: SUPPORTED, PARTLY SUPPORTED, CONTRADICTED, or
  NO DIRECT EVIDENCE. Sources that could not be opened are marked UNVERIFIED.
- Three focused parallel searches go deeper than one broad search, and they
  keep raw search dumps out of the main conversation.
- Reversals are stated outright. The corrected plan spells out what changed
  and why.

## Who It Is For

Anyone who got advice from an AI about learning, health, product, or tech
decisions and wants it checked against real evidence before acting on it.
This also covers anyone who says "AI can be wrong, research it."

## Technical Overview

- Frontmatter: `name: mrt-research-proven`.
- Pure instruction skill, with no `scripts/` or `references/`.
- Needs a subagent tool (Agent/Task) plus WebSearch and WebFetch in the
  subagents.
- Includes a standalone agent prompt template with the method rules: open
  sources, mark UNVERIFIED, be adversarial, and use the verdict vocabulary.
- Output has a fixed shape: headline, limits up front, claim table, a numbers
  table when relevant, and a corrected plan.

## Status

Working. It was extracted from a real session where it overturned two of five
practice recommendations and corrected several numeric thresholds.

## Project Memory

No external state. It can optionally save the report as a research note in
the project (for example `docs/research/<topic>.md`).

## Next Steps

Say something like "verify what you told me with research", "is there
scientific backing for this?", or "do the three-track research on these
claims".
