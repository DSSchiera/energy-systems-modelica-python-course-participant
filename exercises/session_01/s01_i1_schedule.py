"""I1.1 starting file. Run: uv run python exercises/session_01/s01_i1_schedule.py"""

import matplotlib.pyplot as plt  # noqa: F401
import numpy as np

from energy_training.simulation import thermal_zone as tz  # noqa: F401
from energy_training.simulation.inputs import piecewise_constant
from energy_training.utilities import celsius_to_kelvin

H = 3600.0
T_AMB = float(celsius_to_kelvin(0.0))
T0 = float(celsius_to_kelvin(19.0))
DAY = [(0, 1000.0), (6, 6000.0), (9, 2000.0), (17, 6000.0), (22, 1000.0)]  # (start hour, W)


def schedule(days: int = 2):
    """Switching times [s] and heater powers [W] for `days` repetitions of DAY (provided)."""
    times, vals = [], []
    for d in range(days):
        for hour, q in DAY:
            times.append((24 * d + hour) * H)
            vals.append(q)
    return times, vals


q = piecewise_constant(*schedule())
t = np.linspace(0, 48 * H, 48 * 12 + 1)  # 5-min output grid

# TODO 1: simulate with tz.simulate((0, 48 * H), T0, q, T_AMB, tz.ThermalZoneParams(), t_eval=t)
# TODO 2: plot temperature [degC] and heater power [kW] against time [h]
# TODO 3: day-2 heater energy in kWh, by hand and from the simulation (np.trapezoid)
# TODO 4: tz.energy_balance(...) -> explain the residual
# TODO 5: min/max zone temperature on day 2; comfortable (>= 19 degC) during 06:00-22:00?
