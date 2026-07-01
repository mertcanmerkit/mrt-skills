#!/usr/bin/env python3
"""Create a durable private-AI-project memory scaffold."""

from __future__ import annotations

import argparse
from datetime import date
import pathlib
import re
import shlex
import subprocess
from textwrap import dedent


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "private-ai-project"


def write_if_missing(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def append_if_missing(path: pathlib.Path, marker: str, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker in existing:
        return False
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + "\n" + dedent(content).strip() + "\n", encoding="utf-8")
    return True


def update_exact_placeholder(path: pathlib.Path, before: str, after: str) -> None:
    if not path.exists() or before == after:
        return
    content = path.read_text(encoding="utf-8")
    if before in content:
        path.write_text(content.replace(before, after), encoding="utf-8")


def run_git(project_path: pathlib.Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(project_path), *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return "git unavailable"
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def collect_existing_snapshot(project_path: pathlib.Path) -> dict[str, object]:
    ignored = {".git", "node_modules", "vendor", "__pycache__", ".venv", "tmp", "dist", "build"}
    top_level = []
    docs = []
    if project_path.exists():
        for child in sorted(project_path.iterdir(), key=lambda item: item.name.lower()):
            if child.name in ignored or child.name.startswith(".DS_Store"):
                continue
            top_level.append(child.name + ("/" if child.is_dir() else ""))
        docs_dir = project_path / "docs"
        if docs_dir.is_dir():
            docs = sorted(str(path.relative_to(project_path)) for path in docs_dir.rglob("*.md"))

    signals = []
    for name in [
        "README.md",
        "AGENTS.md",
        "package.json",
        "composer.json",
        "pyproject.toml",
        "requirements.txt",
        "Cargo.toml",
        "go.mod",
        "Gemfile",
    ]:
        if (project_path / name).exists():
            signals.append(name)

    return {
        "git_branch": run_git(project_path, "branch", "--show-current") or "none",
        "git_status": run_git(project_path, "status", "--short", "--branch"),
        "git_remotes": run_git(project_path, "remote", "-v"),
        "top_level": top_level[:80],
        "docs": docs[:80],
        "signals": signals,
    }


def markdown_list(values: list[str], empty: str = "TBD") -> str:
    if not values:
        return f"- {empty}"
    return "\n".join(f"- `{value}`" for value in values)


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def append_readme_memory_for_existing(
    readme_path: pathlib.Path,
    *,
    name: str,
    objective: str,
    repo_url: str,
    next_task: str,
) -> None:
    append_if_missing(
        readme_path,
        "<!-- AI_PROJECT_MEMORY_START -->",
        f"""
        <!-- AI_PROJECT_MEMORY_START -->
        ## Overview

        {objective}

        This repository has been adopted into the repo-first AI project workflow. Existing product/code context remains authoritative; the added memory files make future AI sessions easier to restart.

        ## Value Proposition

        - Preserves existing project context as durable AI-readable memory.
        - Turns scattered chat, repo, and source material into versioned project files.
        - Keeps future AI sessions aligned with the current repo state.

        ## Who It Is For

        - The project owner and future AI sessions working on `{name}`.
        - Technical collaborators who need scope, status, trusted inputs, and handoff context.

        ## Technical Overview

        - Existing implementation files stay in place and should not be overwritten casually.
        - Standard agent instructions start at `AGENTS.md`.
        - Tool-specific adapters live in `CLAUDE.md`, `.cursor/rules/project.mdc`, and `.github/copilot-instructions.md`.
        - Machine-readable project state lives in `ai-project.yaml`.
        - AI memory lives in `docs/`, `knowledge/`, and `source_of_truth/`.
        - Existing-project adoption notes live in `docs/05_project_adoption.md`.
        - Validation expectations live in `docs/03_validation.md` and `scripts/ai_project_check.py`.
        - Master/specialist orchestration rules live in `docs/07_ai_orchestration_source_of_truth.md`.

        ## Status

        - Current objective: {objective}
        - Current next task: {next_task}
        - Repo URL: {repo_url}

        ## Project Memory

        1. `AGENTS.md`
        2. `ai-project.yaml`
        3. `knowledge/README_FOR_AI.md`
        4. `docs/00_project_brief.md`
        5. `docs/01_ai_operating_model.md`
        6. `docs/02_session_handoff_prompt.md`
        7. `docs/03_validation.md`
        8. `docs/04_cross_ai_orchestration.md`
        9. `docs/05_project_adoption.md`
        10. `docs/06_memory_freshness.md`
        11. `docs/07_ai_orchestration_source_of_truth.md`
        12. `source_of_truth/README.md`

        ## Next Steps

        1. Review `docs/05_project_adoption.md` and promote any important existing context into durable docs.
        2. Update `source_of_truth/README.md` with trusted existing files, screenshots, PDFs, or exports.
        3. Run `python3 scripts/ai_project_check.py` before pushing or handing off.
        4. Verify GitHub privacy before pushing sensitive work.
        5. Keep `docs/02_session_handoff_prompt.md`, `docs/06_memory_freshness.md`, `docs/07_ai_orchestration_source_of_truth.md`, and `ai-project.yaml` current after meaningful changes.
        <!-- AI_PROJECT_MEMORY_END -->
        """,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="Project directory to scaffold")
    parser.add_argument("--name", required=True, help="Human-readable project name")
    parser.add_argument("--objective", required=True, help="One-sentence project objective")
    parser.add_argument("--repo-url", default="TBD", help="GitHub repo URL, if known")
    parser.add_argument(
        "--origin-mode",
        choices=["new", "existing-project", "existing-chat"],
        default="new",
        help="Whether this is a new project, an existing local project, or a chat being converted into a project",
    )
    parser.add_argument(
        "--source-summary",
        default="TBD",
        help="Short summary of existing chat/project context used during adoption",
    )
    parser.add_argument(
        "--adopt-existing",
        action="store_true",
        help="Shortcut for --origin-mode existing-project; preserves existing files and adds missing AI memory",
    )
    parser.add_argument(
        "--next-task",
        default="Identify the smallest useful next implementation step and execute it after confirming repo context.",
        help="Concrete first task for the next AI session",
    )
    args = parser.parse_args()
    if args.adopt_existing:
        args.origin_mode = "existing-project"

    project_path = pathlib.Path(args.path).expanduser().resolve()
    project_path.mkdir(parents=True, exist_ok=True)
    project_slug = slugify(args.name)
    project_path_shell = shlex.quote(str(project_path))
    existing_snapshot = collect_existing_snapshot(project_path)
    today = date.today().isoformat()

    write_if_missing(
        project_path / "README.md",
        f"""
        # {args.name}

        ## Overview

        {args.objective}

        This repository is the durable home for the project: product context, technical decisions, source-of-truth materials, working notes, validation history, and future AI session handoffs live here instead of being scattered across chat.

        ## Value Proposition

        - Preserves the project intent so future AI and human contributors can restart quickly.
        - Turns important context into versioned files instead of disposable conversation history.
        - Keeps implementation, validation, and handoff work tied to a private GitHub-backed source of truth.

        ## Who It Is For

        - The project owner who needs durable AI-assisted execution.
        - Future AI sessions that need fast, accurate context reconstruction.
        - Technical collaborators who need to understand scope, status, and trusted inputs.

        ## Technical Overview

        - Project memory lives in `docs/`, `knowledge/`, and `source_of_truth/`.
        - Agent compatibility starts at `AGENTS.md` and is mirrored into `CLAUDE.md`, `.cursor/rules/project.mdc`, and `.github/copilot-instructions.md`.
        - Machine-readable project state lives in `ai-project.yaml`.
        - Cross-AI orchestration, specialist AI systems, and triad dispatch plans are tracked in `docs/04_cross_ai_orchestration.md`.
        - Google Stitch and other AI design tool screen/version tracking lives in `source_of_truth/stitch-map.md` when those tools are used.
        - Temporary working notes belong in `work/`.
        - Generated or deliverable artifacts belong in `artifacts/`.
        - Validation expectations are tracked in `docs/03_validation.md` and automated by `scripts/ai_project_check.py`.
        - Master/specialist orchestration rules live in `docs/07_ai_orchestration_source_of_truth.md`.

        ## Status

        - Current objective: {args.objective}
        - Current next task: {args.next_task}
        - Repo URL: {args.repo_url}

        GitHub visibility policy: private by default unless the user explicitly says otherwise.

        ## Project Memory

        1. `AGENTS.md`
        2. `ai-project.yaml`
        3. `knowledge/README_FOR_AI.md`
        4. `docs/00_project_brief.md`
        5. `docs/01_ai_operating_model.md`
        6. `docs/02_session_handoff_prompt.md`
        7. `docs/03_validation.md`
        8. `docs/04_cross_ai_orchestration.md`
        9. `docs/05_project_adoption.md`
        10. `docs/06_memory_freshness.md`
        11. `docs/07_ai_orchestration_source_of_truth.md`
        12. `source_of_truth/README.md`
        13. `source_of_truth/stitch-map.md` when Google Stitch is part of the workflow

        ## Next Steps

        1. Fill in the project brief with the user's exact intent and constraints.
        2. Add trusted inputs to `source_of_truth/` and update its manifest.
        3. Run `python3 scripts/ai_project_check.py`.
        4. Register any external AI systems or triads in `docs/04_cross_ai_orchestration.md`.
        5. Review `docs/05_project_adoption.md` if this project was adopted from an existing chat or repo.
        6. If Google Stitch is used, record project IDs, screen IDs, current versions, archived candidates, and prompts in `source_of_truth/stitch-map.md`.
        7. Update `ai-project.yaml`, `docs/06_memory_freshness.md`, and `docs/07_ai_orchestration_source_of_truth.md` after meaningful changes.
        8. Commit and push meaningful checkpoints to private GitHub.
        """,
    )
    if args.origin_mode != "new":
        append_readme_memory_for_existing(
            project_path / "README.md",
            name=args.name,
            objective=args.objective,
            repo_url=args.repo_url,
            next_task=args.next_task,
        )

    write_if_missing(
        project_path / "AGENTS.md",
        f"""
        # Agent Instructions

        This file is the standard entry point for AI coding agents working in this repository.

        ## Project

        - Name: {args.name}
        - Objective: {args.objective}
        - Origin mode: {args.origin_mode}
        - Repo URL: {args.repo_url}
        - Local path: {project_path}
        - Status: active

        ## Read First

        1. `ai-project.yaml`
        2. `knowledge/README_FOR_AI.md`
        3. `docs/00_project_brief.md`
        4. `docs/01_ai_operating_model.md`
        5. `docs/02_session_handoff_prompt.md`
        6. `docs/03_validation.md`
        7. `docs/04_cross_ai_orchestration.md`
        8. `docs/05_project_adoption.md`
        9. `docs/06_memory_freshness.md`
        10. `docs/07_ai_orchestration_source_of_truth.md`
        11. `source_of_truth/README.md`

        ## Operating Rules

        - Treat the repository as the source of truth, not the chat transcript.
        - Preserve existing files, history, and user work when this is an adopted project.
        - Keep trusted inputs in `source_of_truth/` and update `source_of_truth/README.md`.
        - Keep temporary notes in `work/`; promote durable decisions into `docs/` or `knowledge/`.
        - Keep generated deliverables in `artifacts/` when they should be versioned.
        - Treat master orchestration as synthesis, dispatch, review, and durable memory updates.
        - Send specialist production work to bounded specialist threads or project-scoped chats when the workflow requires it.
        - Treat Google Stitch, Figma, screenshots, and generated mockups as design inputs, not production truth.
        - When using Google Stitch, use `source_of_truth/stitch-map.md` as the current-version registry. Do not infer the accepted screen from canvas position, generation order, or a vague "latest" label.
        - Tell MCP-driven design agents to reuse recorded Stitch project and screen IDs unless the user explicitly asks for a new project.
        - For Google Stitch model choice, use the highest available usable model by default, practically Pro. Use Flash only when the user explicitly says to use Flash for Stitch; do not infer Flash from MVP, prototype, quick draft, or low-importance wording.
        - Keep exactly one `CURRENT` Stitch version per screen or flow; mark older versions as `ARCHIVE` or `CANDIDATE`.
        - Distill accepted Stitch changes into `DESIGN.md`, design tokens, component contracts, docs, or code before treating them as implementation truth.
        - Use direct, technical, pragmatic communication.

        ## Privacy And GitHub

        - Private by default applies to repos, remotes, artifacts, prompts, and handoffs.
        - Do not push to a public remote unless the user explicitly requested public publishing.
        - Before pushing sensitive work, verify GitHub privacy with `gh repo view OWNER/REPO --json isPrivate,url,nameWithOwner`.
        - Do not commit credentials, API keys, tokens, browser cookies, local env files, or unrelated user files.
        - Run `python3 scripts/ai_project_check.py` before a commit, push, or handoff.

        ## Memory Freshness

        Update `ai-project.yaml`, `docs/02_session_handoff_prompt.md`, `docs/03_validation.md`, `docs/06_memory_freshness.md`, and `docs/07_ai_orchestration_source_of_truth.md` when any of these happen:

        - The objective, scope, architecture, active task, repo URL, privacy state, or validation commands change.
        - New trusted source material is added, replaced, or invalidated.
        - External AI output is accepted into the project.
        - A meaningful implementation checkpoint is committed.
        - A handoff to another AI session is prepared.
        - Memory files are older than the freshness window in `ai-project.yaml`.
        - Master/specialist responsibilities, approval gates, or definition-of-done rules change.

        ## Tool Adapters

        - Claude-compatible instructions live in `CLAUDE.md`.
        - Cursor rules live in `.cursor/rules/project.mdc`.
        - GitHub Copilot instructions live in `.github/copilot-instructions.md`.
        - Session handoff guidance for starting the next AI session lives in `docs/02_session_handoff_prompt.md`.
        - Master/specialist orchestration guidance lives in `docs/07_ai_orchestration_source_of_truth.md`.
        - Any coding agent (Claude Code, Codex, Cursor, Copilot) should follow this file as the canonical entry point.

        ## Validation

        Start with:

        ```bash
        python3 scripts/ai_project_check.py
        git status --short --branch
        ```

        Then run any project-specific checks listed in `docs/03_validation.md`.
        """,
    )

    write_if_missing(
        project_path / "CLAUDE.md",
        """
        # Claude Instructions

        Read `AGENTS.md` first and follow it as the canonical project instruction file.

        Claude-specific behavior:

        - Treat `ai-project.yaml` as the machine-readable project manifest.
        - Keep durable context in repository files rather than chat memory.
        - Update `docs/06_memory_freshness.md` and `docs/02_session_handoff_prompt.md` before handing off.
        - Use `docs/07_ai_orchestration_source_of_truth.md` for master/specialist routing, approval gates, and definition of done.
        - Run `python3 scripts/ai_project_check.py` before reporting that the project is ready to push or hand off.
        - Preserve private-by-default GitHub handling unless the user explicitly requests public visibility.
        """,
    )

    write_if_missing(
        project_path / ".cursor" / "rules" / "project.mdc",
        """
        ---
        description: Private AI project memory, validation, and handoff rules
        globs:
          - "**/*"
        alwaysApply: true
        ---

        Read `AGENTS.md` first and treat it as the canonical project instruction file.

        Use `ai-project.yaml` for machine-readable project state and read order.
        Keep `docs/02_session_handoff_prompt.md`, `docs/03_validation.md`, and `docs/06_memory_freshness.md` current after meaningful changes.
        Use `docs/07_ai_orchestration_source_of_truth.md` for master/specialist routing, approval gates, and definition of done.
        Run `python3 scripts/ai_project_check.py` before push or handoff.
        GitHub publishing is private by default unless the user explicitly requests public visibility.
        """,
    )

    write_if_missing(
        project_path / ".github" / "copilot-instructions.md",
        """
        # GitHub Copilot Instructions

        Read `AGENTS.md` first and follow it as the canonical project instruction file.

        Project rules:

        - Use `ai-project.yaml` for read order, active status, privacy policy, and validation commands.
        - Keep durable AI memory in `docs/`, `knowledge/`, and `source_of_truth/`.
        - Keep `docs/02_session_handoff_prompt.md`, `docs/03_validation.md`, and `docs/06_memory_freshness.md` current after meaningful changes.
        - Use `docs/07_ai_orchestration_source_of_truth.md` for master/specialist routing, approval gates, and definition of done.
        - Run `python3 scripts/ai_project_check.py` before push or handoff.
        - Treat GitHub repos and artifacts as private unless the user explicitly requests public visibility.
        """,
    )

    write_if_missing(
        project_path / "ai-project.yaml",
        f"""
        version: 1
        project:
          name: {yaml_quote(args.name)}
          slug: {yaml_quote(project_slug)}
          objective: {yaml_quote(args.objective)}
          origin_mode: {yaml_quote(args.origin_mode)}
          repo_url: {yaml_quote(args.repo_url)}
          local_path: {yaml_quote(str(project_path))}
          status: active
          next_task: {yaml_quote(args.next_task)}
        privacy:
          default_visibility: private
          public_allowed: false
          require_private_remote_verification: true
          verify_command: "gh repo view OWNER/REPO --json isPrivate,url,nameWithOwner"
        memory:
          read_order:
            - AGENTS.md
            - ai-project.yaml
            - knowledge/README_FOR_AI.md
            - docs/00_project_brief.md
            - docs/01_ai_operating_model.md
            - docs/02_session_handoff_prompt.md
            - docs/03_validation.md
            - docs/04_cross_ai_orchestration.md
            - docs/05_project_adoption.md
            - docs/06_memory_freshness.md
            - docs/07_ai_orchestration_source_of_truth.md
            - source_of_truth/README.md
          source_of_truth_manifest: source_of_truth/README.md
          handoff_prompt: docs/02_session_handoff_prompt.md
          scratch_space: work/
        freshness:
          last_reviewed: {today}
          stale_after_days: 14
          update_triggers:
            - before_handoff
            - before_push
            - after_meaningful_implementation_change
            - after_objective_scope_or_architecture_change
            - after_source_of_truth_change
            - after_external_ai_output_is_accepted
            - after_validation_commands_change
        validation:
          commands:
            - python3 scripts/ai_project_check.py
            - git status --short --branch
          required_files:
            - AGENTS.md
            - CLAUDE.md
            - .cursor/rules/project.mdc
            - .github/copilot-instructions.md
            - ai-project.yaml
            - docs/00_project_brief.md
            - docs/01_ai_operating_model.md
            - docs/02_session_handoff_prompt.md
            - docs/03_validation.md
            - docs/04_cross_ai_orchestration.md
            - docs/05_project_adoption.md
            - docs/06_memory_freshness.md
            - docs/07_ai_orchestration_source_of_truth.md
            - knowledge/README_FOR_AI.md
            - source_of_truth/README.md
            - scripts/ai_project_check.py
            - work/README.md
        compatibility:
          standard_agents: AGENTS.md
          claude: CLAUDE.md
          cursor: .cursor/rules/project.mdc
          copilot: .github/copilot-instructions.md
          session_handoff: docs/02_session_handoff_prompt.md
        cross_ai:
          registry: docs/04_cross_ai_orchestration.md
          private_by_default: true
        design_tools:
          google_stitch:
            screen_registry: source_of_truth/stitch-map.md
            model_default: highest_available_usable
            practical_default: pro
            flash_requires_explicit_user_instruction: true
            mvp_is_not_flash_instruction: true
            source_of_truth_rule: "Stitch screens are candidates; accepted current versions must be recorded in the registry and distilled into DESIGN.md, tokens, docs, or code."
        """,
    )

    write_if_missing(
        project_path / "scripts" / "ai_project_check.py",
        """
        #!/usr/bin/env python3
        from __future__ import annotations

        import datetime as dt
        import json
        import pathlib
        import re
        import subprocess
        import sys


        ROOT = pathlib.Path(__file__).resolve().parents[1]
        GH_PRIVACY_COMMAND = "gh repo view OWNER/REPO --json isPrivate,url,nameWithOwner"

        REQUIRED_FILES = [
            "AGENTS.md",
            "CLAUDE.md",
            ".cursor/rules/project.mdc",
            ".github/copilot-instructions.md",
            "ai-project.yaml",
            "scripts/ai_project_check.py",
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
            "work/README.md",
        ]

        MEMORY_FILES = [
            "AGENTS.md",
            "CLAUDE.md",
            ".cursor/rules/project.mdc",
            ".github/copilot-instructions.md",
            "ai-project.yaml",
            "docs/02_session_handoff_prompt.md",
            "docs/03_validation.md",
            "docs/06_memory_freshness.md",
            "docs/07_ai_orchestration_source_of_truth.md",
            "knowledge/README_FOR_AI.md",
            "source_of_truth/README.md",
        ]

        EXCLUDED_DIRS = {
            ".git",
            ".venv",
            "__pycache__",
            "node_modules",
            "vendor",
            "dist",
            "build",
            "tmp",
            ".pytest_cache",
            ".ruff_cache",
        }

        NON_IMPLEMENTATION_FILES = {
            ".gitignore",
            "README.md",
            "scripts/ai_project_check.py",
            "artifacts/.gitkeep",
            "source_of_truth/.gitkeep",
        }

        SECRET_PATTERNS = [
            ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
            ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
            ("OpenAI-style API key", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
            (
                "credential assignment",
                re.compile(r"(?i)(api[_-]?key|secret|token|password)\\s*[:=]\\s*['\\\"][^'\\\"]{12,}['\\\"]"),
            ),
        ]


        def run(command: list[str]) -> tuple[int, str, str]:
            try:
                result = subprocess.run(
                    command,
                    cwd=ROOT,
                    check=False,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except FileNotFoundError as exc:
                return 127, "", str(exc)
            return result.returncode, result.stdout.strip(), result.stderr.strip()


        def read_text(relative: str) -> str:
            return (ROOT / relative).read_text(encoding="utf-8")


        def parse_scalar(text: str, key: str) -> str | None:
            match = re.search(rf"^\\s*{re.escape(key)}:\\s*['\\\"]?([^'\\\"\\n#]+)", text, re.MULTILINE)
            return match.group(1).strip() if match else None


        def parse_bool(text: str, key: str) -> bool | None:
            value = parse_scalar(text, key)
            if value is None:
                return None
            lowered = value.lower()
            if lowered in {"true", "yes"}:
                return True
            if lowered in {"false", "no"}:
                return False
            return None


        def iter_project_files():
            for path in ROOT.rglob("*"):
                if not path.is_file():
                    continue
                relative_parts = path.relative_to(ROOT).parts
                if any(part in EXCLUDED_DIRS for part in relative_parts):
                    continue
                yield path


        def github_repo_from_url(url: str) -> str | None:
            url = url.strip()
            if not url:
                return None
            ssh = re.match(r"git@github\\.com:([^/]+)/(.+?)(?:\\.git)?$", url)
            if ssh:
                return f"{ssh.group(1)}/{ssh.group(2)}"
            https = re.match(r"https://github\\.com/([^/]+)/(.+?)(?:\\.git)?/?$", url)
            if https:
                return f"{https.group(1)}/{https.group(2)}"
            return None


        def check_required_files(errors: list[str]) -> None:
            for relative in REQUIRED_FILES:
                if not (ROOT / relative).is_file():
                    errors.append(f"missing required file: {relative}")


        def check_manifest(errors: list[str]) -> None:
            manifest_path = ROOT / "ai-project.yaml"
            if not manifest_path.is_file():
                errors.append("missing ai-project.yaml")
                return
            manifest = manifest_path.read_text(encoding="utf-8")
            for required in [
                "version:",
                "project:",
                "privacy:",
                "memory:",
                "freshness:",
                "validation:",
                "compatibility:",
                "read_order:",
                "stale_after_days:",
                "require_private_remote_verification:",
            ]:
                if required not in manifest:
                    errors.append(f"ai-project.yaml missing {required}")
            if parse_bool(manifest, "public_allowed") is not False:
                errors.append("ai-project.yaml must set public_allowed: false unless public publishing is intentional")

            last_reviewed = parse_scalar(manifest, "last_reviewed")
            stale_after = parse_scalar(manifest, "stale_after_days")
            if not last_reviewed or not stale_after:
                errors.append("ai-project.yaml must include freshness.last_reviewed and stale_after_days")
                return
            try:
                reviewed_date = dt.date.fromisoformat(last_reviewed)
                stale_days = int(stale_after)
            except ValueError:
                errors.append("ai-project.yaml freshness values are invalid")
                return
            age_days = (dt.date.today() - reviewed_date).days
            if age_days > stale_days:
                errors.append(
                    f"project memory is stale: last_reviewed={last_reviewed}, stale_after_days={stale_days}"
                )


        def check_agent_adapters(errors: list[str]) -> None:
            ag = read_text("AGENTS.md") if (ROOT / "AGENTS.md").is_file() else ""
            if "ai-project.yaml" not in ag or "python3 scripts/ai_project_check.py" not in ag:
                errors.append("AGENTS.md must point to ai-project.yaml and scripts/ai_project_check.py")
            for relative in ["CLAUDE.md", ".cursor/rules/project.mdc", ".github/copilot-instructions.md"]:
                if (ROOT / relative).is_file() and "AGENTS.md" not in read_text(relative):
                    errors.append(f"{relative} must delegate to AGENTS.md")


        def check_privacy(errors: list[str], warnings: list[str]) -> None:
            manifest = read_text("ai-project.yaml") if (ROOT / "ai-project.yaml").is_file() else ""
            require_private = parse_bool(manifest, "require_private_remote_verification")
            code, stdout, _ = run(["git", "remote", "-v"])
            if code != 0 or not stdout:
                return
            repos = sorted({repo for repo in (github_repo_from_url(line.split()[1]) for line in stdout.splitlines() if len(line.split()) >= 2) if repo})
            if not repos:
                return
            for repo in repos:
                gh_code, gh_stdout, gh_stderr = run(["gh", "repo", "view", repo, "--json", "isPrivate,url,nameWithOwner"])
                if gh_code != 0:
                    message = f"could not verify GitHub privacy for {repo}: {gh_stderr or gh_stdout}"
                    if require_private:
                        errors.append(message)
                    else:
                        warnings.append(message)
                    continue
                try:
                    payload = json.loads(gh_stdout)
                except json.JSONDecodeError:
                    errors.append(f"could not parse gh privacy response for {repo}")
                    continue
                if payload.get("isPrivate") is not True:
                    errors.append(f"public GitHub remote blocked: {payload.get('url', repo)}")


        def check_secrets(errors: list[str]) -> None:
            for path in iter_project_files():
                try:
                    if path.stat().st_size > 2_000_000:
                        continue
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                relative = path.relative_to(ROOT)
                for label, pattern in SECRET_PATTERNS:
                    if pattern.search(text):
                        errors.append(f"possible {label} in {relative}")


        def check_memory_freshness(warnings: list[str]) -> None:
            memory_paths = [ROOT / relative for relative in MEMORY_FILES if (ROOT / relative).is_file()]
            if not memory_paths:
                return
            latest_memory = max(path.stat().st_mtime for path in memory_paths)
            implementation_files = []
            memory_set = {path.resolve() for path in memory_paths}
            for path in iter_project_files():
                if path.resolve() in memory_set:
                    continue
                relative = path.relative_to(ROOT)
                if relative.as_posix() in NON_IMPLEMENTATION_FILES:
                    continue
                if relative.parts[0] in {"docs", "knowledge", "source_of_truth", "work", "artifacts"}:
                    continue
                implementation_files.append(path)
            if not implementation_files:
                return
            latest_impl = max(path.stat().st_mtime for path in implementation_files)
            if latest_impl > latest_memory:
                warnings.append(
                    "implementation files are newer than key memory files; review docs/06_memory_freshness.md"
                )


        def main() -> int:
            errors: list[str] = []
            warnings: list[str] = []

            check_required_files(errors)
            check_manifest(errors)
            check_agent_adapters(errors)
            check_privacy(errors, warnings)
            check_secrets(errors)
            check_memory_freshness(warnings)

            for warning in warnings:
                print(f"WARN: {warning}", file=sys.stderr)
            if errors:
                for error in errors:
                    print(f"FAIL: {error}", file=sys.stderr)
                return 1

            print("ai project checks passed")
            return 0


        if __name__ == "__main__":
            raise SystemExit(main())
        """,
    )

    write_if_missing(
        project_path / "docs" / "00_project_brief.md",
        f"""
        # Project Brief

        ## Objective

        {args.objective}

        ## Scope

        - Capture the user's intent as durable project memory.
        - If this is an existing project, preserve existing code, docs, and git history while adding missing AI memory files.
        - If this is an existing chat, convert reusable chat context into repo files and source-of-truth notes.
        - Store source-of-truth files in the repo.
        - Preserve instructions for future AI sessions.
        - Publish to private GitHub by default.
        - Keep validation and next-session instructions current.

        ## Assumptions

        - The user values continuity across AI sessions.
        - The repo is the source of truth, not the chat transcript.
        - Existing project files should be treated as prior work, not as disposable scaffold output.
        - Public publishing is disallowed unless explicitly requested.

        ## Open Questions

        - TBD

        ## Current Next Task

        {args.next_task}
        """,
    )

    write_if_missing(
        project_path / "docs" / "01_ai_operating_model.md",
        """
        # AI Operating Model

        ## User Working Style

        The user works as a master AI operator. Treat projects as durable systems, not one-off chats.

        ## Operating Rules

        - Be direct, technical, and pragmatic.
        - Convert reusable context into files.
        - Treat `AGENTS.md` as the canonical cross-tool agent instruction file.
        - Keep `ai-project.yaml` current as the machine-readable project manifest.
        - Keep source-of-truth artifacts in `source_of_truth/`.
        - Commit and push meaningful checkpoints to private GitHub.
        - Explain AI-use best practices when they materially improve the work.
        - Validate outcomes with commands, tests, screenshots, or source checks when possible.
        - Treat Google Stitch and similar AI design tools as controlled exploration inputs.
        - For Stitch work, update `source_of_truth/stitch-map.md` with project ID, screen/resource IDs, parent/new version links, prompt used, timestamp, and status.
        - Do not decide "current design" from Stitch canvas placement, generation order, or a generic latest label; use the repo registry.
        - For Stitch model selection, use the highest available usable model by default, practically Pro. Use Flash only when the user explicitly says to use Flash for Google Stitch; the word MVP is not a sufficient reason.
        - Keep accepted visual rules in `DESIGN.md`, design-token docs, component contracts, or code.
        - Use the master thread for synthesis, dispatch prompts, memory updates, specialist review, gap identification, and next-step coordination.
        - Use specialist threads or project-scoped chats for specialist production work such as coding, design, research, legal/risk, marketing, voice, video, or thumbnails.
        - Avoid mega-prompts and uncontrolled autonomy; split serious work into bounded tasks with acceptance criteria and checks.
        - Ask for founder approval before product-direction, UX/taste, brand, public publishing, push/PR, legal/risk, paid-launch, irreversible data, credential/provider, or major source-of-truth changes unless already approved.
        - When another specialist AI system can help, use `docs/04_cross_ai_orchestration.md` to define its source URL, rules, dispatch prompt, output contract, and return path.

        ## Default Privacy

        All GitHub repos and shared artifacts are private unless the user explicitly says public.

        ## Durable Context Rules

        - Prefer updating repo files over relying on chat memory.
        - Put trusted inputs in `source_of_truth/` and summarize them in `source_of_truth/README.md`.
        - Put temporary exploration notes in `work/` and promote only durable decisions into `docs/` or `knowledge/`.
        - Keep `docs/02_session_handoff_prompt.md` accurate after meaningful changes.
        - Keep `docs/06_memory_freshness.md` and `ai-project.yaml` accurate before push, handoff, or external AI dispatch.
        - Keep `docs/07_ai_orchestration_source_of_truth.md` accurate when master/specialist routing, approval gates, or definition-of-done rules change.
        - Run `python3 scripts/ai_project_check.py` before claiming the project is ready.
        """,
    )

    write_if_missing(
        project_path / "docs" / "02_session_handoff_prompt.md",
        f"""
        # Session Handoff Prompt

        Use this repository as the durable project memory.

        Repo: {args.repo_url}
        Local path: {project_path}

        If you are starting a new AI coding session on this project, just open this folder as your working directory. Claude Code (and most modern coding agents) persist session context per project folder automatically — no explicit registration step is required.

        Read these first:

        1. `AGENTS.md`
        2. `ai-project.yaml`
        3. `knowledge/README_FOR_AI.md`
        4. `docs/00_project_brief.md`
        5. `docs/01_ai_operating_model.md`
        6. `docs/02_session_handoff_prompt.md`
        7. `docs/03_validation.md`
        8. `docs/04_cross_ai_orchestration.md`
        9. `docs/05_project_adoption.md`
        10. `docs/06_memory_freshness.md`
        11. `docs/07_ai_orchestration_source_of_truth.md`
        12. `source_of_truth/README.md`

        Operate with this policy:

        - GitHub private by default.
        - Preserve source-of-truth files in the repo.
        - Commit and push meaningful checkpoints.
        - Treat the user as a master AI operator: concise, technical, pragmatic.
        - Use `AGENTS.md` as the portable instruction entry point for any coding agent.
        - Keep `ai-project.yaml` current as the machine-readable manifest.
        - Run `python3 scripts/ai_project_check.py` before push or handoff.
        - Use `docs/07_ai_orchestration_source_of_truth.md` for master/specialist routing, approval gates, bounded tasks, and definition of done.
        - If this project was adopted from an existing repo or chat, read `docs/05_project_adoption.md` before assuming missing context.
        - If the task depends on another specialist AI system, read `docs/04_cross_ai_orchestration.md` and dispatch bounded work according to that registry.
        - Update `docs/06_memory_freshness.md` after meaningful implementation, validation, source-of-truth, or orchestration changes.

        First task:

        {args.next_task}
        """,
    )

    write_if_missing(
        project_path / "knowledge" / "README_FOR_AI.md",
        f"""
        # Read This First

        Project: {args.name}

        Objective: {args.objective}

        ## User Defaults

        - The user wants durable AI project memory.
        - The user expects private GitHub publishing unless explicitly stated otherwise.
        - The user prefers technical, pragmatic, master-level AI collaboration.
        - The user wants future AI sessions to inherit context from repo files.
        - The user wants portable agent instructions through `AGENTS.md` plus Claude, Cursor, and Copilot adapters.
        - The user wants `ai-project.yaml` kept current for machine-readable state.
        - The user wants master threads to orchestrate and specialist threads to execute bounded production work.

        ## Read Order

        1. `AGENTS.md`
        2. `ai-project.yaml`
        3. `docs/00_project_brief.md`
        4. `docs/01_ai_operating_model.md`
        5. `docs/02_session_handoff_prompt.md`
        6. `docs/03_validation.md`
        7. `docs/04_cross_ai_orchestration.md`
        8. `docs/05_project_adoption.md`
        9. `docs/06_memory_freshness.md`
        10. `docs/07_ai_orchestration_source_of_truth.md`
        11. `source_of_truth/README.md`
        12. `source_of_truth/`

        ## Next AI Session

        Start by confirming repo status, reading `AGENTS.md` and `ai-project.yaml`, checking private GitHub policy, reviewing cross-AI orchestration and master/specialist routing if relevant, running `python3 scripts/ai_project_check.py`, and executing the handoff prompt's first task.
        """,
    )

    write_if_missing(
        project_path / "docs" / "03_validation.md",
        f"""
        # Validation

        ## Baseline Checks

        - `python3 scripts/ai_project_check.py`
        - `git status --short --branch`
        - `gh repo view OWNER/REPO --json isPrivate,url,nameWithOwner` when a GitHub remote exists.
        - Confirm the GitHub repo is private before pushing sensitive work.
        - Confirm `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/project.mdc`, `.github/copilot-instructions.md`, and `ai-project.yaml` exist.
        - Confirm `ai-project.yaml` has current `project.next_task`, `project.repo_url`, `project.status`, and `freshness.last_reviewed`.
        - Confirm source-of-truth files are present or explicitly marked TBD.
        - Confirm `docs/02_session_handoff_prompt.md` reflects the current next task.
        - Confirm `docs/06_memory_freshness.md` reflects the latest meaningful checkpoint.
        - Confirm `docs/07_ai_orchestration_source_of_truth.md` reflects current master/specialist routing and approval gates.

        ## Privacy And Secret Checks

        - `scripts/ai_project_check.py` scans for common private keys, API key patterns, and credential assignments.
        - If the script reports a public GitHub remote, stop and ask before pushing unless the user explicitly requested public visibility.
        - If GitHub privacy cannot be verified, report the blocker instead of assuming private visibility.

        ## Memory Freshness Checks

        - Update memory files before handoff, before push, after meaningful implementation changes, and after accepting external AI output.
        - Treat `ai-project.yaml:freshness.stale_after_days` as the maximum acceptable age for project memory review.
        - If implementation files are newer than key memory files, review `docs/06_memory_freshness.md` and update the relevant memory files.

        ## Last Verified

        - Date: {today}
        - Result: Initial scaffold generated; run project-specific checks before implementation handoff.
        """,
    )

    write_if_missing(
        project_path / "docs" / "06_memory_freshness.md",
        f"""
        # Memory Freshness

        This project uses repository files as durable AI memory. Memory is useful only while it reflects the actual project state.

        ## Last Review

        - Date: {today}
        - Reviewed by: scaffold
        - Status: initial memory scaffold created

        ## Refresh Triggers

        Update `ai-project.yaml`, `docs/02_session_handoff_prompt.md`, `docs/03_validation.md`, this file, `docs/07_ai_orchestration_source_of_truth.md`, and any affected source-of-truth manifests when:

        - The objective, scope, architecture, active task, repo URL, or privacy state changes.
        - Validation commands, test status, or deployment expectations change.
        - New source material is added to `source_of_truth/` or existing source material becomes obsolete.
        - External AI output is accepted into the project.
        - Master/specialist responsibilities, approval gates, task boundaries, or definition-of-done rules change.
        - A meaningful implementation checkpoint is committed.
        - A handoff to a future AI session is prepared.
        - `ai-project.yaml:freshness.last_reviewed` is older than `freshness.stale_after_days`.

        ## Required Updates

        - `ai-project.yaml`: project status, next task, repo URL, validation commands, and `freshness.last_reviewed`.
        - `docs/02_session_handoff_prompt.md`: current first task and any repo/thread instructions.
        - `docs/03_validation.md`: last verified date, commands run, gaps, and blockers.
        - `source_of_truth/README.md`: trusted input manifest.
        - `docs/04_cross_ai_orchestration.md`: external AI dispatch status and returned outputs.
        - `docs/07_ai_orchestration_source_of_truth.md`: master/specialist routing, approval gates, and definition-of-done rules.

        ## Automation

        Run:

        ```bash
        python3 scripts/ai_project_check.py
        ```

        The check verifies required memory files, adapter files, manifest structure, freshness date, common secret patterns, and GitHub remote privacy when a GitHub remote is present.
        """,
    )
    write_if_missing(
        project_path / "docs" / "07_ai_orchestration_source_of_truth.md",
        """
        # AI Orchestration Source Of Truth

        Use this file for master/specialist routing, durable memory rules, approval gates, bounded task dispatch, and definition of done.

        ## Durable Memory

        - Chat history is temporary.
        - Repository docs, committed files, decision logs, source-of-truth manifests, and structured handoffs are durable.
        - Important decisions must be distilled into canonical docs.
        - Living docs describe current truth. If history matters, keep it in a decision log with status such as accepted, superseded, rejected, or needs founder confirmation.
        - If older context is unavailable or context compaction happened, state the limitation instead of claiming full coverage.

        ## Master Orchestrator Role

        The master orchestrator is for:

        - synthesis
        - decision support
        - prompt writing
        - durable memory updates
        - specialist output review
        - gap identification
        - next-step coordination

        The master should not directly do specialist production work unless explicitly asked.

        Specialist work belongs to specialist agents or project-scoped threads, such as coding, design, research, legal/risk, marketing, voice, video assembly, or thumbnail creation.

        ## Persistent Specialists And Temporary Workers

        There are two worker types:

        1. Persistent specialist threads: long-lived sidebar/project agents that preserve continuity for a specialty.
        2. Temporary same-thread workers: short-lived workers used for bounded parallel analysis or execution.

        For serious projects, use persistent specialist threads as the main structure. Use temporary workers inside a specialist thread only when they help with bounded work.

        Correct flow:

        1. Master creates a bounded prompt.
        2. Specialist thread executes.
        3. Specialist returns durable output.
        4. Master synthesizes.
        5. Durable docs are updated.

        ## Bounded Task Rule

        Avoid mega-prompts and uncontrolled autonomy.

        Split work into bounded tasks with:

        - clear goal
        - scope
        - non-goals
        - source docs
        - acceptance criteria
        - tests/checks
        - screenshot/design review when UI is involved
        - expected output format
        - escalation conditions

        ## Human Approval Gates

        Ask for founder approval before:

        - product direction changes
        - UX/taste acceptance
        - brand direction
        - public publishing
        - GitHub push/PR creation if not already approved
        - legal/platform-risk decisions
        - paid/public launch assumptions
        - irreversible data changes
        - credentials, secrets, or provider setup
        - major source-of-truth changes

        If unsure, document assumptions and continue only when risk is low.

        ## Git And Experiment Strategy

        - Private GitHub is the durable backup and source-control home.
        - Experiments should be isolated in a branch or separate folder.
        - Do not push experiments unless explicitly approved.
        - Do not merge failed experiments wholesale. Cherry-pick useful pieces after review.

        ## Automations

        Automations are scheduled heartbeats, not completion events.

        Use them for reminders, status checks, recurring review, or careful continuation of a known thread.

        Avoid frequent automations for uncontrolled coding because they can create repeated prompts, context clutter, token waste, and drift.

        ## Design Inputs

        Figma, Paper, Google Stitch, screenshots, competitor references, and generated mockups are visual inputs, not production truth.

        Production truth is:

        - repo docs
        - accepted decisions
        - design tokens
        - component contracts
        - coded implementation
        - tests
        - screenshot review

        Competitor screenshots are inspiration only. Extract UX principles, but do not copy exact UI, branding, colors, typography, icons, wording, layout, trade dress, or product identity.

        ## Google Stitch Workflow

        Use Stitch for exploration, high-fidelity candidates, product-surface concepts, and design-to-code handoff. Do not use Stitch canvas placement or generation order as the source of truth for the current design.

        Required Stitch discipline:

        - Keep `source_of_truth/stitch-map.md` current whenever Stitch is used.
        - Record project ID, screen/resource ID, parent screen, generated screen, version label, timestamp, prompt used, status, and notes.
        - Maintain exactly one `CURRENT` version per screen or flow. Mark older useful versions as `ARCHIVE`; mark unaccepted experiments as `CANDIDATE` or `REJECTED`.
        - Tell MCP-driven agents to reuse the recorded project and screen IDs unless the user explicitly says `NEW PROJECT`.
        - Use the highest available usable Stitch model by default, practically Pro. Use Flash only when the user explicitly says to use Flash for Google Stitch.
        - Do not infer Flash from project labels such as MVP, prototype, quick draft, early version, cheap, or low importance.
        - Ask for one screen/component and one or two changes per Stitch prompt.
        - Preserve accepted visual rules in `DESIGN.md`, design-token docs, component contracts, or code before implementation.
        - If Stitch listing tools disagree with known screen IDs, trust the recorded resource IDs until verified manually.

        ## UI Workflow

        Product UI should move through:

        1. Product docs and information architecture.
        2. Visual direction reference.
        3. Prototype contract.
        4. UI tokens and components.
        5. Fake-data coded prototype.
        6. Screenshot review.
        7. Approved pieces promoted to production structure.
        8. Prototype-only routes deleted or isolated.
        9. Real logic implemented as separate tasks.

        A coded prototype should not silently become production logic.

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

        Each coding task should include:

        - source docs to read
        - GitHub Issue number and branch name
        - exact scope
        - domain/API contracts
        - acceptance criteria
        - tests
        - lint/type/build checks
        - migration/data safety notes
        - screenshot review if UI is involved
        - docs updates if behavior changes

        A task is not complete because the code runs. It is complete only when the PR checks pass, the lead review is satisfied, and the relevant durable docs are updated.

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

        ## Project Spawn Flow

        When a high-level request starts in a master playground and should become a serious project:

        1. Preserve the initial chat/request as source material in the new project.
        2. Create or adopt a new local project folder.
        3. Create a new private GitHub repo.
        4. Register the folder with the coding agent's own project mechanism, if it has one (e.g. Codex Desktop Projects).
        5. Create a project-scoped master thread with a proper title.
        6. Write a plan and ask the user whether to implement or revise before launching specialist execution, unless the user already explicitly approved implementation.
        7. After approval, execute from the new project-scoped master thread.
        8. Dispatch bounded work to persistent specialist threads or project-scoped specialist chats.
        9. Run work asynchronously where tool support allows, while keeping outputs bounded and reconciled.
        10. Bring specialist outputs back into the project repo, update durable docs, validate, and report final paths.

        For a YouTube video production request, typical specialist tracks are idea/script, visual storyboard/slides, voice, Remotion/video assembly, thumbnail, and QA.
        """,
    )
    write_if_missing(
        project_path / "docs" / "05_project_adoption.md",
        f"""
        # Project Adoption

        ## Origin Mode

        {args.origin_mode}

        ## Adoption Intent

        This file explains whether the project was created from scratch, converted from an existing chat, or adopted from an existing local repo/project. It prevents future AI sessions from treating old project context as missing context.

        ## Existing Context Used

        {args.source_summary}

        ## Detected Repo State

        - Git branch: `{existing_snapshot["git_branch"]}`
        - Git status:

        ```text
        {existing_snapshot["git_status"]}
        ```

        - Git remotes:

        ```text
        {existing_snapshot["git_remotes"]}
        ```

        ## Detected Project Signals

        {markdown_list(existing_snapshot["signals"])}

        ## Top-Level Files At Adoption

        {markdown_list(existing_snapshot["top_level"])}

        ## Existing Docs At Adoption

        {markdown_list(existing_snapshot["docs"])}

        ## Preservation Rules

        - Do not overwrite existing user code, docs, prompts, assets, or git history just to fit the scaffold.
        - Promote useful existing context into `docs/`, `knowledge/`, or `source_of_truth/`.
        - If existing files conflict with generated memory docs, preserve existing files and record the conflict here.
        - Stage only intended project-memory changes when committing adoption work.

        ## Adoption Checklist

        - [ ] Existing README, AGENTS, CLAUDE, Cursor, Copilot, docs, and source files reviewed.
        - [ ] Durable project memory files created or updated.
        - [ ] `AGENTS.md` is the canonical portable instruction entry point.
        - [ ] `CLAUDE.md`, `.cursor/rules/project.mdc`, and `.github/copilot-instructions.md` delegate to `AGENTS.md`.
        - [ ] `ai-project.yaml` reflects current repo URL, status, next task, read order, privacy policy, and freshness date.
        - [ ] Existing GitHub remote privacy checked, or private repo created.
        - [ ] `python3 scripts/ai_project_check.py` passes or reports clear blockers.
        - [ ] Handoff prompt updated with current repo URL and next task.
        - [ ] Memory freshness reviewed in `docs/06_memory_freshness.md`.
        - [ ] AI orchestration source of truth reviewed in `docs/07_ai_orchestration_source_of_truth.md`.
        - [ ] Agent-specific project registration completed, if the coding agent supports one and it was requested.
        """,
    )
    write_if_missing(
        project_path / "docs" / "04_cross_ai_orchestration.md",
        """
        # Cross-AI Orchestration

        Use this file when this project should coordinate with other AI systems, specialist chats, or triads.

        ## Intent

        Preserve the user's reusable AI-network knowledge: which AI systems exist, what each one is good at, where its GitHub-backed instructions live, what rules it follows, how to dispatch work to it, and how to bring the output back into this project.

        Use `docs/07_ai_orchestration_source_of_truth.md` for master/specialist responsibilities, approval gates, bounded task requirements, and definition of done.

        ## AI System Registry

        | AI System | Role | Source URL | Read First | Dispatch Status | Output Location |
        | --- | --- | --- | --- | --- | --- |
        | TBD | TBD | TBD | TBD | Not dispatched | TBD |

        ## Triads

        | Triad | Roles | Shared Inputs | Handoff Order | Validation Owner | Status |
        | --- | --- | --- | --- | --- | --- |
        | TBD | TBD | TBD | TBD | TBD | TBD |

        ## Dispatch Prompt Template

        ```text
        You are being used as a specialist AI system for a GitHub-backed private project.

        Current project:
        - Repo: <current-project-repo-url>
        - Local path: <current-project-local-path>
        - Objective: <project-objective>

        Read first:
        1. <current-project-memory-file>
        2. <relevant-source-of-truth-file>
        3. <external-ai-system-rules-url-or-file>

        Specialist role:
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
        - Stay inside the bounded task. Escalate product direction, UX/taste, brand, public publishing, push/PR, legal/risk, paid-launch, irreversible data, credentials/provider, or major source-of-truth decisions.
        - Return enough context for this project to update its memory files.
        ```

        ## Workflow

        1. Read this project's memory files and `docs/07_ai_orchestration_source_of_truth.md` before dispatching external work.
        2. Read the target AI system's source URL or local documentation.
        3. Use the master thread for synthesis and dispatch; use specialist threads for bounded production work.
        4. Create a project-scoped thread when the tool supports it.
        5. Create a bounded dispatch prompt with inputs, role, output contract, validation expectations, and escalation conditions.
        6. Save returned outputs under `source_of_truth/`, `docs/`, `artifacts/`, or `work/` as appropriate.
        7. Update this file with dispatch status, output location, and next steps.

        ## Guardrails

        - Private by default applies to all linked repos, prompts, generated artifacts, and handoffs.
        - Do not copy private source material into a public AI system.
        - Do not let external chat memory become the only source of truth.
        - Do not dispatch vague tasks; every dispatch needs a bounded output contract.
        - For Google Stitch or AI design tool dispatches, require the specialist to update `source_of_truth/stitch-map.md` and return parent/new screen IDs, prompt used, accepted status, and any DESIGN.md/token changes.
        - Do not use automations as completion events; treat them as scheduled heartbeats for a known thread.
        """,
    )
    write_if_missing(
        project_path / "source_of_truth" / "stitch-map.md",
        f"""
        # Google Stitch Screen Map

        Use this file only when Google Stitch is part of the project workflow. It prevents future AI sessions from guessing which generated canvas item is current.

        ## Rules

        - Do not infer the accepted screen from canvas position, generation order, or a vague "latest" label.
        - Keep exactly one `CURRENT` version per screen or flow.
        - Mark exploratory outputs as `CANDIDATE`, useful old versions as `ARCHIVE`, rejected outputs as `REJECTED`, and implementation-ready outputs as `HANDOFF`.
        - Tell MCP-driven agents to reuse recorded project and screen IDs unless the user explicitly says `NEW PROJECT`.
        - Use the highest available usable Stitch model by default, practically Pro.
        - Use Flash only when the user explicitly says to use Flash for Google Stitch. Do not infer Flash from MVP/prototype wording.
        - After accepting a Stitch change, distill durable rules into `DESIGN.md`, design tokens, component contracts, docs, or code.

        ## Projects

        | Project Name | Stitch Project ID | Purpose | Status | Notes |
        | --- | --- | --- | --- | --- |
        | TBD | TBD | TBD | TBD | TBD |

        ## Screens

        | Flow/Screen | Status | Version | Stitch Project ID | Screen/Resource ID | Parent Screen ID | Prompt Used | Timestamp | Handoff Target | Notes |
        | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        | TBD | CURRENT | v1 | TBD | TBD | TBD | TBD | {today} | TBD | Replace this row when Stitch is first used. |

        ## Accepted Design Rules

        | Rule | Source Screen/Version | Destination | Status |
        | --- | --- | --- | --- |
        | TBD | TBD | `DESIGN.md` / tokens / docs / code | TBD |

        ## MCP Prompt Guardrail

        ```text
        Google Stitch workflow rules:
        - Do not create a new Stitch project unless I explicitly say NEW PROJECT.
        - Use the highest available usable Stitch model by default, practically Pro.
        - Use Flash only if I explicitly say to use Flash for Google Stitch.
        - Do not infer Flash from words like MVP, prototype, quick draft, cheap, or low importance.
        - Reuse the project and screen IDs recorded in source_of_truth/stitch-map.md.
        - Before generating, identify the target CURRENT screen from source_of_truth/stitch-map.md.
        - Never decide latest/current by canvas position, generation order, or a generic latest label.
        - Create one candidate variant per prompt unless asked otherwise.
        - Report parent screen ID, new screen ID, version label, timestamp, prompt used, and recommended status.
        - Update source_of_truth/stitch-map.md after the generation is accepted or rejected.
        ```
        """,
    )
    write_if_missing(
        project_path / "source_of_truth" / "README.md",
        """
        # Source of Truth

        Store trusted project inputs here: briefs, exports, screenshots, PDFs, datasets, transcripts, API notes, and decision records.

        ## Manifest

        | Path | Source | Why It Matters | Last Checked |
        | --- | --- | --- | --- |
        | TBD | TBD | TBD | TBD |

        ## AI Design Tool Inputs

        Use `source_of_truth/stitch-map.md` when Google Stitch is part of the workflow. Stitch screens are candidates until the accepted version is recorded there and the durable rules are distilled into `DESIGN.md`, design tokens, component contracts, docs, or code.

        ## Rules

        - Do not commit credentials, tokens, cookies, or local-only secrets.
        - Prefer original files plus a short summary over chat-only context.
        - Update this manifest when adding or replacing trusted inputs.
        - Run `python3 scripts/ai_project_check.py` after adding sensitive or externally sourced material.
        """,
    )
    write_if_missing(
        project_path / "work" / "README.md",
        """
        # Work Notes

        Use this folder for temporary analysis, scratch plans, and intermediate outputs that are useful during active work.

        Promote durable decisions, handoff instructions, and trusted inputs into `docs/`, `knowledge/`, or `source_of_truth/`.
        """,
    )
    write_if_missing(project_path / "source_of_truth" / ".gitkeep", "")
    write_if_missing(project_path / "artifacts" / ".gitkeep", "")
    write_if_missing(
        project_path / ".gitignore",
        """
        .DS_Store
        tmp/
        .env
        .env.*
        __pycache__/
        *.pyc
        .pytest_cache/
        .ruff_cache/
        """,
    )

    if args.repo_url != "TBD":
        update_exact_placeholder(project_path / "docs" / "02_session_handoff_prompt.md", "Repo: TBD", f"Repo: {args.repo_url}")

    print(f"scaffolded {project_slug} at {project_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
