# AI Orchestration Source Of Truth

Use this reference when a project needs master/specialist orchestration rules, bounded dispatch, approval gates, or multi-thread execution.

## Placement Rule

Store global orchestration doctrine in the user's master AI control-plane repo when one exists (for example, a personal AI playground/registry repo).

Also copy the applicable project-local rules into each bootstrapped project so the project remains usable when the playground is not in context.

## Operating Principles

- Durable memory beats chat memory. Important decisions must be distilled into canonical repo docs.
- Living docs describe current truth. Historical decisions belong in a decision log with status such as accepted, superseded, rejected, or needs founder confirmation.
- If context compaction happened or older context is unavailable, say so. Do not claim full coverage.
- The master orchestrator synthesizes, writes prompts, updates durable memory, reviews specialist outputs, identifies gaps, and coordinates next steps.
- The master does not do specialist production work unless explicitly asked.
- Use persistent specialist threads for serious recurring specialties such as design, coding, research, legal/risk, marketing, voice, video, and thumbnail work.
- Use temporary same-thread subagents only for bounded parallel analysis or execution inside a specialist thread.
- Correct flow: master creates prompt, specialist thread executes, specialist returns output, master synthesizes, durable docs are updated.
- Avoid mega prompts and uncontrolled autonomy. Split work into bounded tasks with goal, scope, non-goals, source docs, acceptance criteria, checks, output format, and escalation conditions.
- Human approval gates matter for product direction, UX/taste, brand direction, public publishing, push/PR creation when not already approved, legal/platform risk, paid/public launch assumptions, irreversible data changes, credentials/provider setup, and major source-of-truth changes.
- Private GitHub is the default durable backup and source-control layer.
- Isolate experiments in a branch or separate folder. Do not merge experiments wholesale; cherry-pick useful pieces after review.
- Automations are scheduled heartbeats, not completion events. Use them for reminders, status checks, recurring review, or careful continuation of a known thread.
- Design tools and competitor references are inputs, not truth. Production truth lives in repo docs, accepted decisions, tokens, component contracts, coded implementation, tests, and screenshot review.
- Competitor screenshots are inspiration only. Extract UX principles; do not copy exact UI, branding, colors, typography, icons, wording, layout, trade dress, or product identity.

## Google Stitch Discipline

Use Google Stitch as a controlled exploration and handoff tool, not as the source of truth for the accepted design.

- Do not infer the current screen from canvas position, generation order, or a vague "latest" label.
- Keep the durable Stitch registry in `source_of_truth/stitch-map.md` when a project uses Stitch.
- Record project IDs, screen/resource IDs, parent screen, generated screen, version label, timestamp, prompt used, and status.
- Maintain exactly one `CURRENT` Stitch version per screen or flow. Mark older useful versions as `ARCHIVE`, unaccepted outputs as `CANDIDATE`, and rejected outputs as `REJECTED`.
- Tell MCP-driven agents to reuse recorded project and screen IDs unless the user explicitly says `NEW PROJECT`.
- Use the highest available usable Stitch model by default, practically Pro. Use Flash only when the user explicitly says to use Flash for Google Stitch.
- Do not infer Flash from project labels such as MVP, prototype, quick draft, early version, cheap, or low importance.
- Keep prompts focused on one screen/component and one or two changes.
- Distill accepted changes into `DESIGN.md`, design tokens, component contracts, docs, or code before treating them as production truth.
- If Stitch listing tools disagree with known resource IDs, trust the recorded IDs until manually verified.

## Preferred UI Workflow

Use this progression for product UI:

1. Product docs and information architecture.
2. Visual direction references.
3. Prototype contract.
4. UI tokens and components.
5. Fake-data coded prototype.
6. Screenshot review.
7. Approved pieces promoted to production structure.
8. Prototype-only routes deleted or isolated.
9. Real logic implemented as separate tasks.

A coded prototype must not silently become production logic. Fake data and prototype routes must be clearly isolated.

## Production Coding Workflow

Production coding must use the `Lead + Issue Worker + CI Gate` flow for serious product work:

1. Master chooses priority, protected gates, and durable memory updates.
2. Platform lead decomposes work into GitHub Issues, sizes/splits issues, reviews architecture, reviews PRs, and interprets CI.
3. Issue worker owns exactly one GitHub Issue, one branch, one PR, and bounded checks.
4. GitHub Actions or the project's CI is the objective merge gate.
5. Master synthesizes the accepted result and updates source-of-truth docs.

Do not let a master thread or one broad "backend dev", "web dev", or "core dev" thread sequentially implement an entire platform queue. A platform specialist can lead and review, but production implementation should be routed through issue-scoped workers.

Cross-platform issues must be split before implementation when they cannot stay small and reviewable.

### Controlled Parallel Issue Workers

Parallel issue workers are allowed only when the lead can name the dependency boundary and file-conflict boundary before dispatch.

Default concurrency cap:

- maximum 2 implementation workers at the same time
- maximum 1 additional research, planning, or gate worker

Rules:

- Master/lead owns the dependency map before dispatch.
- Workers do not self-select parallel work.
- No two implementation workers should edit the same API contract, migration, route group, major UI surface, or shared package at the same time unless one explicitly stacks on the other.
- CI green is not enough; merge order must respect dependencies.
- Dependent branches must rebase after upstream merges.
- If conflict risk is unclear, default to sequential work.

Each task should include:

- source docs to read
- GitHub Issue number and branch name
- exact scope
- domain/API contracts
- acceptance criteria
- tests
- lint/type/build checks
- migration/data safety notes
- screenshot review when UI is involved
- docs updates when behavior changes

A task is complete only when the PR checks pass, the lead review is satisfied, and the relevant durable docs are updated.

## Definition Of Done

Before calling work done, verify:

- relevant tests pass
- lint/type/build checks pass
- responsive behavior is checked for UI
- accessibility basics are checked
- screenshots are reviewed when UI is involved
- docs are updated when durable behavior or decisions changed
- known risks are recorded
- git state is clear and explainable

## Specialist Output Format

Every specialist output should include:

- what was done
- what files/docs were touched
- what decisions were made
- what assumptions were used
- what checks were run
- what failed or remains unverified
- risks or tradeoffs
- open questions
- recommended next step
- whether anything must be written back to durable docs

## Master Final Responsibility

The master keeps the system coherent:

- prevent scope explosion
- prevent conflicting sources of truth
- ensure important conclusions enter durable docs
- compare specialist outputs
- challenge weak assumptions
- create clean prompts for the next specialist
- avoid letting raw chat become product memory

Optimize for durable clarity, not for doing the most work in one chat.

## Project Spawn Flow From A Master Playground

When a high-level request starts in a master playground and should become a serious project:

1. Preserve the initial chat/request as source material in the new project.
2. Create or adopt a new local project folder.
3. Create a new private GitHub repo.
4. Register the folder with the coding agent's own project mechanism, if it has one (e.g. Codex Desktop Projects).
5. Create a project-scoped master thread with a proper title.
6. Write a plan and ask the user whether to implement or revise before launching specialist execution, unless the user already explicitly approved implementation.
7. After approval, execute from the new project-scoped master thread.
8. Dispatch bounded work to persistent specialist threads or project-scoped specialist chats.
9. Run work asynchronously where tool support allows, but keep outputs bounded and reconciled.
10. Bring specialist outputs back into the project repo, update durable docs, validate, and report final paths.

For a YouTube video production request, typical specialist tracks are idea/script, visual storyboard/slides, voice, Remotion/video assembly, thumbnail, and QA.
