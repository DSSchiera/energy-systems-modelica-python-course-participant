"""Input signals for simulations: constants and piecewise-constant schedules.

A :class:`Signal` is a function of time that also reports where it jumps (``breakpoints``),
so simulators can restart integration at discontinuities instead of stepping across them.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np

__all__ = ["Signal", "constant", "piecewise_constant", "as_signal"]


@dataclass(frozen=True)
class Signal:
    """Callable time signal u(t) with known discontinuity times."""

    func: Callable[[float], float]
    breakpoints: tuple[float, ...] = ()

    def __call__(self, t: float) -> float:
        return self.func(t)


def constant(value: float) -> Signal:
    """u(t) = value."""
    v = float(value)
    return Signal(lambda t: v)


def piecewise_constant(times: Sequence[float], values: Sequence[float]) -> Signal:
    """u(t) = values[k] for times[k] <= t < times[k+1]; values[-1] after the last time.

    Before ``times[0]`` the signal equals ``values[0]``. ``times`` must be strictly increasing.
    """
    tt = np.asarray(times, dtype=float)
    vv = np.asarray(values, dtype=float)
    if tt.ndim != 1 or tt.shape != vv.shape or len(tt) == 0:
        raise ValueError("times and values must be 1-D sequences of equal, non-zero length")
    if np.any(np.diff(tt) <= 0):
        raise ValueError("times must be strictly increasing")

    def f(t: float) -> float:
        k = int(np.searchsorted(tt, t, side="right")) - 1
        return float(vv[max(k, 0)])

    return Signal(f, tuple(float(x) for x in tt[1:]))


def as_signal(u: float | Signal | Callable[[float], float]) -> Signal:
    """Wrap a constant or plain function as a :class:`Signal` (plain functions: no breakpoints)."""
    if isinstance(u, Signal):
        return u
    if callable(u):
        return Signal(u)
    return constant(u)
