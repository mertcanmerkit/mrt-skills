# mrt-skills

## Overview

A private collection of Mertcan's personal Claude Code skills, migrated from Codex CLI's personal skill library (`~/.codex/skills/`). Each skill lives in its own subfolder with a `SKILL.md` (the agent-facing skill definition Claude Code auto-discovers) and a `README.md` (human-facing documentation of what it does and why).

## Value Proposition

- Single source of truth and backup for skills that used to live only on one machine's `~/.codex/skills/`.
- Documents what each skill does in plain language, separate from the agent-facing `SKILL.md` instructions.
- Preserves the migration decisions — what was dropped, what was adapted, what has no equivalent, and why — so future sessions don't have to reverse-engineer them from a diff.

## Who It Is For

Mertcan, as the personal skill library backing his day-to-day Claude Code usage, and any future AI session that needs to understand why these skills look the way they do.

## Technical Overview

- **Naming convention:** every skill is prefixed `mrt-` to distinguish personal skills from third-party or plugin-provided skills.
- **Layout:** `mrt-<skill-name>/{SKILL.md, README.md, references/, scripts/}` — the same layout Claude Code auto-discovers under `~/.claude/skills/`. To install on a new machine, copy or clone each `mrt-<skill-name>/` folder into `~/.claude/skills/`.
- **Provenance:** originally written as Codex CLI skills. Three Codex skills were deliberately excluded from this migration as third-party, not personal: `.system/` (Codex's own built-in skills — imagegen, openai-docs, plugin-creator, skill-creator, skill-installer), `hatch-pet` (Apache-2.0, depends on Codex's built-in `$imagegen`), and `motion-design` (MIT, authored by LottieFiles).

| Skill | What it does |
|---|---|
| [`mrt-bootstrap-private-ai-project`](mrt-bootstrap-private-ai-project/README.md) | Bootstrap/adopt a durable, private, GitHub-backed AI project with portable memory. |
| [`mrt-register-with-ai-playground`](mrt-register-with-ai-playground/README.md) | Register a project into Mertcan's personal AI project registry. |
| [`mrt-save-knowledge-gained`](mrt-save-knowledge-gained/README.md) | Save useful chat learnings into durable project Markdown for future AI sessions. |
| [`mrt-skill-smoke-test`](mrt-skill-smoke-test/README.md) | Smoke-test another Claude Code skill's `SKILL.md` for validity and real usability. |
| [`mrt-open-codex-project`](mrt-open-codex-project/README.md) | Reference note: Claude Code has no Codex-Desktop-Projects equivalent. |
| [`mrt-feature-proof-auditor`](mrt-feature-proof-auditor/README.md) | Browser-screenshot proof that a requested feature actually works. |
| [`mrt-trello-proof-card-closer`](mrt-trello-proof-card-closer/README.md) | Attach audit proof to Trello cards and move them to done. |
| [`mrt-current-changes-issue-summary`](mrt-current-changes-issue-summary/README.md) | Turn current git changes into a Turkish GitHub-issue checklist. |
| [`mrt-pre-push-gate`](mrt-pre-push-gate/README.md) | Pre-push test/doc hygiene gate for a specific Laravel project. |
| [`mrt-ui-design-guardrails`](mrt-ui-design-guardrails/README.md) | Interview + design-system brief before UI implementation. |
| [`mrt-ui-polish-sourcing`](mrt-ui-polish-sourcing/README.md) | Source-aware UI polish: use outside libraries only when they solve a real gap. |
| [`mrt-evidence-based-docs`](mrt-evidence-based-docs/README.md) | Generate evidence-based, file:line-cited docs (CLAUDE.md/AGENTS.md/CONTEXT.md, subsystems, ADRs) for a legacy repo via a multi-agent Workflow. |

## Status

All 12 skills are working under Claude Code. Of the 10 migrated from Codex CLI, four required adaptation beyond a straight copy, because they relied on Codex-only mechanics (Codex Desktop's Projects registry, Codex-specific frontmatter/packaging conventions): `mrt-bootstrap-private-ai-project`, `mrt-register-with-ai-playground`, `mrt-skill-smoke-test`, `mrt-open-codex-project`. The rest moved over verbatim or with a one-line wording fix ("Codex" → "Claude" in trigger descriptions). `mrt-evidence-based-docs` and `mrt-save-knowledge-gained` are native additions, not migrated.

## Project Memory

Each skill's own `README.md` documents its specifics — frontmatter, bundled files, what changed during migration, and how to invoke it. Migration-level decisions that apply across the whole collection (what's third-party, what's Codex-only, what has no Claude Code equivalent) are recorded once here instead of repeated per skill.

## Next Steps

- To use these skills on a new machine: clone this repo and copy each `mrt-<skill-name>/` subfolder into `~/.claude/skills/`. Claude Code auto-discovers skills there — no plugin registration or restart required.
- New skills added to this collection should follow the same layout (`SKILL.md` + `README.md`, `mrt-` prefix) and get added to the table above.
- Run `mrt-skill-smoke-test` against any new or edited skill before considering it done.
