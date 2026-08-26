"""Render canonical template content for a target repository."""

from pup_core.base.types import RepositoryContext
from pup_core.templates.types import TemplateFile, TemplateSnapshot

__all__ = [
    "read_rendered_template",
    "render_template",
]


def render_template(
    text: str,
    repository: RepositoryContext,
) -> str:
    """Render repository-specific values into template text."""
    replacements = {
        "repo_name": repository.repo_name,
        "github_handle": repository.github_handle,
        "repo_url": repository.repo_url,
        "site_url": repository.site_url,
        "src_package": repository.src_package,
    }

    rendered = text

    for name, value in replacements.items():
        rendered = rendered.replace(
            f"{{{{ {name} }}}}",
            value,
        )
        rendered = rendered.replace(
            f"{{{{{name}}}}}",
            value,
        )

    return rendered


def read_rendered_template(
    *,
    snapshot: TemplateSnapshot,
    template_file: TemplateFile,
    repository: RepositoryContext,
) -> str:
    """Read and render one canonical template file."""
    source_path = snapshot.root / template_file.layer / template_file.template_path

    text = source_path.read_text(encoding="utf-8")

    return render_template(text, repository)
