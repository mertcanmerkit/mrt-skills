---
name: mrt-current-changes-issue-summary
description: Summarize only the repository's current git changes as a concise Turkish, GitHub-compatible checked issue checklist with an issue title containing the two most important work items. Use when the user asks for "mevcut changesler", "gerekli formatta dönüş", "boss/patron için özet", "GitHub checkbox liste", "issue başlığı", "what did I do today", or asks for screenshots proving the current local changes. Also use for screenshot-pack requests tied to changed features.
---

# Current Changes Issue Summary

## Goal

Produce a boss-ready, human-readable Turkish summary for the current working tree only. Default output is a GitHub issue title plus checked checklist.

## Hard Rules

- Inspect staged, unstaged, and untracked changes.
- Do not run `git add`, `git commit`, `git push`, branch operations, or destructive git commands.
- Do not edit project files for this task.
- Do not summarize old conversation context, previous screenshots, or already-finished work unless it is still present in current git changes.
- Do not include noisy files such as `.DS_Store`, cache, local lens/config, or generated metadata unless they materially explain the change.
- Do not claim tests were run unless you actually ran them in this turn.
- Keep output concise: usually 5-10 checked bullets.
- Write in Turkish.

## Investigation Workflow

Run read-only git commands first:

```bash
git status --short --branch
git diff --stat
git diff --cached --stat
git diff --name-only
git diff --cached --name-only
git ls-files --others --exclude-standard
```

Then inspect only the diffs needed to understand the main themes:

- Group related files by feature area instead of listing every file.
- Read untracked source/test files with `sed` or `rg` when needed.
- Treat tests, docs, migrations, config, frontend, backend, and commands as separate signal categories.
- If the diff is large, identify the strongest 2-4 themes and ignore mechanical churn.

## Summary Rules

- The issue title must include the two most important work items.
- Bullets must be checked GitHub checkboxes: `- [x]`.
- Prefer business-readable feature descriptions over file names.
- Mention tests/docs only when changed files include them.
- Mention dependency or migration changes only when they matter to the feature.
- If there are no current changes, output:

```markdown
**Issue Başlığı:** Mevcut Git Değişikliği Yok

- [x] Şu anda raporlanacak changed dosya bulunmuyor.
```

## Output Format

Default final answer:

```markdown
**Issue Başlığı:** En Önemli İş 1 ve En Önemli İş 2

- [x] Kilit iş 1 kısa özeti.
- [x] Kilit iş 2 kısa özeti.
- [x] Kilit iş 3 kısa özeti.
- [x] Test/dokümantasyon/config notu, varsa.
```

Do not add a long explanation after the checklist.

## Screenshot Mode

When the user asks for screenshots tied to the current changes:

- Use the provided local URL or discover the running local URL.
- Open screens that visibly prove the changed features, not generic pages.
- Save screenshots outside the repo, preferably:
  `~/Desktop/<repo-name>-current-changes-screenshots-YYYY-MM-DD/`
- Create a zip beside the folder.
- Do not stage screenshots or add them to git.
- Final output should include the normal issue checklist plus short screenshot links/list:

```markdown
**Ekran Görüntüleri**

[Klasör](/absolute/path)
[ZIP](/absolute/path.zip)

- [x] Screenshot 1 kısa adı
- [x] Screenshot 2 kısa adı
```
