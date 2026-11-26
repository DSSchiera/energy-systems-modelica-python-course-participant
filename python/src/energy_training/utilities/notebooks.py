"""Exercise notebooks: run their code cells without a kernel, compare starting file and solution.

A starting notebook and its solution have the same cells; only cells tagged ``exercise`` differ.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

EXERCISE_TAG = "exercise"


def _cells(path: str | Path) -> list[dict[str, Any]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))["cells"]


def _source(cell: dict[str, Any]) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else src


def _tags(cell: dict[str, Any]) -> list[str]:
    return list(cell.get("metadata", {}).get("tags", []))


def run_code_cells(path: str | Path, skip_tags: Iterable[str] = ()) -> dict[str, Any]:
    """Execute the code cells of a notebook in order, in one fresh namespace; return it.

    No kernel and no output capture: use it in tests to read the variables a notebook computes.
    Plots are created but not shown (select a non-interactive Matplotlib backend first).
    Cells carrying one of ``skip_tags`` (for example ``omc``: needs OpenModelica) are skipped.
    """
    skip = set(skip_tags)
    namespace: dict[str, Any] = {"__name__": "__notebook__"}
    for i, cell in enumerate(_cells(path)):
        if cell["cell_type"] == "code" and not skip.intersection(_tags(cell)):
            exec(compile(_source(cell), f"{Path(path).name}[cell {i}]", "exec"), namespace)
    return namespace


def starter_solution_problems(starter: str | Path, solution: str | Path) -> list[str]:
    """Differences that are not allowed between a starting notebook and its solution.

    Allowed: different sources in cells tagged ``exercise``. Not allowed: a different number,
    type or tags of cells, a different provided (untagged) cell, or outputs in either notebook.
    """
    a, b = _cells(starter), _cells(solution)
    problems: list[str] = []
    if len(a) != len(b):
        return [f"{len(a)} cells in the starting notebook, {len(b)} in the solution"]
    for i, (ca, cb) in enumerate(zip(a, b, strict=True)):
        if ca["cell_type"] != cb["cell_type"] or _tags(ca) != _tags(cb):
            problems.append(f"cell {i}: type or tags differ")
        elif EXERCISE_TAG not in _tags(ca) and _source(ca) != _source(cb):
            problems.append(f"cell {i}: provided cell differs (tag it '{EXERCISE_TAG}'?)")
        for name, cell in (("starting notebook", ca), ("solution", cb)):
            if cell.get("outputs") or cell.get("execution_count"):
                problems.append(f"cell {i}: {name} has outputs (clear them before committing)")
    return problems
