"""Smoke tests: the package imports and the utilities behave."""

import importlib.util

import numpy as np

import energy_training
from energy_training.utilities import celsius_to_kelvin, kelvin_to_celsius, repo_root


def test_version():
    assert energy_training.__version__


def test_temperature_roundtrip():
    t = np.array([-10.0, 0.0, 55.0])
    np.testing.assert_allclose(kelvin_to_celsius(celsius_to_kelvin(t)), t)
    assert float(celsius_to_kelvin(0.0)) == 273.15


def test_repo_root():
    assert (repo_root() / "pyproject.toml").is_file()
    assert (repo_root() / "python/src/energy_training/__init__.py").is_file()


def test_notebook_interface_installed():
    """`uv sync` installs JupyterLab and the kernel, the course notebook interface."""
    for module in ("jupyterlab", "ipykernel"):
        assert importlib.util.find_spec(module) is not None, f"{module} missing: run `uv sync`"
