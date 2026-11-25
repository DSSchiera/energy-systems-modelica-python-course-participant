"""G3.1: simulate your M02 model with OpenModelica and compare it with the Python M02 of Session 2.

Run from the repository folder:

    uv run python exercises/session_03/s03_g1_compare.py exercises/session_03/S03_G1_ZoneRC_start.mo

The Modelica file must contain a model ``S03_G1_ZoneRC`` with components ``zone`` and
``envelope`` (MSL ``HeatCapacitor``), as in the starting file. The simulation uses a local
OpenModelica installation if ``omc`` is found, otherwise the course Docker image.
Pass criterion of the exercise: largest deviation below 0.01 K for both temperatures.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from energy_training.omc.results import read_result
from energy_training.omc.runner import simulate
from energy_training.simulation import zone_rc as zr

T_AMB, Q_BEFORE, Q_AFTER = 273.15, 1000.0, 4000.0  # as in the starting file
TOLERANCE_K = 0.01


def compare(result: pd.DataFrame) -> dict[str, float]:
    """Largest absolute deviation [K] of zone and envelope temperature from the Python M02."""
    p = zr.ZoneRCParams()
    t = result.index.to_numpy(dtype=float)
    ref = zr.simulate(
        (0.0, float(t[-1])), zr.steady_state(Q_BEFORE, T_AMB, p), Q_AFTER, T_AMB, p, t_eval=t
    )
    return {
        "zone": float(np.abs(result["zone.T"].to_numpy() - ref.T_z).max()),
        "envelope": float(np.abs(result["envelope.T"].to_numpy() - ref.T_e).max()),
    }


def main(mo_file: str) -> int:
    out = Path("output/s03_g1")  # git-ignored
    run = simulate("S03_G1_ZoneRC", [mo_file], out_dir=out, load_library=False)
    dev = compare(read_result(run.csv))
    for name, d in dev.items():
        print(f"max |T_{name} (Modelica) - T_{name} (Python)| = {d:.2e} K")
    ok = max(dev.values()) < TOLERANCE_K
    print("PASS" if ok else f"not yet: deviation >= {TOLERANCE_K} K")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
