# mrt-prove-then-fix

Turn "a client says there's a bug" into either a data-backed refutation or a proven, TDD-fixed root cause — with a hard guarantee that nothing which worked before behaves differently now.

## Why

Most bug reports arrive as claims: "I entered one number and the system showed another." Some are misunderstandings. Some are real. And some are *reinterpretations* — a real bug, but not the one described. Fixing before proving wastes work on ghosts, and fixing without a behavior guarantee trades one bug for another.

This skill enforces a strict pipeline:

1. **Claim → falsifiable statement.** Confirmed / refuted / reinterpreted are all live options until data decides.
2. **Evidence before code.** Logs, database timestamps, audit/snapshot tables, cross-user sweeps — read-only on live systems.
3. **Deterministic red loop.** One runnable command that goes red on this exact bug, executed and pasted, before any hypothesis.
4. **TDD fix.** Regression test first (new file), watch it fail, minimal fix, watch it pass.
5. **Existing tests are read-only.** Green tests pin current behavior; if the fix would require editing one, the skill stops and asks instead of silently redefining "correct".
6. **Behavior-preservation sweep.** Full suite green; any leftover failures proven pre-existing by comparing against a clean tree.
7. **Deterministic report.** Fixed schema: real problem, why, why missed, fix, TDD verification, behavior guarantee, pending items (observed-only).

## Install

```bash
cp -R mrt-prove-then-fix ~/.claude/skills/
```

## Use

```
/mrt-prove-then-fix a client claims an item quantity in their cart changed on its own
```

Or just describe the suspected bug and ask Claude to "prove it before fixing".

Pairs with [mrt-deterministic-fix-report](../mrt-deterministic-fix-report/) for the closing report (embedded compact version works standalone).
