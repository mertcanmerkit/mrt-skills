# Cross-AI Orchestration

Use this reference when a project should coordinate multiple AI systems, specialist chats, or triads instead of relying on one long conversation.

## Intent

The user is a master AI operator. They may maintain separate AI systems for different specialties, such as video ideation, voice direction, text writing, editing, research, coding, or publishing. Each system can have its own GitHub-backed memory, rules, source material, and preferred workflow.

Use `references/ai_orchestration_source_of_truth.md` when master/specialist responsibilities, approval gates, project-spawn flow, or asynchronous multi-thread execution matter.

The bootstrap project should preserve enough information for future sessions to:

- find the relevant AI system repositories or documentation
- read their rules before dispatching work
- read this project's `AGENTS.md` and `ai-project.yaml` before acting
- create project-scoped follow-up chats when possible
- send the right source material and constraints to each AI
- bring outputs, decisions, and validation results back into this project repo

## Core Model

Treat external AI systems as project dependencies.

The master orchestrator owns synthesis, dispatch prompts, durable memory updates, review, and next-step coordination. Specialist systems own bounded production outputs.

Each dependency needs:

- **Name**: short identifier for the AI system or triad.
- **Role**: what this AI is trusted to do.
- **Source URL**: private GitHub repo, markdown file, or other durable source that describes the AI system.
- **Read order**: files the receiving AI must read first.
- **Dispatch prompt**: what to ask that AI to do for this project.
- **Inputs to pass**: project files, source material, briefs, constraints, or artifacts.
- **Expected outputs**: files, decisions, generated text, media, analysis, or validation notes.
- **Return path**: where outputs should be written back in this repo.
- **Privacy level**: private by default unless the user explicitly says public.

## Registry

Every bootstrapped project that uses cross-AI work should maintain `docs/04_cross_ai_orchestration.md`.

The project-specific registry should include:

| AI System | Role | Source URL | Read First | Dispatch Status | Output Location |
| --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD |

Source URLs may point to private GitHub repos. Do not assume the receiving AI has access. If access is unavailable, report the limitation and ask the user to provide the needed content or access path.

## Dispatch Workflow

1. Read the current project's memory files first.
2. Identify whether another AI system is relevant to the next task.
3. Decide whether this should use a persistent specialist thread, a project-scoped session, or a temporary same-thread worker.
4. Open the AI system's source URL or local repo documentation when available.
5. Extract only the rules, source material, and constraints needed for the task.
6. Write a dispatch prompt that includes:
   - current project repo URL and local path
   - exact task
   - source files to read, starting with `AGENTS.md` and `ai-project.yaml`
   - external AI system rules to follow
   - output format and destination
   - privacy rule: private by default
   - validation expectations
   - requirement to update or return proposed changes for `docs/06_memory_freshness.md` when outputs affect durable memory
   - escalation conditions for product direction, UX/taste, brand, public publishing, push/PR, legal/risk, paid launch, irreversible data, credentials/provider setup, and major source-of-truth changes
7. If a thread tool is available, create a project-scoped thread for the receiving AI/project when possible.
8. Store the dispatch prompt in `work/` or `docs/04_cross_ai_orchestration.md`.
9. After the external AI returns work, save durable outputs under `source_of_truth/`, `docs/`, or `artifacts/` as appropriate.
10. Update the registry with status, output location, and follow-up tasks.
11. Commit and push meaningful checkpoints to the private GitHub repo.

## Dispatch Prompt Template

```text
You are being used as a specialist AI system for a GitHub-backed private project.

Current project:
- Repo: <current-project-repo-url>
- Local path: <current-project-local-path>
- Objective: <project-objective>

Read first:
1. <current-project-AGENTS.md>
2. <current-project-ai-project.yaml>
3. <current-project-brief-or-knowledge-file>
4. <relevant-source-of-truth-files>
5. <external-ai-system-rules-url-or-file>

Your specialist role:
<role and boundaries>

Task:
<specific task>

Inputs:
<files, links, constraints, examples, style requirements>

Output:
- what was done
- files/docs touched
- decisions made
- assumptions used
- checks run
- failed or unverified items
- risks or tradeoffs
- open questions
- recommended next step
- whether anything must be written back to durable docs
- exact files, format, decision record, or artifact expected

Rules:
- Treat GitHub publishing and artifacts as private unless the user explicitly says public.
- Do not invent missing source material. Report missing access or ambiguity.
- Preserve reusable decisions in markdown, not only chat.
- Keep machine-readable state in ai-project.yaml current when your output changes project state.
- Return freshness updates for docs/06_memory_freshness.md when your output changes durable project memory.
- Stay inside the bounded task. Escalate approval-gated decisions instead of silently deciding them.
- Return enough context for the orchestrating project to update its memory files.
```

## Triads

A triad is a coordinated group of specialist AI systems working on one outcome. Use a triad only when the roles are meaningfully different.

Common triad shapes:

- **Strategy / Production / QA**: one AI defines direction, one produces the artifact, one validates.
- **Ideation / Script / Voice**: one AI develops the idea, one writes the text, one adapts it for voice or delivery.
- **Research / Implementation / Review**: one AI gathers trusted context, one implements, one audits risks and tests.

For triads, define:

- lead orchestrator
- specialist roles
- handoff order
- shared source-of-truth files
- merge rule for conflicting outputs
- final validation owner

## Guardrails

- Do not copy sensitive private repo content into public systems.
- Do not create public repos or public artifacts unless the user explicitly says public.
- Do not let an external AI's chat memory become the only source of truth.
- Do not dispatch vague tasks. Give each AI a bounded output contract.
- Do not treat external AI output as verified until it is reviewed, tested, or reconciled into this repo.
- Prefer private GitHub links and project files over long pasted chat transcripts.

## What To Preserve

When a useful AI chat happens elsewhere, convert it into durable memory:

- `docs/` for decisions, process, handoff prompts, and operating rules
- `source_of_truth/` for trusted inputs, transcripts, source exports, and examples
- `artifacts/` for generated deliverables
- `work/` for temporary dispatch prompts, scratch notes, and intermediate analysis

The goal is not to archive everything. The goal is to preserve the reusable intelligence that lets the next AI session work at the same level without rediscovering the context.
