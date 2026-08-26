"""GitHub Actions workflow inspection."""

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Literal

__all__ = [
    "ActionReference",
    "ActionVersionStyle",
    "WorkflowInfo",
    "inspect_workflow",
    "list_workflow_files",
]

ActionVersionStyle = Literal[
    "major",
    "exact",
    "sha",
    "branch-or-other",
]

# Match GitHub Actions step references such as:
#   - uses: actions/checkout@v7
#   - uses: astral-sh/setup-uv@v10.0.1
#
# ^                 Start of a line.
# \s*               Allow indentation before the YAML list item.
# -                 Require the YAML list marker used for a workflow step.
# \s*               Allow spaces after the list marker.
# uses:             Require the GitHub Actions `uses:` key.
# \s*               Allow spaces after the colon.
# (?P<action>       Capture the action name as `action`.
#   [^\s@]+         Read non-whitespace characters up to the `@` separator.
# )
# @                 Require the separator between action name and Git ref.
# (?P<ref>          Capture the Git ref as `ref`.
#   [^\s#]+         Read until whitespace or a YAML comment begins.
# )
#
# re.MULTILINE makes ^ apply to the beginning of every workflow line,
# not only the beginning of the entire file.
_USES_RE = re.compile(
    r"^\s*-\s*uses:\s*(?P<action>[^\s@]+)@(?P<ref>[^\s#]+)",
    re.MULTILINE,
)


# Match the top-level workflow name, for example:
#   name: CI
#   name: Docs Deploy (Zensical)
#
# ^                 Start of a line.
# name:             Require the YAML `name:` key.
# \s*               Allow spaces after the colon.
# (?P<name>         Capture the workflow name as `name`.
#   .+?             Match one or more characters, minimally.
# )
# \s*               Allow trailing whitespace.
# $                 Require the end of the line.
#
# re.MULTILINE makes ^ and $ operate on individual lines.
_NAME_RE = re.compile(
    r"^name:\s*(?P<name>.+?)\s*$",
    re.MULTILINE,
)


# Match an immutable 40-character Git commit SHA, for example:
#   3b7c4f1e2d8a9b0c1234567890abcdef12345678
#
# ^                 Start of the entire string.
# [0-9a-fA-F]       Allow hexadecimal digits in either case.
# {40}              Require exactly 40 hexadecimal characters.
# $                 Require the end of the string.
_SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")


# Match a moving major-version GitHub Action tag, for example:
#   v7
#   v10
#
# ^                 Start of the entire string.
# v                 Require the conventional leading `v`.
# \d+               Require one or more digits for the major version.
# $                 Require the end of the string.
#
# These are the preferred moving-major references for the PUP baseline.
_MAJOR_RE = re.compile(r"^v\d+$")


# Match an explicitly pinned semantic-version-style action tag, for example:
#   v10.0
#   v10.0.1
#
# ^                 Start of the entire string.
# v                 Require the conventional leading `v`.
# \d+               Require the major version.
# (?:               Begin a non-capturing repeated group.
#   \.               Require a literal period.
#   \d+              Require the next numeric version component.
# )
# {1,2}             Require one or two additional components:
#                   `vMAJOR.MINOR` or `vMAJOR.MINOR.PATCH`.
# $                 Require the end of the string.
_EXACT_RE = re.compile(r"^v\d+(?:\.\d+){1,2}$")


@dataclass(frozen=True)
class ActionReference:
    """One external action reference in a workflow."""

    action: str
    ref: str
    version_style: ActionVersionStyle


@dataclass(frozen=True)
class WorkflowInfo:
    """Selected facts about one GitHub Actions workflow."""

    path: Path
    name: str
    actions: tuple[ActionReference, ...]


def list_workflow_files(root: Path) -> tuple[Path, ...]:
    """Return GitHub Actions workflow files in a repository."""
    workflow_root = root / ".github" / "workflows"

    if not workflow_root.is_dir():
        return ()

    return tuple(
        sorted(
            path
            for path in workflow_root.iterdir()
            if path.is_file() and path.suffix.lower() in {".yml", ".yaml"}
        )
    )


def inspect_workflow(path: Path) -> WorkflowInfo:
    """Inspect one GitHub Actions workflow without modifying it."""
    text = path.read_text(encoding="utf-8")

    name_match = _NAME_RE.search(text)
    name = name_match.group("name").strip() if name_match else path.stem

    actions = tuple(
        ActionReference(
            action=match.group("action"),
            ref=match.group("ref"),
            version_style=_classify_ref(match.group("ref")),
        )
        for match in _USES_RE.finditer(text)
    )

    return WorkflowInfo(
        path=path,
        name=name,
        actions=actions,
    )


def _classify_ref(ref: str) -> ActionVersionStyle:
    """Classify a GitHub Action reference."""
    if _SHA_RE.fullmatch(ref):
        return "sha"

    if _MAJOR_RE.fullmatch(ref):
        return "major"

    if _EXACT_RE.fullmatch(ref):
        return "exact"

    return "branch-or-other"
