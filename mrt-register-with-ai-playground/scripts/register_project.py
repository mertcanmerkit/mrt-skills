#!/usr/bin/env python3
"""Register a project in the user's AI project registry repo."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
from datetime import datetime


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "project"


def read_json(path: pathlib.Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def write_json(path: pathlib.Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def upsert_json(path: pathlib.Path, row: dict) -> None:
    rows = read_json(path)
    key = row["repo_url"]
    updated = False
    for index, existing in enumerate(rows):
        if existing.get("repo_url") == key or existing.get("project_name") == row["project_name"]:
            rows[index] = {**existing, **row}
            updated = True
            break
    if not updated:
        rows.append(row)
    rows.sort(key=lambda item: item.get("project_name", "").lower())
    write_json(path, rows)


def ensure_registered_projects_md(path: pathlib.Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Registered Projects\n\n"
        "Projects registered into this AI project registry.\n\n",
        encoding="utf-8",
    )


def upsert_project_block(path: pathlib.Path, slug: str, row: dict) -> None:
    ensure_registered_projects_md(path)
    content = path.read_text(encoding="utf-8")
    start = f"<!-- project:{slug}:start -->"
    end = f"<!-- project:{slug}:end -->"
    read_first = "\n".join(f"- `{item}`" for item in row["read_first"]) or "- TBD"
    block = f"""\
{start}
## {row['project_name']}

- Role: {row['role']}
- Repo: {row['repo_url']}
- Local path: `{row['project_path']}`
- Status: {row['status']}
- Last updated: {row['last_updated']}

### Read First

{read_first}

### Usage

{row['usage']}
{end}
"""
    if start in content and end in content:
        before = content.split(start)[0]
        after = content.split(end, 1)[1]
        content = before + block + after
    else:
        suffix = "" if content.endswith("\n") else "\n"
        content = content + suffix + "\n" + block + "\n"
    path.write_text(content, encoding="utf-8")


def append_system_registry(path: pathlib.Path, row: dict) -> None:
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    lines = [line for line in content.splitlines() if not line.startswith(f"| {row['project_name']} |")]
    content = "\n".join(lines) + "\n"
    section = "\n## Registered Project Additions\n\n"
    table_header = "| System | Role | GitHub URL | Local Path | Read First | Dispatch Use |\n| --- | --- | --- | --- | --- | --- |\n"
    if "## Registered Project Additions" not in content:
        content = content.rstrip() + section + table_header
    read_first = ", ".join(f"`{item}`" for item in row["read_first"]) or "TBD"
    line = (
        f"| {row['project_name']} | {row['role']} | `{row['repo_url']}` | "
        f"`{row['project_path']}` | {read_first} | {row['usage']} |\n"
    )
    content = content.rstrip() + "\n" + line
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-path", required=True)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--project-path", required=True)
    parser.add_argument("--repo-url", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--usage", required=True)
    parser.add_argument("--read-first", action="append", default=[])
    parser.add_argument("--status", default="active")
    args = parser.parse_args()

    registry = pathlib.Path(args.registry_path).expanduser().resolve()
    row = {
        "project_name": args.project_name,
        "project_path": str(pathlib.Path(args.project_path).expanduser().resolve()),
        "repo_url": args.repo_url,
        "role": args.role,
        "usage": args.usage,
        "read_first": args.read_first,
        "status": args.status,
        "last_updated": datetime.now().astimezone().strftime("%Y-%m-%d"),
    }
    slug = slugify(args.project_name)

    upsert_json(registry / "source_of_truth" / "registered_projects.json", row)
    upsert_project_block(registry / "docs" / "10_registered_projects.md", slug, row)
    append_system_registry(registry / "docs" / "06_ai_system_registry.md", row)
    print(f"registered {args.project_name} in {registry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
