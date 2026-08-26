"""pyproject.toml inspection."""

from pathlib import Path
import tomllib
from typing import Any, Literal

from pup_core.base.errors import PyprojectError
from pup_core.base.types import PyprojectInfo

__all__ = [
    "inspect_pyproject",
    "load_pyproject",
]


def load_pyproject(root: Path) -> dict[str, Any]:
    """Load pyproject.toml without modifying it."""
    path = root / "pyproject.toml"

    if not path.is_file():
        raise PyprojectError(f"pyproject.toml not found: {path}")

    try:
        with path.open("rb") as file:
            return tomllib.load(file)
    except tomllib.TOMLDecodeError as exc:
        raise PyprojectError(f"Invalid pyproject.toml: {path}") from exc


def inspect_pyproject(root: Path) -> PyprojectInfo:
    """Return selected project and tooling facts from pyproject.toml."""
    data = load_pyproject(root)

    project = _mapping(data.get("project"))
    dependency_groups = _dependency_mapping(data.get("dependency-groups"))
    optional_dependencies = _dependency_mapping(project.get("optional-dependencies"))

    tool = _mapping(data.get("tool"))
    uv = _mapping(tool.get("uv"))
    ruff = _mapping(tool.get("ruff"))

    pytest = _mapping(tool.get("pytest"))
    pytest_ini = _mapping(pytest.get("ini_options"))

    hatch = _mapping(tool.get("hatch"))
    hatch_build = _mapping(hatch.get("build"))
    hatch_targets = _mapping(hatch_build.get("targets"))
    hatch_wheel = _mapping(hatch_targets.get("wheel"))
    hatch_hooks = _mapping(hatch_build.get("hooks"))
    hatch_vcs_hook = _mapping(hatch_hooks.get("vcs"))

    build_system = _mapping(data.get("build-system"))

    return PyprojectInfo(
        path=root / "pyproject.toml",
        project_name=_string(project.get("name")),
        requires_python=_string(project.get("requires-python")),
        dependencies=_string_tuple(project.get("dependencies")),
        dependency_groups=dependency_groups,
        optional_dependencies=optional_dependencies,
        scripts=_string_mapping(project.get("scripts")),
        build_backend=_string(build_system.get("build-backend")),
        uv_default_groups=_uv_default_groups(uv.get("default-groups")),
        ruff_target_version=_string(ruff.get("target-version")),
        pytest_testpaths=_string_tuple(pytest_ini.get("testpaths")),
        pytest_addopts=_string(pytest_ini.get("addopts")),
        hatch_version_file=_string(hatch_vcs_hook.get("version-file")),
        hatch_wheel_packages=_string_tuple(hatch_wheel.get("packages")),
    )


def _mapping(value: object) -> dict[str, Any]:
    """Return a mapping value or an empty mapping."""
    return dict(value) if isinstance(value, dict) else {}


def _string(value: object) -> str:
    """Return a string value or an empty string."""
    return value if isinstance(value, str) else ""


def _string_tuple(value: object) -> tuple[str, ...]:
    """Return a tuple containing only string values."""
    if not isinstance(value, list):
        return ()

    return tuple(item for item in value if isinstance(item, str))


def _string_mapping(value: object) -> dict[str, str]:
    """Return a string-to-string mapping."""
    if not isinstance(value, dict):
        return {}

    return {
        key: item
        for key, item in value.items()
        if isinstance(key, str) and isinstance(item, str)
    }


def _dependency_mapping(value: object) -> dict[str, tuple[str, ...]]:
    """Return dependency groups as immutable value tuples."""
    if not isinstance(value, dict):
        return {}

    result: dict[str, tuple[str, ...]] = {}

    for key, items in value.items():
        if isinstance(key, str) and isinstance(items, list):
            result[key] = tuple(item for item in items if isinstance(item, str))

    return result


def _uv_default_groups(
    value: object,
) -> tuple[str, ...] | Literal["all"] | None:
    """Normalize uv default-groups."""
    if value == "all":
        return "all"

    if isinstance(value, list):
        return tuple(item for item in value if isinstance(item, str))

    return None
