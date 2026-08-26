"""Tests for Python source inspection."""

from pathlib import Path

from pup_core.base.types import RepositoryContext
from pup_core.inspect.python_source import (
    extract_module_docstring,
    list_python_source_files,
    read_module_docstring,
)


def test_extract_module_docstring() -> None:
    """Module docstrings are extracted with Python AST semantics."""
    source = '''"""Example module."""

VALUE = 1
'''

    assert extract_module_docstring(source) == "Example module."


def test_read_module_docstring(tmp_path: Path) -> None:
    """Module docstrings can be read from Python source files."""
    path = tmp_path / "example.py"
    path.write_text('"""Example module."""\n', encoding="utf-8")

    assert read_module_docstring(path) == "Example module."


def test_list_python_source_files(tmp_path: Path) -> None:
    """Source files are listed from the detected source package."""
    package = tmp_path / "src" / "example_package"
    package.mkdir(parents=True)

    (package / "__init__.py").write_text(
        '"""Package."""\n',
        encoding="utf-8",
    )
    (package / "app.py").write_text(
        '"""App."""\n',
        encoding="utf-8",
    )

    repository = RepositoryContext(
        root=tmp_path,
        github_handle="example",
        repo_name="example-project",
        repo_url="https://github.com/example/example-project",
        site_url="https://example.github.io/example-project/",
        src_package="example_package",
        files=frozenset(),
    )

    result = list_python_source_files(repository)

    assert result == (
        package / "__init__.py",
        package / "app.py",
    )
