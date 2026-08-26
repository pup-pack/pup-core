"""Load the human-readable repository-inspection capability catalog."""

from importlib.resources import files
import tomllib
from typing import Any

__all__ = ["load_repository_feature_catalog"]


def load_repository_feature_catalog() -> dict[str, Any]:
    """Return the packaged repository-feature catalog."""
    resource = files("pup_core.data").joinpath("repository_features.toml")

    with resource.open("rb") as stream:
        return tomllib.load(stream)
