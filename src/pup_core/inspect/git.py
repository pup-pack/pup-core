"""Git repository inspection."""

from pathlib import Path
import re
import shutil
import subprocess

from pup_core.base.types import GitInfo

__all__ = ["inspect_git"]


_GITHUB_REMOTE_RE = re.compile(
    r"(?:git@github\.com:|https://github\.com/)"
    r"(?P<owner>[^/\s]+)/(?P<repo>[^/\s]+?)"
    r"(?:\.git)?/?$"
)


def inspect_git(root: Path) -> GitInfo:
    """Inspect Git facts without modifying the repository."""
    origin_url = _run_git(root, "config", "--get", "remote.origin.url")
    github_owner, github_repo = _parse_github_remote(origin_url)

    tracked_files = _lines(_run_git(root, "ls-files"))
    untracked_files = _lines(
        _run_git(root, "ls-files", "--others", "--exclude-standard")
    )
    ignored_files = _lines(
        _run_git(
            root,
            "ls-files",
            "--others",
            "--ignored",
            "--exclude-standard",
        )
    )

    status = _run_git(root, "status", "--porcelain")

    return GitInfo(
        origin_url=origin_url,
        github_owner=github_owner,
        github_repo=github_repo,
        tracked_files=frozenset(tracked_files),
        untracked_files=frozenset(untracked_files),
        ignored_files=frozenset(ignored_files),
        dirty=bool(status.strip()),
    )


def _run_git(root: Path, *args: str) -> str:
    """Run a read-only Git command and return stdout."""
    if not (root / ".git").exists():
        return ""

    git_executable = shutil.which("git")
    if git_executable is None:
        return ""

    result = subprocess.run(
        [git_executable, *args],
        cwd=root,
        capture_output=True,
        check=False,
        text=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        return ""

    return result.stdout.strip()


def _parse_github_remote(url: str) -> tuple[str, str]:
    """Return GitHub owner and repository name from a remote URL."""
    match = _GITHUB_REMOTE_RE.fullmatch(url.strip())

    if match is None:
        return "", ""

    return match.group("owner"), match.group("repo")


def _lines(value: str) -> set[str]:
    """Return non-empty normalized output lines."""
    return {
        line.strip().replace("\\", "/") for line in value.splitlines() if line.strip()
    }
