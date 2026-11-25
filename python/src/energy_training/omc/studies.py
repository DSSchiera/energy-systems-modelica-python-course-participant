"""Session 4 study: cost and accuracy of OpenModelica solvers on M03 for a growing number of nodes.

Each case simulates ``EnergyTraining.Examples.S04_StorageCharging`` (M03 charged with 0.1 kg/s at
60 degC, surroundings at 20 degC) with one node count and one solver setting, and compares the
outlet temperature with the Python M03 of Session 2 solved with a tight tolerance
(``energy_training.simulation.storage``, BDF, rtol = atol = 1e-10).
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from energy_training.omc.runner import simulate_variant
from energy_training.simulation import storage as st

__all__ = ["M03_EXAMPLE", "SolverCase", "reference_outlet", "storage_solver_study"]

M03_EXAMPLE = "EnergyTraining.Examples.S04_StorageCharging"
"""Modelica example used by the study (case of the Session 2 guided example)."""

_M_FLOW, _T_IN, _T_ENV, _T_START = 0.1, 333.15, 293.15, 303.15


@dataclass(frozen=True)
class SolverCase:
    """One solver setting: OpenModelica method, output interval [s] (the step of fixed-step
    methods) and tolerance (``None``: the default of the example, 1e-6)."""

    method: str
    interval: float
    tolerance: float | None = None

    @property
    def label(self) -> str:
        tol = f", tol {self.tolerance:g}" if self.tolerance is not None else ""
        return f"{self.method}, {self.interval:g} s{tol}"


def reference_outlet(n: int, t: np.ndarray) -> np.ndarray:
    """Outlet temperature [K] of the Python M03 with ``n`` nodes at the times ``t`` [s]."""
    p = st.StorageParams(N=n)
    res = st.simulate((0.0, float(t[-1])), _T_START, _M_FLOW, _T_IN, _T_ENV, p,
                      t_eval=t, method="BDF", rtol=1e-10, atol=1e-10)  # fmt: skip
    return res.T_out


def storage_solver_study(
    node_counts: Iterable[int],
    cases: Sequence[SolverCase],
    *,
    stop_time: float,
    out_dir: str | Path,
    compare_every: float = 300.0,
) -> pd.DataFrame:
    """Simulate every (N, case) and return one row per run.

    Columns: ``N``, ``case``, ``method``, ``interval``, ``tolerance``, ``tau_node`` [s] (node
    time constant rho V / (N m_flow)), ``steps``, ``f_calls`` (right-hand-side evaluations),
    ``cpu_time`` [s], ``max_error`` [K] (largest |T_out - reference| on a grid of
    ``compare_every`` seconds; ``inf`` if the result is not finite).
    """
    t = np.arange(0.0, stop_time + 0.5 * compare_every, compare_every)
    rows = []
    for n in node_counts:
        ref = reference_outlet(n, t)
        tau = st.StorageParams(N=n).m_node / _M_FLOW
        for case in cases:
            run = simulate_variant(M03_EXAMPLE, {"N": n}, out_dir=out_dir, stop_time=stop_time,
                                   interval=case.interval, method=case.method,
                                   tolerance=case.tolerance)  # fmt: skip
            t_out = run.result["storage.T_out"].reindex(t, method="nearest").to_numpy()
            finite = np.all(np.isfinite(t_out))
            err = float(np.max(np.abs(t_out - ref))) if finite else float("inf")
            rows.append({
                "N": n, "case": case.label, "method": case.method,
                "interval": case.interval, "tolerance": case.tolerance, "tau_node": tau,
                "steps": run.stats["steps"], "f_calls": run.stats["f_calls"],
                "cpu_time": run.stats["cpu_time"], "max_error": err,
            })  # fmt: skip
    return pd.DataFrame(rows)
