# pup-core: Professional Python Project Tools: Core Library

[![PyPI](https://img.shields.io/pypi/v/pup-core?logo=pypi&label=pypi)](https://pypi.org/project/pup-core/)
[![Docs Site](https://img.shields.io/badge/docs-site-blue?logo=github)](https://pup-pack.github.io/pup-core/)
[![Repo](https://img.shields.io/badge/repo-GitHub-black?logo=github)](https://github.com/pup-pack/pup-core)
[![Python 3.15](https://img.shields.io/badge/python-3.15%2B-blue?logo=python)](https://github.com/pup-pack/pup-core/blob/main/pyproject.toml)
[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://github.com/pup-pack/pup-core/blob/main/LICENSE)

[![CI](https://github.com/pup-pack/pup-core/actions/workflows/ci-python-zensical.yml/badge.svg?branch=main)](https://github.com/pup-pack/pup-core/actions/workflows/ci-python-zensical.yml)
[![Docs-Deploy](https://github.com/pup-pack/pup-core/actions/workflows/deploy-zensical.yml/badge.svg?branch=main)](https://github.com/pup-pack/pup-core/actions/workflows/deploy-zensical.yml)
[![Pre-Release](https://github.com/pup-pack/pup-core/actions/workflows/pre-release.yml/badge.svg?branch=main)](https://github.com/pup-pack/pup-core/actions/workflows/pre-release.yml)
[![Release](https://github.com/pup-pack/pup-core/actions/workflows/release-pypi.yml/badge.svg)](https://github.com/pup-pack/pup-core/actions/workflows/release-pypi.yml)
[![Links](https://github.com/pup-pack/pup-core/actions/workflows/links.yml/badge.svg?branch=main)](https://github.com/pup-pack/pup-core/actions/workflows/links.yml)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen.svg)](https://github.com/pup-pack/pup-core/security)

<img
src="https://raw.githubusercontent.com/pup-pack/pup-core/main/docs/images/pup.png"
alt="pup logo"
width="110">

> Shared core library for professional Python project tools.

## Purpose

This library centralizes functionality across tools, including:

- repository root and project detection
- `pyproject.toml` inspection
- Python package and source-layout detection
- Python source-file and module-docstring inspection
- notebook detection
- Python version normalization
- project and package name normalization
- safe repository-relative path handling
- Git metadata and file-history inspection
- GitHub Actions workflow and action-version inspection
- canonical template discovery, layering, fetching, and rendering
- reusable file and content comparison
- managed file-section detection and manipulation
- shared immutable types and errors

`pup-core` contains shared repository inspection, template, comparison,
metadata, Git-history, Python-source, and GitHub Actions mechanisms.

## Template Source

- [templates](https://github.com/pup-pack/templates)

## Developer Command Reference

<details>
<summary>Show command reference</summary>

### In a machine terminal

Open a machine terminal where you want the project:

```shell
git clone https://github.com/pup-pack/pup-core

cd pup-core
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.15
uv python install
uv lock --upgrade
uv sync

uv run pre-commit install
uv run pre-commit autoupdate

git add -A
uv run pre-commit run --all-files
# repeat if changes were made
uv run pre-commit run --all-files

# types, tests, docs
uv run ty check
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Documentation

- [Documentation](https://pup-pack.github.io/pup-core/)

## Annotations

[.annotations/annotations.md](https://github.com/pup-pack/pup-core/blob/main/.annotations/annotations.md)

## Citation

[CITATION.cff](https://github.com/pup-pack/pup-core/blob/main/CITATION.cff)

## License

[MIT](https://github.com/pup-pack/pup-core/blob/main/LICENSE)
