#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Validate the public illustrated-paper-guide skill package."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_SKILLS = {
    "illustrated-paper-guide": "teaching-diagram-maker",
    "teaching-diagram-maker": None,
}
REQUIRED_ROOT_FILES = ["README.md", "LICENSE", "AGENTS.md", ".gitignore"]
EXPECTED_LICENSE = "MIT-0"
PUBLIC_GIT_IDENTITY = "Illustrated Paper Guide contributors"
FORBIDDEN_TEXT = [
    "/" "Users/",
    "/" "home/",
    "C:" "\\Users\\",
]
FORBIDDEN_BINARY_SUFFIXES = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".tiff",
    ".webp",
}
TEXT_SUFFIXES = {"", ".md", ".json", ".yaml", ".yml", ".py", ".txt"}
EMAIL_PATTERN = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+[.][A-Z]{2,}", re.IGNORECASE)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        fail(errors, f"{path.relative_to(ROOT)}: missing valid YAML frontmatter")
        return {}
    parsed: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def validate_skill(name: str, companion: str | None, errors: list[str]) -> None:
    skill_dir = ROOT / "skills" / name
    required = ["SKILL.md", "meta.json", "agents/openai.yaml"]
    for relative in required:
        if not (skill_dir / relative).is_file():
            fail(errors, f"skills/{name}/{relative}: required file is missing")

    skill_path = skill_dir / "SKILL.md"
    if not skill_path.is_file():
        return

    frontmatter = parse_frontmatter(skill_path, errors)
    if frontmatter.get("name") != name:
        fail(errors, f"skills/{name}/SKILL.md: frontmatter name must match directory")
    description = frontmatter.get("description")
    if not description:
        fail(errors, f"skills/{name}/SKILL.md: description is required")
    if frontmatter.get("license") != EXPECTED_LICENSE:
        fail(
            errors,
            f"skills/{name}/SKILL.md: license must be {EXPECTED_LICENSE}",
        )

    try:
        metadata = json.loads((skill_dir / "meta.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"skills/{name}/meta.json: invalid JSON: {exc}")
        metadata = {}
    if metadata.get("slug") != name:
        fail(errors, f"skills/{name}/meta.json: slug must match directory")
    if metadata.get("entry_point") != "SKILL.md":
        fail(errors, f"skills/{name}/meta.json: entry_point must be SKILL.md")

    try:
        openai_text = (skill_dir / "agents/openai.yaml").read_text(encoding="utf-8")
    except OSError as exc:
        fail(errors, f"skills/{name}/agents/openai.yaml: cannot read file: {exc}")
        openai_text = ""
    if not re.search(r"^interface:\s*$", openai_text, re.MULTILINE):
        fail(errors, f"skills/{name}/agents/openai.yaml: interface is required")

    if companion:
        content = skill_path.read_text(encoding="utf-8")
        if companion not in content:
            fail(errors, f"skills/{name}/SKILL.md: missing companion {companion}")


def scan_repository(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if path.suffix.lower() in FORBIDDEN_BINARY_SUFFIXES:
            fail(errors, f"{relative}: binary paper/image asset must not be bundled")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            fail(errors, f"{relative}: text file is not valid UTF-8")
            continue
        for marker in FORBIDDEN_TEXT:
            if marker in content:
                fail(errors, f"{relative}: contains private marker {marker!r}")
        if EMAIL_PATTERN.search(content):
            fail(errors, f"{relative}: contains an email address")
        if re.search(r"\[(?:TODO|FIXME)(?::|\])", content, re.IGNORECASE):
            fail(errors, f"{relative}: contains unfinished TODO/FIXME marker")


def scan_git_metadata(errors: list[str]) -> None:
    if not (ROOT / ".git").exists():
        return
    try:
        result = subprocess.run(
            ["git", "log", "--all", "--format=%an%x00%ae%x00%cn%x00%ce"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(errors, f"could not inspect Git author metadata: {exc}")
        return
    for line in result.stdout.splitlines():
        fields = line.split("\0")
        if len(fields) != 4:
            fail(errors, "Git history returned malformed identity metadata")
            continue
        author_name, author_email, committer_name, committer_email = fields
        for role, name, email in (
            ("author", author_name, author_email),
            ("committer", committer_name, committer_email),
        ):
            if name != PUBLIC_GIT_IDENTITY:
                fail(errors, f"Git history contains a non-public {role} name")
            if not email.endswith("@users.noreply.github.com"):
                fail(errors, f"Git history contains a non-noreply {role} email")


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_ROOT_FILES:
        if not (ROOT / relative).is_file():
            fail(errors, f"{relative}: required root file is missing")
    for name, companion in EXPECTED_SKILLS.items():
        validate_skill(name, companion, errors)
    try:
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    except OSError as exc:
        fail(errors, f"LICENSE: cannot read file: {exc}")
    else:
        if not license_text.startswith("MIT No Attribution\n"):
            fail(errors, "LICENSE: must contain the canonical MIT-0 license")
    if (ROOT / "CLAUDE.md").exists():
        fail(errors, "CLAUDE.md: duplicate root instructions; use AGENTS.md only")
    scan_repository(errors)
    scan_git_metadata(errors)

    if errors:
        print("Package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Package validation passed")
    print(f"Validated {len(EXPECTED_SKILLS)} bundled skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
