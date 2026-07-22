# mrt-evidence-based-docs-reconcile

## What it does

Reconciles an **existing documentation layer** against the current code. Where
`mrt-evidence-based-docs` *generates* docs for an undocumented repo, this sibling
*refreshes* docs that already exist — because legacy docs drift, and a confidently
wrong doc is worse than no doc.

Every existing claim is treated as an **unverified claim, not ground truth.** The skill
re-derives the truth from code, migrations, tests, and config, ties it to a `file:line`
citation, and then **keeps, corrects, drops, or marks `UNCERTAIN`** each claim — while
**preserving human-authored prose.** Missing docs are created; nothing is
blind-overwritten.

In one run it reconciles:

- **`CLAUDE.md`** — merged in place (architecture, conventions, gotchas, links).
- **`AGENTS.md`** — merged in place (real build/test/lint/run commands + conventions).
- **`CONTEXT.md`** — merged and deduped against the existing glossary; stays pure domain vocabulary.
- **`docs/subsystems/*.md`** — each existing doc reconciled claim-by-claim; missing ones created.
- **`docs/adr/*.md`** — existing ADRs kept and never renumbered; genuinely new decisions numbered from `max+1`.

## Why it exists

The greenfield skill explicitly scopes itself out of documented repos — run on a repo
that already has a `CLAUDE.md`, its `Write`-everything phases **clobber** the existing
docs and **renumber ADRs from 0001 over the top of existing ones.** That's data loss.

Reconcile mode inverts the posture: **read → verify → merge → preserve → flag drift.**
Its most valuable output is the **drift report** — the specific claims that had gone
stale and the real `file:line` truth that replaced them. As with the greenfield scan,
an honest evidence pass routinely surfaces genuine code defects along the way.

It is a **superset** of the greenfield behavior (missing doc → create, existing doc →
reconcile), so it is the right tool for any repo that already has *some* markdown docs.

## How it works

A 6-phase, multi-agent Claude Code **Workflow** (Inventory → Split → parallel Reconcile
→ Synthesis → AGENTS.md → parallel Verify). Phase 0 adds a full **existing-doc
inventory** (classifies every `.md` as canonical / auxiliary / orphan, records the
highest ADR number, detects single-vs-multi context layout). Phase 2 and Phase 5 fan
out one agent per subsystem, so cost scales with repo size (~20-25 agents on a medium
repo). The skill presents a plan and gets approval before spending tokens.

Framework-agnostic — the inventory phase discovers the stack from dependency manifests
and entry points, so it works on any language/framework.

**Because it edits tracked files**, it recommends a clean working tree or a branch
first, and prompts a `git diff --stat` review afterward.

## Bundled files

- **`SKILL.md`** — agent-facing definition (frontmatter + methodology + guardrails).
- **`scripts/evidence_based_docs_reconcile_workflow.js`** — the executable Workflow
  body. Pass it to the Workflow tool inline, or by `scriptPath` with
  `args: { repoRoot, hint }`.

## How to invoke

> My repo already has CLAUDE.md / CONTEXT.md / subsystem docs but they're probably stale — reconcile them against the current code, keep what holds, fix what drifted, all file:line cited.

or explicitly: `/mrt-evidence-based-docs-reconcile`.

## Relationship to `mrt-evidence-based-docs`

| | greenfield (`mrt-evidence-based-docs`) | reconcile (this skill) |
|---|---|---|
| Repo state | no docs | some/all docs already exist |
| Core verb | write | read → verify → merge → preserve |
| Existing files | assumes none | treats as unverified claims; never clobbers |
| ADR numbering | from 0001 | from `max existing + 1` |
| Signature output | first-time docs | **drift report** |

## Provenance

Derived from `mrt-evidence-based-docs` (itself distilled from a proven run against a
legacy Laravel monolith), then inverted from generate-mode to reconcile-mode to close
the "docs already exist" gap the greenfield skill explicitly excludes.
