# mrt-skill-smoke-test

## Overview

Smoke-tests another skill's `SKILL.md` — checks it's structurally valid (frontmatter, no TODOs, script shebangs/executable bits) and then exercises one real, safe, minimal task with it.

## Value Proposition

Catches "this skill looks fine but doesn't actually trigger or work" before shipping it — the same bug class as an untested feature flag.

## Who It Is For

Mertcan, when authoring or editing any Claude Code skill (including the other 9 skills in this repo).

## Technical Overview

- Frontmatter: `name: mrt-skill-smoke-test`.
- `scripts/skill_smoke_probe.py`: static prober — validates frontmatter (`name` is lowercase-hyphen and matches the folder name, `description` present and non-trivial), flags TODO placeholders, checks bundled `scripts/` for shebang + executable bit, optionally runs a skill's own validator script.
- Workflow layer in `SKILL.md` adds the behavioral half: derive the smallest realistic task from the skill's own description, execute one safe path (dry-run/temp files/disposable folders), and report `PASS` / `WARN` / `FAIL`.

## Status

Adapted from Codex: wording updated ("Codex skill" → "Claude Code skill" throughout, `$target-skill-name` invocation syntax → `/target-skill-name`, script paths updated). The probe script's actual validation logic needed no changes — it only ever checked generic `name`/`description` frontmatter, never Codex-only fields.

## Project Memory

None persistent. Each run targets one skill directory passed as an argument; no state carries over between runs.

## Next Steps

Run directly: `~/.claude/skills/mrt-skill-smoke-test/scripts/skill_smoke_probe.py /absolute/path/to/skill --markdown`, or ask Claude to "smoke test this skill."
