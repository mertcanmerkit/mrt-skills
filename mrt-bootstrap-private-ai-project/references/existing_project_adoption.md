# Existing Project Adoption

Use this reference when the user already has a chat, folder, repo, or existing AI project and wants it brought under this skill's private GitHub-backed project-memory workflow.

## Modes

- **New project**: no meaningful prior folder or repo exists. Create the normal scaffold.
- **Existing chat**: useful context exists in the current or pasted chat, but not yet as a repo. Create a project folder and convert the reusable chat context into docs, source-of-truth notes, and handoff prompts.
- **Existing local project/repo**: code, docs, assets, or git history already exist. Preserve them and add missing AI memory files.
- **Existing registered project**: workspace already appears in the coding agent's own project list (e.g. Codex Desktop's Projects), but repo memory files, private GitHub continuity, or handoff docs are missing. Add them without recreating the project.

## Existing Project Workflow

1. Inspect before writing:
   - `git status --short --branch`
   - `git remote -v`
   - existing `README.md`, `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `.github/copilot-instructions.md`, `ai-project.yaml`, `docs/`, package manifests, source-of-truth folders, orchestration docs, and obvious project files
2. Determine what should become durable memory:
   - user intent and working style
   - current objective and next task
   - important existing docs or prompts
   - trusted screenshots, PDFs, exports, datasets, transcripts, or links
   - validation commands and known gaps
3. Run the scaffold in adoption mode:

```bash
python3 scripts/scaffold_private_ai_project.py \
  --path /absolute/existing/project \
  --name "<Project Name>" \
  --objective "<current objective>" \
  --origin-mode existing-project \
  --source-summary "<what existing context was used>" \
  --next-task "<next task>"
```

4. Fill or update the generated memory files using the existing project context.
5. If `README.md` already existed, preserve it. The script appends an AI project-memory section instead of replacing the file.
6. Align portable agent compatibility:
   - Keep existing `AGENTS.md` if it already contains meaningful project instructions; append missing private AI project rules instead of replacing it casually.
   - Ensure `CLAUDE.md`, `.cursor/rules/project.mdc`, and `.github/copilot-instructions.md` delegate to `AGENTS.md`.
   - Ensure `ai-project.yaml` records current repo URL, local path, active status, next task, read order, privacy policy, validation commands, and freshness date.
   - Ensure `docs/06_memory_freshness.md` records the latest memory review and refresh triggers.
   - Ensure `docs/07_ai_orchestration_source_of_truth.md` records master/specialist routing, approval gates, bounded task rules, definition of done, and specialist output format.
7. Verify or create private GitHub continuity:
   - If no remote exists, create a private repo.
   - If a private remote exists, push intentional adoption changes.
   - If the existing remote is public and the user did not explicitly request public, stop and ask before pushing.
   - Run `python3 scripts/ai_project_check.py` before push or handoff when available.
8. If the user's coding agent supports its own project registration (e.g. Codex Desktop Projects), register the workspace accordingly.

## Existing Chat Workflow

When the source is a chat rather than a folder:

1. Create/select a project directory.
2. Run the scaffold with `--origin-mode existing-chat`.
3. Save the reusable chat context into durable files:
   - `docs/00_project_brief.md` for objective, scope, assumptions, and open questions
   - `docs/01_ai_operating_model.md` for user working style and operating rules
   - `docs/05_project_adoption.md` for what was imported from the chat
   - `source_of_truth/` for pasted source material, transcripts, screenshots, PDFs, links, or examples
4. Do not rely on "the chat above" as future memory. Promote anything important into files.

## Preservation Rules

- Do not overwrite existing project files unless the user explicitly asks.
- Do not reset git history or discard local changes.
- Do not stage unrelated project files while committing adoption docs.
- Do not invent project facts from filenames alone. Use filenames as hints and mark uncertain items as TBD.
- Do not push to an existing public remote unless the user explicitly confirms public publishing.
- Do not replace an existing `AGENTS.md`, `CLAUDE.md`, Cursor rule, Copilot instruction, or `ai-project.yaml` if it contains useful project-specific rules. Merge missing rules and record conflicts in `docs/05_project_adoption.md`.

## Adoption Done Means

- Existing context has been read and reflected in project memory.
- Missing docs, knowledge, validation, source-of-truth, handoff, and adoption files exist.
- `AGENTS.md`, Claude/Cursor/Copilot adapters, `ai-project.yaml`, and `docs/06_memory_freshness.md` exist and reflect the adopted project.
- `docs/07_ai_orchestration_source_of_truth.md` exists and reflects the adopted project's orchestration rules.
- `python3 scripts/ai_project_check.py` passes or reports explicit blockers.
- GitHub privacy is verified or the public/private blocker is reported.
- `docs/02_session_handoff_prompt.md` gives a future AI session an accurate start point.
- `docs/05_project_adoption.md` records what was adopted and what still needs review.
