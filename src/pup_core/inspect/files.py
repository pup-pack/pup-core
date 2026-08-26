"""Repository file inspection."""

from pathlib import Path

__all__ = [
    "find_files_by_suffix",
    "is_python_source_path",
    "list_repository_files",
]

_DEFAULT_IGNORED_DIRECTORIES = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "htmlcov",
        "site",
    }
)


def list_repository_files(
    root: Path,
    *,
    ignored_directories: frozenset[str] = _DEFAULT_IGNORED_DIRECTORIES,
) -> tuple[Path, ...]:
    """Return authored repository files beneath a root."""
    files: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        relative = path.relative_to(root)

        if any(part in ignored_directories for part in relative.parts):
            continue

        files.append(relative)

    return tuple(sorted(files))


def find_files_by_suffix(
    root: Path,
    suffix: str,
) -> tuple[Path, ...]:
    """Return repository-relative files matching a suffix."""
    return tuple(path for path in list_repository_files(root) if path.suffix == suffix)


def is_python_source_path(path: Path) -> bool:
    """Return whether a path represents authored Python source."""
    return path.suffix == ".py" and "__pycache__" not in path.parts
