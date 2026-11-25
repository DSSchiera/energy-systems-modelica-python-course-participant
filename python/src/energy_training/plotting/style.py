"""Course figure style. Models compute in SI; this module converts to h and degC for display."""

from __future__ import annotations

import matplotlib as mpl
import numpy as np

from energy_training.utilities.units import kelvin_to_celsius

__all__ = ["apply_style", "hours", "degc", "COLORS"]

# Colour-blind-safe qualitative palette (Okabe-Ito).
COLORS = {
    "primary": "#0072B2",
    "secondary": "#D55E00",
    "tertiary": "#009E73",
    "quaternary": "#CC79A7",
    "neutral": "#555555",
    "reference": "#000000",
}


def apply_style() -> None:
    """Apply the course Matplotlib style (call once per script/notebook)."""
    mpl.rcParams.update(
        {
            "figure.figsize": (7.0, 3.6),
            "figure.dpi": 110,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "axes.grid": True,
            "grid.alpha": 0.3,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.prop_cycle": mpl.cycler(color=list(COLORS.values())),
            "font.size": 11,
            "legend.frameon": False,
            "lines.linewidth": 2.0,
        }
    )


def hours(t_s: np.ndarray | float) -> np.ndarray:
    """Seconds -> hours."""
    return np.asarray(t_s, dtype=float) / 3600.0


def degc(T_K: np.ndarray | float) -> np.ndarray:
    """Kelvin -> degC."""
    return np.asarray(kelvin_to_celsius(T_K))
