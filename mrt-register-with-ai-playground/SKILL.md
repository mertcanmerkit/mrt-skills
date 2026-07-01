---
name: mrt-register-with-ai-playground
description: Register the current work as a durable private AI project in Mertcan Merkit AI Development Playground. Use when Mertcan wants an existing chat, folder, repo, registered project, or newly bootstrapped project to be converted/adopted with mrt-bootstrap-private-ai-project, pushed to private GitHub, and written back into the playground registry with repo URL, local path, role, usage notes, read-first files, and dispatch guidance.
---

# Register With AI Playground

## Purpose

Do one thing: make the current work discoverable from Mertcan Merkit AI Development Playground.

This skill is a bridge after or during project bootstrap. It ensures the current project is private GitHub-backed, then records what it is, how to use it, and where it lives in the playground.

## Hard Defaults

- Private GitHub by default.
- Use `mrt-bootstrap-private-ai-project` first if the current work is not already a durable private AI project.
- Do not treat an ad hoc chat as a substitute for a durable registered project.
- Do not push to a public remote unless Mertcan explicitly requested public.
- Do not implement unrelated feature work. This skill only bootstraps/adopts/registers projects.
- If the current work produces reusable AI operating doctrine, update the playground source-of-truth docs instead of leaving the rule only in the current project, chat, or automation prompt.
- If the reusable doctrine concerns heartbeat automations, preserve adaptive cadence rules: recurring master heartbeats stay between 5 and 14 minutes, long waits clamp to 14 minutes, and rollovers retarget the heartbeat to the new master thread.

## Required Playground

- Local path: `/Users/mertcanmerkit/Documents/Mertcan Merkit AI Development Playground`
- Repo: `https://github.com/mertcanmerkit/mertcan-merkit-ai-development-playground`
- Registry files:
  - `docs/06_ai_system_registry.md`
  - `docs/10_registered_projects.md`
  - `source_of_truth/registered_projects.json`

## Workflow

1. Resolve the current project path.
   - Use the current workspace/cwd when obvious.
   - If the user supplied a path, use that path.
2. Ensure the project follows `mrt-bootstrap-private-ai-project`.
   - If the project has no durable memory files, load and follow `/Users/mertcanmerkit/.claude/skills/mrt-bootstrap-private-ai-project/SKILL.md`.
   - Use origin mode `existing-project` for existing folders/repos and `existing-chat` for chat-to-project conversion.
3. Verify or create private GitHub.
   - If no remote exists, create a private repo.
   - If a remote exists, verify `isPrivate=true`.
   - If the remote is public and Mertcan did not explicitly request public, stop and report the blocker.
4. Infer the project role and usage.
   - Prefer `README.md`, `knowledge/README_FOR_AI.md`, `docs/00_project_brief.md`, `SKILL.md`, or `AGENTS.md`.
   - If the project contains `source_of_truth/DESIGN.md`, `source_of_truth/stitch-map.md`, or `docs/*stitch*`, treat it as a design/Stitch-aware project. Include those files in `--read-first` and mention in `--usage` that agents must not infer the current design from Stitch canvas position or a vague latest label. Also mention that Stitch uses the highest available usable model by default, practically Pro, and Flash is allowed only when Mertcan explicitly says to use Flash for Google Stitch.
   - If the project contains master orchestration, specialist threads, scheduled heartbeats, or automation rollover rules, preserve reusable automation doctrine in the playground source of truth and mention the project-local read-first docs where those rules live.
   - If uncertain, write a conservative usage note and mark unknowns as `TBD`.
5. Update the playground registry:

```bash
python3 /Users/mertcanmerkit/.claude/skills/mrt-register-with-ai-playground/scripts/register_project.py \
  --project-name "<Project Name>" \
  --project-path "/absolute/project/path" \
  --repo-url "https://github.com/mertcanmerkit/<repo>" \
  --role "<what this project does>" \
  --usage "<how Mertcan should use or dispatch to it>" \
  --read-first "README.md" \
  --read-first "knowledge/README_FOR_AI.md"
```

6. Commit and push the playground update.
7. Commit and push the current project if this skill changed it.
8. End with:
   - current project repo URL
   - playground repo URL
   - files updated in playground
   - privacy confirmation
   - commit hashes

## Validation

Before final response:

- Confirm the target project repo is private.
- Confirm the playground repo is private.
- Confirm `docs/10_registered_projects.md` contains the project repo URL.
- Confirm `source_of_truth/registered_projects.json` contains the project repo URL.
- Confirm `git status --short --branch` is clean in the playground after push.
