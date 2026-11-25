"""M01 ThermalZone — a single lumped thermal mass with losses to ambient.

Physical system
    A heated building zone (air + internal mass) treated as ONE node at uniform temperature T.

Assumptions
    lumped (uniform T), constant C and UA, heat losses proportional to T - T_amb,
    heater power Q_flow and ambient temperature T_amb are given inputs.

Governing equation (energy balance of the node)
    C dT/dt = Q_flow - UA (T - T_amb)

State x = T [K] · inputs u = (Q_flow [W], T_amb [K]) · parameters C [J/K], UA [W/K] · output y = T.
All quantities SI; convert to degC only for display.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np

from energy_training.simulation.inputs import Signal
from energy_training.simulation.ode import simulate_ode

__all__ = [
    "ThermalZoneParams",
    "SimulationResult",
    "rhs",
    "time_constant",
    "steady_state",
    "analytic_step",
    "analytic_piecewise",
    "state_space",
    "simulate",
    "energy_balance",
]


@dataclass(frozen=True)
class ThermalZoneParams:
    """Parameters of M01.

    Default values are ILLUSTRATIVE (round numbers for a small house), not sourced data.
    """

    C: float = 1.0e7
    """Heat capacity of the lumped node [J/K]."""
    UA: float = 200.0
    """Overall heat-loss conductance to ambient [W/K]."""

    def __post_init__(self) -> None:
        if self.C <= 0 or self.UA <= 0:
            raise ValueError("C and UA must be positive")


@dataclass(frozen=True)
class SimulationResult:
    """Time series returned by :func:`simulate` (SI units)."""

    t: np.ndarray
    """Time [s]."""
    T: np.ndarray
    """Zone temperature [K]."""
    Q_flow: np.ndarray
    """Heater power [W] evaluated at ``t``."""
    T_amb: np.ndarray
    """Ambient temperature [K] evaluated at ``t``."""


def rhs(t: float, T: float, Q_flow: float, T_amb: float, p: ThermalZoneParams) -> float:
    """Right-hand side dT/dt = (Q_flow - UA (T - T_amb)) / C  [K/s]."""
    return (Q_flow - p.UA * (T - T_amb)) / p.C


def time_constant(p: ThermalZoneParams) -> float:
    """tau = C / UA [s]."""
    return p.C / p.UA


def steady_state(Q_flow: float, T_amb: float, p: ThermalZoneParams) -> float:
    """Equilibrium temperature for constant inputs: T_ss = T_amb + Q_flow / UA [K]."""
    return T_amb + Q_flow / p.UA


def analytic_step(
    t: np.ndarray | float, T0: float, Q_flow: float, T_amb: float, p: ThermalZoneParams
) -> np.ndarray:
    """Exact solution for constant inputs: T(t) = T_ss + (T0 - T_ss) exp(-t / tau)."""
    T_ss = steady_state(Q_flow, T_amb, p)
    return T_ss + (T0 - T_ss) * np.exp(-np.asarray(t, dtype=float) / time_constant(p))


def analytic_piecewise(
    t: np.ndarray,
    T0: float,
    breakpoints: Sequence[float],
    Q_values: Sequence[float],
    T_amb_values: Sequence[float],
    p: ThermalZoneParams,
) -> np.ndarray:
    """Exact solution for piecewise-constant inputs.

    Segment k covers [breakpoints[k], breakpoints[k+1]) with inputs Q_values[k], T_amb_values[k];
    the last segment extends to +inf. ``breakpoints[0]`` must be <= t[0].
    The solution of segment k starts from the end state of segment k-1 (state continuity).
    """
    t = np.asarray(t, dtype=float)
    bp = np.asarray(breakpoints, dtype=float)
    if not (len(bp) == len(Q_values) == len(T_amb_values)):
        raise ValueError("breakpoints, Q_values and T_amb_values must have equal length")
    if t[0] < bp[0]:
        raise ValueError("first breakpoint must not be after t[0]")
    if np.any(np.diff(bp) <= 0):
        raise ValueError("breakpoints must be strictly increasing")
    out = np.empty_like(t)
    T_start, t_start = T0, bp[0]
    for k in range(len(bp)):
        t_end = bp[k + 1] if k + 1 < len(bp) else np.inf
        mask = (t >= t_start) & (t < t_end)
        out[mask] = analytic_step(t[mask] - t_start, T_start, Q_values[k], T_amb_values[k], p)
        if np.isfinite(t_end):
            T_start = float(
                analytic_step(t_end - t_start, T_start, Q_values[k], T_amb_values[k], p)
            )
            t_start = t_end
    return out


def state_space(p: ThermalZoneParams) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Matrices of dx/dt = A x + B u, y = C x + D u with x = [T], u = [Q_flow, T_amb], y = [T]."""
    A = np.array([[-p.UA / p.C]])
    B = np.array([[1.0 / p.C, p.UA / p.C]])
    Cm = np.array([[1.0]])
    D = np.zeros((1, 2))
    return A, B, Cm, D


def simulate(
    t_span: tuple[float, float],
    T0: float,
    Q_flow: float | Signal | Callable[[float], float],
    T_amb: float | Signal | Callable[[float], float],
    p: ThermalZoneParams | None = None,
    *,
    t_eval: np.ndarray | None = None,
    breakpoints: Sequence[float] = (),
    method: str = "RK45",
    rtol: float = 1e-8,
    atol: float = 1e-8,
) -> SimulationResult:
    """Integrate M01 numerically with :func:`scipy.integrate.solve_ivp`.

    Inputs may be constants or functions of time. If the inputs jump (heater schedule), pass the
    jump times in ``breakpoints`` (or use :class:`~energy_training.simulation.inputs.Signal`, whose
    breakpoints are used automatically): the integration restarts at each jump so the solver never
    steps across a discontinuity.

    Tolerances default to 1e-8 (SciPy's defaults are rtol=1e-3, atol=1e-6) so that results can be
    compared against the analytic solution in lessons and tests.
    """
    p = p or ThermalZoneParams()
    res = simulate_ode(
        lambda t, x, u: [rhs(t, x[0], u["Q_flow"], u["T_amb"], p)],
        t_span,
        [T0],
        {"Q_flow": Q_flow, "T_amb": T_amb},
        t_eval=t_eval,
        breakpoints=breakpoints,
        method=method,
        rtol=rtol,
        atol=atol,
    )
    return SimulationResult(t=res.t, T=res.x[:, 0], Q_flow=res.u["Q_flow"], T_amb=res.u["T_amb"])


def energy_balance(res: SimulationResult, p: ThermalZoneParams) -> dict[str, float]:
    """Energy terms over the simulated interval [J] (trapezoidal integration of the samples).

    stored = C (T_end - T_start); supplied = int Q_flow dt; lost = int UA (T - T_amb) dt;
    residual = stored - (supplied - lost) must be ~0 (first law for the node).
    Accuracy depends on the output grid: inputs with jumps between samples add quadrature error.
    """
    stored = p.C * (res.T[-1] - res.T[0])
    supplied = float(np.trapezoid(res.Q_flow, res.t))
    lost = float(np.trapezoid(p.UA * (res.T - res.T_amb), res.t))
    return {
        "stored": stored,
        "supplied": supplied,
        "lost": lost,
        "residual": stored - (supplied - lost),
    }
