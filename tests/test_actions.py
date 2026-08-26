"""Tests for GitHub Actions inspection."""

from pathlib import Path

from pup_core.inspect.actions import inspect_workflow, list_workflow_files


def test_inspect_workflow_action_versions(tmp_path: Path) -> None:
    """Action references distinguish moving majors from exact pins."""
    workflow = tmp_path / "ci.yml"
    workflow.write_text(
        """name: CI

jobs:
  test:
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.0.1
""",
        encoding="utf-8",
    )

    info = inspect_workflow(workflow)

    assert info.name == "CI"
    assert info.actions[0].version_style == "major"
    assert info.actions[1].version_style == "exact"


def test_list_workflow_files(tmp_path: Path) -> None:
    """Workflow files are discovered under .github/workflows."""
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    first = workflows / "ci.yml"
    second = workflows / "deploy.yaml"
    first.write_text("name: CI\n", encoding="utf-8")
    second.write_text("name: Deploy\n", encoding="utf-8")

    assert list_workflow_files(tmp_path) == (first, second)
