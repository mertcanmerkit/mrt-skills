---
name: mrt-prove-then-fix
description: Deterministically prove a claimed bug before touching any code, then fix it TDD-style without breaking any current behavior, and close with a fixed-schema deterministic report. Use when the user reports a suspected bug ("a client claims…", "sometimes X happens", "the number changed on its own"), wants a bug verified with data before any code change, says "prove it, don't assume", or wants a fix guaranteed not to alter existing tests or behavior. Do NOT use for feature work, or when the bug already has a reliable failing test — jump straight to the fix there.
---

# Prove, Then Fix

## Goal

Turn "someone says there is a bug" into either (a) a data-backed refutation, or (b) a proven root cause fixed through TDD with a hard guarantee that nothing which worked before behaves differently now — finished with a deterministic report.

The defining stance: **a bug report is a claim, not a fact.** Users misread screens, click the wrong thing, and describe symptoms of a different bug than the one that exists. Every phase below produces evidence; no phase is allowed to run on assumption.

## Workflow

### 1. Restate the claim as a falsifiable statement

Rewrite the report into one testable sentence with concrete identifiers: who, what object/record, what expected vs. observed value, when. If the report lacks these, extract them from the user or the system's own records before proceeding.

Three possible verdicts you are working toward — keep all three alive until the data decides:

- **Confirmed** — the claimed behavior happened as described.
- **Refuted** — the data shows the system behaved correctly (misunderstanding, wrong click, display asymmetry).
- **Reinterpreted** — something real is wrong, but it is a *different* bug than the one described. This is common: the claimed numbers often decode into the actual mechanism (an exact multiplier, an exact sum of hidden rows). Chase arithmetic coincidences.

### 2. Evidence before code

Find the system's own traces before reading a single line of implementation:

- Application logs (including INFO-level noise nobody reads — search for the exact time window).
- Database state: the records themselves, plus timestamps (`created_at` gaps between sibling rows are a free profiler).
- Incidental journals: audit tables, snapshot/history tables, event logs, analytics — systems often record more than anyone remembers. Discover what exists; don't assume.
- Cross-user sweep: if the mechanism is real, other victims usually exist. One query that finds the same signature across users turns an anecdote into a systemic finding.

Hard rules: **read-only against any live/production system**; never modify, delete, or "fix" data while investigating. If the claim is refuted here, write the report (Phase 6) with the evidence and STOP — no code changes for a bug that does not exist.

### 3. Build a deterministic red loop

Before hypothesizing about cause, construct **one runnable command** that goes red on this exact bug:

- Prefer a failing test at the closest seam; fall back to an HTTP script, a CLI invocation with a fixture, or a headless-browser script.
- It must be: **red-capable** (asserts the user's exact symptom, not "doesn't crash"), **deterministic** (same verdict every run), **fast** (seconds), and **agent-runnable** (no human in the loop).
- Run it. Paste the red output. If you cannot build such a loop, say so explicitly, list what you tried, and ask for a captured artifact or environment access — do not proceed on vibes.

For data-shaped bugs, seed the fixture with the *real* shape from Phase 2 (same field values, same duplicated structure) — minimized to only the load-bearing parts.

### 4. TDD fix

1. Write the regression test **first**, in a **new test file**, encoding the Phase 3 repro. Run it. Watch it fail. Paste the failure.
2. Apply the smallest fix that makes it pass. Prefer the layer where the invariant belongs, not where the symptom appears.
3. Run the new test. Watch it go green.

**Hard rule — existing tests are read-only.** Currently-green tests pin current behavior; editing one to make your fix pass silently redefines "correct". `git status` on the test directories must show only added files, zero modifications. If the fix genuinely requires changing an existing test (e.g. it asserts the exact value you need to remove), STOP: that test is telling you the behavior is depended upon. Surface the conflict to the user and either get explicit approval or redesign the fix to work around the pinned behavior.

### 5. Behavior-preservation sweep

1. Run the affected suites, then the full suite.
2. Any remaining failures must be **provably pre-existing**: re-run the same failing tests on a clean tree (`git stash` → run → `git stash pop`, or a separate worktree) and require the failure sets to be identical. "Probably unrelated" is not evidence.
3. If real data exhibiting the bug is available (an imported copy, a fixture dump), run the fixed code against it and show the before/after state.

### 6. Deterministic report

Close with the fixed-schema report — if `mrt-deterministic-fix-report` is installed, follow its full contract; otherwise use this compact schema, in the user's language, one block per problem:

1. **Real problem** — what actually happened, with the decisive numbers/identifiers.
2. **Why it happened** — the mechanism, each step evidence-backed.
3. **Why it was missed until now** — silent catch, INFO-level logging, display masking, "worked in the common case".
4. **The fix** — what changed, where, and why that layer.
5. **TDD verification** — the new tests, their red output before and green after.
6. **Current-behavior guarantee** — suite counts, zero modified test files, pre-existing-failure parity.
7. **Pending items** (one shared section at the end) — ONLY (a) findings actually observed but not fixed this round, or (b) concrete observation suggestions (which log line, metric, or query to watch). Speculation is banned.

## Rules

- Never commit or push unless the user explicitly asks in the current conversation.
- Read-only on production/live systems, always; local/dev data may be mutated only for verification and said so.
- Respond and report in the user's language; keep code, commands, and test names verbatim.
- Every claim in the final report must trace back to something you ran or read this session — a log line, a query result, a test output. If it has no evidence, it does not go in.
