"""Repository path helpers so scripts and notebooks work from any working directory."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """Return the course repository root: the directory with ``pyproject.toml`` and ``python/src``.

    Works in the development repository and in the participant repository.
    """
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").is_file() and (
            parent / "python/src/energy_training"
        ).is_dir():
            return parent
    raise FileNotFoundError("Course repository root not found above " + str(here))
