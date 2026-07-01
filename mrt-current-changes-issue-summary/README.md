# mrt-current-changes-issue-summary

## Overview

Turns the repository's current git changes (staged, unstaged, and untracked) into a short, Turkish-language, GitHub-compatible issue checklist, with an issue title naming the two most important work items.

## Value Proposition

Saves the "what did I do today" recap for a boss/PM — no manual changelog writing, no re-reading diffs by hand. The output is copy-paste ready as a GitHub issue.

## Who It Is For

Mertcan's day-to-day workflow: reporting current-session work in Turkish. Anyone on his team who consumes GitHub-issue-style status updates.

## Technical Overview

- Frontmatter: `name: mrt-current-changes-issue-summary`.
- No bundled scripts or references — pure git-inspection and formatting logic lives in `SKILL.md`.
- Reads `git status`, `git diff --stat`, `git diff --cached --stat`, `git diff --name-only` (read-only; never stages, commits, or pushes).
- Optional screenshot mode captures proof screenshots into `~/Desktop/<repo-name>-current-changes-screenshots-YYYY-MM-DD/` plus a zip.

## Status

Working, unchanged from the original Codex skill. No Codex-specific mechanics were found, so it moved over verbatim — only the frontmatter `name:` gained the `mrt-` prefix.

## Project Memory

No external state. Every run is self-contained: it reads the current git working tree and produces a checklist; nothing persists between runs.

## Next Steps

Trigger with phrases like "mevcut changesler", "boss için özet", "issue başlığı çıkar", "what did I do today", or explicitly: `Use mrt-current-changes-issue-summary`.
