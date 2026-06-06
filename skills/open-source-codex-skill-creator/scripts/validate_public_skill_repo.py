#!/usr/bin/env python3
"""Validate the basic shape of a public open source Codex skill repository."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_ROOT_FILES = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/test.yml",
]


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        _, raw, _ = text.split("---", 2)
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc

    values: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def validate_skill(skill_dir: Path) -> list[str]:
    failures: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir}: missing SKILL.md"]

    try:
        frontmatter = parse_frontmatter(skill_md)
    except ValueError as exc:
        return [f"{skill_md}: {exc}"]

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        failures.append(f"{skill_md}: invalid or missing hyphen-case name")
    if name and skill_dir.name != name:
        failures.append(f"{skill_dir}: folder name must match frontmatter name '{name}'")
    if not description or len(description) > 1024:
        failures.append(f"{skill_md}: description missing or longer than 1024 characters")
    if "<" in description or ">" in description:
        failures.append(f"{skill_md}: description cannot contain angle brackets")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        failures.append(f"{skill_dir}: missing agents/openai.yaml")
    else:
        openai_text = openai_yaml.read_text(encoding="utf-8")
        for token in ("interface:", "display_name:", "short_description:", "default_prompt:"):
            if token not in openai_text:
                failures.append(f"{openai_yaml}: missing {token}")
        if f"${name}" not in openai_text:
            failures.append(f"{openai_yaml}: default_prompt should mention ${name}")

    for forbidden in ("README.md", "CHANGELOG.md", "CONTRIBUTING.md", "INSTALLATION_GUIDE.md"):
        if (skill_dir / forbidden).exists():
            failures.append(f"{skill_dir}: move {forbidden} to repo root")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("--skill", help="Specific skill folder name under skills/")
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    failures: list[str] = []
    if not repo.exists():
        print(f"Repository path does not exist: {repo}")
        return 2

    for rel_path in REQUIRED_ROOT_FILES:
        if not (repo / rel_path).exists():
            failures.append(f"missing required file: {rel_path}")

    license_text = (repo / "LICENSE").read_text(encoding="utf-8") if (repo / "LICENSE").exists() else ""
    if "MIT License" not in license_text:
        failures.append("LICENSE should contain MIT License unless another OSI license was requested")

    skills_dir = repo / "skills"
    if args.skill:
        skill_dirs = [skills_dir / args.skill]
    elif skills_dir.exists():
        skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    else:
        skill_dirs = []

    if not skill_dirs:
        failures.append("no skill folders found under skills/")
    for skill_dir in skill_dirs:
        failures.extend(validate_skill(skill_dir))

    if failures:
        print("Public skill repo validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 2

    print("Public skill repo is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
