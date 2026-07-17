# mrt-bootstrap-private-ai-project

## Overview

Bootstraps or adopts a durable, private, GitHub-backed AI project — from a raw idea, an ongoing chat, or an existing repo/folder — with a portable memory system (`AGENTS.md`, `ai-project.yaml`, `docs/`, `source_of_truth/`) that survives past a single chat session.

Most AI work gets weaker when it lives only in chat: the working style, project assumptions, trusted inputs, decisions, validation steps, and next-session prompt all become hard to recover once the conversation gets long. This skill turns that into a repeatable, file-backed workflow instead.

## Value Proposition

- Turns "the best context is buried in this chat" into versioned, git-tracked files instead of prose that evaporates.
- Generates compatibility adapters (`CLAUDE.md`, `.cursor/rules/project.mdc`, `.github/copilot-instructions.md`) that delegate to one canonical `AGENTS.md`, so the same project works across agents.
- Publishes privately to GitHub by default and verifies `isPrivate=true` before every push — never public by accident.
- Adds automated project checks for required memory files, stale memory, common secret patterns, and GitHub privacy.
- Preserves master/specialist orchestration doctrine (bounded dispatch, approval gates, specialist output contracts, project-spawn flow) and cross-AI dispatch rules for larger multi-agent workflows.
- Preserves Google Stitch / AI design-tool control files so generated screens stay traceable instead of becoming canvas clutter.

## Who It Is For

Anyone who wants an AI-assisted project — solo or multi-agent — to survive longer than one chat session.

## Technical Overview

- Frontmatter: `name: mrt-bootstrap-private-ai-project`.
- `scripts/scaffold_private_ai_project.py`: the generator. Creates or updates all required project memory files for three origin modes — `new`, `existing-chat` (convert a conversation into a repo), `existing-project` (adopt an existing repo/folder without wiping prior work).
- `scripts/quick_validate.py`: self-test gate for this skill itself — validates its own `SKILL.md`/`README.md`/`references/`, and can also validate a scaffolded project's output (`--scaffold-output <path>`).
- `references/`: `master_ai_user_protocol.md`, `private_github_policy.md`, `cross_ai_orchestration.md`, `ai_orchestration_source_of_truth.md`, `existing_project_adoption.md`.
- Every bootstrapped project gets: `README.md`, `AGENTS.md` (canonical instruction entry point), `CLAUDE.md` / `.cursor/rules/project.mdc` / `.github/copilot-instructions.md` (thin adapters), `ai-project.yaml` (machine-readable manifest), `docs/00`–`07_*.md` (brief, operating model, session handoff, validation, cross-AI orchestration, adoption notes, memory freshness, orchestration source-of-truth), `knowledge/README_FOR_AI.md`, `source_of_truth/`, `scripts/ai_project_check.py`, `work/README.md`.
- Workflow: derive name/slug/objective/origin mode → scaffold or adopt via the generator script → fill the generated docs from real context → init/preserve git → publish private → run the generated checker → keep `docs/02_session_handoff_prompt.md` current for the next AI session.

## Status

Working. Self-validated: `scripts/quick_validate.py` passes, and a full scaffold smoke test (new project + existing-project adoption) passes.

## Project Memory

This skill's own memory is its `references/` docs, listed above. The projects it *generates* carry their own separate memory system (`ai-project.yaml`, `docs/`, `knowledge/`, `source_of_truth/`) — building that memory system for other projects is the entire point of this skill.

## Next Steps

Validate after editing this skill:

```bash
python3 scripts/quick_validate.py
```

Run a scaffold smoke test:

```bash
tmpdir="$(mktemp -d)"
python3 scripts/scaffold_private_ai_project.py \
  --path "$tmpdir/example-project" \
  --name "Example Project" \
  --objective "Validate durable private AI project scaffolding." \
  --repo-url "https://github.com/example/example-project" \
  --next-task "Verify the generated memory files and private GitHub defaults."
python3 scripts/quick_validate.py --scaffold-output "$tmpdir/example-project"
python3 "$tmpdir/example-project/scripts/ai_project_check.py"
```

Use it in a Claude Code session:

```text
Use mrt-bootstrap-private-ai-project to turn this idea into a private GitHub-backed AI project with durable memory.
```

```text
Use mrt-bootstrap-private-ai-project to adopt this existing project into the private GitHub-backed AI project workflow without overwriting prior work.
```
