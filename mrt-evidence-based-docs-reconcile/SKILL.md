---
name: mrt-evidence-based-docs-reconcile
description: Reconcile and refresh an EXISTING documentation layer (CLAUDE.md, AGENTS.md, CONTEXT.md, docs/subsystems/, docs/adr/) against the current code using a parallel multi-agent Workflow — verify every existing claim, correct drift, fill gaps, preserve human prose, never blind-overwrite. Use when a repo ALREADY has these docs (or a partial set) and they may be stale/inaccurate, or when the user wants to update / refresh / re-verify / reconcile docs rather than generate from scratch. For a repo with NO docs at all, use mrt-evidence-based-docs instead.
---

# Evidence-Based Documentation — Reconcile Mode

## Goal

A repo that **already has documentation** (a full or partial set of `CLAUDE.md`,
`AGENTS.md`, `CONTEXT.md`, `docs/subsystems/`, `docs/adr/`, plus scattered markdown)
has one problem the greenfield case doesn't: **the docs may be wrong.** Legacy docs
drift — a claim that was true 40 commits ago is now confidently false.

This skill reconciles the existing docs against the current code. Every existing claim
is treated as an **unverified claim, not ground truth**; the source of truth is always
the code, migrations, tests, and config. Each claim is verified with a real `file:line`
citation and then **kept, corrected, dropped, or marked `UNCERTAIN`** — while
**human-authored prose is preserved, not clobbered.** Gaps are filled with new cited
detail.

It is the sibling of **`mrt-evidence-based-docs`** (greenfield generation). Same
evidence discipline, opposite posture: that skill *writes*, this one *reads → verifies
→ merges → preserves → flags drift*. It is a **superset** — a missing doc is created,
an existing doc is reconciled — so it is the right tool for any repo that already has
*some* docs.

```
/
├── CLAUDE.md              # merged in place: architecture, conventions, gotchas, links
├── AGENTS.md              # merged in place: build/test/lint/run commands + conventions
├── CONTEXT.md             # merged in place: pure domain glossary, deduped
├── CONTEXT-MAP.md         # only if multi-context (respected if it already exists)
├── docs/
│   ├── adr/               # existing ADRs kept; new ones numbered from max+1
│   └── subsystems/        # existing docs reconciled; missing ones created
└── (existing source + any auxiliary docs left in place)
```

## When to use

- The repo **already has** a `CLAUDE.md` / `AGENTS.md` / `CONTEXT.md` / `docs/` tree
  (full or partial) and the user wants it **updated, refreshed, re-verified, or
  reconciled** against the current code.
- The user suspects the docs are **stale, drifted, or partly wrong** and wants the
  claims checked against code.
- The user adds this skill to a repo that has *some* markdown docs already.

Do **not** use for: a repo with **no docs at all** — use `mrt-evidence-based-docs`
(greenfield) instead, which is simpler and faster with nothing to reconcile.

## How it works — two steps

This skill drives the **Workflow** tool (multi-agent orchestration). The skill's
instruction to use Workflow IS the opt-in — no extra permission needed.

### Step 1 — Plan, then get approval

Before spending tokens, present a short plan and get the user's approval:

- The 6-phase pipeline (below) and rough agent count (Phase 2 + Phase 5 scale with
  subsystem count — typically ~20-25 agents total on a medium repo).
- That it is a substantial token spend (deep, parallel, verified).
- **Explicitly: it edits/merges existing docs in place and never blind-overwrites, but
  it does modify tracked files — recommend a clean working tree (or a branch) first so
  the diff is reviewable.**
- The output tree and the guardrails.

Present this inline and wait for a yes. Do not start the Workflow until approved.

### Step 2 — Run the Workflow

Use the bundled script as the Workflow body:

- **By path (preferred):** `Workflow({ scriptPath: "<abs path to scripts/evidence_based_docs_reconcile_workflow.js>", args: { repoRoot: "<abs repo path>" } })`.
- **Adapt inline:** read the script, pass it as the Workflow `script`. Optionally
  `args: { repoRoot: "<abs path>", hint: "<stack hint>" }`.

The script is **framework-agnostic** — Phase 0 discovers the stack and the existing-doc
inventory. Do not hardcode language/framework assumptions.

## The 6 phases

| Phase | Agents | Mode | Produces |
|---|---|---|---|
| **0 Inventory** | 1 | single | Code scan (entry points, folders, stack, tests, config) **plus a full existing-doc inventory**: every `.md`/sub-`.md`, classified canonical / auxiliary / orphan, with staleness signal; canonical-file presence, highest existing ADR number, and single-vs-multi context layout. |
| **1 Split** | 1 | single | Subsystem boundaries from the code, each **mapped to its existing doc** (full / partial / stale / missing). Flags orphan subsystem docs (no matching subsystem). |
| **2 Reconcile** | one per subsystem | **parallel (barrier)** | Each agent **reads its existing doc first**, verifies every claim + citation against code, keeps/corrects/drops/flags, fills gaps, **preserves human prose** — and returns CONTEXT/ADR candidates + a **drift report**. Missing doc → created fresh. |
| **3 Synthesis** | 3 | parallel | `CLAUDE.md`, `CONTEXT.md`, `docs/adr/*` — each **merged into the existing file** (dedup, preserve). New ADRs numbered from **max+1**; existing ADRs never renumbered. |
| **4 AGENTS.md** | 1 | single | Real build/test/lint/run commands from manifests; **edits existing AGENTS.md**; bidirectional link with CLAUDE.md. |
| **5 Verify** | one per doc + 3 | **parallel** | Grep-check every citation (new **and** surviving pre-existing), CONTEXT purity, ADR tags; anti-clobber check (human content survived, no duplicate canonical files, no broken/orphaned links). **Fix or remove** failures. |

**Why the barrier after Phase 2:** synthesis needs *all* reconciled subsystem docs and
*all* candidates merged/deduped before it can touch CLAUDE.md / CONTEXT.md / ADRs.

**Why agents edit the files, not the script:** Workflow scripts have no filesystem
access. Each agent does its own `Read`/`Edit`/`Write`; the script only aggregates
structured returns. Every agent owns a *distinct* path — no write conflicts, no
worktrees needed.

## Hard rules (baked into the script prompts — keep them if you adapt)

1. **Every claim carries a real `path:line` citation.** Phase 5 re-greps every one.
2. **Secrets never enter docs.** Config key / env var *name* only, never the value.
3. **`CONTEXT.md` is pure domain vocabulary.** Term + business definition. No file
   names, no code identifiers, no line numbers. Phase 5 enforces this.
4. **ADRs are honest and rare.** Only when all three hold: hard to reverse **+**
   surprising without context **+** a real trade-off. Every ADR carries the mandatory
   tag *"Inferred from code scan, not the original decision rationale."*
5. **`UNCERTAIN`, never fabricated.** Anything unproven is labelled, not guessed.
6. **Never blind-overwrite.** Read the existing doc first, then edit/merge in place.
   **Preserve human-authored prose and any claim that still holds.** Losing human
   content is a failure, not a side effect.
7. **Existing docs are unverified claims.** Verify each against code: keep what holds,
   correct what drifted (with the real `file:line`), drop only the provably obsolete.
8. **No duplicate canonical files.** Edit the existing `CLAUDE.md` / `AGENTS.md` /
   `CONTEXT.md`. **New ADRs number from (highest existing + 1)** — never renumber or
   overwrite existing ADRs. Rebuild `docs/adr/README.md` from the files actually on
   disk (old + new), never from the new ones alone.
9. **Layout is detected, not assumed.** Default single-context. If a `CONTEXT-MAP.md`
   already exists or the repo is an obvious monorepo / multi-bounded-context, use the
   multi-context layout — and never clobber an existing `CONTEXT-MAP.md`.

## After it finishes

The Workflow returns a summary object and runs in the background (you are re-invoked on
completion). Then:

1. Verify the files on disk (`ls` the tree; count lines/citations) and — because this
   mode *edits* tracked files — run **`git diff --stat`** so the user sees exactly what
   changed. Preserved human sections should still be present; the diff should read as
   corrections + additions, not wholesale rewrites.
2. Independent secret-leak grep across the changed docs (must be empty).
3. Surface the **drift report**: the specific claims that were stale/wrong and how they
   were corrected — this is the highest-value output of reconcile mode.
4. List any **orphan docs** Phase 0/1 found (docs with no matching subsystem, stray
   auxiliary markdown) for the user to decide keep / link / migrate — never auto-delete.
5. Report: files changed, drift fixed, subsystem list, verify verdicts, and any real
   code defects the scan surfaced.

Then, if this repo is one the user commits: offer to commit the changes on a branch. Do
not push/merge without explicit approval.
