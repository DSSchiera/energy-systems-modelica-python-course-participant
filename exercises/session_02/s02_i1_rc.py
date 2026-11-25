"""I2.1 starting file. Run: uv run python exercises/session_02/s02_i1_rc.py"""

import numpy as np

from energy_training.simulation import zone_rc as zr
from energy_training.utilities import celsius_to_kelvin

P = zr.ZoneRCParams()
T_AMB = float(celsius_to_kelvin(0.0))
H = 3600.0

if __name__ == "__main__":
    A, B, Cy, D = zr.state_space(P)
    # TODO 1: eigenvalues and eigenvectors of A -> time constants [h]
    # TODO 2: interpret the eigenvectors (do T_z and T_e move together?)
    # TODO 3: heater step 1 kW -> 4 kW from zr.steady_state(1000.0, T_AMB, P); simulate 96 h with
    #         zr.simulate and find when T_z has completed 63.2 % of its rise
    _ = np
