"""M03 StorageSystem — hot-water storage tank as N fully mixed nodes with a through-flow.

Physical system
    A vertical tank of volume V filled with water, divided into N horizontal layers of equal mass
    (node 1 at the top, node N at the bottom). Water flows through the tank: entering at the top
    and leaving at the bottom (m_flow > 0, charging with hot water) or entering at the bottom and
    leaving at the top (m_flow < 0, discharging by cold return water). Each node loses heat
    through the insulation to the surroundings at T_env; neighbouring nodes exchange heat by
    conduction (effective conductance G, optional).

Assumptions
    incompressible water with constant density and specific heat (Buildings.Media.Water
    constants: d = 995.586 kg/m3, cp = 4184 J/(kg K)); each node fully mixed; plug flow between
    nodes, the inflow to a node has the temperature of the upstream node (upwind); equal loss
    conductance UA_loss/N per node; no buoyancy model (a cold inflow at the top is simply mixed,
    temperature inversions are not corrected).

Governing equations (energy balance of node k, open system, m_k = rho V / N)
    m_k cp dT_k/dt = |m_flow| cp (T_up(k) - T_k)                      advection (upwind)
                     + G (T_{k-1} - T_k) + G (T_{k+1} - T_k)          conduction (internal nodes)
                     - (UA_loss/N) (T_k - T_env)                        losses
    with T_up(k) the upstream node, or T_in for the inlet node.

States x = (T_1 .. T_N) [K] · inputs u = (m_flow [kg/s], T_in [K], T_env [K]) ·
output T_out (outlet node temperature) · parameters V [m3], N [-], UA_loss [W/K], G [W/K].
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np

from energy_training.simulation.inputs import Signal
from energy_training.simulation.ode import simulate_ode

__all__ = [
    "RHO_WATER",
    "CP_WATER",
    "StorageParams",
    "StorageResult",
    "rhs",
    "outlet_temperature",
    "residence_time",
    "loss_time_constant",
    "analytic_series_step",
    "simulate",
    "energy_balance",
]

RHO_WATER = 995.586
"""Density of water [kg/m3] (constant; Buildings.Media.Water, Buildings 14.0.0)."""
CP_WATER = 4184.0
"""Specific heat capacity of water [J/(kg K)] at 20 degC (Buildings.Media.Water)."""


@dataclass(frozen=True)
class StorageParams:
    """Parameters of M03. V, UA_loss and G are ILLUSTRATIVE values, not sourced data."""

    V: float = 0.3
    """Tank volume [m3]."""
    N: int = 10
    """Number of fully mixed nodes [-]."""
    UA_loss: float = 2.0
    """Total heat-loss conductance through the insulation [W/K]."""
    G: float = 0.0
    """Conductance across each interface between neighbouring nodes [W/K] (0: no conduction).

    Physically G = k A / dz = k A N / H_tank, so the same G means different conduction at a
    different N: scale G with N when comparing discretisations."""
    rho: float = RHO_WATER
    """Density [kg/m3]."""
    cp: float = CP_WATER
    """Specific heat capacity [J/(kg K)]."""

    def __post_init__(self) -> None:
        if self.V <= 0 or self.N < 1 or self.UA_loss < 0 or self.G < 0:
            raise ValueError("need V > 0, N >= 1, UA_loss >= 0, G >= 0")
        if self.rho <= 0 or self.cp <= 0:
            raise ValueError("rho and cp must be positive")

    @property
    def m_node(self) -> float:
        """Water mass of one node [kg]."""
        return self.rho * self.V / self.N

    @property
    def C_node(self) -> float:
        """Heat capacity of one node [J/K]."""
        return self.m_node * self.cp


@dataclass(frozen=True)
class StorageResult:
    """Time series returned by :func:`simulate`; ``T`` has shape (len(t), N), node 1 first."""

    t: np.ndarray
    T: np.ndarray
    m_flow: np.ndarray
    T_in: np.ndarray
    T_env: np.ndarray

    @property
    def T_out(self) -> np.ndarray:
        """Outlet temperature: bottom node when charging (m_flow >= 0), top node otherwise."""
        return np.where(self.m_flow >= 0, self.T[:, -1], self.T[:, 0])


def rhs(
    t: float,
    T: np.ndarray,
    m_flow: float,
    T_in: float,
    T_env: float,
    p: StorageParams,
) -> np.ndarray:
    """dT/dt for the node temperatures T (node 1 = top)."""
    T = np.asarray(T, dtype=float)
    q = np.zeros_like(T)  # net heat flow into each node [W]
    if m_flow >= 0:  # downward: inlet at the top, upstream of node k is node k-1
        upstream = np.r_[T_in, T[:-1]]
    else:  # upward: inlet at the bottom, upstream of node k is node k+1
        upstream = np.r_[T[1:], T_in]
    q += abs(m_flow) * p.cp * (upstream - T)
    if p.G > 0 and T.size > 1:
        dq = p.G * (T[:-1] - T[1:])  # conduction from node k to node k+1
        q[:-1] -= dq
        q[1:] += dq
    q -= p.UA_loss / p.N * (T - T_env)
    return q / p.C_node


def outlet_temperature(T: np.ndarray, m_flow: float) -> float:
    """Temperature leaving the tank for the given flow direction."""
    return float(T[-1] if m_flow >= 0 else T[0])


def residence_time(m_flow: float, p: StorageParams) -> float:
    """Mean residence time of the water in the tank, rho V / |m_flow| [s] (needs m_flow != 0)."""
    if m_flow == 0:
        raise ValueError("no flow: the residence time is infinite")
    return p.rho * p.V / abs(m_flow)


def loss_time_constant(p: StorageParams) -> float:
    """Time constant of the standby losses of a uniformly mixed tank, rho V cp / UA_loss [s]."""
    if p.UA_loss == 0:
        raise ValueError("UA_loss = 0: no standby losses")
    return p.rho * p.V * p.cp / p.UA_loss


def analytic_series_step(
    t: np.ndarray, k: int, T0: float, T_in: float, m_flow: float, p: StorageParams
) -> np.ndarray:
    """Exact temperature of node k (1-based, counted from the inlet) after an inlet step.

    Valid without losses and conduction, for a tank initially uniform at T0 and a constant inflow
    at T_in from t = 0 (N mixed nodes in series; tau_n = m_node/|m_flow|):
        T_k(t) = T_in + (T0 - T_in) exp(-t/tau_n) sum_{j=0}^{k-1} (t/tau_n)^j / j!
    """
    s = np.asarray(t, dtype=float) / (p.m_node / abs(m_flow))
    term = np.ones_like(s)
    acc = np.ones_like(s)
    for j in range(1, k):
        term = term * s / j
        acc = acc + term
    return T_in + (T0 - T_in) * np.exp(-s) * acc


def simulate(
    t_span: tuple[float, float],
    T0: float | Sequence[float],
    m_flow: float | Signal | Callable[[float], float],
    T_in: float | Signal | Callable[[float], float],
    T_env: float | Signal | Callable[[float], float],
    p: StorageParams | None = None,
    *,
    t_eval: np.ndarray | None = None,
    breakpoints: Sequence[float] = (),
    method: str = "RK45",
    rtol: float = 1e-8,
    atol: float = 1e-8,
) -> StorageResult:
    """Integrate M03. ``T0`` is one temperature (uniform tank) or N node temperatures (top first).

    For many nodes the system becomes stiff (node time constant m_node/|m_flow| much shorter than
    the loss time constant): pass ``method="BDF"`` or ``"Radau"`` if RK45 needs too many steps.
    """
    p = p or StorageParams()
    x0 = np.full(p.N, float(T0)) if np.ndim(T0) == 0 else np.asarray(T0, dtype=float)
    if x0.shape != (p.N,):
        raise ValueError(f"T0 must be a scalar or have N = {p.N} values")
    res = simulate_ode(
        lambda t, x, u: rhs(t, x, u["m_flow"], u["T_in"], u["T_env"], p),
        t_span,
        x0,
        {"m_flow": m_flow, "T_in": T_in, "T_env": T_env},
        t_eval=t_eval,
        breakpoints=breakpoints,
        method=method,
        rtol=rtol,
        atol=atol,
    )
    return StorageResult(
        t=res.t, T=res.x, m_flow=res.u["m_flow"], T_in=res.u["T_in"], T_env=res.u["T_env"]
    )


def energy_balance(res: StorageResult, p: StorageParams) -> dict[str, float]:
    """Energy terms over the simulated interval [J] (trapezoidal integration of the samples).

    stored   = sum_k C_node (T_k(end) - T_k(start))
    advected = int |m_flow| cp (T_in - T_out) dt   (net enthalpy brought in by the flow)
    lost     = int sum_k UA_loss/N (T_k - T_env) dt
    residual = stored - (advected - lost); conduction between nodes cancels in the sum.

    The integrals use the samples only: an input jump smears over one output interval and adds up
    to |jump in advected power| * dt / 2 to the residual. For a small residual put the jumps on
    the output grid and use a fine grid (or compare against that bound).
    """
    stored = p.C_node * float(np.sum(res.T[-1] - res.T[0]))
    advected = float(np.trapezoid(np.abs(res.m_flow) * p.cp * (res.T_in - res.T_out), res.t))
    lost = float(np.trapezoid(p.UA_loss / p.N * np.sum(res.T - res.T_env[:, None], axis=1), res.t))
    return {
        "stored": stored,
        "advected": advected,
        "lost": lost,
        "residual": stored - (advected - lost),
    }
