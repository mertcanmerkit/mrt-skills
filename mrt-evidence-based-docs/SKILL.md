---
name: mrt-evidence-based-docs
description: Generate evidence-based, file:line-cited documentation for an undocumented or legacy codebase using a parallel multi-agent Workflow. Produces CLAUDE.md, AGENTS.md, CONTEXT.md, docs/subsystems/, and docs/adr/. Use when the user wants to document or onboard a legacy/unfamiliar repo, create a CLAUDE.md / AGENTS.md / CONTEXT.md, map subsystems, extract a domain glossary, or record architecture decisions — with every claim grounded in code, not generic descriptions.
---

# Evidence-Based Codebase Documentation

## Goal

Document an existing (usually legacy, usually undocumented) codebase so that **every
claim is derived directly from code, migrations, tests, or config, with a `file:line`
citation.** No generic, surface-level, or framework-boilerplate descriptions. If a
fact cannot be verified in the code, it is marked `UNCERTAIN`, never invented.

The output is a durable documentation layer an AI agent (or human) reads first:

```
/
├── CLAUDE.md              # top-level map: architecture, conventions, gotchas, links
├── AGENTS.md              # runbook: build/test/lint/run commands + conventions
├── CONTEXT.md             # pure domain glossary — zero implementation detail
├── docs/
│   ├── adr/               # architecture decisions, only when they earn it
│   └── subsystems/        # one deep-dive per subsystem, fully file:line cited
└── (existing source, unchanged)
```

## When to use

- The user wants to document / onboard / "make sense of" a legacy or unfamiliar repo.
- They ask for a `CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, subsystem docs, a domain
  glossary, or retroactive ADRs.
- They want the docs to be *evidence-based* / *cited* / *not generic*.

Do **not** use for: a quick one-file explanation, a README polish, or a repo that is
already well-documented and just needs a small edit.

## How it works — two steps

This skill drives the **Workflow** tool (multi-agent orchestration). The skill's
instruction to use Workflow IS the opt-in — you do not need extra permission.

### Step 1 — Plan, then get approval

Before spending tokens, present a short plan and get the user's approval:

- The 6-phase pipeline (below) and roughly how many agents (Phase 2 + Phase 5 scale
  with subsystem count — typically ~20-25 agents total on a medium repo).
- Note that it is a substantial token spend (deep, parallel, verified).
- The output tree above.
- The guardrails (secrets, citations, ADR criteria).

Present this inline and wait for a yes. Do not start the Workflow until approved.

### Step 2 — Run the Workflow

Use the bundled script as the Workflow body. Two ways:

- **Adapt inline:** read `scripts/evidence_based_docs_workflow.js`, and pass it as the
  Workflow `script`. Optionally pass `args: { repoRoot: "<abs path>", hint: "<stack hint>" }`.
- **By path:** `Workflow({ scriptPath: "<abs path to scripts/evidence_based_docs_workflow.js>", args: { repoRoot: "<abs repo path>" } })`.

The script is **framework-agnostic** — Phase 0 discovers the stack. Do not hardcode
language/framework assumptions into it.

## The 6 phases

| Phase | Agents | Mode | Produces |
|---|---|---|---|
| **0 Inventory** | 1 | single | Structured scan: entry points (HTTP/CLI/API/events), folders, stack (from manifests), tests, config, boundary hints. `mkdir -p docs/{adr,subsystems}`. |
| **1 Split** | 1 | single | Subsystem boundaries (typically 5-9) derived from Phase 0 — *not* hardcoded. Each with name, scope, seed globs, key files. |
| **2 Deep-dive** | one per subsystem | **parallel (barrier)** | Each agent writes its own `docs/subsystems/<name>.md` (file:line cited) **and** returns structured CONTEXT-term + ADR candidates. |
| **3 Synthesis** | 3 | parallel | `CLAUDE.md` (from all docs) · `CONTEXT.md` (deduped pure vocab) · `docs/adr/*` (accepted ADRs + index). |
| **4 AGENTS.md** | 1 | single | Real build/test/lint/run commands from actual manifests; bidirectional link with CLAUDE.md. |
| **5 Verify** | one per doc + 3 | **parallel** | Grep-check every citation, CONTEXT purity, ADR tags. **Fix or remove** anything that fails. |

**Why the barrier after Phase 2:** synthesis genuinely needs *all* subsystem docs and
*all* candidates merged/deduped before it can write CLAUDE.md / CONTEXT.md / ADRs.
Everything else fans out.

**Why agents write the files, not the script:** Workflow scripts have no filesystem
access. Each agent does its own `Write`; the script only aggregates the structured
candidate data in memory and hands it to the Phase 3 writers. No git worktrees are
needed because every agent writes a *distinct* path — no write conflicts.

## Hard rules (baked into the script prompts — keep them if you adapt)

1. **Every claim carries a real `path:line` citation.** Open/grep the file; never
   invent a line number. Phase 5 re-greps every citation and fixes or deletes bad ones.
2. **Secrets never enter docs.** Tokens, passwords, keys, connection strings → refer
   to the config *key* / env var *name* only. Never the value.
3. **`CONTEXT.md` is pure domain vocabulary.** Term + business definition. No file
   names, no code identifiers, no line numbers. A non-coder must understand it.
   Phase 5 enforces this.
4. **ADRs are honest and rare.** Write one only when all three hold: hard to reverse
   **+** surprising without context **+** the result of a real trade-off. Every ADR
   carries the mandatory tag *"Inferred from code scan, not the original decision
   rationale"* — legacy code may have lost the real reasoning; do not invent it.
5. **`UNCERTAIN`, never fabricated.** Anything unproven is labelled, not guessed.
6. **Single-context layout.** One repo = one context. No `CONTEXT-MAP.md`.

## After it finishes

The Workflow returns a summary object and runs in the background (you are re-invoked
on completion). Then:

1. Verify the files exist on disk (`ls` the tree; count lines/citations).
2. Independent secret-leak grep across the new docs (must be empty).
3. Spot-check 1-2 headline citations yourself before trusting the batch.
4. Report: files written, subsystem list, verify verdicts, and any real defects the
   scan surfaced (evidence-based scans routinely catch genuine bugs — surface them).

Then, if this repo is one the user commits: offer to commit the `docs/` tree + the
three root files on a branch. Do not push/merge without explicit approval.
