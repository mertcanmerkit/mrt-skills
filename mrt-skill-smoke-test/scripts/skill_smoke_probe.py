#!/usr/bin/env python3
import argparse
import json
import re
import stat
import subprocess
import sys
from pathlib import Path


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return {}, "missing frontmatter fence"
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, "missing closing frontmatter fence"
    raw = text[4:end]
    data = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return data, f"invalid frontmatter line: {line}"
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, None


def run_validator(validator, skill_dir):
    if not validator:
        return None
    validator_path = Path(validator)
    if not validator_path.exists():
        return {"status": "error", "output": f"validator not found: {validator}"}
    result = subprocess.run(
        [sys.executable, str(validator_path), str(skill_dir)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
    )
    return {
        "status": "pass" if result.returncode == 0 else "fail",
        "returncode": result.returncode,
        "output": result.stdout.strip(),
    }


def inspect_scripts(scripts_dir):
    scripts = []
    if not scripts_dir.exists():
        return scripts
    for path in sorted(p for p in scripts_dir.iterdir() if p.is_file()):
        mode = path.stat().st_mode
        text = path.read_text(errors="ignore")[:256]
        scripts.append(
            {
                "path": str(path),
                "executable": bool(mode & stat.S_IXUSR),
                "has_shebang": text.startswith("#!"),
            }
        )
    return scripts


def main():
    parser = argparse.ArgumentParser(description="Static probe for a Claude Code skill smoke test.")
    parser.add_argument("skill_dir", help="Path to a Claude Code skill directory")
    parser.add_argument("--validator", help="Path to skill-creator quick_validate.py")
    parser.add_argument("--markdown", action="store_true", help="Print a Markdown report instead of JSON")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    skill_md = skill_dir / "SKILL.md"
    errors = []
    warnings = []

    if not skill_dir.exists() or not skill_dir.is_dir():
        errors.append(f"skill directory does not exist: {skill_dir}")
        report = {"skill_dir": str(skill_dir), "errors": errors, "warnings": warnings}
        print_report(report, args.markdown)
        return 1

    if not skill_md.exists():
        errors.append("SKILL.md is missing")
        text = ""
        frontmatter = {}
    else:
        text = skill_md.read_text(errors="replace")
        frontmatter, fm_error = parse_frontmatter(text)
        if fm_error:
            errors.append(fm_error)

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not name:
        errors.append("frontmatter.name is missing")
    elif not re.fullmatch(r"[a-z0-9-]{1,63}", name):
        errors.append("frontmatter.name must be lowercase hyphen-case under 64 chars")
    elif name != skill_dir.name:
        warnings.append(f"frontmatter.name ({name}) does not match folder name ({skill_dir.name})")

    if not description:
        errors.append("frontmatter.description is missing")
    elif len(description) < 40:
        warnings.append("frontmatter.description is short; trigger behavior may be weak")

    if re.search(r"(^|\n)\s*(\[?TODO\b|TODO:)", text):
        errors.append("SKILL.md still contains TODO placeholders")

    body = text.split("\n---\n", 2)[-1] if text else ""
    if len(body.strip()) < 200:
        warnings.append("SKILL.md body is very short; behavior may be underspecified")

    scripts = inspect_scripts(skill_dir / "scripts")
    for script in scripts:
        if not script["has_shebang"]:
            warnings.append(f"script has no shebang: {script['path']}")
        if not script["executable"]:
            warnings.append(f"script is not executable: {script['path']}")

    validator = run_validator(args.validator, skill_dir)
    if validator and validator["status"] != "pass":
        errors.append("quick_validate.py failed")

    report = {
        "skill_dir": str(skill_dir),
        "name": name,
        "description_present": bool(description),
        "scripts": scripts,
        "validator": validator,
        "errors": errors,
        "warnings": warnings,
        "static_status": "fail" if errors else ("warn" if warnings else "pass"),
    }
    print_report(report, args.markdown)
    return 1 if errors else 0


def print_report(report, markdown):
    if not markdown:
        print(json.dumps(report, indent=2))
        return

    print(f"## Skill Static Probe: {report['static_status'].upper()}")
    print()
    print(f"Target: `{report['skill_dir']}`")
    print(f"Name: `{report.get('name')}`")
    print(f"Description present: `{report.get('description_present')}`")
    print()
    print("Errors:")
    if report["errors"]:
        for item in report["errors"]:
            print(f"- {item}")
    else:
        print("- None")
    print()
    print("Warnings:")
    if report["warnings"]:
        for item in report["warnings"]:
            print(f"- {item}")
    else:
        print("- None")
    print()
    print("Scripts:")
    if report["scripts"]:
        for script in report["scripts"]:
            print(f"- `{script['path']}` executable={script['executable']} shebang={script['has_shebang']}")
    else:
        print("- None")
    if report.get("validator") is not None:
        print()
        print("Validator:")
        print(f"- Status: `{report['validator']['status']}`")
        output = report["validator"].get("output") or ""
        if output:
            print(f"- Output: `{output}`")


if __name__ == "__main__":
    raise SystemExit(main())
