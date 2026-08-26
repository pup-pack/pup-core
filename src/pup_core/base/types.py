"""Shared typed records."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

__all__ = [
    "GitInfo",
    "ManagedSection",
    "PackageInfo",
    "PyprojectInfo",
    "RepositoryContext",
    "SectionAction",
    "SectionPlan",
]


@dataclass(frozen=True)
class GitInfo:
    """Detected Git repository information."""

    origin_url: str
    github_owner: str
    github_repo: str
    tracked_files: frozenset[str]
    untracked_files: frozenset[str]
    ignored_files: frozenset[str]
    dirty: bool


@dataclass(frozen=True)
class PackageInfo:
    """Detected Python package information."""

    src_layout: bool
    packages: tuple[str, ...]
    primary_package: str


@dataclass(frozen=True)
class PyprojectInfo:
    """Selected facts read from pyproject.toml."""

    path: Path
    project_name: str
    requires_python: str
    dependencies: tuple[str, ...]
    dependency_groups: dict[str, tuple[str, ...]]
    optional_dependencies: dict[str, tuple[str, ...]]
    scripts: dict[str, str]
    build_backend: str
    uv_default_groups: tuple[str, ...] | Literal["all"] | None
    ruff_target_version: str
    pytest_testpaths: tuple[str, ...]
    pytest_addopts: str
    hatch_version_file: str
    hatch_wheel_packages: tuple[str, ...]


@dataclass(frozen=True)
class RepositoryContext:
    """Detected information about a target repository."""

    root: Path
    github_handle: str
    repo_name: str
    repo_url: str
    site_url: str
    src_package: str
    files: frozenset[str]


@dataclass(frozen=True)
class ManagedSection:
    """A uniquely identified managed section in file text."""

    name: str
    start_marker: str
    end_marker: str
    start_index: int
    end_index: int
    content_start: int
    content_end: int
    content: str


SectionAction = Literal[
    "unchanged",
    "add",
    "replace",
    "delete",
]


@dataclass(frozen=True)
class SectionPlan:
    """Planned operation for one explicitly managed section."""

    name: str
    action: SectionAction
    start_marker: str
    end_marker: str
    current: ManagedSection | None
    desired_content: str | None
    insert_before_marker: str | None = None
