# mrt-deterministic-fix-report

Render completed bug-fix or diagnosis work into a fixed-schema, evidence-only report: same session, same facts → same report.

## The schema

Per problem, always in this order:

1. **Real problem** — with the decisive numbers, identifiers, and log signatures.
2. **Why it happened** — the causal chain, every link evidence-backed.
3. **Why it was missed until now** — the concrete masking factor (silent catch, INFO-level logs, display hiding the corrupt state…).
4. **The fix** — what changed, where, and why that layer.
5. **TDD verification** — new tests by name, red before, green after.
6. **Current-behavior guarantee** — suite counts, zero modified existing tests, pre-existing-failure parity, real-data before/after.

Then one shared **Pending items** section — observed-but-unfixed findings or concrete observation suggestions only. Speculation is banned; "None" is a valid answer.

## Why "deterministic"

The report may contain nothing the session cannot prove: numbers over adjectives, unknowns labeled unknown, every claim re-verifiable from the identifiers given. It reads like an incident postmortem a manager can trust and an engineer can audit.

## Install

```bash
cp -R mrt-deterministic-fix-report ~/.claude/skills/
```

## Use

```
/mrt-deterministic-fix-report
```

after a debugging/fixing session — or ask for an "özet rapor" / summary report of the fixes. Output arrives in your language.

Pairs with [mrt-prove-then-fix](../mrt-prove-then-fix/), which ends its pipeline with this report format.
