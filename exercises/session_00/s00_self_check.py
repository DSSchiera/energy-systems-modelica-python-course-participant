"""S0.1 starting file — complete the three TODO functions, then run the file.

Run: uv run python exercises/session_00/s00_self_check.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from energy_training.data.weather import load_tmy
from energy_training.plotting.style import apply_style, degc

J_PER_KWH = 3.6e6
DT_H = 3600.0  # s, one hourly sample


def daily_stats(tmy: pd.DataFrame) -> pd.DataFrame:
    """Daily mean ambient temperature T_mean [K] and horizontal irradiation H_h [kWh/m2].

    Hint: ``tmy["T_amb"].resample("D")``. Treat each hourly value of ``G_h`` [W/m2] as
    representative of its hour (duration 3600 s).
    """
    raise NotImplementedError("TODO")


def coldest_and_sunniest(daily: pd.DataFrame) -> tuple[pd.Timestamp, pd.Timestamp]:
    """Dates of the lowest daily mean temperature and of the highest daily irradiation."""
    raise NotImplementedError("TODO: look up Series.idxmin / Series.idxmax")


def monthly_irradiation(tmy: pd.DataFrame) -> pd.Series:
    """Horizontal irradiation of each month [kWh/m2], indexed by month number 1-12."""
    raise NotImplementedError("TODO: group by tmy.index.month")


if __name__ == "__main__":
    apply_style()
    tmy = load_tmy()
    daily = daily_stats(tmy)
    cold, sunny = coldest_and_sunniest(daily)
    monthly = monthly_irradiation(tmy)
    print(f"coldest day : {cold:%d %b}, mean {degc(daily.loc[cold, 'T_mean']):.1f} degC")
    print(f"sunniest day: {sunny:%d %b}, {daily.loc[sunny, 'H_h']:.2f} kWh/m2")
    print(f"year        : {monthly.sum():.0f} kWh/m2 on the horizontal plane")
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7.0, 5.0))
    ax1.plot(daily.index, degc(daily["T_mean"]))
    ax1.set(ylabel="daily mean T [°C]", title="Turin, typical meteorological year (PVGIS)")
    ax2.bar(daily.index, daily["H_h"], width=1.0)
    ax2.set(ylabel="H [kWh/m²]")
    plt.show()
