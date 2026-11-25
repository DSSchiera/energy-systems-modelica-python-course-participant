"""G2.1 starting file — complete the TODOs.

Run: uv run python exercises/session_02/s02_g1_storage.py
"""

import numpy as np
from scipy.integrate import solve_ivp

from energy_training.simulation.storage import CP_WATER, RHO_WATER  # noqa: F401 (for rhs)
from energy_training.utilities import celsius_to_kelvin

V = 0.2  # m3      (illustrative)
N = 5  # nodes, node 1 at the top
UA_LOSS = 1.5  # W/K  (illustrative)
M_FLOW = 0.05  # kg/s, enters at the top
T_IN = float(celsius_to_kelvin(55.0))
T_ENV = float(celsius_to_kelvin(20.0))
T_START = float(celsius_to_kelvin(25.0))
DURATION = 3 * 3600.0


def rhs(t, T, n=N):
    """Return dT/dt [K/s] for the n node temperatures T (top first)."""
    raise NotImplementedError(
        "TODO: m_node cp dT_k/dt = m_flow cp (T_up - T_k) - UA_loss/n (T_k - T_env)"
    )


def energy_terms(t, T, n=N):
    """Return (stored, advected, lost) in J for the sampled solution T of shape (len(t), n)."""
    raise NotImplementedError("TODO: use np.trapezoid for the integrals")


if __name__ == "__main__":
    t_eval = np.arange(0.0, DURATION + 1.0, 60.0)
    sol = solve_ivp(rhs, (0.0, DURATION), np.full(N, T_START), t_eval=t_eval, rtol=1e-8, atol=1e-8)
    stored, advected, lost = energy_terms(sol.t, sol.y.T)
    print(
        f"stored {stored / 3.6e6:.3f} kWh, advected {advected / 3.6e6:.3f} kWh, "
        f"lost {lost / 3.6e6:.3f} kWh, residual {stored - (advected - lost):.1f} J"
    )
