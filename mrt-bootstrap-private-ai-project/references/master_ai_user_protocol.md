# Master AI User Protocol

Use this protocol when bootstrapping a serious AI project.

## Operating Principles

- **Project over chat**: Durable work belongs in a repo with memory files, not only in a conversation.
- **Source-of-truth first**: Store PDFs, screenshots, datasets, source manifests, prompts, and user constraints under version control.
- **Context is an asset**: Future AI sessions should be able to reconstruct the project from files.
- **Adopt before rebuilding**: When a chat, repo, or existing project already exists, preserve it and add missing memory files instead of starting over.
- **README carries the story**: Every project needs an explanatory README that supports both technical onboarding and marketing/product positioning.
- **AI systems are dependencies**: When the user works across multiple AI chats, specialist systems, or triads, store their source URLs, roles, dispatch rules, and outputs in the project repo.
- **Master orchestrates, specialists execute**: Use the master thread for synthesis, dispatch prompts, memory updates, specialist review, gap identification, and next-step coordination. Use specialist threads for bounded production work.
- **Bounded work beats mega-prompts**: Split large asks into tasks with source docs, scope, non-goals, acceptance criteria, checks, expected output, and escalation conditions.
- **Approval gates matter**: Ask before product direction, UX/taste, brand, public publishing, push/PR, legal/risk, paid launch, irreversible data, credential/provider, or major source-of-truth changes unless already approved.
- **Private by default**: Publish to private GitHub unless the user explicitly requests public visibility.
- **Design inputs are not production truth**: Figma, mockups, screenshots, and competitor references are inputs. Production truth lives in repo docs, accepted decisions, component contracts, code, tests, and screenshot review.
- **Stitch needs a registry**: When Google Stitch is used, track project IDs, screen IDs, current versions, archived candidates, prompts, and handoff status in `source_of_truth/stitch-map.md`. Do not trust canvas position or a vague "latest" label as the current design.
- **Stitch model default is Pro**: Use the highest available usable Stitch model by default. Use Flash only when the user explicitly says to use Flash for Google Stitch; do not infer Flash from MVP or prototype wording.
- **Executable over aspirational**: Prefer scripts, checklists, and validation commands over prose-only intentions.
- **Handoff stays current**: Update the handoff prompt after meaningful decisions, repo changes, or next-task changes.

## How to Talk to the User

- Treat the user as a master AI operator.
- Be direct about tradeoffs, uncertainty, and tool limits.
- Share pragmatic AI-use improvements when they are relevant to the task.
- Keep the user oriented around leverage: what should become a file, a repo, a script, a skill, a test, or a reusable prompt.
- When the user is starting serious work in ordinary chat, recommend moving durable context into the repo before implementation details sprawl.

## Recommended Project Loop

1. Capture the real objective and decision context.
2. Decide whether this is `new`, `existing-chat`, or `existing-project`.
3. Create or adopt the project repo and memory structure.
4. Write a README with overview, value proposition, target audience, technical overview, status, project memory, privacy, and next steps.
5. For existing projects/chats, fill `docs/05_project_adoption.md` with what was adopted, detected repo state, and preservation rules.
6. Save source-of-truth artifacts.
7. Record source artifacts in `source_of_truth/README.md`.
8. If cross-AI work is relevant, fill `docs/04_cross_ai_orchestration.md` with AI system links, triad roles, dispatch prompts, and return paths.
9. If master/specialist orchestration is relevant, fill `docs/07_ai_orchestration_source_of_truth.md` with routing rules, approval gates, definition of done, and specialist output format.
10. Convert the user prompt into a handoff prompt for future sessions.
11. Implement the first useful slice.
12. Verify behavior with commands, screenshots, or tests.
13. Commit and push to private GitHub.
14. Write the next-session instructions.

## Quality Bar

The setup is not complete until another AI session can open the repo, read `knowledge/README_FOR_AI.md`, and understand:

- what the project is
- why the project matters and who it is for
- what the user wants
- what has already been decided
- whether the project was created new, adopted from chat, or adopted from an existing repo
- what source material is trusted
- which external AI systems or triads are relevant
- where master orchestration ends and specialist production begins
- what approval gates and definition-of-done rules apply
- what work should happen next
- what validation has been run
- how private publishing should be handled
