---
name: mrt-pre-push-gate
description: Audit staged and unstaged git diffs for test and documentation hygiene before a push, and report only the required actions — no fluff, at most one question. Run with /mrt-pre-push-gate before pushing.
disable-model-invocation: true
---

# Pre-push gate check

Audit current git changes for test and documentation hygiene with maximum token efficiency.

## Rules (do not break these)

1. Be concise. Output only actionable items. No preambles, summaries, or fluff.
2. Do NOT create or update any `.md` file unless the code change strictly requires it (changed API contract, new subsystem, contradiction with existing doc).
3. If a changed subsystem has NO existing related tests in the repo:
   - Do NOT write new tests directly.
   - Ask exactly one question: `No related tests exist for <subsystem>. Should I write tests for the entire subsystem or skip?`
4. Only add/update tests when:
   - Related tests already exist for the changed code (found via grep/glob in `tests/`), AND
   - The change logically requires test updates (e.g. schema key additions that break hardcoded counts or assertions).
5. Evaluate risk against the project's own conventions: read `CLAUDE.md`, `AGENTS.md`, or contributing docs for rules to enforce (e.g. tenancy scoping, cache-key discipline). Always flag leftover debug output (`dd()`, `dump()`, `die()`, `console.log`, `debugger`, debug logs) and cache-clearing calls in production code paths.
6. Never push. Never run `git push` unless user clearly and explicitly says to push.

## What to do

### A) Inspect diffs

Run:

```bash
git diff --stat
git diff --cached --stat
git diff --name-only
git diff --cached --name-only
```

Ignore archived/backup directories the project conventionally excludes (e.g. `_abandoned/`, `_backup/`).

For each modified file, classify by subsystem using the project's own documentation, checked in this order:

1. Subsystem docs at the repo root (e.g. `*-SYSTEM.md`) or under `docs/subsystems/`.
2. A subsystem/doc map in `CLAUDE.md` or `AGENTS.md`.
3. If no subsystem docs exist, group changes by top-level module or folder and note that no doc mapping exists.

### B) For each subsystem with changes

Report a compact line-item:

```md
**<subsystem>** (files: `path1`, `path2`)
- Existing tests: <yes/no + file paths>
- Test update needed: <yes/no + 1-line reason>
- MD update needed: <yes/no + 1-line reason>
```

### C) If any subsystem has no related tests

Ask the single required question from Rule 3.

- Ask at most one question total.
- Choose the highest-risk missing-test subsystem if multiple exist.

## Output format

Return exactly:

```md
### Critical issues before push
- <item> or "None"

### Required actions
- <item> or "None"

### Optional actions
- <item> or "None" (max 3)
```

Then, if applicable, the single question from Rule 3.
