"""M02 ZoneRC — two-node (2R2C) thermal network of a building zone.

Physical system
    The building is split into two lumped nodes: the zone (indoor air and light internal mass,
    temperature T_z) and the building envelope (heavy construction, temperature T_e). The heater
    acts on the zone node; the envelope exchanges heat with the zone and with the ambient.

Structure: deterministic part of the two-state "TiTe" grey-box model of Bacher & Madsen (2011),
Sec. 2, Eq. (1)-(2), without solar gains and noise terms.

Assumptions
    two lumped nodes with constant capacities; linear conductances (1/R) between zone and
    envelope and between envelope and ambient; no direct zone-to-ambient path (ventilation and
    windows are folded into the envelope path); heater power and ambient temperature are inputs.

Governing equations (energy balance of each node)
    C_z dT_z/dt = (T_e - T_z)/R_ze + Q_flow
    C_e dT_e/dt = (T_z - T_e)/R_ze + (T_amb - T_e)/R_ea

States x = (T_z, T_e) [K] · inputs u = (Q_flow [W], T_amb [K]) · output y = T_z.
Parameters C_z, C_e [J/K]; R_ze, R_ea [K/W]. All quantities SI.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np

from energy_training.simulation.inputs import Signal
from energy_training.simulation.ode import simulate_ode

__all__ = [
    "ZoneRCParams",
    "ZoneRCResult",
    "rhs",
    "state_space",
    "time_constants",
    "steady_state",
    "lumped_equivalent",
    "simulate",
    "energy_balance",
]

KWH_PER_K = 3.6e6  # J/K in one kWh/K
K_PER_KW = 1e-3  # K/W in one K/kW


@dataclass(frozen=True)
class ZoneRCParams:
    """Parameters of M02.

    Defaults are the estimates of Bacher & Madsen (2011), Table 3, model TiTeTh, for a 120 m2
    single-storey house (heater node dropped): C_z = Ci = 1.07 kWh/K, C_e = Ce = 2.92 kWh/K,
    R_ze = Rie = 0.863 K/kW, R_ea = Rea = 4.54 K/kW, converted to SI.
    """

    C_z: float = 1.07 * KWH_PER_K
    """Heat capacity of the zone node (air + light internal mass) [J/K]."""
    C_e: float = 2.92 * KWH_PER_K
    """Heat capacity of the envelope node [J/K]."""
    R_ze: float = 0.863 * K_PER_KW
    """Thermal resistance zone -> envelope [K/W]."""
    R_ea: float = 4.54 * K_PER_KW
    """Thermal resistance envelope -> ambient [K/W]."""

    def __post_init__(self) -> None:
        if min(self.C_z, self.C_e, self.R_ze, self.R_ea) <= 0:
            raise ValueError("all capacities and resistances must be positive")


@dataclass(frozen=True)
class ZoneRCResult:
    """Time series returned by :func:`simulate` (SI units)."""

    t: np.ndarray
    T_z: np.ndarray
    T_e: np.ndarray
    Q_flow: np.ndarray
    T_amb: np.ndarray


def rhs(t: float, x: Sequence[float], Q_flow: float, T_amb: float, p: ZoneRCParams) -> np.ndarray:
    """Right-hand side dx/dt for x = (T_z, T_e)."""
    T_z, T_e = x
    q_ze = (T_z - T_e) / p.R_ze  # zone -> envelope [W]
    q_ea = (T_e - T_amb) / p.R_ea  # envelope -> ambient [W]
    return np.array([(Q_flow - q_ze) / p.C_z, (q_ze - q_ea) / p.C_e])


def state_space(p: ZoneRCParams) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """(A, B, C_y, D) for x = (T_z, T_e), u = (Q_flow, T_amb), y = T_z."""
    a_z = 1.0 / (p.R_ze * p.C_z)
    A = np.array(
        [
            [-a_z, a_z],
            [1.0 / (p.R_ze * p.C_e), -(1.0 / p.R_ze + 1.0 / p.R_ea) / p.C_e],
        ]
    )
    B = np.array([[1.0 / p.C_z, 0.0], [0.0, 1.0 / (p.R_ea * p.C_e)]])
    return A, B, np.array([[1.0, 0.0]]), np.zeros((1, 2))


def time_constants(p: ZoneRCParams) -> np.ndarray:
    """Time constants tau_i = -1/lambda_i of the two modes [s], fast first.

    The eigenvalues are real and negative: A is similar to a symmetric negative-definite matrix
    (scale the rows by C_z, C_e), as for any passive RC network.
    """
    lam = np.linalg.eigvals(state_space(p)[0])
    return np.sort(-1.0 / lam.real)


def steady_state(Q_flow: float, T_amb: float, p: ZoneRCParams) -> tuple[float, float]:
    """Equilibrium (T_z, T_e) for constant inputs: the two resistances act in series."""
    return T_amb + Q_flow * (p.R_ze + p.R_ea), T_amb + Q_flow * p.R_ea


def lumped_equivalent(p: ZoneRCParams) -> tuple[float, float]:
    """(C, UA) of the one-node model M01 with the same total capacity and steady-state loss."""
    return p.C_z + p.C_e, 1.0 / (p.R_ze + p.R_ea)


def simulate(
    t_span: tuple[float, float],
    x0: Sequence[float],
    Q_flow: float | Signal | Callable[[float], float],
    T_amb: float | Signal | Callable[[float], float],
    p: ZoneRCParams | None = None,
    *,
    t_eval: np.ndarray | None = None,
    breakpoints: Sequence[float] = (),
    method: str = "RK45",
    rtol: float = 1e-8,
    atol: float = 1e-8,
) -> ZoneRCResult:
    """Integrate M02 from ``x0 = (T_z0, T_e0)``; inputs as in M01 (constants, functions, Signals).

    Jumps in the inputs are handled as in :func:`energy_training.simulation.ode.simulate_ode`.
    """
    p = p or ZoneRCParams()
    res = simulate_ode(
        lambda t, x, u: rhs(t, x, u["Q_flow"], u["T_amb"], p),
        t_span,
        x0,
        {"Q_flow": Q_flow, "T_amb": T_amb},
        t_eval=t_eval,
        breakpoints=breakpoints,
        method=method,
        rtol=rtol,
        atol=atol,
    )
    return ZoneRCResult(
        t=res.t, T_z=res.x[:, 0], T_e=res.x[:, 1], Q_flow=res.u["Q_flow"], T_amb=res.u["T_amb"]
    )


def energy_balance(res: ZoneRCResult, p: ZoneRCParams) -> dict[str, float]:
    """Energy terms over the simulated interval [J] (trapezoidal integration of the samples).

    stored = C_z dT_z + C_e dT_e; supplied = int Q_flow dt; lost = int (T_e - T_amb)/R_ea dt;
    residual = stored - (supplied - lost). The internal flow zone -> envelope cancels in the sum.
    An input jump between samples adds up to |jump| * dt / 2 to the residual (trapezoid rule).
    """
    stored = p.C_z * (res.T_z[-1] - res.T_z[0]) + p.C_e * (res.T_e[-1] - res.T_e[0])
    supplied = float(np.trapezoid(res.Q_flow, res.t))
    lost = float(np.trapezoid((res.T_e - res.T_amb) / p.R_ea, res.t))
    return {
        "stored": stored,
        "supplied": supplied,
        "lost": lost,
        "residual": stored - (supplied - lost),
    }
