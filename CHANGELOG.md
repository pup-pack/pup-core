# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.2.0] - 2026-08-26

### Added

- Shared canonical template types, fetching, layering, and rendering.
- Shared Git file-history inspection.
- Shared repository file comparison primitives.
- Python source-file inspection and module docstring extraction.
- GitHub Actions workflow inspection and action-version classification.
- Human-readable repository feature catalog for shared inspection capabilities.
- Tests for template, comparison, Python source, and GitHub Actions inspection.

### Changed

- Expanded `pup-core` from basic repository inspection into the shared
  repository-intelligence layer for the PUP tool family.
- Prepared template and inspection functionality for reuse by `pup-up`,
  `pup-down`, `pup-check`, and repository explorer applications.
- Standardized GitHub Action version inspection to distinguish moving major
  versions from exact version pins.

---

## [0.1.3] - 2026-08-13

- updated actions (one source of python version in project root)
- updated pyproject.toml
- deleted pyright; added ty and uv block in pyproject.toml

---

## [0.1.1] - 2026-08-10

- updated the organization

---

## [0.1.0] - 2026-08-09

- moved to pup-pack

---

## [0.0.5] - 2026-08-09

- updated docs/ and README

---

## [0.0.4] - 2026-08-08

### Added

- Added `paths/` utilities for repository-relative path normalization and safe path resolution.
- Added `python/` utilities for Python package-name and version normalization.
- Added `sections/` support for detecting, planning, adding, replacing, and deleting file sections.
- Added shared typed records for Git, package, project metadata, and managed-section operations.
- Added repository inspection support for Git metadata, Python packages, and `pyproject.toml`.
- Added tests for errors, types, repo inspection, path handling, Python normalization, and managed sections.

---

## [0.0.3] - 2026-08-08

### Added

- Initial release of `pup-core`.
- Added shared foundation for the Professional Python Project (`pup`) tool family.
- Added common project types and errors.
- Added repository detection and inspection support.
- Added support for identifying professional Python repository structure.
- Added typed-package support with `py.typed`.
- Added professional project documentation, testing, type checking, linting, CI, and release infrastructure.

---

## Notes on Versioning and Releases

- We use **SemVer**:
  - **MAJOR** - breaking changes
  - **MINOR** - backward-compatible additions
  - **PATCH** - fixes, documentation, tooling
- Versions are driven by git tags.
- Tag `vX.Y.Z` to release.
- Docs are deployed per version tag and aliased to **latest**.

## Release Procedure

Follow these steps when creating a new release.

### Task 1. Update release metadata (manual edits)

1. Update `CITATION.cff`: change `version` and `date-released`
2. Update `CHANGELOG.md`: move from unreleased, add entry, update links
3. Update `pyproject.toml`: update `[tool.hatch.version] fallback-version`

### Task 2. Validate

```shell
uv lock --upgrade
uv sync

uv run pre-commit install

git add -A
uv run pre-commit run --all-files
# rerun if changes made
uv run pre-commit run --all-files

npx markdownlint-cli2 --fix
uvx cffconvert --validate

uv run ty check
uv run python -m pytest
uv run python -m zensical build

uv run python -c "import shutil; from pathlib import Path; shutil.rmtree(Path('dist'), ignore_errors=True)"

uv build
uvx twine check dist/*
```

### Task 3. Commit, push, tag

```shell
git add -A
git commit -m "Prepare X.Y.Z"
git push -u origin main
````.\sh

Verify actions run on GitHub. After success:

```shell
git tag vX.Y.Z -m "X.Y.Z"
git push origin vX.Y.Z
```

## Only As Needed (delete a tag)

```shell
git tag -d vX.Z.Y
git push origin :refs/tags/vX.Z.Y
```

## Links

[Unreleased]: https://github.com/pup-pack/pup-core/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/pup-pack/pup-core/releases/tag/v0.2.0
[0.1.3]: https://github.com/pup-pack/pup-core/releases/tag/v0.1.3
[0.1.1]: https://github.com/pup-pack/pup-core/releases/tag/v0.1.1
[0.1.0]: https://github.com/pup-pack/pup-core/releases/tag/v0.1.0
[0.0.5]: https://github.com/pup-pack/pup-core/releases/tag/v0.0.5
[0.0.4]: https://github.com/pup-pack/pup-core/releases/tag/v0.0.4
[0.0.3]: https://github.com/pup-pack/pup-core/releases/tag/v0.0.3

<!-- markdownlint-enable MD024 -->
