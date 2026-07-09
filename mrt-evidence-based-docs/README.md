# mrt-evidence-based-docs

## What it does

Generates an **evidence-based documentation layer** for an undocumented or legacy
codebase. Every claim is tied to a `file:line` citation — no generic, framework-
boilerplate, or hand-wavy descriptions. Anything that can't be verified in the code is
marked `UNCERTAIN` instead of invented.

It produces, in one run:

- **`CLAUDE.md`** — the top-level map an AI agent reads first (architecture, conventions, gotchas, links).
- **`AGENTS.md`** — the runbook: real build/test/lint/run commands + tool-agnostic conventions, cross-linked with `CLAUDE.md`.
- **`CONTEXT.md`** — a pure domain glossary, deliberately free of any implementation detail.
- **`docs/subsystems/*.md`** — one deep-dive per subsystem, fully cited (execution flow, data model, config, tests, gotchas).
- **`docs/adr/*.md`** — retroactive architecture decision records, written only when a decision is hard to reverse *and* surprising *and* a real trade-off, each tagged as inferred from a code scan.

## Why it exists

Legacy repos accumulate knowledge that lives only in the code and in people's heads.
Generic AI-written docs make it worse — confident, plausible, and wrong. This skill
forces the opposite discipline: **cite or don't claim it.** A final verification pass
re-greps every single citation and deletes or fixes anything that doesn't hold up, so
the docs can be trusted as a source of truth for future AI sessions.

As a side effect, an honest evidence-based scan routinely surfaces real defects
(mismatched constants, dead code, broken endpoints, missing config) — because it reads
what the code actually does rather than what it's supposed to do.

## How it works

A 6-phase, multi-agent Claude Code **Workflow** (Inventory → Split → parallel
Deep-dive → Synthesis → AGENTS.md → parallel Verify). Subsystem boundaries are derived
from the repo, not hardcoded. Phase 2 and Phase 5 fan out one agent per subsystem, so
cost scales with repo size (~20-25 agents on a medium repo). The skill instructs the
agent to present a plan and get approval before spending tokens.

It is **framework-agnostic** — the inventory phase discovers the stack from the
dependency manifests and entry points, so it works on any language/framework.

## Bundled files

- **`SKILL.md`** — agent-facing definition (frontmatter + methodology + guardrails).
- **`scripts/evidence_based_docs_workflow.js`** — the executable Workflow body. Pass it
  to the Workflow tool inline, or by `scriptPath` with
  `args: { repoRoot, hint }`.

## How to invoke

> Document this legacy repo with evidence-based docs — CLAUDE.md, AGENTS.md, CONTEXT.md, subsystem docs and ADRs, all file:line cited.

or explicitly: `/mrt-evidence-based-docs`.

## Provenance

Distilled from a real run against a legacy Laravel monolith (which produced 8 subsystem
docs, 7 ADRs, ~600 citations, and caught 6 genuine bugs), then generalized to be
framework-agnostic. The phase structure, JSON schemas, and guardrails in the bundled
script are the ones that run proved out.
