"""Zensical-specific template helpers."""

from collections.abc import Mapping
from copy import deepcopy
from typing import Any

__all__ = [
    "merge_zensical_project_navigation",
]


def merge_zensical_project_navigation(
    *,
    template_data: Mapping[str, Any],
    repository_data: Mapping[str, Any],
) -> dict[str, Any]:
    """Preserve repository-specific navigation in a canonical Zensical baseline.

    The canonical template governs shared configuration. Repository-specific
    navigation remains local when present.
    """
    merged = deepcopy(dict(template_data))

    template_project = _mapping(merged.get("project"))
    repository_project = _mapping(repository_data.get("project"))

    if "nav" in repository_project:
        template_project["nav"] = deepcopy(repository_project["nav"])

    merged["project"] = template_project

    return merged


def _mapping(value: object) -> dict[str, Any]:
    """Return a mapping value or an empty mapping."""
    return dict(value) if isinstance(value, dict) else {}
