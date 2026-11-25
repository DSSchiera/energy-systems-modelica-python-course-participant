"""Teaching integrators. Written for readability, not performance.

Use :func:`scipy.integrate.solve_ivp` for real work; these exist so the participant can see what an
integrator does and observe accuracy (error ~ h) and stability (|1 - h/tau| < 1) of explicit Euler.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

__all__ = ["explicit_euler", "euler_amplification"]


def explicit_euler(
    f: Callable[[float, np.ndarray], np.ndarray],
    t_span: tuple[float, float],
    y0: float | np.ndarray,
    h: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Explicit (forward) Euler: y_{k+1} = y_k + h f(t_k, y_k).

    Returns (t, y) with y of shape (len(t), n). The last step is shortened to land on t_span[1].
    """
    if h <= 0:
        raise ValueError("step size h must be positive")
    t0, t1 = t_span
    n_full = int(np.floor((t1 - t0) / h + 1e-12))
    t = t0 + h * np.arange(n_full + 1)
    if t[-1] < t1 - 1e-12 * max(1.0, abs(t1)):
        t = np.append(t, t1)
    y = np.empty((len(t), np.size(y0)))
    y[0] = np.atleast_1d(np.asarray(y0, dtype=float))
    for k in range(len(t) - 1):
        y[k + 1] = y[k] + (t[k + 1] - t[k]) * np.atleast_1d(f(t[k], y[k]))
    return t, y


def euler_amplification(h: float, tau: float) -> float:
    """Error amplification factor of explicit Euler on dx/dt = -x/tau: g = 1 - h/tau.

    |g| < 1 (i.e. 0 < h < 2 tau) -> stable; g < 0 (h > tau) -> the numerical solution oscillates
    although the exact solution never does; |g| > 1 (h > 2 tau) -> it diverges.
    """
    return 1.0 - h / tau
