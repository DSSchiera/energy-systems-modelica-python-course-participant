"""Read OpenModelica CSV results (``simulate(..., outputFormat="csv")``) into pandas."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

__all__ = ["read_result", "solver_stats"]


def read_result(csv: str | Path, *, unique_time: bool = True) -> pd.DataFrame:
    """Return the result as a DataFrame indexed by ``time`` [s], one column per variable.

    OpenModelica writes a row before and after every event, so a time can appear twice. With
    ``unique_time`` (default) only the first row of each time is kept, which gives a strictly
    increasing index that can be compared with other results sample by sample.
    """
    df = pd.read_csv(csv)
    if unique_time:
        df = df.drop_duplicates(subset="time", keep="first")
    return df.set_index("time")


_STATS = {
    "state_events": r"(\d+) state events",
    "time_events": r"(\d+) time events",
    "steps": r"(\d+) steps taken",
    "f_calls": r"(\d+) calls of functionODE",
    "jacobians": r"(\d+) evaluations of jacobian",
    "error_test_failures": r"(\d+) error test failures",
    "convergence_failures": r"(\d+) convergence test failures",
}


def solver_stats(log: str) -> dict[str, float | str]:
    """Statistics printed by a simulation run with the runtime flag ``-lv=LOG_STATS``.

    Returns ``solver`` (method name), ``steps``, ``f_calls`` (evaluations of the right-hand
    side), ``jacobians``, ``state_events``, ``time_events``, ``error_test_failures``,
    ``convergence_failures`` and ``cpu_time`` [s] (the ``total`` timer of the simulation
    executable). Raises ``ValueError`` if the log has no statistics.
    """
    if "### STATISTICS ###" not in log:
        raise ValueError("no solver statistics in the log: simulate with simflags='-lv=LOG_STATS'")
    log = log[log.index("### STATISTICS ###") :]  # other messages may contain similar words
    stats: dict[str, float | str] = {}
    solver = re.search(r"solver: (\w+)", log)
    stats["solver"] = solver.group(1) if solver else ""
    for key, pattern in _STATS.items():
        m = re.search(pattern, log)
        stats[key] = int(m.group(1)) if m else 0
    total = re.search(r"([0-9.e+-]+)s \[\s*100\.0%\] total", log)
    stats["cpu_time"] = float(total.group(1)) if total else float("nan")
    return stats
