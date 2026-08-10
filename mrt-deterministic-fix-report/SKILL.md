---
name: mrt-deterministic-fix-report
description: Produce a deterministic, fixed-schema summary report of bug-fix or diagnosis work — Real Problem, Why It Happened, Why It Was Missed Until Now, The Fix, TDD Verification, Current-Behavior Guarantee, and an observed-only Pending Items section. Use when the user asks for a summary report of what was done, an "özet rapor", a deterministic write-up of a resolved bug, or a management-ready explanation of a fix. Do NOT use for planning future work, feature changelogs, or status updates on unfinished tasks.
---

# Deterministic Fix Report

## Goal

Render completed bug-fix / diagnosis work into a report whose content is fully determined by the facts of the session: same session, same facts → same report. No adjectives doing the work of measurements, no narrative padding, nothing the session cannot prove.

## The schema (order is fixed)

One block per problem, in the order the problems were tackled. Headings translate into the user's language; the structure never changes:

1. **Real problem** — what actually happened, stated with the decisive identifiers: the exact numbers, record/entity involved, timestamps, log signature. If the original report was a misunderstanding, say what the user *thought* vs. what the data showed.
2. **Why it happened** — the mechanism as a causal chain, each link backed by something read or run this session (a code line, a query result, a measured timing).
3. **Why it was missed until now** — the concrete masking factor: a silent catch block, INFO-level logging nobody watches, a display layer hiding the corrupt state, "correct in the common case", missing observability.
4. **The fix** — what changed, in which file/layer, and why that layer is where the invariant belongs. Name the files.
5. **TDD verification** — the new tests by name, the red result before the fix, the green result after. If the fix was not test-driven, state that plainly instead of dressing it up.
6. **Current-behavior guarantee** — how it was proven nothing else changed: suite names and counts (e.g. "553/553 green"), zero modified existing test files, pre-existing failures shown identical on a clean tree, real-data before/after when available.

After all problem blocks, exactly one shared closing section:

7. **Pending items** — ONLY two kinds of entries are allowed:
   - findings actually **observed** this session but deliberately not fixed (with their evidence), or
   - concrete **observation suggestions**: the specific log pattern, metric, or query to watch, and what reading would confirm or refute the concern.
   Speculative "maybe X is also broken" entries are banned. If nothing qualifies, write "None".

## Determinism rules

- Every statement must trace to session evidence: a command that was run, output that was seen, a file that was read. No memory-of-similar-projects filler.
- Numbers over adjectives: "38 s of the 41 s total, 0.9 s per row across 42 rows" — never "very slow". (Illustrative shape only; use the session's own measurements.)
- Unknowns are labeled unknown ("not verified this session"), never smoothed over.
- Test counts, file paths, log signatures, and timestamps are quoted verbatim in backticks.
- If multiple problems were handled, every one gets its own full block — no merging "smaller" fixes into a footnote.

## Format

- User's language throughout (headings included); code, file paths, test names, and log lines stay verbatim.
- Title + date line at the top; state where the work currently lives (committed / uncommitted / deployed) if known.
- Compact: a reader with no session context must understand each problem in under a minute; a technical reader must be able to re-verify every claim from the identifiers given.
- Write for a manager who is technical enough to care: spell out terms on first use, no invented shorthand.

## Workflow

1. Inventory the session: which distinct problems were diagnosed/fixed, in what order.
2. For each, collect its evidence set (log lines, query results, red/green test outputs, suite counts) — from this session only.
3. Fill the schema per problem; mark anything unprovable as not verified rather than inventing.
4. Build the single Pending Items section from observed leftovers only.
5. Deliver as one message (or a file if the user asks); offer nothing speculative.
