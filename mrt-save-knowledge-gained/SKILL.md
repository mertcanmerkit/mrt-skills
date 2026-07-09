---
name: mrt-save-knowledge-gained
description: Capture and persist the knowledge gained in a chat into related project Markdown files so future AI sessions can continue with the right product vision. Use when Mertcan says phrases like "save the knowledge gained", "knowledge gained on this chat", "save chat knowledge to MD files", "continue developing this product with proper vision", or asks to preserve useful requirements, decisions, research findings, rejected attempts, bugs, next steps, handoff prompts, or source-of-truth IDs from a current or old AI chat.
---

# Save Knowledge Gained

## Goal

Turn useful chat context into durable repo memory. The output should help a fresh AI session understand the project without rereading the full chat.

Two recurring meanings from Mertcan's prior Codex chats:

- `019ed13a-afea-7752-af21-dfd3eed622f0`: the chat output was bad, but the requirements, prompts, design direction, and answered questions were valuable. Preserve the useful brief; mark failed output as rejected.
- `019e91db-0404-7fd2-8b78-9cb4b4c5b67e`: the chat contained device/product findings, decisions, bugs, and next steps that must be saved into MD files so a fresh session can continue.

Use those IDs as semantic anchors. Do not open them unless the user explicitly asks or the current task needs old-chat evidence.

## Defaults

- Treat this as memory/documentation work, not feature implementation.
- Edit Markdown/source-of-truth files only unless the user explicitly asks for code changes.
- Preserve exact names, URLs, file paths, chat IDs, Stitch IDs, commands, errors, and user wording when they matter.
- Do not dump the transcript. Extract durable knowledge: decisions, requirements, constraints, research findings, rejected paths, known bugs, validation state, and next actions.
- Mark rejected or failed work clearly. Do not let a bad implementation become accepted project truth.
- Prefer existing read-order docs over creating scattered new files.
- Keep private GitHub as the default when committing or pushing project memory.

## Workflow

1. Resolve the target.
   - Use the current repo/workspace when obvious.
   - If the user names old chat IDs, inspect those chat logs when available.
   - If the target repo is unclear and a wrong choice could pollute another product's memory, ask one concise question.

2. Inspect current memory structure before writing.
   - Check `git status -sb`.
   - Look for `AGENTS.md`, `CLAUDE.md`, `README.md`, `ai-project.yaml`, `knowledge/`, `docs/`, `source_of_truth/`, and existing handoff or freshness docs.
   - If the project is not yet a durable AI project and `mrt-bootstrap-private-ai-project` is available, use it or follow its read-order conventions.

3. Extract knowledge into a compact working outline.
   - Product vision and target user.
   - Locked decisions and why they matter.
   - Requirements, UX rules, design direction, and accepted assets/IDs.
   - Research findings and source links.
   - Failed/rejected attempts and why they were rejected.
   - Known bugs, risks, open questions, and validation status.
   - Next-session prompt or next concrete tasks.

4. Write to the right docs.
   - `knowledge/README_FOR_AI.md`: read-first summary for future agents.
   - `docs/00_project_brief.md`: product vision, audience, scope, constraints.
   - `docs/02_session_handoff_prompt.md`: exact prompt for the next AI session.
   - `docs/05_project_adoption.md`: old chat IDs, imported context, preservation notes.
   - `docs/06_memory_freshness.md`: latest memory refresh date and trigger.
   - `source_of_truth/README.md`: durable source files, screenshots, URLs, IDs.
   - `source_of_truth/stitch-map.md`: accepted Stitch project/screen IDs when design tools are involved.
   - `README.md`: only high-level status/read-order links, not dense chat notes.
   - `AGENTS.md` or `CLAUDE.md`: only stable operating rules, not one-off facts.

5. Keep the docs usable.
   - Write in concise sections with explicit headings.
   - Separate "Accepted" from "Rejected".
   - Include dates for memory refreshes.
   - Add a short "Read order for next AI session" when missing.
   - Remove or update stale statements contradicted by the new knowledge.

6. Validate before finishing.
   - Review `git diff` and confirm only intended memory files changed.
   - Run `python3 scripts/ai_project_check.py` if present.
   - Run project-specific docs/validation checks if documented.
   - Search changed files for obvious secrets before commit or push.
   - If pushing, verify the GitHub repo is private unless Mertcan explicitly asked for public.

## Output Shape

End with:

- files updated
- what knowledge was preserved
- what was marked rejected/stale
- validation run
- commit/push status when requested
