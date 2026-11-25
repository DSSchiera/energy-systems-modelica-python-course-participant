"""G1.1 starting file — complete the TODOs.

Run: uv run python exercises/session_01/s01_g1_step.py
"""

import numpy as np

from energy_training.simulation.integrators import explicit_euler
from energy_training.utilities import celsius_to_kelvin

C = 8.0e6  # J/K   (illustrative)
UA = 250.0  # W/K  (illustrative)
T_AMB = float(celsius_to_kelvin(-5.0))
Q = 6000.0  # W
T0 = float(celsius_to_kelvin(12.0))


def rhs(t, y):
    """Return dT/dt [K/s] as a 1-element array. y[0] is the zone temperature [K]."""
    raise NotImplementedError("TODO: energy balance C dT/dt = Q - UA (T - T_amb)")


def estimate_tau(t, T, T0, T_ss):
    """Return the time [s] at which 63.2 % of the step T0 -> T_ss is reached (interpolate)."""
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    t, y = explicit_euler(rhs, (0.0, 5 * 24 * 3600.0), T0, 600.0)
    T = y[:, 0]
    T_ss_est = T[-1]
    tau_est = estimate_tau(t, T, T0, T_ss_est)
    print(f"T_ss estimate: {T_ss_est - 273.15:.2f} degC")
    print(f"tau estimate: {tau_est / 3600:.2f} h  (C/UA = {C / UA / 3600:.2f} h)")
    _ = np  # numpy is useful for the interpolation
