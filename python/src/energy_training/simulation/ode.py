"""Integrate a model ODE with time-varying inputs that may jump (shared by M01-M03).

The model supplies ``f(t, x, u) -> dx/dt`` where ``u`` is a dict of input values. Inputs are
constants, plain functions of time, or :class:`~energy_training.simulation.inputs.Signal` objects
whose ``breakpoints`` mark jumps. Integration restarts at every jump, and inside a segment the
inputs are held at their value *inside* that segment, so the solver never sees a discontinuity.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from energy_training.simulation.inputs import Signal, as_signal

__all__ = ["OdeResult", "simulate_ode"]

InputLike = float | Signal | Callable[[float], float]


@dataclass(frozen=True)
class OdeResult:
    """States ``x`` (shape ``(len(t), n)``) and input samples ``u[name]`` on the grid ``t``."""

    t: np.ndarray
    x: np.ndarray
    u: dict[str, np.ndarray]


def simulate_ode(
    f: Callable[[float, np.ndarray, dict[str, float]], Sequence[float] | np.ndarray],
    t_span: tuple[float, float],
    x0: Sequence[float] | np.ndarray,
    inputs: Mapping[str, InputLike],
    *,
    t_eval: np.ndarray | None = None,
    breakpoints: Sequence[float] = (),
    method: str = "RK45",
    rtol: float = 1e-8,
    atol: float = 1e-8,
) -> OdeResult:
    """Integrate ``dx/dt = f(t, x, u(t))`` with :func:`scipy.integrate.solve_ivp`.

    Jump times are the union of ``breakpoints`` and the breakpoints of the input signals.
    ``t_eval`` defaults to 501 points; it must be strictly increasing and lie within ``t_span``.
    Tolerances default to 1e-8 (SciPy's defaults are rtol=1e-3, atol=1e-6).
    """
    if not t_span[1] > t_span[0]:
        raise ValueError("t_span must satisfy t_span[1] > t_span[0]")
    sig = {name: as_signal(v) for name, v in inputs.items()}
    if t_eval is None:
        t_eval = np.linspace(*t_span, 501)
    t_eval = np.asarray(t_eval, dtype=float)
    if t_eval.size == 0 or t_eval.min() < t_span[0] or t_eval.max() > t_span[1]:
        raise ValueError("t_eval must be non-empty and lie within t_span")
    if np.any(np.diff(t_eval) <= 0):
        raise ValueError("t_eval must be strictly increasing")

    jumps = set(breakpoints).union(*(s.breakpoints for s in sig.values()))
    edges = [t_span[0], *sorted(b for b in jumps if t_span[0] < b < t_span[1]), t_span[1]]

    x_start = np.atleast_1d(np.asarray(x0, dtype=float))
    x_out = np.empty((t_eval.size, x_start.size))
    for k, (a, b) in enumerate(zip(edges[:-1], edges[1:], strict=True)):
        last = k == len(edges) - 2
        mask = (t_eval >= a) & ((t_eval <= b) if last else (t_eval < b))
        t_seg = t_eval[mask]
        # always evaluate at the segment end b (state handed to the next segment)
        ends_at_b = t_seg.size > 0 and t_seg[-1] == b
        # Hold the inputs at their value INSIDE the segment: Runge-Kutta stages are evaluated at
        # t = b exactly, where a right-continuous schedule already returns the next value.
        t_in = np.nextafter(b, a) if not last else b

        def rhs(t, x, t_in=t_in):
            tc = min(t, t_in)
            return f(t, x, {name: s(tc) for name, s in sig.items()})

        sol = solve_ivp(
            rhs,
            (a, b),
            x_start,
            method=method,
            t_eval=t_seg if ends_at_b else np.r_[t_seg, b],
            rtol=rtol,
            atol=atol,
        )
        if not sol.success:
            raise RuntimeError(f"solve_ivp failed on [{a}, {b}]: {sol.message}")
        x_out[mask] = (sol.y if ends_at_b else sol.y[:, :-1]).T
        x_start = sol.y[:, -1]

    u_out = {name: np.array([s(t) for t in t_eval]) for name, s in sig.items()}
    return OdeResult(t=t_eval, x=x_out, u=u_out)
