"""Template-layer discovery and effective-file selection."""

from pathlib import Path

from pup_core.templates.types import TemplateFile, TemplateSnapshot

__all__ = [
    "infer_layers",
    "list_template_files",
]


def infer_layers(
    *,
    repo_root: Path,
    repo_name: str,
    files: set[str],
) -> list[str]:
    """Infer additive template layers from repository structure.

    Args:
        repo_root: Repository root.
        repo_name: Repository name.
        files: Repository-relative file markers.

    Returns:
        Ordered additive template layers.
    """
    del repo_name

    has_py = "pyproject.toml" in files
    has_src = (repo_root / "src").is_dir()
    has_pypi = has_py and _is_pypi_project(repo_root)

    layers = ["ALL"]

    if has_py:
        layers.append("ALL-PY")

    if has_py and has_src:
        layers.append("ALL-PY-SRC")

    if has_py and has_src and has_pypi:
        layers.append("ALL-PY-SRC-PYPI")

    return layers


def list_template_files(
    *,
    snapshot: TemplateSnapshot,
    layers: tuple[str, ...] | list[str],
) -> list[TemplateFile]:
    """Return effective template files for selected additive layers.

    Later layers override earlier layers for the same target path.
    """
    by_target: dict[str, TemplateFile] = {}

    for layer in layers:
        layer_root = snapshot.root / layer

        if not layer_root.is_dir():
            continue

        for source_path in sorted(layer_root.rglob("*")):
            if not source_path.is_file():
                continue

            relative_path = source_path.relative_to(layer_root).as_posix()

            if _ignore_template_internal_file(relative_path):
                continue

            target_path = relative_path.removesuffix(".template")

            by_target[target_path] = TemplateFile(
                layer=layer,
                template_path=relative_path,
                target_path=target_path,
            )

    return sorted(
        by_target.values(),
        key=lambda item: item.target_path,
    )


def _is_pypi_project(repo_root: Path) -> bool:
    """Return whether repository metadata indicates a published package."""
    pyproject_path = repo_root / "pyproject.toml"

    if not pyproject_path.is_file():
        return False

    text = pyproject_path.read_text(encoding="utf-8")

    return (
        "[build-system]" in text
        and "[tool.hatch.version]" in text
        and "[project.urls]" in text
    )


def _ignore_template_internal_file(path: str) -> bool:
    """Return whether a template-repository file is internal metadata."""
    path_obj = Path(path)

    if path_obj.name == ".DS_Store":
        return True

    if "__pycache__" in path_obj.parts:
        return True

    return path_obj.suffix == ".pyc"
