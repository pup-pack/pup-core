"""Tests for pyproject.toml inspection."""

from pathlib import Path

import pytest

from pup_core.base.errors import PyprojectError
from pup_core.inspect.pyproject import inspect_pyproject, load_pyproject

PYPROJECT_TEXT = """
[project]
name = "example"
requires-python = ">=3.15"
dependencies = ["requests"]

[project.optional-dependencies]
feature = ["rich"]

[project.scripts]
example = "example.cli:main"

[dependency-groups]
dev = ["pytest", "ruff"]
docs = ["zensical"]

[build-system]
build-backend = "hatchling.build"
requires = ["hatchling", "hatch-vcs"]

[tool.uv]
default-groups = "all"

[tool.ruff]
target-version = "py315"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=example --cov-fail-under=60"

[tool.hatch.build.hooks.vcs]
version-file = "src/example/_version.py"

[tool.hatch.build.targets.wheel]
packages = ["src/example"]
"""


def test_load_pyproject(tmp_path: Path) -> None:
    """Load valid TOML data."""
    path = tmp_path / "pyproject.toml"
    path.write_text(PYPROJECT_TEXT, encoding="utf-8")

    data = load_pyproject(tmp_path)

    assert data["project"]["name"] == "example"


def test_inspect_pyproject(tmp_path: Path) -> None:
    """Extract selected project and tooling facts."""
    path = tmp_path / "pyproject.toml"
    path.write_text(PYPROJECT_TEXT, encoding="utf-8")

    info = inspect_pyproject(tmp_path)

    assert info.project_name == "example"
    assert info.requires_python == ">=3.15"
    assert info.dependencies == ("requests",)
    assert info.optional_dependencies == {"feature": ("rich",)}
    assert info.dependency_groups["dev"] == ("pytest", "ruff")
    assert info.dependency_groups["docs"] == ("zensical",)
    assert info.scripts == {"example": "example.cli:main"}
    assert info.build_backend == "hatchling.build"
    assert info.uv_default_groups == "all"
    assert info.ruff_target_version == "py315"
    assert info.pytest_testpaths == ("tests",)
    assert info.pytest_addopts == "--cov=example --cov-fail-under=60"
    assert info.hatch_version_file == "src/example/_version.py"
    assert info.hatch_wheel_packages == ("src/example",)


def test_load_pyproject_rejects_missing_file(tmp_path: Path) -> None:
    """Raise PyprojectError when pyproject.toml is absent."""
    with pytest.raises(PyprojectError, match="not found"):
        load_pyproject(tmp_path)


def test_load_pyproject_rejects_invalid_toml(tmp_path: Path) -> None:
    """Raise PyprojectError for malformed TOML."""
    path = tmp_path / "pyproject.toml"
    path.write_text("[project\nname = broken", encoding="utf-8")

    with pytest.raises(PyprojectError, match="Invalid pyproject.toml"):
        load_pyproject(tmp_path)
