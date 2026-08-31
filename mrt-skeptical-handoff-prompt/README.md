# mrt-skeptical-handoff-prompt

## Overview

Turns an unresolved investigation into a copy-paste handoff prompt for a
stronger or different AI session — but unlike a clean-slate restart, it
deliberately carries this session's own findings forward, each one clearly
labeled as unverified, plus the environment and access details the next
session needs to check everything itself.

## Value Proposition

- Prevents the common failure mode of a model-escalation handoff: pasting a
  lower-effort session's conclusions into a stronger session and having it
  accept them uncritically instead of actually re-investigating.
- Separates what this session actually observed (command output, logs,
  reproduced errors) from what it merely inferred or guessed, and surfaces
  any point where its own explanation was wrong and later revised, as an
  explicit reliability flag.
- Bundles concrete, independently runnable environment and access
  instructions (servers, repos, databases, SSH commands) so the receiving
  AI never has to take the write-up on faith.
- Defaults the handoff to analysis-and-propose-only scope, so the stronger
  session verifies and recommends before anything actually changes.

## Who It Is For

Anyone who ran a lower-effort or lower-tier-model first pass on a bug, an
ambiguous incident, or open research, and now wants to switch to a stronger
model or a fresh session — without smuggling in unverified conclusions as
if they were settled facts.

## Technical Overview

- Frontmatter: `name: mrt-skeptical-handoff-prompt`.
- Pure instruction skill — no `scripts/` or `references/`; the full
  behavior lives in `SKILL.md`.
- Output is always one self-contained, fenced prompt block with five fixed
  sections: Your Role, Environment & Access, Observed Symptom, Prior
  Finding / Hypothesis, and What I Need From You.
- Sibling to `mrt-portable-prompt`, with the opposite inclusion rule: that
  skill strips the assistant's own findings out entirely for a clean
  restart, while this one keeps them in but demotes them to an unverified,
  must-check-yourself lead, and adds the environment/access layer that
  `mrt-portable-prompt` doesn't have.

## Status

Working.

## Project Memory

No external state; operates on whatever conversation it's invoked in.

## Next Steps

Trigger when handing an unresolved investigation from a lower-effort model
or session to a stronger one — say something like "I'm switching to a
bigger model, write up what you found so far but flag it as unconfirmed,"
or ask directly for a skeptical or verification handoff prompt.
