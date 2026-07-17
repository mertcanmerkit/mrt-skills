---
name: mrt-register-with-ai-playground
description: Register the current project into the user's AI project registry ("playground") — a private GitHub-backed repo indexing all their AI projects with repo URL, local path, role, usage notes, and read-first files. Use when the user wants the current chat, folder, or repo registered in their playground/registry, or wants a project bootstrapped with mrt-bootstrap-private-ai-project and then recorded in the registry.
---

# Register With AI Playground

## Purpose

Do one thing: make the current work discoverable from the user's AI project registry repo (their "playground").

This skill is a bridge after or during project bootstrap. It ensures the current project is private GitHub-backed, then records what it is, how to use it, and where it lives in the registry.

## Hard Defaults

- Private GitHub by default.
- Use `mrt-bootstrap-private-ai-project` first if the current work is not already a durable private AI project.
- Do not treat an ad hoc chat as a substitute for a durable registered project.
- Do not push to a public remote unless the user explicitly requested public.
- Do not implement unrelated feature work. This skill only bootstraps/adopts/registers projects.
- If the current work produces reusable AI operating doctrine, update the registry source-of-truth docs instead of leaving the rule only in the current project, chat, or automation prompt.

## Registry Resolution

The registry is a private GitHub-backed repo the user maintains as an index of their AI projects. Resolve its location in this order:

1. A local path or repo URL the user supplied in this conversation.
2. A registry/playground location already recorded in the current project's docs (check `ai-project.yaml` and `docs/04_cross_ai_orchestration.md`).
3. Ask the user once for the registry repo path. If none exists, offer to bootstrap one with `mrt-bootstrap-private-ai-project`.

Registry files (the script creates them if missing):

- `docs/06_ai_system_registry.md`
- `docs/10_registered_projects.md`
- `source_of_truth/registered_projects.json`

Field contract: `references/registry_contract.md`.

## Workflow

1. Resolve the current project path.
   - Use the current workspace/cwd when obvious.
   - If the user supplied a path, use that path.
2. Ensure the project follows `mrt-bootstrap-private-ai-project`.
   - If the project has no durable memory files, load and follow `~/.claude/skills/mrt-bootstrap-private-ai-project/SKILL.md`.
   - Use origin mode `existing-project` for existing folders/repos and `existing-chat` for chat-to-project conversion.
3. Verify or create private GitHub.
   - If no remote exists, create a private repo.
   - If a remote exists, verify `isPrivate=true`.
   - If the remote is public and the user did not explicitly request public, stop and report the blocker.
4. Infer the project role and usage.
   - Prefer `README.md`, `knowledge/README_FOR_AI.md`, `docs/00_project_brief.md`, `SKILL.md`, or `AGENTS.md`.
   - If the project contains `source_of_truth/DESIGN.md`, `source_of_truth/stitch-map.md`, or `docs/*stitch*`, treat it as a design/Stitch-aware project. Include those files in `--read-first` and mention in `--usage` that agents must not infer the current design from Stitch canvas position or a vague latest label. Also mention that Stitch uses the highest available usable model by default, practically Pro, and Flash is allowed only when the user explicitly says to use Flash for Google Stitch.
   - If the project contains master orchestration, specialist threads, scheduled heartbeats, or automation rollover rules, preserve reusable automation doctrine in the registry source of truth and mention the project-local read-first docs where those rules live.
   - If uncertain, write a conservative usage note and mark unknowns as `TBD`.
5. Update the registry:

```bash
python3 ~/.claude/skills/mrt-register-with-ai-playground/scripts/register_project.py \
  --registry-path "/absolute/registry/path" \
  --project-name "<Project Name>" \
  --project-path "/absolute/project/path" \
  --repo-url "https://github.com/<owner>/<repo>" \
  --role "<what this project does>" \
  --usage "<how to use or dispatch to it>" \
  --read-first "README.md" \
  --read-first "knowledge/README_FOR_AI.md"
```

6. Commit and push the registry update.
7. Commit and push the current project if this skill changed it.
8. End with:
   - current project repo URL
   - registry repo URL
   - files updated in the registry
   - privacy confirmation
   - commit hashes

## Validation

Before final response:

- Confirm the target project repo is private.
- Confirm the registry repo is private.
- Confirm `docs/10_registered_projects.md` contains the project repo URL.
- Confirm `source_of_truth/registered_projects.json` contains the project repo URL.
- Confirm `git status --short --branch` is clean in the registry after push.
