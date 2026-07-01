# mrt-register-with-ai-playground

## Overview

Registers the current project into Mertcan Merkit AI Development Playground — a private, personal registry of all of Mertcan's AI-related projects — recording repo URL, local path, role, usage notes, and read-first files.

## Value Proposition

Solves "which of my side projects does X" with one central, searchable, git-backed registry instead of scattered memory across chats and folders.

## Who It Is For

Mertcan personally. Assumes and depends on the specific external playground repo at `github.com/mertcanmerkit/mertcan-merkit-ai-development-playground`.

## Technical Overview

- Frontmatter: `name: mrt-register-with-ai-playground`.
- `scripts/register_project.py`: writes/updates the playground's three registry files (`docs/10_registered_projects.md`, `docs/06_ai_system_registry.md`, `source_of_truth/registered_projects.json`).
- `references/playground_contract.md`: the registry's required-fields contract, kept byte-for-byte — it documents the actual external registry schema shared with the live playground repo, including a `codex_status` field name that predates this migration and is left as-is for data continuity.
- Depends on `mrt-bootstrap-private-ai-project` — runs it first if the target project isn't already a durable private AI project.

## Status

Adapted from Codex: dropped the step that registered the folder as a "Codex Project" (it called into a script that no longer exists in the Claude Code copy of `mrt-bootstrap-private-ai-project`); script paths updated to `~/.claude/skills/...`. The registry script itself (`register_project.py`) and its `--codex-status` field were intentionally left unchanged — they're the live external registry's actual schema, not a Codex mechanic.

## Project Memory

Reads and writes the external playground repo at `/Users/mertcanmerkit/Documents/Mertcan Merkit AI Development Playground`. This skill assumes that path and repo already exist.

## Next Steps

Use after (or during) bootstrapping a project: "register this project in the playground", or explicitly `Use mrt-register-with-ai-playground`.
