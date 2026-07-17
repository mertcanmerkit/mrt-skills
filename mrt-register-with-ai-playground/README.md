# mrt-register-with-ai-playground

## Overview

Registers the current project into your AI project registry ("playground") — a private, GitHub-backed repo that indexes all of your AI-related projects — recording repo URL, local path, role, usage notes, and read-first files.

## Value Proposition

Solves "which of my side projects does X" with one central, searchable, git-backed registry instead of scattered memory across chats and folders.

## Who It Is For

Anyone maintaining many AI-assisted side projects who wants one searchable, git-backed index of them. The registry repo is yours: the skill resolves its location from the conversation or project docs, or asks once — and can bootstrap one with `mrt-bootstrap-private-ai-project` if none exists.

## Technical Overview

- Frontmatter: `name: mrt-register-with-ai-playground`.
- `scripts/register_project.py`: writes/updates the registry's three files (`docs/10_registered_projects.md`, `docs/06_ai_system_registry.md`, `source_of_truth/registered_projects.json`). Takes a required `--registry-path` pointing at your registry repo.
- `references/registry_contract.md`: the registry's required-fields contract.
- Depends on `mrt-bootstrap-private-ai-project` — runs it first if the target project isn't already a durable private AI project.

## Status

Working.

## Project Memory

Reads and writes the external registry repo you point it at; creates the registry files inside it if missing.

## Next Steps

Use after (or during) bootstrapping a project: "register this project in the playground", or explicitly `Use mrt-register-with-ai-playground`.
