"""Typed records for canonical template access."""

from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "TemplateFile",
    "TemplateSnapshot",
    "TemplateSource",
]


@dataclass(frozen=True)
class TemplateFile:
    """One effective file supplied by a template layer."""

    layer: str
    template_path: str
    target_path: str


@dataclass(frozen=True)
class TemplateSnapshot:
    """Resolved canonical template snapshot."""

    root: Path
    repository: str
    ref: str
    from_local: bool


@dataclass(frozen=True)
class TemplateSource:
    """Location of the canonical template repository."""

    repository: str = "pup-pack/templates"
    ref: str = "main"
    local_path: Path | None = None
