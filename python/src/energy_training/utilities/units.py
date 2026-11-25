"""Unit helpers. Models compute in SI (K); conversion to degC happens only for display."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

T_ZERO_CELSIUS = 273.15  # K, exact by definition of the Celsius scale


def celsius_to_kelvin(t_c: ArrayLike) -> np.ndarray | float:
    """Convert temperature from degC to K."""
    return np.asarray(t_c, dtype=float) + T_ZERO_CELSIUS


def kelvin_to_celsius(t_k: ArrayLike) -> np.ndarray | float:
    """Convert temperature from K to degC."""
    return np.asarray(t_k, dtype=float) - T_ZERO_CELSIUS
