"""Python source-file inspection."""

import ast
from pathlib import Path

from pup_core.base.types import RepositoryContext

__all__ = [
    "extract_module_docstring",
    "is_python_source_file",
    "list_python_source_files",
    "read_module_docstring",
]


def is_python_source_file(path: Path) -> bool:
    """Return whether a path is a Python source file."""
    return path.is_file() and path.suffix == ".py"


def extract_module_docstring(source: str) -> str | None:
    """Return a Python module docstring from source text."""
    try:
        module = ast.parse(source)
    except SyntaxError:
        return None

    return ast.get_docstring(module, clean=True)


def read_module_docstring(path: Path) -> str | None:
    """Return a Python module docstring from a source file."""
    if not is_python_source_file(path):
        return None

    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None

    return extract_module_docstring(source)


def list_python_source_files(
    repository: RepositoryContext,
) -> tuple[Path, ...]:
    """Return Python source files for a detected repository."""
    root = repository.root

    if repository.src_package:
        package_root = root / "src" / repository.src_package

        if package_root.is_dir():
            return tuple(
                sorted(path for path in package_root.rglob("*.py") if path.is_file())
            )

    src_root = root / "src"

    if src_root.is_dir():
        return tuple(sorted(path for path in src_root.rglob("*.py") if path.is_file()))

    return tuple(sorted(path for path in root.glob("*.py") if path.is_file()))
