"""Weather of the case-study site: the PVGIS typical meteorological year (TMY) for Turin.

Source: JRC PVGIS 5.3, tool ``tmy`` (registry id ``pvgis-5.3``), downloaded 2026-11-19 for
lat 45.070, lon 7.687: solar radiation from PVGIS-SARAH3, other variables from ERA5, years
2005-2023. The committed file ``data/processed/weather_turin_tmy.csv`` keeps the PVGIS column
names and units; :func:`load_tmy` converts to the course conventions (SI, temperatures in K).

A TMY joins 12 calendar months taken from different years (one "typical" month each). The raw
time stamps therefore jump between years at month boundaries. :func:`load_tmy` replaces them with
one continuous hourly index in a nominal non-leap year (:data:`NOMINAL_YEAR`, a label only) and
keeps the original year of each month in the column ``source_year``.

Time stamps are UTC (PVGIS convention); local time in Turin is UTC+1 (UTC+2 in summer).
Every row is labelled HH:00, but PVGIS returns the irradiance of the SARAH time stamp, offset
from HH:00 by the "irradiance time offset" of the site (0.1762 h for this file); the offset is
needed when the sun position is computed for these values (PVGIS TMY tool documentation).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from energy_training.utilities.paths import repo_root
from energy_training.utilities.units import celsius_to_kelvin

__all__ = [
    "IRRADIANCE_TIME_OFFSET_H",
    "NOMINAL_YEAR",
    "TMY_FILE",
    "COLUMNS",
    "read_raw_tmy",
    "load_tmy",
    "write_buildings_mos",
]

IRRADIANCE_TIME_OFFSET_H = 0.1762
"""Offset [h] of the irradiance values from the HH:00 row label (from the PVGIS response)."""

NOMINAL_YEAR = 2023
"""Non-leap year used to label the continuous TMY index (no meaning beyond the label)."""

TMY_FILE = Path("data/processed/weather_turin_tmy.csv")
"""Path of the committed TMY file, relative to the repository root."""

COLUMNS = {
    "T2m": ("T_amb", "K", "2-m air temperature (file: degC)"),
    "RH": ("RH", "%", "relative humidity"),
    "G(h)": ("G_h", "W/m2", "global irradiance on the horizontal plane"),
    "Gb(n)": ("G_bn", "W/m2", "beam irradiance on a plane normal to the sun rays"),
    "Gd(h)": ("G_dh", "W/m2", "diffuse irradiance on the horizontal plane"),
    "IR(h)": ("IR_h", "W/m2", "infrared (thermal) irradiance on the horizontal plane"),
    "WS10m": ("v_wind", "m/s", "10-m wind speed"),
    "WD10m": ("dir_wind", "deg", "10-m wind direction (0 = N, 90 = E)"),
    "SP": ("p_amb", "Pa", "surface air pressure"),
}
"""PVGIS column -> (course name, unit after :func:`load_tmy`, description)."""


def read_raw_tmy(path: str | Path | None = None) -> pd.DataFrame:
    """Read the TMY file as stored: PVGIS column names and units, original UTC time stamps."""
    path = Path(path) if path is not None else repo_root() / TMY_FILE
    return pd.read_csv(path, parse_dates=["time_utc"])


def load_tmy(path: str | Path | None = None) -> pd.DataFrame:
    """Return the TMY with SI columns (see :data:`COLUMNS`) on a continuous hourly UTC index.

    The index runs from 1 January ``NOMINAL_YEAR`` 00:00 UTC in 8760 hourly steps. Each row
    keeps the value of the same calendar hour in the original file; ``source_year`` records the
    year the month was taken from.
    """
    raw = read_raw_tmy(path)
    if len(raw) != 8760:
        raise ValueError(f"expected 8760 hourly rows, got {len(raw)}")
    stamps = raw["time_utc"]
    nominal = pd.to_datetime(
        {
            "year": NOMINAL_YEAR,
            "month": stamps.dt.month,
            "day": stamps.dt.day,
            "hour": stamps.dt.hour,
        }
    )
    index = pd.DatetimeIndex(nominal, name="time").tz_localize("UTC")
    expected = pd.date_range(f"{NOMINAL_YEAR}-01-01", periods=8760, freq="h", tz="UTC")
    if not index.equals(expected):
        raise ValueError("TMY time stamps do not form one complete hourly year")
    out = raw.drop(columns="time_utc").rename(columns={k: v[0] for k, v in COLUMNS.items()})
    out["T_amb"] = celsius_to_kelvin(out["T_amb"].to_numpy())
    out["source_year"] = stamps.dt.year.to_numpy()
    out.index = index
    return out


_MOS_COLUMNS = [
    "Time in seconds. Beginning of a year is 0s.",
    "Dry bulb temperature in Celsius at indicated time",
    "Dew point temperature in Celsius at indicated time",
    "Relative humidity in percent at indicated time",
    "Atmospheric station pressure in Pa at indicated time",
    "Extraterrestrial horizontal radiation in Wh/m2",
    "Extraterrestrial direct normal radiation in Wh/m2",
    "Horizontal infrared radiation intensity in Wh/m2",
    "Global horizontal radiation in Wh/m2",
    "Direct normal radiation in Wh/m2",
    "Diffuse horizontal radiation in Wh/m2",
    "Averaged global horizontal illuminance in lux during minutes preceding the indicated time",
    "Direct normal illuminance in lux during minutes preceding the indicated time",
    "Diffuse horizontal illuminance in lux during minutes preceding the indicated time",
    "Zenith luminance in Cd/m2 during minutes preceding the indicated time",
    "Wind direction at indicated time. N=0, E=90, S=180, W=270",
    "Wind speed in m/s at indicated time",
    "Total sky cover at indicated time",
    "Opaque sky cover at indicated time",
    "Visibility in km at indicated time",
    "Ceiling height in m",
    "Present weather observation",
    "Present weather codes",
    "Precipitable water in mm",
    "Aerosol optical depth",
    "Snow depth in cm",
    "Days since last snowfall",
    "Albedo",
    "Liquid precipitation depth in mm at indicated time",
    "Liquid precipitation quantity",
]
"""Column descriptions of a Modelica Buildings weather file (as in the library's own files)."""


def write_buildings_mos(
    path: str | Path,
    raw: pd.DataFrame | None = None,
    *,
    lat: float = 45.070,
    lon: float = 7.687,
    elevation: float = 250.0,
    offset_h: float = IRRADIANCE_TIME_OFFSET_H,
) -> Path:
    """Write the TMY as a weather file for ``Buildings.BoundaryConditions.WeatherData.ReaderTMY3``.

    The Buildings reader (Buildings 14.0.0) reads solar radiation 30 min *before* the row time,
    because TMY3 radiation is the energy of the hour ending at the time stamp. PVGIS irradiance
    is instead the value at label + ``offset_h`` (UTC). To make the reader use every value at
    its true instant (checked against PVGIS in-plane irradiance in the Session 5 PV spike):

    - time zone 0 (UTC) in the ``#LOCATION`` line;
    - row ``j`` (UTC label ``j`` h) at time ``(j + offset_h + 0.5) * 3600`` s;
    - solar radiation columns (global, direct normal, diffuse) as delivered: the reader shifts
      only these three columns by 30 min (``ReaderTMY3``, reader ``datRea30Min``);
    - all other columns read at the row time (temperature, humidity, pressure, wind speed and
      infrared radiation) interpolated to the row time.

    Pressure is written but not read by default (``pAtmSou = Parameter``, 101325 Pa). The first
    row is at 0.676 h: the reader extrapolates over the first 0.676 h of the year, and the last
    row repeats the last values (``numpy.interp`` clamps); both effects are limited to the first
    and last hour of the year.

    Columns PVGIS does not provide (dew point, sky cover, illuminance, ...) are written as
    placeholders. They are not read when the reader is configured as in the course:
    ``calTSky = HorizontalRadiation``, ``TDewPoiSou``, ``totSkyCovSou``, ``opaSkyCovSou`` and
    ``ceiHeiSou`` = ``Parameter``, ``computeWetBulbTemperature = false``.
    """
    import numpy as np

    raw = read_raw_tmy() if raw is None else raw
    n = len(raw)
    if n != 8760:
        raise ValueError(f"expected 8760 hourly rows, got {n}")
    label = np.arange(n, dtype=float)  # [h] since 1 Jan 00:00 UTC
    t_row = label + offset_h + 0.5

    def interp(col: str) -> np.ndarray:
        return np.interp(t_row, label, raw[col].to_numpy(dtype=float))

    T, RH, p, ws, ir = (interp(c) for c in ("T2m", "RH", "SP", "WS10m", "IR(h)"))
    placeholder_dew = T  # placeholder, not read with TDewPoiSou = Parameter
    lines = [
        "#1",
        f"double tab1({n},30)",
        f"#LOCATION,Turin,-,ITA,PVGIS 5.3 TMY,-,{lat:.3f},{lon:.3f},0.0,{elevation:.1f}",
        "#COMMENTS 1,Written by energy_training.data.weather.write_buildings_mos from "
        "data/processed/weather_turin_tmy.csv (PVGIS 5.3 TMY; PVGIS (c) European Communities "
        "2001-2026; contains modified Copernicus Climate Change Service information 2026)",
        f"#COMMENTS 2,Time zone 0 (UTC); rows at label + {offset_h} h + 0.5 h; non-solar columns "
        "interpolated; placeholders in columns not provided by PVGIS",
        "#DATA PERIODS,1,1,Data,Sunday, 1/ 1,12/31",
        *(f"#C{i + 1} {d}" for i, d in enumerate(_MOS_COLUMNS)),
    ]
    for j in range(n):
        r = raw.iloc[j]
        row = [
            f"{t_row[j] * 3600.0:.1f}",
            f"{T[j]:.2f}",
            f"{placeholder_dew[j]:.2f}",
            f"{RH[j]:.2f}",
            f"{p[j]:.0f}",
            "0",
            "0",
            f"{ir[j]:.2f}",
            f"{r['G(h)']:.2f}",
            f"{r['Gb(n)']:.2f}",
            f"{r['Gd(h)']:.2f}",
            "0",
            "0",
            "0",
            "0",
            f"{r['WD10m']:.0f}",
            f"{ws[j]:.2f}",
            "5",
            "5",
            "16",
            "20000",
            "9",
            "999999999",
            "0",
            "0.1",
            "0",
            "88",
            "0.2",
            "0",
            "1",
        ]
        lines.append("\t".join(row))
    path = Path(path)
    path.write_text("\n".join(lines) + "\n")
    return path
