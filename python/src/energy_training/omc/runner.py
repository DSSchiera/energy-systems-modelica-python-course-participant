"""Simulate a Modelica model with OpenModelica from Python and return the CSV result file.

Two back ends, chosen automatically:

- ``native``: the ``omc`` compiler of a local OpenModelica installation (on ``PATH``, or in
  ``$OPENMODELICAHOME/bin`` when that variable is set);
- ``docker``: the course's pinned image (default ``openmodelica/openmodelica:v1.27.1-minimal``),
  with the Modelica libraries cached in the Docker volume ``energy-training-omlibs``. All files
  must then lie inside the repository, which is mounted at ``/work``.

The script given to ``omc`` loads the Modelica Standard Library 4.1.0 (installed on first use if
missing), optionally the course library ``EnergyTraining``, then the given files, and calls
``simulate(..., outputFormat="csv")`` (:func:`simulate`) or ``instantiateModel`` (:func:`flatten`).
Simulation settings not passed here come from the model's ``experiment`` annotation.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from energy_training.omc.results import read_result, solver_stats
from energy_training.utilities.paths import repo_root

__all__ = [
    "OMC_IMAGE",
    "MSL_VERSION",
    "SimulationRun",
    "find_omc",
    "build_script",
    "simulate",
    "flatten",
    "backend_info",
    "write_variant",
    "VariantRun",
    "simulate_variant",
]

OMC_IMAGE = os.environ.get("OM_IMAGE", "openmodelica/openmodelica:v1.27.1-minimal")
"""Docker image of the ``docker`` back end (the version pinned for the course)."""

MSL_VERSION = "4.1.0"
"""Version of the Modelica Standard Library loaded before the model."""

LIBRARY = Path("modelica/EnergyTraining/package.mo")
"""Course library, relative to the repository root."""


@dataclass(frozen=True)
class SimulationRun:
    """Outcome of :func:`simulate`."""

    csv: Path
    """Result file (one column per variable, first column ``time``)."""
    log: str
    """Everything ``omc`` printed, for reading error messages."""


def find_omc() -> str | None:
    """Path of a local ``omc`` executable, or ``None``."""
    found = shutil.which("omc")
    if found:
        return found
    home = os.environ.get("OPENMODELICAHOME")
    if home:
        for name in ("omc.exe", "omc"):
            candidate = Path(home) / "bin" / name
            if candidate.is_file():
                return str(candidate)
    return None


def _mo_string(path: str) -> str:
    """A path as a Modelica string literal (forward slashes also work on Windows)."""
    return '"' + path.replace("\\", "/").replace('"', '\\"') + '"'


_FLAT_BEGIN, _FLAT_END = "=== flat model begin ===", "=== flat model end ==="
_INFO_BEGIN = "=== back-end report begin ==="


def build_script(
    model: str,
    files: Sequence[str],
    *,
    library: str | None,
    result_prefix: str,
    stop_time: float | None = None,
    interval: float | None = None,
    tolerance: float | None = None,
    method: str | None = None,
    simflags: str | None = None,
    debug_flags: str | None = None,
    action: str = "simulate",
) -> str:
    """Text of the ``.mos`` script run by :func:`simulate` (``action="simulate"``),
    :func:`flatten` (``action="flatten"``) or :func:`backend_info` (``action="translate"``);
    paths as ``omc`` will see them."""
    lines = [
        "echo(false);",
        f'if not loadModel(Modelica, {{"{MSL_VERSION}"}}) then',
        f'  installPackage(Modelica, "{MSL_VERSION}+maint.om", exactMatch=true);',
        f'  loadModel(Modelica, {{"{MSL_VERSION}"}});',
        "end if;",
        "echo(true);",
        "getErrorString();",
    ]
    for f in ([library] if library else []) + list(files):
        lines += [
            f"ok := loadFile({_mo_string(f)}); getErrorString();",
            f'if not ok then print("FAILED to load {f}\\n"); exit(1); end if;',
        ]
    if action == "flatten":
        lines += [
            f'print("{_FLAT_BEGIN}\\n");',
            f"print(instantiateModel({model}));",
            f'print("\\n{_FLAT_END}\\n");',
            "getErrorString();",
            "exit(0);",
        ]
        return "\n".join(lines) + "\n"
    if action == "translate":
        if debug_flags:
            lines.append(f'setCommandLineOptions("-d={debug_flags}"); getErrorString();')
        lines += [
            f'print("{_INFO_BEGIN}\n");',
            f'buildModel({model}, fileNamePrefix="{result_prefix}");',
            "getErrorString();",
            "exit(0);",
        ]
        return "\n".join(lines) + "\n"
    options = ['outputFormat="csv"', f'fileNamePrefix="{result_prefix}"']
    if stop_time is not None:
        options.append(f"stopTime={stop_time!r}")
    if interval is not None and stop_time is not None:
        options.append(f"numberOfIntervals={max(1, round(stop_time / interval))}")
    if tolerance is not None:
        options.append(f"tolerance={tolerance!r}")
    if method is not None:
        options.append(f'method="{method}"')
    if simflags is not None:
        options.append(f"simflags={_mo_string(simflags)}")
    lines += [
        f"simulate({model}, {', '.join(options)});",
        "getErrorString();",
        f'if not regularFileExists("{result_prefix}_res.csv") then exit(1); end if;',
        "exit(0);",
    ]
    return "\n".join(lines) + "\n"


def simulate(
    model: str,
    files: Sequence[str | Path] = (),
    *,
    out_dir: str | Path,
    load_library: bool = True,
    stop_time: float | None = None,
    interval: float | None = None,
    tolerance: float | None = None,
    method: str | None = None,
    simflags: str | None = None,
    backend: str = "auto",
    timeout: float = 600.0,
) -> SimulationRun:
    """Simulate ``model`` (full class name) and return the CSV result.

    ``files`` are extra ``.mo`` files to load (an exercise model, for example). With
    ``load_library`` the course library ``EnergyTraining`` is loaded first. ``method`` is an
    OpenModelica integration method (``"dassl"``, ``"ida"``, ``"cvode"``, ``"euler"``, ...);
    ``simflags`` are runtime flags of the simulation executable, for example
    ``"-lv=LOG_STATS"`` (solver statistics, read them with
    :func:`energy_training.omc.results.solver_stats`). ``backend`` is ``"native"``,
    ``"docker"`` or ``"auto"`` (native if ``omc`` is found). Raises ``RuntimeError`` with the
    ``omc`` output if the simulation fails.
    """
    out = Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    prefix = model.replace(".", "_")
    csv = out / f"{prefix}_res.csv"
    csv.unlink(missing_ok=True)  # never return a stale result
    options = {
        "stop_time": stop_time,
        "interval": interval,
        "tolerance": tolerance,
        "method": method,
        "simflags": simflags,
    }
    log = _run(model, files, out, load_library, backend, timeout, "simulate", prefix, options)
    if not csv.is_file():
        raise RuntimeError(f"simulation of {model} failed:\n{log}")
    return SimulationRun(csv=csv, log=log)


def flatten(
    model: str,
    files: Sequence[str | Path] = (),
    *,
    out_dir: str | Path,
    load_library: bool = True,
    backend: str = "auto",
    timeout: float = 600.0,
) -> str:
    """Return the flat model of ``model`` (OpenModelica ``instantiateModel``): every component
    equation and every equation generated by ``connect``, with full variable names."""
    out = Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    log = _run(model, files, out, load_library, backend, timeout, "flatten", "flat", {})
    if _FLAT_BEGIN not in log or _FLAT_END not in log:
        raise RuntimeError(f"flattening of {model} failed:\n{log}")
    text = log.split(_FLAT_BEGIN, 1)[1].split(_FLAT_END, 1)[0].strip()
    if not text.startswith("class"):
        raise RuntimeError(f"flattening of {model} failed:\n{log}")
    return text


def backend_info(
    model: str,
    files: Sequence[str | Path] = (),
    *,
    out_dir: str | Path,
    flags: str = "backenddaeinfo,dumpLoops",
    load_library: bool = True,
    backend: str = "auto",
    timeout: float = 600.0,
) -> str:
    """Translate ``model`` with the ``omc`` debug flags ``flags`` and return what ``omc`` reports.

    The default flags print the model statistics after the back end (number of states, of
    strong components, of torn linear and nonlinear systems: ``backenddaeinfo``) and the
    equations of every algebraic loop with its iteration variables (``dumpLoops``). List of
    flags: ``omc --help=debug``.
    """
    out = Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    options = {"debug_flags": flags}
    log = _run(model, files, out, load_library, backend, timeout, "translate", "info", options)
    if _INFO_BEGIN not in log:
        raise RuntimeError(f"translation of {model} failed:\n{log}")
    return log.split(_INFO_BEGIN, 1)[1].strip()


def write_variant(base: str, name: str, modifiers: dict[str, object], out_dir: str | Path) -> Path:
    """Write ``<out_dir>/<name>.mo`` = ``model <name> extends <base>(<modifiers>);`` (path).

    Use it for parameters that cannot change after compilation, such as an array size:
    ``write_variant("EnergyTraining.Examples.S04_StorageCharging", "N20", {"N": 20}, out)``.
    The ``experiment`` annotation of ``base`` is not copied: pass ``stop_time`` and ``interval``
    to :func:`simulate`.
    """
    if not name.isidentifier():
        raise ValueError(f"{name!r} is not a valid Modelica class name")
    mods = ", ".join(f"{k}={v}" for k, v in modifiers.items())
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.mo"
    path.write_text(f"model {name}\n  extends {base}({mods});\nend {name};\n")
    return path


@dataclass(frozen=True)
class VariantRun:
    """Outcome of :func:`simulate_variant`."""

    result: pd.DataFrame
    """Result indexed by time [s] (:func:`energy_training.omc.results.read_result`)."""
    stats: dict
    """Solver statistics (:func:`energy_training.omc.results.solver_stats`)."""
    log: str
    """Everything ``omc`` printed."""


def simulate_variant(
    base: str,
    modifiers: dict[str, object],
    *,
    out_dir: str | Path,
    name: str | None = None,
    **options,
) -> VariantRun:
    """Compile and simulate ``base`` with ``modifiers`` (also structural parameters such as an
    array size), with solver statistics.

    ``options`` are passed to :func:`simulate` (``stop_time``, ``interval``, ``tolerance``,
    ``method``, ...); ``stop_time`` and ``interval`` are needed because the variant does not
    inherit the ``experiment`` annotation. Example: M03 with 50 nodes and explicit Euler::

        run = simulate_variant("EnergyTraining.Examples.S04_StorageCharging", {"N": 50},
                               out_dir="output/s04", stop_time=86400, interval=60,
                               method="euler")
        run.result["storage.T_out"], run.stats["steps"]
    """
    name = name or "V_" + "_".join(f"{k}{v}" for k, v in modifiers.items()).replace(".", "p")
    out = Path(out_dir) / name / str(options.get("method") or "default")
    path = write_variant(base, name, modifiers, out)
    flags = " ".join(["-lv=LOG_STATS", options.pop("simflags", None) or ""]).strip()
    run = simulate(name, [path], out_dir=out, simflags=flags, **options)
    return VariantRun(result=read_result(run.csv), stats=solver_stats(run.log), log=run.log)


def _run(
    model: str,
    files: Sequence[str | Path],
    out: Path,
    load_library: bool,
    backend: str,
    timeout: float,
    action: str,
    prefix: str,
    options: dict,
) -> str:
    """Write ``script.mos`` in ``out``, run ``omc`` and return its output."""
    root = repo_root()
    paths = [Path(f).resolve() for f in files]
    library = (root / LIBRARY).resolve() if load_library else None

    if backend == "auto":
        backend = "native" if find_omc() else "docker"
    if backend == "native":
        omc = find_omc()
        if omc is None:
            raise RuntimeError("omc not found: install OpenModelica or use backend='docker'")
        seen = [str(p) for p in paths]
        lib = str(library) if library else None
        cmd = [omc, "script.mos"]
    elif backend == "docker":
        for p in [*paths, out]:
            if not p.is_relative_to(root):
                raise RuntimeError(f"{p} is outside the repository (not visible to docker)")
        seen = [f"/work/{p.relative_to(root).as_posix()}" for p in paths]
        lib = f"/work/{LIBRARY.as_posix()}" if library else None
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{root}:/work",
            "-w", f"/work/{out.relative_to(root).as_posix()}",
            "-v", "energy-training-omlibs:/root/.openmodelica",
            OMC_IMAGE, "omc", "script.mos",
        ]  # fmt: skip
    else:
        raise ValueError(f"unknown backend {backend!r}")

    script = build_script(model, seen, library=lib, result_prefix=prefix, action=action, **options)
    (out / "script.mos").write_text(script)
    proc = subprocess.run(
        cmd, cwd=out, capture_output=True, text=True, timeout=timeout, check=False
    )
    log = proc.stdout + proc.stderr
    if proc.returncode != 0:
        raise RuntimeError(f"omc failed on {model} (backend {backend}):\n{log}")
    return log
