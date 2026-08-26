"""Tests for shared typed records."""

from pathlib import Path

from pup_core.base.types import (
    GitInfo,
    ManagedSection,
    PackageInfo,
    PyprojectInfo,
    RepositoryContext,
    SectionPlan,
)


def test_repository_context() -> None:
    """RepositoryContext stores detected repository facts."""
    context = RepositoryContext(
        root=Path("repo"),
        github_handle="pup-pack",
        repo_name="example",
        repo_url="https://github.com/pup-pack/example",
        site_url="https://pup-pack.github.io/example/",
        src_package="example",
        files=frozenset({"pyproject.toml", "src/example/__init__.py"}),
    )

    assert context.repo_name == "example"
    assert context.src_package == "example"
    assert "pyproject.toml" in context.files


def test_git_info() -> None:
    """GitInfo stores detected Git facts."""
    info = GitInfo(
        origin_url="https://github.com/pup-pack/example.git",
        github_owner="pup-pack",
        github_repo="example",
        tracked_files=frozenset({"README.md"}),
        untracked_files=frozenset({"notes.txt"}),
        ignored_files=frozenset({".venv/"}),
        dirty=True,
    )

    assert info.github_owner == "pup-pack"
    assert info.github_repo == "example"
    assert info.dirty is True


def test_package_info() -> None:
    """PackageInfo stores detected package facts."""
    info = PackageInfo(
        src_layout=True,
        packages=("example",),
        primary_package="example",
    )

    assert info.src_layout is True
    assert info.primary_package == "example"


def test_pyproject_info() -> None:
    """PyprojectInfo stores selected project metadata."""
    info = PyprojectInfo(
        path=Path("pyproject.toml"),
        project_name="example",
        requires_python=">=3.15",
        dependencies=("requests",),
        dependency_groups={"dev": ("pytest",)},
        optional_dependencies={},
        scripts={"example": "example.cli:main"},
        build_backend="hatchling.build",
        uv_default_groups="all",
        ruff_target_version="py315",
        pytest_testpaths=("tests",),
        pytest_addopts="--cov=example",
        hatch_version_file="src/example/_version.py",
        hatch_wheel_packages=("src/example",),
    )

    assert info.project_name == "example"
    assert info.dependency_groups["dev"] == ("pytest",)
    assert info.uv_default_groups == "all"


def test_managed_section_and_plan() -> None:
    """Section records store section boundaries and planned operations."""
    section = ManagedSection(
        name="example",
        start_marker="# BEGIN\n",
        end_marker="# END\n",
        start_index=0,
        end_index=20,
        content_start=8,
        content_end=14,
        content="value\n",
    )

    plan = SectionPlan(
        name="example",
        action="replace",
        start_marker="# BEGIN\n",
        end_marker="# END\n",
        current=section,
        desired_content="new\n",
    )

    assert plan.action == "replace"
    assert plan.current == section
    assert plan.desired_content == "new\n"
