#!/usr/bin/env python3
"""Quick quality gate for the bootstrap-private-ai-project skill."""

from __future__ import annotations

import argparse
import pathlib
import py_compile
import sys


REQUIRED_SKILL_FILES = [
    "README.md",
    "SKILL.md",
    "references/master_ai_user_protocol.md",
    "references/private_github_policy.md",
    "references/cross_ai_orchestration.md",
    "references/ai_orchestration_source_of_truth.md",
    "references/existing_project_adoption.md",
    "scripts/scaffold_private_ai_project.py",
]

REQUIRED_PROJECT_FILES = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    ".cursor/rules/project.mdc",
    ".github/copilot-instructions.md",
    "ai-project.yaml",
    "docs/00_project_brief.md",
    "docs/01_ai_operating_model.md",
    "docs/02_session_handoff_prompt.md",
    "docs/03_validation.md",
    "docs/04_cross_ai_orchestration.md",
    "docs/05_project_adoption.md",
    "docs/06_memory_freshness.md",
    "docs/07_ai_orchestration_source_of_truth.md",
    "knowledge/README_FOR_AI.md",
    "source_of_truth/README.md",
    "scripts/ai_project_check.py",
    "work/README.md",
    ".gitignore",
]

README_REQUIRED_SECTIONS = [
    "## Overview",
    "## Value Proposition",
    "## Who It Is For",
    "## Technical Overview",
    "## Status",
    "## Project Memory",
    "## Next Steps",
]


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_skill(root: pathlib.Path, errors: list[str]) -> None:
    for relative in REQUIRED_SKILL_FILES:
        require((root / relative).is_file(), f"missing skill file: {relative}", errors)

    skill_md = read(root / "SKILL.md")
    skill_lower = skill_md.lower()
    require(
        "private by default" in skill_lower or "private-by-default" in skill_lower,
        "SKILL.md must preserve private-by-default policy",
        errors,
    )
    require("master AI operator" in skill_md, "SKILL.md must encode master AI operator style", errors)
    require("scripts/scaffold_private_ai_project.py" in skill_md, "SKILL.md must point to scaffold script", errors)
    require("quick_validate.py" in skill_md, "SKILL.md must mention the quick validation gate", errors)
    require("marketing/product positioning" in skill_md, "SKILL.md must require marketing-supportive README positioning", errors)
    require("existing-project" in skill_md, "SKILL.md must support existing-project adoption mode", errors)
    require("existing-chat" in skill_md, "SKILL.md must support existing-chat conversion mode", errors)
    require("references/existing_project_adoption.md" in skill_md, "SKILL.md must point to existing project adoption reference", errors)
    require("cross-AI orchestration" in skill_md, "SKILL.md must require cross-AI orchestration handling", errors)
    require("docs/04_cross_ai_orchestration.md" in skill_md, "SKILL.md must require project cross-AI orchestration memory", errors)
    require("docs/05_project_adoption.md" in skill_md, "SKILL.md must require project adoption memory", errors)
    require("docs/06_memory_freshness.md" in skill_md, "SKILL.md must require memory freshness tracking", errors)
    require("docs/07_ai_orchestration_source_of_truth.md" in skill_md, "SKILL.md must require AI orchestration source-of-truth output", errors)
    require(
        "references/ai_orchestration_source_of_truth.md" in skill_md,
        "SKILL.md must point to AI orchestration source-of-truth reference",
        errors,
    )
    require("AGENTS.md" in skill_md, "SKILL.md must require standard AGENTS.md output", errors)
    require("CLAUDE.md" in skill_md, "SKILL.md must require Claude adapter output", errors)
    require(".cursor/rules/project.mdc" in skill_md, "SKILL.md must require Cursor adapter output", errors)
    require(".github/copilot-instructions.md" in skill_md, "SKILL.md must require Copilot adapter output", errors)
    require("ai-project.yaml" in skill_md, "SKILL.md must require machine-readable ai-project.yaml manifest", errors)
    require("scripts/ai_project_check.py" in skill_md, "SKILL.md must require generated automated project checker", errors)
    require("portable" in skill_lower, "SKILL.md must describe portable agent compatibility", errors)
    require("freshness" in skill_lower, "SKILL.md must describe memory freshness", errors)

    private_policy = read(root / "references/private_github_policy.md")
    require("--private" in private_policy, "private GitHub policy must require --private for new repos", errors)
    require("isPrivate" in private_policy, "private GitHub policy must require isPrivate verification", errors)
    require("scripts/ai_project_check.py" in private_policy, "private GitHub policy must require generated project checker", errors)
    require("secret" in private_policy.lower(), "private GitHub policy must mention secret scanning", errors)
    require("stop and ask" in private_policy.lower(), "private GitHub policy must stop before public pushes", errors)

    cross_ai = read(root / "references/cross_ai_orchestration.md")
    require("AI System Registry" in cross_ai or "Registry" in cross_ai, "cross-AI reference must include a registry", errors)
    require("Dispatch Prompt Template" in cross_ai, "cross-AI reference must include a dispatch prompt template", errors)
    require("Triads" in cross_ai, "cross-AI reference must document triads", errors)
    require("private by default" in cross_ai.lower(), "cross-AI reference must preserve private-by-default policy", errors)

    orchestration = read(root / "references/ai_orchestration_source_of_truth.md")
    for expected in [
        "Durable memory beats chat memory",
        "master orchestrator",
        "persistent specialist threads",
        "Human approval gates",
        "Specialist Output Format",
        "Project Spawn Flow",
    ]:
        require(expected in orchestration, f"AI orchestration reference must include {expected}", errors)

    adoption = read(root / "references/existing_project_adoption.md")
    require("Existing Project Workflow" in adoption, "existing adoption reference must document existing project workflow", errors)
    require("Existing Chat Workflow" in adoption, "existing adoption reference must document existing chat workflow", errors)
    require("Preservation Rules" in adoption, "existing adoption reference must include preservation rules", errors)
    require("public remote" in adoption.lower(), "existing adoption reference must handle public remote blocker", errors)
    require("ai-project.yaml" in adoption, "existing adoption reference must mention manifest adoption", errors)
    require("AGENTS.md" in adoption, "existing adoption reference must mention AGENTS adoption", errors)

    scaffold = root / "scripts/scaffold_private_ai_project.py"
    py_compile.compile(str(scaffold), doraise=True)
    scaffold_text = read(scaffold)
    for expected in REQUIRED_PROJECT_FILES:
        parts = [part for part in pathlib.PurePosixPath(expected).parts if part != "."]
        require(all(part in scaffold_text for part in parts), f"scaffold script must create or reference {expected}", errors)
    for section in README_REQUIRED_SECTIONS:
        require(section in scaffold_text, f"scaffold README template must include {section}", errors)
    require("--next-task" in scaffold_text, "scaffold script must support concrete next-task handoff", errors)
    require("--origin-mode" in scaffold_text, "scaffold script must support origin-mode", errors)
    require("--source-summary" in scaffold_text, "scaffold script must support source-summary", errors)
    require("append_readme_memory_for_existing" in scaffold_text, "scaffold script must preserve existing README with appended memory", errors)
    require("gh repo view" in scaffold_text, "scaffold script must generate GitHub privacy verification", errors)
    require("SECRET_PATTERNS" in scaffold_text, "scaffold script must generate secret scanning", errors)
    require("stale_after_days" in scaffold_text, "scaffold script must generate freshness automation", errors)


def validate_project(project: pathlib.Path, errors: list[str]) -> None:
    for relative in REQUIRED_PROJECT_FILES:
        require((project / relative).is_file(), f"missing scaffold output: {relative}", errors)

    if not (project / "README.md").is_file():
        return

    checker = project / "scripts" / "ai_project_check.py"
    if checker.is_file():
        py_compile.compile(str(checker), doraise=True)

    combined = "\n".join(read(project / relative) for relative in REQUIRED_PROJECT_FILES if (project / relative).is_file())
    readme = read(project / "README.md")
    for section in README_REQUIRED_SECTIONS:
        require(section in readme, f"README.md must include {section}", errors)
    require("value proposition" in readme.lower(), "README.md must support marketing/product positioning", errors)
    require("Technical Overview" in readme, "README.md must support technical onboarding", errors)
    require("private by default" in combined.lower(), "scaffold output must preserve private-by-default policy", errors)
    require("AGENTS.md" in combined, "scaffold output must include AGENTS.md read order", errors)
    require("CLAUDE.md" in combined, "scaffold output must include Claude adapter", errors)
    require(".cursor/rules/project.mdc" in combined, "scaffold output must include Cursor adapter", errors)
    require(".github/copilot-instructions.md" in combined, "scaffold output must include Copilot adapter", errors)
    require("ai-project.yaml" in combined, "scaffold output must include ai-project.yaml manifest", errors)
    require("scripts/ai_project_check.py" in combined, "scaffold output must include automated checker references", errors)
    require("master AI operator" in combined, "scaffold output must preserve master AI operator style", errors)
    require("docs/03_validation.md" in combined, "scaffold output must include validation in read order", errors)
    require("docs/04_cross_ai_orchestration.md" in combined, "scaffold output must include cross-AI orchestration in read order", errors)
    require("docs/05_project_adoption.md" in combined, "scaffold output must include project adoption in read order", errors)
    require("docs/06_memory_freshness.md" in combined, "scaffold output must include memory freshness in read order", errors)
    require(
        "docs/07_ai_orchestration_source_of_truth.md" in combined,
        "scaffold output must include AI orchestration source-of-truth in read order",
        errors,
    )
    require("source_of_truth/README.md" in combined, "scaffold output must include source-of-truth manifest", errors)

    agents = read(project / "AGENTS.md")
    require("ai-project.yaml" in agents, "AGENTS.md must point to ai-project.yaml", errors)
    require("python3 scripts/ai_project_check.py" in agents, "AGENTS.md must require automated project checks", errors)
    require("Private by default" in agents or "private by default" in agents.lower(), "AGENTS.md must preserve private policy", errors)

    manifest = read(project / "ai-project.yaml")
    for expected in [
        "version:",
        "project:",
        "privacy:",
        "public_allowed: false",
        "require_private_remote_verification: true",
        "memory:",
        "read_order:",
        "freshness:",
        "last_reviewed:",
        "stale_after_days:",
        "validation:",
        "compatibility:",
        "cross_ai:",
    ]:
        require(expected in manifest, f"ai-project.yaml must include {expected}", errors)

    for relative in ["CLAUDE.md", ".cursor/rules/project.mdc", ".github/copilot-instructions.md"]:
        require("AGENTS.md" in read(project / relative), f"{relative} must delegate to AGENTS.md", errors)

    checker_text = read(project / "scripts" / "ai_project_check.py") if checker.is_file() else ""
    require("gh repo view" in checker_text, "ai_project_check.py must verify GitHub privacy with gh", errors)
    require("SECRET_PATTERNS" in checker_text, "ai_project_check.py must include secret scanning", errors)
    require("public GitHub remote blocked" in checker_text, "ai_project_check.py must block public remotes", errors)
    require("project memory is stale" in checker_text, "ai_project_check.py must fail stale memory dates", errors)

    require("AI System Registry" in read(project / "docs/04_cross_ai_orchestration.md"), "cross-AI project doc must include AI System Registry", errors)
    require("Dispatch Prompt Template" in read(project / "docs/04_cross_ai_orchestration.md"), "cross-AI project doc must include dispatch prompt template", errors)
    require("Triads" in read(project / "docs/04_cross_ai_orchestration.md"), "cross-AI project doc must include triads", errors)
    freshness_doc = read(project / "docs" / "06_memory_freshness.md")
    require("Refresh Triggers" in freshness_doc, "memory freshness doc must include refresh triggers", errors)
    require("scripts/ai_project_check.py" in freshness_doc, "memory freshness doc must include automation command", errors)
    orchestration_doc = read(project / "docs" / "07_ai_orchestration_source_of_truth.md")
    require("Master Orchestrator" in orchestration_doc, "AI orchestration doc must include master orchestrator rules", errors)
    require("Specialist Output Format" in orchestration_doc, "AI orchestration doc must include specialist output format", errors)
    require("Project Spawn Flow" in orchestration_doc, "AI orchestration doc must include project spawn flow", errors)
    adoption_doc = read(project / "docs" / "05_project_adoption.md")
    require("Origin Mode" in adoption_doc, "project adoption doc must include origin mode", errors)
    require("Detected Repo State" in adoption_doc, "project adoption doc must include detected repo state", errors)
    require("Preservation Rules" in adoption_doc, "project adoption doc must include preservation rules", errors)
    require("First task:" in read(project / "docs/02_session_handoff_prompt.md"), "handoff prompt must include a first task", errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=pathlib.Path(__file__).resolve().parents[1], type=pathlib.Path)
    parser.add_argument("--scaffold-output", type=pathlib.Path, help="Optional generated project to validate")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    errors: list[str] = []

    validate_skill(root, errors)
    if args.scaffold_output:
        validate_project(args.scaffold_output.expanduser().resolve(), errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    target = f" and {args.scaffold_output}" if args.scaffold_output else ""
    print(f"quick validation passed for {root}{target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
