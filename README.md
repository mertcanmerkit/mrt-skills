# mrt-skills

A collection of [Agent Skills](https://code.claude.com/docs/en/skills) for [Claude Code](https://www.claude.com/product/claude-code). Each skill is a folder with a `SKILL.md` Claude Code auto-discovers, plus a human-facing `README.md`; some bundle `scripts/` and `references/`.

Skills respond in your language (English by default). The `mrt-` prefix marks them as coming from this collection, so they never collide with other installed skills.

## Installation

Clone the repo and copy (or symlink) any skill folder into `~/.claude/skills/`:

```bash
git clone https://github.com/mertcanmerkit/mrt-skills.git
cp -R mrt-skills/mrt-portable-prompt ~/.claude/skills/
```

Claude Code discovers them automatically — no plugin registration or restart needed.

## Skills

### Project memory & handoff

For making AI-assisted work survive longer than one chat session.

- **[mrt-bootstrap-private-ai-project](mrt-bootstrap-private-ai-project/)** — Turn an idea, chat, or existing repo into a durable, private, GitHub-backed AI project with portable memory files (`AGENTS.md`, `ai-project.yaml`, docs, adapters for Claude/Cursor/Copilot).
- **[mrt-register-with-ai-playground](mrt-register-with-ai-playground/)** — Record a project in your personal AI-projects registry repo: repo URL, local path, role, usage notes, read-first files.
- **[mrt-save-knowledge-gained](mrt-save-knowledge-gained/)** — Distill a chat's useful knowledge (decisions, findings, rejected attempts, next steps) into the project's Markdown memory so a fresh session can continue.
- **[mrt-portable-prompt](mrt-portable-prompt/)** — Restate everything you asked for in this conversation as one clean prompt for another AI — with the assistant's answers deliberately stripped out.

### Documentation

- **[mrt-evidence-based-docs](mrt-evidence-based-docs/)** — Generate file:line-cited docs (`CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, subsystem deep-dives, ADRs) for an undocumented / legacy repo via a parallel multi-agent workflow.
- **[mrt-evidence-based-docs-reconcile](mrt-evidence-based-docs-reconcile/)** — The sibling for repos that *already* have those docs: verify every claim against the current code, correct drift, fill gaps, and preserve human-authored prose — never blind-overwrite.

### Git & shipping

- **[mrt-current-changes-issue-summary](mrt-current-changes-issue-summary/)** — Turn the current uncommitted changes into a boss-ready GitHub issue title plus checked checklist.
- **[mrt-pre-push-gate](mrt-pre-push-gate/)** — User-invoked (`/mrt-pre-push-gate`): audit staged and unstaged diffs for test/doc hygiene against the project's own subsystem docs before a push.

### Verification & proof

- **[mrt-feature-proof-auditor](mrt-feature-proof-auditor/)** — Prove requested features actually work with real browser screenshots and a Done/Missing/Uncertain/Blocked audit matrix.
- **[mrt-trello-proof-card-closer](mrt-trello-proof-card-closer/)** — Attach audit proof to matching Trello cards, tick them complete, and move them to the done list.

### UI & design

- **[mrt-ui-design-guardrails](mrt-ui-design-guardrails/)** — Interview + design-system pass that turns "make it beautiful" into an implementation-ready UI brief before any code.
- **[mrt-ui-polish-sourcing](mrt-ui-polish-sourcing/)** — Source-aware UI polish: use existing project conventions first, pull in outside libraries only when they close a concrete gap.

### Meta

- **[mrt-skill-smoke-test](mrt-skill-smoke-test/)** — Smoke-test another skill: static probe of its `SKILL.md` plus one real, safe, minimal task.
- **[mrt-open-codex-project](mrt-open-codex-project/)** — Reference note for Codex Desktop migrants: Claude Code has no "Projects" registry; here's the closest analogue.

## Contributing

New skills follow the same layout (`SKILL.md` + `README.md`, `mrt-` prefix) and get an entry above. Run `mrt-skill-smoke-test` against any new or edited skill before considering it done.

## License

[MIT](LICENSE)
