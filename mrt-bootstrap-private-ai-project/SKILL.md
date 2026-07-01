---
name: mrt-bootstrap-private-ai-project
description: Bootstrap or adopt a durable, private, GitHub-backed AI project from a user idea, normal chat, existing AI project, existing repo, or existing working folder. Use when the user wants to start a new AI project, convert a one-off or ongoing chat into a durable project, retrofit an existing project with repo memory/docs/source-of-truth files, preserve instructions and context for future AI sessions, publish everything privately to GitHub by default, or prepare a follow-up session with a handoff prompt.
---

# Bootstrap Private AI Project

## Core Defaults

- Treat GitHub visibility as private unless the user explicitly says public.
- Private by default applies to every repo, remote, artifact, and handoff unless the user explicitly says public.
- Preserve continuity as a first-class deliverable: write project memory before implementation work.
- Keep source-of-truth, working notes, and handoff prompts inside the repo.
- Always create an explanatory `README.md` that supports both technical onboarding and marketing/product positioning.
- Always create standard portable agent instructions in `AGENTS.md`.
- Always create compatibility adapters for Claude, Cursor, and GitHub Copilot that delegate to `AGENTS.md`.
- Always create a machine-readable `ai-project.yaml` manifest for read order, privacy, validation, freshness, and active project state.
- Always create `scripts/ai_project_check.py` so generated projects can verify required memory files, stale memory, common secret patterns, and GitHub privacy.
- Support both new bootstrap and existing-project adoption. If a repo, folder, or prior chat already exists, preserve it and add missing project memory instead of treating it as blank.
- Preserve cross-AI orchestration knowledge when the user works across specialist AI systems, chats, or triads.
- Preserve master-orchestrator doctrine: master threads synthesize and dispatch; specialist threads execute bounded production work; durable docs absorb decisions.
- For serious production coding, preserve `Lead + Issue Worker + CI Gate`: the master sets priority and gates, platform leads split/review GitHub Issues, issue workers own exactly one issue/branch/PR, and CI is the objective merge gate.
- Preserve controlled parallelism: default to at most 2 implementation issue workers plus 1 research/gate worker, require a dependency map before dispatch, and default to sequential work when conflict risk is unclear.
- Preserve provider portability: any coding agent should be able to start from `AGENTS.md`, `ai-project.yaml`, and the compatibility adapter files without a tool-specific registration step.
- Treat memory freshness as part of done: update manifest, handoff, validation, and freshness docs after meaningful changes.
- Treat AI design tools such as Google Stitch as exploration inputs, not production truth. When a project uses Stitch, preserve project IDs, screen IDs, accepted versions, prompts, and current/archived status in `source_of_truth/stitch-map.md` instead of relying on canvas position or "latest" guesses.
- For Google Stitch model choice, default to the highest available usable model, practically Pro. Use Flash models only when the user explicitly says to use Flash for Stitch. Project labels such as MVP, prototype, quick draft, or low importance are not enough to choose Flash by inference.
- Speak to the user as a master AI operator: direct, technical, pragmatic, and focused on durable leverage.
- Do not leave the work as a plan when tools can execute the setup.

## Workflow

1. Derive the project name, slug, objective, owner, and origin mode from the user request. Origin mode is `new`, `existing-chat`, or `existing-project`. Ask only if a wrong assumption would be materially risky.
2. Create or select a local project directory. For a new project, prefer `~/Documents/<project-slug>`. For an existing project, use the existing repo/workspace path.
3. If the project already exists, load `references/existing_project_adoption.md`, inspect current files and git state, and preserve existing code/docs/history.
4. Run `scripts/scaffold_private_ai_project.py` to create missing memory structure:
   - New project: `python3 scripts/scaffold_private_ai_project.py --path <path> --name "<name>" --objective "<objective>" --origin-mode new`
   - Existing repo/project: `python3 scripts/scaffold_private_ai_project.py --path <path> --name "<name>" --objective "<objective>" --origin-mode existing-project --source-summary "<existing context used>"`
   - Existing chat: `python3 scripts/scaffold_private_ai_project.py --path <path> --name "<name>" --objective "<objective>" --origin-mode existing-chat --source-summary "<chat context imported>"`
5. For existing projects, update generated docs from existing repo/chat context instead of leaving generic placeholders. Do not overwrite existing files casually; append README project-memory section when needed.
6. Fill the generated docs with the user's exact intent, working norms, constraints, open questions, source-of-truth manifest, validation expectations, adoption notes, and next-action plan.
   - Keep `README.md` clear enough for technical contributors and strong enough to explain the project externally: overview, value proposition, target audience, technical overview, status, and privacy.
   - Keep `AGENTS.md` as the canonical portable agent entry point.
   - Keep `CLAUDE.md`, `.cursor/rules/project.mdc`, and `.github/copilot-instructions.md` as thin adapters that defer to `AGENTS.md`.
   - Keep `ai-project.yaml` current with repo URL, local path, active status, next task, read order, privacy policy, validation commands, and freshness date.
   - Keep `docs/06_memory_freshness.md` current with refresh triggers and the last meaningful memory review.
   - Keep `docs/07_ai_orchestration_source_of_truth.md` current with master/specialist roles, approval gates, bounded dispatch, Lead + Issue Worker + CI Gate rules, definition of done, specialist output format, and project-spawn flow.
   - If the project uses Google Stitch, keep `source_of_truth/stitch-map.md` current with exactly one `CURRENT` version per screen/flow, archived candidates, parent/new screen IDs, prompt used, timestamp, and accepted DESIGN.md/token changes.
   - If the user mentions other AI systems, specialist chats, GitHub links with AI instructions, or triads, load `references/cross_ai_orchestration.md` and fill `docs/04_cross_ai_orchestration.md`.
   - If the user describes a master playground, persistent specialists, or async multi-thread work, load `references/ai_orchestration_source_of_truth.md` and apply those rules.
7. Initialize git if needed. For existing repos, keep existing history and inspect status before staging. Stage only intended project/adoption files.
8. Create or verify private GitHub repo and push:
   - Use `gh repo create <owner>/<repo> --private --source=. --remote=origin --push` for new repos.
   - If the repo already exists, verify `isPrivate=true` before pushing.
   - If an existing remote is public and the user did not explicitly ask for public, stop and ask before pushing.
   - Run `python3 scripts/ai_project_check.py` before pushing when the generated project has the checker.
9. Update `docs/02_session_handoff_prompt.md`, `ai-project.yaml`, `docs/03_validation.md`, and `docs/06_memory_freshness.md` after the first push if the repo URL, privacy status, validation result, or next task changed.
10. If the user wants a follow-up AI session on this project, keep `docs/02_session_handoff_prompt.md` current. Opening the project folder in Claude Code (or another coding agent) and reading that file is the handoff step — no separate registration mechanic is required.
11. End with the repo URL, commit hash, privacy confirmation, key files, adoption mode, handoff status, and any blocked items.

## Required Project Memory

Every bootstrapped project should contain:

- `README.md`: explanatory project README for both technical onboarding and marketing/product positioning. It should include overview, value proposition, audience, technical overview, status, project memory/read order, privacy, and next steps.
- `AGENTS.md`: canonical portable agent instruction file for Claude Code and other coding agents.
- `CLAUDE.md`: Claude adapter that delegates to `AGENTS.md`.
- `.cursor/rules/project.mdc`: Cursor rule adapter that delegates to `AGENTS.md`.
- `.github/copilot-instructions.md`: GitHub Copilot adapter that delegates to `AGENTS.md`.
- `ai-project.yaml`: machine-readable manifest for project state, read order, privacy, validation commands, freshness, compatibility adapters, and cross-AI registry location.
- `docs/00_project_brief.md`: objective, scope, deliverables, assumptions, constraints.
- `docs/01_ai_operating_model.md`: how the user wants AI to work in this project.
- `docs/02_session_handoff_prompt.md`: prompt to start the next AI session.
- `docs/03_validation.md`: commands, checks, and last-known validation state.
- `docs/04_cross_ai_orchestration.md`: registry and dispatch protocol for specialist AI systems, external AI repos, project-scoped chats, and triads.
- `docs/05_project_adoption.md`: origin mode, existing context used, detected repo state, preservation rules, and adoption checklist.
- `docs/06_memory_freshness.md`: when and how to refresh project memory so future AI sessions do not operate from stale context.
- `docs/07_ai_orchestration_source_of_truth.md`: master/specialist orchestration doctrine, approval gates, bounded task format, Lead + Issue Worker + CI Gate rules, definition of done, specialist output contract, and project-spawn flow.
- `knowledge/README_FOR_AI.md`: read-first context for future AI sessions.
- `source_of_truth/README.md`: manifest for durable source files, screenshots, PDFs, data, or references.
- `source_of_truth/`: the actual durable source files.
- `source_of_truth/stitch-map.md`: generated tracking file for Google Stitch projects; use it only when Stitch is part of the workflow.
- `scripts/ai_project_check.py`: generated project checker for required files, manifest structure, stale memory, common secret patterns, and GitHub remote privacy.
- `work/README.md`: guidance for temporary working notes that should not replace durable docs.
- `.gitignore`: excludes temp files and local-only artifacts.

## Master AI User Protocol

Load `references/master_ai_user_protocol.md` when the project needs deeper operating guidance or the user asks how to work better with AI.

In short:

- Convert vague intent into a durable repo, not a disposable chat.
- Separate instructions, source-of-truth, working notes, and generated artifacts.
- Ask AI for strategy, implementation, verification, and handoff as separate passes.
- Keep high-value context in files so future sessions do not depend on chat memory.
- Commit meaningful checkpoints to private GitHub.

## Private GitHub Policy

Load `references/private_github_policy.md` before publishing or changing remotes.

Never create a public repo unless the user explicitly says public. If an existing repo is public and the user did not explicitly request public visibility, stop and ask before pushing sensitive work.

## Existing Project Adoption

Load `references/existing_project_adoption.md` when the user says the project/chat already exists, was started earlier, has an existing folder/repo, or should be brought into this workflow retroactively.

For existing projects, the job is not to recreate the project. The job is to inspect the current state, preserve prior work, add missing memory files, fill those files from existing context, verify private GitHub continuity, and leave a future AI session with a clean read order.

## Session Handoff

Keep `docs/02_session_handoff_prompt.md` current whenever the project state changes meaningfully.

Opening the project folder in Claude Code (or another coding agent) and reading that file is the handoff step. There is no separate project-registration mechanic to run first — the project folder itself is the durable unit.

## Cross-AI Orchestration

Load `references/cross_ai_orchestration.md` when the user wants this project to coordinate with another AI system, an external AI memory repo, a specialist chat, or a triad.

Treat external AI systems as project dependencies. Record their names, roles, GitHub/source URLs, read order, dispatch prompts, expected outputs, return paths, and privacy expectations in `docs/04_cross_ai_orchestration.md`. When dispatching work, create bounded prompts and project-scoped threads when possible, then bring durable outputs back into this repo.

## AI Design Tool Discipline

When Google Stitch or similar AI design tools are used, treat generated screens as candidates. Do not infer the current design from canvas placement, generation order, or a vague "latest" label. Keep `source_of_truth/stitch-map.md` as the durable screen/version registry, use `DESIGN.md` or design-token docs for accepted visual rules, and tell MCP-driven agents to reuse the recorded project and screen IDs unless the user explicitly asks for a new project.

For Stitch model selection, choose the highest available usable model by default. In practice, this means Pro unless the available tool names differ. Use Flash only when the user explicitly says to use Flash for Google Stitch. Do not infer Flash from words like MVP, prototype, quick, draft, cheap, or low importance.

## AI Orchestration Source Of Truth

Load `references/ai_orchestration_source_of_truth.md` when the user mentions master orchestration, persistent specialist threads, temporary subagents, async multi-thread work, YouTube/video pipelines, approval gates, or wants to preserve global AI operating rules.

If a master playground repo exists, write the global doctrine there as source of truth. Also copy the applicable project-local rules into `docs/07_ai_orchestration_source_of_truth.md` so the bootstrapped project remains self-contained.

## Validation

Before final response:

- If modifying this skill, run `python3 scripts/quick_validate.py` and a scaffold smoke test.
- Confirm `git status --short --branch` is clean after push.
- Confirm GitHub repo exists and `isPrivate=true`.
- Confirm the handoff prompt and `knowledge/README_FOR_AI.md` exist.
- Confirm `source_of_truth/README.md` and `docs/03_validation.md` exist.
- Confirm `docs/04_cross_ai_orchestration.md` exists and contains any user-provided external AI source links or triad rules.
- Confirm `docs/05_project_adoption.md` exists and records whether this was `new`, `existing-chat`, or `existing-project`.
- Confirm `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/project.mdc`, `.github/copilot-instructions.md`, and `ai-project.yaml` exist.
- Confirm `docs/06_memory_freshness.md` exists and reflects the latest meaningful memory review.
- Confirm `docs/07_ai_orchestration_source_of_truth.md` exists when orchestration rules are relevant.
- Run `python3 scripts/ai_project_check.py` inside generated projects before push or handoff when available.
- Confirm no obvious secrets, tokens, or unrelated files were committed.
- Report any official tool limitation plainly.

## Skill Maintenance Smoke Test

When changing the scaffold script or this skill's workflow, create a temporary project and validate it:

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

existing="$tmpdir/existing-project"
mkdir -p "$existing"
printf '# Existing App\n\nPre-existing README.\n' > "$existing/README.md"
git -C "$existing" init
python3 scripts/scaffold_private_ai_project.py \
  --path "$existing" \
  --name "Existing Project" \
  --objective "Adopt an existing repo into the private AI project workflow." \
  --origin-mode existing-project \
  --source-summary "Existing README and git repo were present before adoption." \
  --next-task "Review adoption notes and commit private project memory."
python3 scripts/quick_validate.py --scaffold-output "$existing"
python3 "$existing/scripts/ai_project_check.py"
```
