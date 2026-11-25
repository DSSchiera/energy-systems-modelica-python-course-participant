"""Tests for energy_training.data.weather (PVGIS TMY for Turin)."""

import numpy as np
import pandas as pd
import pytest

from energy_training.data import weather


@pytest.fixture(scope="module")
def tmy():
    return weather.load_tmy()


def test_continuous_hourly_index(tmy):
    assert len(tmy) == 8760
    assert tmy.index.tz is not None
    assert (tmy.index.to_series().diff().dropna() == pd.Timedelta(hours=1)).all()
    assert tmy.index[0] == pd.Timestamp(f"{weather.NOMINAL_YEAR}-01-01", tz="UTC")


def test_columns_and_units(tmy):
    expected = {v[0] for v in weather.COLUMNS.values()} | {"source_year"}
    assert set(tmy.columns) == expected
    raw = weather.read_raw_tmy()
    # temperature converted degC -> K, row by row
    np.testing.assert_allclose(tmy["T_amb"].to_numpy(), raw["T2m"].to_numpy() + 273.15)
    np.testing.assert_allclose(tmy["G_h"].to_numpy(), raw["G(h)"].to_numpy())


def test_one_source_year_per_month(tmy):
    per_month = tmy.groupby(tmy.index.month)["source_year"].nunique()
    assert (per_month == 1).all()


def test_physical_ranges(tmy):
    assert tmy["T_amb"].between(273.15 - 30, 273.15 + 45).all()
    assert (tmy[["G_h", "G_bn", "G_dh"]] >= 0).all().all()
    assert tmy["RH"].between(0, 100).all()
    # diffuse cannot exceed global horizontal irradiance
    assert (tmy["G_dh"] <= tmy["G_h"] + 1e-9).all()


def test_annual_values_plausible(tmy):
    """Annual horizontal irradiation and mean temperature of this file (regression values)."""
    H_h = tmy["G_h"].sum() * 3600 / 3.6e6  # Wh/m2 per hourly sample -> kWh/m2
    assert H_h == pytest.approx(1528.5, abs=0.1)
    assert tmy["T_amb"].mean() - 273.15 == pytest.approx(12.22, abs=0.01)


def test_wrong_length_rejected(tmp_path):
    raw = weather.read_raw_tmy()
    bad = tmp_path / "short.csv"
    raw.iloc[:100].to_csv(bad, index=False)
    with pytest.raises(ValueError, match="8760"):
        weather.load_tmy(bad)


def test_write_buildings_mos(tmp_path):
    raw = weather.read_raw_tmy()
    out = weather.write_buildings_mos(tmp_path / "turin.mos", raw)
    lines = out.read_text().splitlines()
    assert lines[0] == "#1" and lines[1] == "double tab1(8760,30)"
    loc = next(ln for ln in lines if ln.startswith("#LOCATION")).split(",")
    assert len(loc) == 10 and float(loc[6]) == 45.07 and float(loc[8]) == 0.0  # lat, UTC
    data = np.array(
        [[float(v) for v in ln.split("\t")] for ln in lines if not ln.startswith(("#", "double"))]
    )
    assert data.shape == (8760, 30)
    shift = weather.IRRADIANCE_TIME_OFFSET_H + 0.5
    np.testing.assert_allclose(data[:, 0], (np.arange(8760) + shift) * 3600.0, atol=0.06)
    # radiation as delivered (read by Buildings 30 min before the row time = true instant)
    np.testing.assert_allclose(data[:, 8], raw["G(h)"], atol=0.006)
    np.testing.assert_allclose(data[:, 9], raw["Gb(n)"], atol=0.006)
    np.testing.assert_allclose(data[:, 10], raw["Gd(h)"], atol=0.006)
    # temperature interpolated to the row time
    T = raw["T2m"].to_numpy()
    expected = T[100] + shift * (T[101] - T[100])
    assert data[100, 1] == pytest.approx(expected, abs=0.006)
    IR = raw["IR(h)"].to_numpy()  # infrared is not shifted by the reader: interpolated too
    assert data[100, 7] == pytest.approx(IR[100] + shift * (IR[101] - IR[100]), abs=0.006)
