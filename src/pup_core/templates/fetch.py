"""Fetch canonical template snapshots without modifying target repositories."""

from collections.abc import Iterator
from contextlib import contextmanager
import io
import json
import os
from pathlib import Path
import re
import tarfile
from tempfile import TemporaryDirectory
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from pup_core.templates.types import TemplateSnapshot, TemplateSource

__all__ = [
    "fetch_template_snapshot",
    "resolve_ref_to_commit",
]

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


@contextmanager
def fetch_template_snapshot(
    *,
    source: TemplateSource,
) -> Iterator[TemplateSnapshot]:
    """Resolve a template source to one local immutable snapshot."""
    if source.local_path is not None:
        yield TemplateSnapshot(
            root=source.local_path.expanduser().resolve(),
            repository=source.repository,
            ref=source.ref,
            from_local=True,
        )
        return

    commit = resolve_ref_to_commit(
        repository=source.repository,
        ref=source.ref,
    )

    url = f"https://codeload.github.com/{source.repository}/tar.gz/{commit}"
    request = Request(url, headers=_github_headers())

    try:
        with urlopen(request, timeout=60) as response:
            archive_bytes = response.read()
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"Could not download template snapshot: {url}") from exc

    with TemporaryDirectory(prefix="pup-core-templates-") as raw_destination:
        destination = Path(raw_destination)

        try:
            with tarfile.open(
                fileobj=io.BytesIO(archive_bytes),
                mode="r:gz",
            ) as archive:
                archive.extractall(
                    path=destination,
                    filter="data",
                )
        except (tarfile.TarError, OSError) as exc:
            raise RuntimeError(f"Could not extract template snapshot: {url}") from exc

        directories = [entry for entry in destination.iterdir() if entry.is_dir()]

        if len(directories) != 1:
            raise RuntimeError(f"Unexpected template snapshot layout: {url}")

        yield TemplateSnapshot(
            root=directories[0],
            repository=source.repository,
            ref=commit,
            from_local=False,
        )


def resolve_ref_to_commit(
    *,
    repository: str,
    ref: str,
) -> str:
    """Resolve a GitHub branch or tag to an immutable commit SHA."""
    if _SHA_RE.fullmatch(ref):
        return ref

    url = f"https://api.github.com/repos/{repository}/commits/{quote(ref, safe='/')}"
    headers = _github_headers()
    headers["Accept"] = "application/vnd.github.sha"
    request = Request(url, headers=headers)

    try:
        with urlopen(request, timeout=30) as response:
            value = response.read().decode("utf-8").strip()
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"Could not resolve template ref: {url}") from exc

    if _SHA_RE.fullmatch(value):
        return value

    try:
        payload = json.loads(value)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Unexpected GitHub ref response: {value!r}") from exc

    sha = payload.get("sha", "") if isinstance(payload, dict) else ""

    if not isinstance(sha, str) or not _SHA_RE.fullmatch(sha):
        raise RuntimeError(f"Unexpected GitHub ref response: {value!r}")

    return sha


def _github_headers() -> dict[str, str]:
    """Return standard GitHub request headers."""
    headers = {
        "User-Agent": "pup-core",
        "Accept": "application/vnd.github+json",
    }

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers
