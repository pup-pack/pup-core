"""Tests for shared template primitives."""

from pathlib import Path

from pup_core.base.types import RepositoryContext
from pup_core.templates.baseline import list_template_files
from pup_core.templates.render import render_template
from pup_core.templates.types import TemplateSnapshot


def test_render_template_src_package(tmp_path: Path) -> None:
    """Repository package tokens are rendered."""
    repository = RepositoryContext(
        root=tmp_path,
        github_handle="pup-pack",
        repo_name="example-project",
        repo_url="https://github.com/pup-pack/example-project",
        site_url="https://pup-pack.github.io/example-project/",
        src_package="example_package",
        files=frozenset(),
    )

    assert render_template("{{ src_package }}", repository) == "example_package"


def test_later_template_layer_overrides_earlier(tmp_path: Path) -> None:
    """Later additive layers supersede the same target path."""
    (tmp_path / "ALL").mkdir()
    (tmp_path / "ALL-PY").mkdir()
    (tmp_path / "ALL" / "example.txt").write_text(
        "all",
        encoding="utf-8",
    )
    (tmp_path / "ALL-PY" / "example.txt").write_text(
        "python",
        encoding="utf-8",
    )

    snapshot = TemplateSnapshot(
        root=tmp_path,
        repository="pup-pack/templates",
        ref="main",
        from_local=True,
    )

    files = list_template_files(
        snapshot=snapshot,
        layers=("ALL", "ALL-PY"),
    )

    assert len(files) == 1
    assert files[0].layer == "ALL-PY"
