"""Read-only file and history comparison primitives."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

__all__ = [
    "FileComparison",
    "FileRelationship",
    "classify_file_relationship",
    "compare_text_files",
]

FileRelationship = Literal[
    "same",
    "different",
    "left-only",
    "right-only",
    "left-newer",
    "right-newer",
]


@dataclass(frozen=True)
class FileComparison:
    """Facts about two corresponding files."""

    left_path: Path
    right_path: Path
    relationship: FileRelationship
    left_text: str | None
    right_text: str | None
    left_changed: datetime | None = None
    right_changed: datetime | None = None


def compare_text_files(
    *,
    left_path: Path,
    right_path: Path,
    left_changed: datetime | None = None,
    right_changed: datetime | None = None,
) -> FileComparison:
    """Compare two UTF-8 text files without modifying either file."""
    left_text = _read_text(left_path)
    right_text = _read_text(right_path)

    relationship = classify_file_relationship(
        left_exists=left_path.is_file(),
        right_exists=right_path.is_file(),
        left_text=left_text,
        right_text=right_text,
        left_changed=left_changed,
        right_changed=right_changed,
    )

    return FileComparison(
        left_path=left_path,
        right_path=right_path,
        relationship=relationship,
        left_text=left_text,
        right_text=right_text,
        left_changed=left_changed,
        right_changed=right_changed,
    )


def classify_file_relationship(
    *,
    left_exists: bool,
    right_exists: bool,
    left_text: str | None,
    right_text: str | None,
    left_changed: datetime | None = None,
    right_changed: datetime | None = None,
) -> FileRelationship:
    """Classify corresponding files using presence, content, and history."""
    if left_exists and not right_exists:
        return "left-only"

    if right_exists and not left_exists:
        return "right-only"

    if left_text == right_text:
        return "same"

    if left_changed is not None and right_changed is not None:
        if left_changed > right_changed:
            return "left-newer"

        if right_changed > left_changed:
            return "right-newer"

    return "different"


def _read_text(path: Path) -> str | None:
    """Read UTF-8 text when the path is a readable file."""
    if not path.is_file():
        return None

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
