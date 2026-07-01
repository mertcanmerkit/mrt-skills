---
name: mrt-feature-proof-auditor
description: Produce browser screenshot evidence for feature audits. Use when the user asks Claude to verify git changes, review implemented feature requests, inspect thread/chat screenshots, compare requested outcomes with a running app, or return proof screenshots that requested features work. Triggers include git changes denetle, thread screenshotlarindan istekleri kontrol et, ozellikler calisiyor mu browser screenshot ile kanitla, and similar audit/proof requests.
---

# Feature Proof Auditor

## Overview

Turn feature requests, git changes, and thread/chat screenshots into a concise proof audit backed by real browser screenshots from the running project.

Use repo facts first, then browser evidence. Keep the skill project-neutral: discover framework, commands, routes, auth state, and test data from the current workspace instead of assuming any stack.

## Workflow

1. Build the request inventory.
   - Read user-provided screenshots, thread titles, final answers, git status/diff/logs, PR text, or commit messages.
   - Create an audit matrix with `id`, `requested`, `evidence page`, `status`, and `screenshot`.
   - Use statuses: `Tamam`, `Eksik`, `Şüpheli`, `Bloklandı`.

2. Discover the app safely.
   - Inspect README, package manifests, framework configs, docker/dev docs, routes, and tests.
   - Reuse an existing local server when available.
   - Start a dev server only when normal for the project and necessary for browser proof.
   - Do not edit repo files while auditing.

3. Collect browser evidence.
   - Prefer the in-app Browser when available.
   - Use a real browser page for each feature, not code-only proof.
   - Save screenshots outside the repo by default:
     `~/Desktop/feature-proof-audit-YYYY-MM-DD-HHMM/`.
   - Use clear filenames: `01-short-slug.png`.
   - If a feature needs state, use existing data and normal UI flows first.

4. Handle state and blockers.
   - Do not run migrations, seeders, destructive commands, or production-affecting actions without explicit user approval.
   - If temporary demo state is unavoidable, back it up first, explain the change, and restore it before the final response.
   - If browser navigation is blocked, data is missing, auth is unavailable, or the feature cannot be proven, mark the row `Bloklandı` or `Şüpheli` and say why.

5. Return the audit.
   - Keep the final response short and in the user's language.
   - Include the screenshot folder path.
   - Include a compact `requested / status` table.
   - Embed local images with absolute Markdown paths when the client can render them.
   - Mention any repo or database changes made during audit; the default should be none.

## Optional Helper

Use `scripts/capture-browser-evidence.mjs` when a deterministic screenshot batch is easier than manual browser control.

Example manifest:

```json
[
  {
    "id": "01",
    "slug": "homepage-header",
    "url": "/",
    "viewport": { "width": 1280, "height": 720 },
    "waitMs": 1000,
    "scrollText": "Header",
    "fullPage": false
  }
]
```

Run:

```bash
node /Users/mertcanmerkit/.claude/skills/mrt-feature-proof-auditor/scripts/capture-browser-evidence.mjs \
  --base-url http://127.0.0.1:8000 \
  --out ~/Desktop/feature-proof-audit-$(date +%Y-%m-%d-%H%M) \
  --manifest /path/to/manifest.json
```

Add `--chrome "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"` when Playwright exists but its bundled browser is missing.

## Quality Bar

- Screenshot evidence must correspond to the requested feature, not just a nearby page.
- A green audit row needs either visible UI proof or a directly observable browser result.
- Code markers, tests, curl responses, and thread final answers can support the conclusion but should not replace browser proof when the user asked for screenshots.
- Never hide uncertainty. Use `Şüpheli` when the page loads but the observed behavior is incomplete or indirect.
