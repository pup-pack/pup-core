"""Read-only Git and GitHub file-history inspection."""

from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

__all__ = [
    "local_last_changed",
    "remote_last_changed",
]


def local_last_changed(
    *,
    repo_root: Path,
    path: str,
) -> datetime | None:
    """Return when a repository path was last changed in committed Git history."""
    git_executable = shutil.which("git")

    if git_executable is None or not (repo_root / ".git").exists():
        return None

    result = subprocess.run(
        [
            git_executable,
            "log",
            "-1",
            "--format=%cI",
            "--",
            path,
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    if result.returncode != 0:
        return None

    value = result.stdout.strip()

    if not value:
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def remote_last_changed(
    *,
    repository: str,
    path: str,
    ref: str,
) -> datetime | None:
    """Return when a file was last changed in a GitHub repository."""
    encoded_path = quote(path, safe="/")
    encoded_ref = quote(ref, safe="")

    url = (
        f"https://api.github.com/repos/{repository}/commits"
        f"?path={encoded_path}&sha={encoded_ref}&per_page=1"
    )

    headers = {
        "User-Agent": "pup-core",
        "Accept": "application/vnd.github+json",
    }

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url, headers=headers)

    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError, URLError, json.JSONDecodeError:
        return None

    if not isinstance(payload, list) or not payload:
        return None

    first = payload[0]

    if not isinstance(first, dict):
        return None

    commit = first.get("commit")

    if not isinstance(commit, dict):
        return None

    committer = commit.get("committer")

    if not isinstance(committer, dict):
        return None

    value = committer.get("date")

    if not isinstance(value, str) or not value:
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None
