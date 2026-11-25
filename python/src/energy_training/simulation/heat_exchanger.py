"""Steady-state heat exchanger with the effectiveness-NTU method (Session 2, model fidelity).

A heat exchanger with capacity rates C_h = m_h cp_h and C_c = m_c cp_c, inlet temperatures
T_h_in > T_c_in and conductance UA transfers Q = eps * C_min * (T_h_in - T_c_in), with
NTU = UA / C_min and C_r = C_min / C_max. The effectiveness eps(NTU, C_r) depends on the flow
arrangement [src: incropera, effectiveness-NTU method]. The expressions below are also checked
in the tests against a direct numerical solution of the exchanger's temperature profiles.

This is a *steady-state* component model: it has no states and answers instantly. Inside a
dynamic system model it is valid when the exchanger's own thermal inertia is small compared to the
time scales of interest.
"""

from __future__ import annotations

import math

__all__ = ["effectiveness", "heat_flow"]


def effectiveness(NTU: float, C_r: float, arrangement: str = "counterflow") -> float:
    """Effectiveness of a parallel-flow or counterflow exchanger, 0 <= C_r <= 1, NTU >= 0."""
    if NTU < 0 or not 0 <= C_r <= 1:
        raise ValueError("need NTU >= 0 and 0 <= C_r <= 1")
    if arrangement == "parallel":
        return (1.0 - math.exp(-NTU * (1.0 + C_r))) / (1.0 + C_r)
    if arrangement == "counterflow":
        if math.isclose(C_r, 1.0):
            return NTU / (1.0 + NTU)
        e = math.exp(-NTU * (1.0 - C_r))
        return (1.0 - e) / (1.0 - C_r * e)
    raise ValueError("arrangement must be 'parallel' or 'counterflow'")


def heat_flow(
    UA: float,
    C_h: float,
    C_c: float,
    T_h_in: float,
    T_c_in: float,
    arrangement: str = "counterflow",
) -> float:
    """Heat flow from the hot to the cold stream [W] (capacity rates in W/K, temperatures in K)."""
    if UA < 0 or C_h <= 0 or C_c <= 0:
        raise ValueError("need UA >= 0 and positive capacity rates")
    C_min, C_max = min(C_h, C_c), max(C_h, C_c)
    return effectiveness(UA / C_min, C_min / C_max, arrangement) * C_min * (T_h_in - T_c_in)
