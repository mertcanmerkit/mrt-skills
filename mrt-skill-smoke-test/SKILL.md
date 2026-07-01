---
name: mrt-skill-smoke-test
description: Smoke test a Claude Code skill or SKILL.md to check whether it is structurally valid and behaviorally usable in a minimal realistic scenario. Use when the user asks to test a skill, smoke test a skill, validate whether a SKILL.md works, evaluate a newly created skill, or perform agent-instruction QA for Claude Code skills.
---

# Skill Smoke Test

## Goal

Test whether a skill can actually be used by another agent, not only whether the files exist.

This is not a unit test for code. It is a smoke test for agent behavior:

- Does the skill trigger for the intended request?
- Is `SKILL.md` valid and free of obvious placeholders?
- Are its instructions actionable?
- Do bundled scripts/resources exist and run in at least one safe path?
- Can an agent complete one minimal realistic task using the skill?

## Workflow

1. Read the target skill's `SKILL.md` completely.
2. Run the bundled probe:

```bash
~/.claude/skills/mrt-skill-smoke-test/scripts/skill_smoke_probe.py /absolute/path/to/skill --markdown
```

If the system validator exists, pass it too:

```bash
~/.claude/skills/mrt-skill-smoke-test/scripts/skill_smoke_probe.py /absolute/path/to/skill --validator /path/to/quick_validate.py --markdown
```

3. Identify the smallest realistic task the skill claims to support.
4. Execute one safe representative path:
   - Prefer dry-run, `--help`, temp files, local-only fixtures, or disposable folders.
   - Avoid production systems, secrets, paid actions, network side effects, destructive actions, and irreversible UI actions.
   - If the skill's real task needs a live external side effect, mark that part `WARN` unless the user explicitly approved the side effect.
5. Capture evidence: commands, key outputs, files created, thread ids, validation output, or screenshots when relevant.
6. Clean up disposable artifacts.
7. Report the result as `PASS`, `WARN`, or `FAIL`.

## Result Rules

Use `PASS` only when:

- Static probe has no blocking errors.
- The skill validator passes when available.
- One primary workflow path was actually exercised.
- The evidence matches the expected behavior.

Use `WARN` when:

- The skill is structurally valid, but a full behavior test needs unavailable credentials, UI access, network side effects, or user approval.
- A cleanup limitation remains but the core skill behavior worked.

Use `FAIL` when:

- `SKILL.md` is missing or invalid.
- Frontmatter is missing required fields.
- Instructions still contain TODO placeholders.
- The claimed main workflow cannot be executed or is internally contradictory.
- Bundled scripts required by the workflow fail on a safe minimal input.

## Smoke Scenario Design

Derive the smoke scenario from the skill's own frontmatter description and body. Do not invent a task unrelated to the skill.

Good smoke scenarios:

- A PDF skill rotates a tiny disposable PDF.
- A document skill creates a one-page temporary `.docx`.
- A project-opening skill registers a disposable folder and creates a project thread.
- A prompt/ticket skill transforms one short example request into the promised output format.

Bad smoke scenarios:

- Only reading the skill and saying it looks fine.
- Only running a syntax validator when the skill includes executable behavior.
- Testing with production data.
- Passing only because the test prompt leaks the expected result.

## Forward Testing

When a skill is complex enough and the environment supports separate threads/subagents, perform a forward test with minimal context:

```text
Use /target-skill-name at /absolute/path/to/skill to complete this realistic task: ...
```

Do not tell the forward tester the expected answer unless the test requires comparing against a specification. Review its output and artifacts as evidence.

## Report Template

```md
## Skill Smoke Test Result: PASS|WARN|FAIL

Target: /absolute/path/to/skill

Static checks:
- ...

Behavior check:
- Scenario:
- Evidence:
- Cleanup:

Risks / gaps:
- ...

Verdict:
- ...
```
