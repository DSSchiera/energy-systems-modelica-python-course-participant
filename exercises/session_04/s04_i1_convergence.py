"""I4.1 starting file: how many nodes does M03 need, and which tolerance? Complete the TODOs.

Run from the repository folder (OpenModelica: local omc or the course Docker image):

    uv run python exercises/session_04/s04_i1_convergence.py

Every simulation compiles a variant of EnergyTraining.Examples.S04_StorageCharging (M03, 300 L
at 30 degC, charged from the top with 0.1 kg/s at 60 degC). N sets the size of the arrays, so
each N is a new model: simulate_variant writes it, compiles it and returns the result and the
solver statistics.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from energy_training.omc.runner import simulate_variant
from energy_training.omc.studies import M03_EXAMPLE, reference_outlet  # noqa: F401 (part 2)
from energy_training.plotting.style import degc  # noqa: F401 (part 1)
from energy_training.simulation import storage as st

OUT = Path("output/s04_i1")  # git-ignored
STOP, INTERVAL = 3 * 3600.0, 60.0  # 3 h, results every minute
NODE_COUNTS = (1, 2, 5, 10, 20, 50)
TOLERANCES = (1e-2, 1e-4, 1e-6, 1e-8, 1e-10)


def stored_energy(result: pd.DataFrame, n: int) -> float:
    """Energy stored in the tank between the first and the last sample [J]."""
    c_node = st.StorageParams(N=n).C_node
    cols = [f"storage.tank.T[{k}]" for k in range(1, n + 1)]
    return float(c_node * (result[cols].iloc[-1] - result[cols].iloc[0]).sum())


def node_count_study(node_counts=NODE_COUNTS) -> pd.DataFrame:
    """Part 1: one row per N with T_out after 1 h [degC], stored energy after 3 h [kWh], steps."""
    rows = []
    for n in node_counts:
        run = simulate_variant(M03_EXAMPLE, {"N": n}, out_dir=OUT, stop_time=STOP,  # noqa: F841
                               interval=INTERVAL)  # fmt: skip
        # run.result: DataFrame indexed by time [s]; run.stats: solver statistics (dict)
        raise NotImplementedError("TODO: append one row per N to rows")
    return pd.DataFrame(rows).set_index("N")


def tolerance_study(n: int, tolerances=TOLERANCES) -> pd.DataFrame:
    """Part 2 (after the session): per tolerance the largest error of T_out [K] and the cost."""
    t = np.arange(0.0, STOP + 1.0, INTERVAL)  # noqa: F841 (comparison times)
    raise NotImplementedError(
        "TODO: reference_outlet(n, t) is the Python M03 with a tight tolerance; simulate with "
        "simulate_variant(..., tolerance=tol) and compare storage.T_out at the times t"
    )


if __name__ == "__main__":
    print(node_count_study())
    # TODO: choose N from part 1 for the two purposes of the exercise and justify each choice
    # After the session: run part 2 with the N chosen for the energy
    # print(tolerance_study(n=...))
