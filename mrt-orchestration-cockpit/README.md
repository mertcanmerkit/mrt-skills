# mrt-orchestration-cockpit

## Overview

A pattern for running one orchestrator AI session that coordinates several
parallel sub-sessions, with a live "cockpit" page the human checks and answers
from. The page shows work packages, sub-session handoff cards (claims vs.
verified evidence), human to-dos and staleness signals. It also holds an
async decision inbox: the orchestrator posts non-urgent questions with options
and a recommendation, the human answers whenever, and the orchestrator
consumes the answers at the start of its next turn by writing them into the
repo's decisions log.

## Value Proposition

- One glance shows what the sessions did while you were away and what is
  waiting on you.
- Non-urgent questions stop interrupting you; urgent ones still do.
- Answers cannot get lost or be acted on twice: each one ends as a numbered
  decision in the repo, and the inbox item records which decision it became.
- Sub-session "done" claims are kept apart from what the orchestrator actually
  verified.
- Staleness is visible instead of silently misleading.

## Who It Is For

Developers who delegate work to several AI coding sessions in parallel (for
example Claude Code sessions in separate git worktrees) and want a control
surface that does not become a second source of truth.

## Technical Overview

- Frontmatter: `name: mrt-orchestration-cockpit`.
- `references/data-model.md`: collections and fields, including the inbox
  state machine (`open → answered → consumed | stale | withdrawn`).
- `references/turn-protocol.md`: what the orchestrator does at turn start and
  end, the sub-session brief and handoff checklist, staleness signals, and
  what never goes on the page.
- Works with a claude.ai Artifact using the `db` capability, or with plain
  Markdown files in the repo as a fallback.

## Status

Draft. Extracted from a real multi-session epic and checked against published
guidance on multi-agent systems and human-in-the-loop patterns. The inbox
protocol itself has not yet been run end to end.

## Project Memory

Reads and writes the project's decisions log, open-questions log and
implementation plan. Pairs with `mrt-save-knowledge-gained` for the memory
files and `mrt-skeptical-handoff-prompt` for handing an unresolved package to
another session.

## Next Steps

Say something like "set up a cockpit page for this epic", "I want to answer
your questions from the tracker", or "make the orchestration hands-off but
keep me in the loop".
