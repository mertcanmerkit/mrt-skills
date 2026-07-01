---
name: mrt-pre-push-gate
description: Use ONLY when user runs /pre-push or says "pre-push check", "before push", "check tests docs", or "gate check". Audit staged + unstaged diffs for this Laravel multi-tenant project and report only required test/doc hygiene actions.
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
5. Respect project conventions when evaluating risk:
   - multi-tenant scope (`ShopScope`, `getShopId()`, `getShopDomain()`)
   - cache key discipline (`getCacheKey()`)
   - no `dd()`, `dump()`, `die()`, debug logs in production code
   - no `Artisan::call('cache:clear')` in production paths
6. Never push. Never run `git push` unless user clearly and explicitly says to push.

## What to do

### A) Inspect diffs

Run:

```bash
git diff --stat -- ':!_abandoned/' ':!_backup/' ':!.DS_Store'
git diff --cached --stat -- ':!_abandoned/' ':!_backup/' ':!.DS_Store'
git diff --name-only -- ':!_abandoned/' ':!_backup/' ':!.DS_Store'
git diff --cached --name-only -- ':!_abandoned/' ':!_backup/' ':!.DS_Store'
```

For each modified file, classify by subsystem using project docs in root:

- `CHECKOUT-ORDER-SYSTEM.md`
- `PAYMENT-SYSTEM.md`
- `CAMPAIGN-SYSTEM.md`
- `PRICE-DISPLAY-SYSTEM.md`
- `PRODUCT-SEARCH-SYSTEM.md`
- `CACHE-SYSTEM.md`
- `AI-CHAT-SYSTEM.md`
- `ERP-INTEGRATION-SYSTEM.md`
- `HELPERS-SYSTEM.md`
- `ADMIN-SYSTEM.md`
- `USER-SYSTEM.md`
- `CONTENT-SYSTEM.md`
- `NOTIFICATIONS-SYSTEM.md`
- `FRONTEND-SYSTEM.md`
- `CUSTOM-ASSETS-SYSTEM.md`
- `MEDIA-SYSTEM.md`
- `RETURN-REFUND-SYSTEM.md`
- `TENANT-SYSTEM.md`
- `TESTING-SYSTEM.md`

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
