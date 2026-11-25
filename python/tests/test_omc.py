"""Tests of energy_training.omc that need no OpenModelica (the simulations themselves run in the
course's Modelica checks, the Session 3 notebook and the G3.1 comparison script)."""

import pandas as pd
import pytest

from energy_training.omc.results import read_result, solver_stats
from energy_training.omc.runner import MSL_VERSION, build_script, find_omc, write_variant


def test_script_loads_msl_library_and_files_then_simulates():
    s = build_script(
        "S03_G1_ZoneRC",
        ["C:\\work\\my model.mo"],
        library="/work/modelica/EnergyTraining/package.mo",
        result_prefix="S03_G1_ZoneRC",
        stop_time=7200.0,
        interval=600.0,
        tolerance=1e-8,
    )
    assert f'loadModel(Modelica, {{"{MSL_VERSION}"}})' in s
    assert s.index("EnergyTraining/package.mo") < s.index("my model.mo") < s.index("simulate(")
    assert 'loadFile("C:/work/my model.mo")' in s  # backslashes are not escapes in omc strings
    assert "stopTime=7200.0, numberOfIntervals=12, tolerance=1e-08" in s
    assert 'outputFormat="csv"' in s


def test_script_without_settings_uses_experiment_annotation():
    s = build_script("M", [], library=None, result_prefix="M")
    assert "stopTime" not in s and "tolerance" not in s and "loadFile" not in s


def test_read_result_drops_repeated_event_rows(tmp_path):
    csv = tmp_path / "r_res.csv"
    pd.DataFrame({"time": [0.0, 1.0, 1.0, 2.0], "x": [0.0, 1.0, 5.0, 6.0]}).to_csv(csv, index=False)
    df = read_result(csv)
    assert list(df.index) == [0.0, 1.0, 2.0]
    assert df.loc[1.0, "x"] == 1.0  # value before the event
    assert len(read_result(csv, unique_time=False)) == 4


def test_find_omc_uses_openmodelicahome(tmp_path, monkeypatch):
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))
    monkeypatch.setenv("OPENMODELICAHOME", str(tmp_path))
    assert find_omc() is None
    (tmp_path / "bin").mkdir()
    (tmp_path / "bin" / "omc").write_text("")
    assert find_omc() == str(tmp_path / "bin" / "omc")


def test_script_passes_method_and_runtime_flags():
    s = build_script("M", [], library=None, result_prefix="M", method="euler",
                     simflags="-lv=LOG_STATS")  # fmt: skip
    assert 'method="euler"' in s and 'simflags="-lv=LOG_STATS"' in s


def test_translate_script_sets_debug_flags_before_building():
    s = build_script("M", [], library=None, result_prefix="info", action="translate",
                     debug_flags="backenddaeinfo,dumpLoops")  # fmt: skip
    assert s.index('setCommandLineOptions("-d=backenddaeinfo,dumpLoops")') < s.index("buildModel(M")
    assert "simulate(" not in s


def test_write_variant_extends_with_modifiers(tmp_path):
    path = write_variant("Lib.Example", "N20", {"N": 20, "k": 1.5}, tmp_path)
    assert path.read_text() == "model N20\n  extends Lib.Example(N=20, k=1.5);\nend N20;\n"
    with pytest.raises(ValueError):
        write_variant("Lib.Example", "not valid", {}, tmp_path)


LOG = """LOG_STDOUT | info | Chattering detected (100 state events in a row ...).
LOG_STATS         | info    | ### STATISTICS ###
|                 | |       | | timer
|                 | |       | | |      1.25659s [ 34.3%] event-handling
|                 | |       | | |      3.66334s [100.0%] total
|                 | |       | | events
|                 | |       | | | 528782 state events
|                 | |       | | |     0 time events
|                 | |       | | solver: dassl
|                 | |       | | | 567349 steps taken
|                 | |       | | | 567351 calls of functionODE
|                 | |       | | | 543346 evaluations of jacobian
|                 | |       | | |     0 error test failures
|                 | |       | | |     0 convergence test failures
"""  # OpenModelica 1.27.1 output of EnergyTraining.Examples.Broken.ChatteringThermostat


def test_solver_stats_reads_the_statistics_block_only():
    s = solver_stats(LOG)
    assert s["solver"] == "dassl"
    assert s["state_events"] == 528782  # not the "100 state events in a row" of the warning
    assert (s["steps"], s["f_calls"], s["jacobians"]) == (567349, 567351, 543346)
    assert s["cpu_time"] == pytest.approx(3.66334)
    with pytest.raises(ValueError):
        solver_stats("LOG_SUCCESS | info | The simulation finished successfully.")
