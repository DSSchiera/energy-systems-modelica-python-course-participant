# Session 0 — Python 101 for the course (guide)

Session 0 is a 2.5-h contact session, extra to the 20 core hours. This guide is its reference:
in class the notebook is followed step by step and exercise S0.1 is done at the end.
**Before the session**, do §2 (install the environment, about 30–45 min, mostly downloads).
After the session, use the guide to review; the table below gives the self-study time of each
part if you go through it again on your own (about 4–6 h in all).

| Step | What | Self-study time |
|------|------|------|
| §1–§2 | why Python here; install the environment | 45 min |
| §3 | notebooks and scripts; working in JupyterLab | 30 min |
| §4–§6 | the language subset, the libraries, units | 2–3 h with the notebook |
| §7 | the course package and its tests | 20 min |
| §8 | the tools used later in the course (read only) | 15 min |
| §9 | self-check exercise S0.1 | 30–45 min |

## 1. Why Python in this course

The course writes physical models in **Modelica** (Sessions 3–5) and uses **Python** around
them: to prototype a model before it is written in Modelica (Sessions 1–2), to read and plot
weather and simulation results, to run many simulations of an exported model (an FMU, Session
6), to compute costs (Session 7) and to optimize design and operation (Session 8). You do not
need to be a programmer: you need to read, run and modify short, well-structured code.

The case study of the whole course is one house in Turin with a heat pump, a thermal storage
tank, PV, a battery and a grid connection. Session 0 already uses its weather data.

## 2. Install the environment

Follow the [software setup](../../SETUP.md) guide up to and including "open the
notebooks": get the course files, install **uv**, run `uv sync`, open a notebook (OpenModelica
can wait until Session 3). About 30–45 min, mostly downloads.

What these pieces are `[src: uv-docs]`:

| Piece | Role |
|-------|------|
| **uv** | installs Python and the packages, and runs commands in the course environment |
| `pyproject.toml` | the project: its name and the packages it depends on |
| `.python-version` | the Python version of the project (3.12) |
| `uv.lock` | the **exact** version of every package; written by uv, never edited by hand |
| `.venv/` | the environment itself (a folder in the course directory) |
| **JupyterLab** | the course interface for notebooks and Python files; installed in `.venv` by `uv sync` |

The commands you need:

- `uv sync` makes `.venv` match `uv.lock`. Run it once, and again after updating the course
  files.
- `uv run <command>` runs a command inside the environment, for example
  `uv run python file.py`, `uv run pytest`, `uv run jupyter lab`. Before running, uv checks that
  the lock file and the environment are up to date, and updates them if needed.
- `uv add <package>` adds a package to the project. **Do not use it on the course files:** the
  versions in `uv.lock` are the ones the course results were produced with.

You do not need to "activate" the environment if you always start commands with `uv run`.

> **Why a lock file?** Numerical results change, slightly, between library versions. With the
> same lock file, your plots and numbers match the course material.

## 3. Notebooks and scripts

The course uses both.

- A **notebook** (`.ipynb`) mixes text, code and results. It is for exploring and explaining:
  every session has one in `python/notebooks/`. The course opens notebooks with **JupyterLab**
  (§3.1) `[src: jupyterlab-docs]`.
- A **script** (`.py`) runs from top to bottom: `uv run python exercises/session_00/s00_self_check.py`.
  It is for code that must give the same result every time: exercises, figures, tests. You can
  read and edit scripts in JupyterLab too, and run them from its terminal.

### 3.1 Working in JupyterLab

JupyterLab runs in your web browser, but everything stays on your computer: the files are the
ones in the course folder, and the code runs in the course environment `.venv`.

**Start.** Open a terminal (PowerShell on Windows) in the course folder and type
`uv run jupyter lab`. A browser tab opens on `http://localhost:8888/lab`. Keep the terminal open:
closing it stops JupyterLab. Always start it this way, from the course folder: then the notebook
kernel, shown top right as **Python 3 (ipykernel)**, is the course environment and
`import energy_training` works.

**The screen.**

| Part | Where | What for |
|------|-------|----------|
| file browser | left side bar, folder icon | open notebooks (`python/notebooks/`), exercises, scripts, data; right-click for new file, rename, download |
| main area | centre, with tabs | notebooks, text and Python editors, terminals; drag a tab to see two side by side |
| launcher | **+** next to the tabs, or *File → New Launcher* | new notebook, Python file, Markdown file or **terminal** |
| kernel status | top right of a notebook, and the status bar at the bottom | *Python 3 (ipykernel)*; *Idle* or *Busy* |
| table of contents | left side bar, list icon | jump between the sections of a long notebook |

**A cell is in one of two modes** (the blue bar on its left shows the selected cell): *edit mode*
(you type in the cell; press Enter on a selected cell) and *command mode* (keys act on whole cells;
press Esc).

| Action | Key | Menu |
|--------|-----|------|
| run the cell and go to the next one | Shift+Enter | *Run → Run Selected Cell* |
| run the cell and stay on it | Ctrl+Enter (Cmd+Enter on macOS) | *Run → Run Selected Cell and Do not Advance* |
| new cell above / below (command mode) | A / B | **+** in the notebook toolbar (below) |
| make the cell Markdown / code (command mode) | M / Y | cell-type list in the notebook toolbar |
| delete the cell (command mode) | D, D | *Edit → Delete Cell* |
| undo a cell operation (command mode) | Z | *Edit → Undo Cell Operation* |
| interrupt a cell that hangs | I, I | *Kernel → Interrupt Kernel* |
| restart the kernel | 0, 0 | *Kernel → Restart Kernel…* |
| **restart and run everything** | — | ***Kernel → Restart Kernel and Run All Cells…*** |
| save | Ctrl+S (Cmd+S on macOS) | *File → Save Notebook* |

**Scripts and tests inside JupyterLab.** Open a terminal from the launcher. It starts in the
folder shown in the file browser: go back to the course folder first (`cd` there, or click the
folder icon at the start of the file-browser path before opening the terminal). Then use the same
commands as in §2: `uv run python exercises/session_00/s00_self_check.py`, `uv run pytest`.
Double-click a `.py` file in the file browser to edit it.

**Stop.** Save, then *File → Shut Down*; or press Ctrl+C twice in the terminal that started
JupyterLab. Closing only the browser tab leaves JupyterLab and its kernels running.

> **Alternative, optional:** VS Code with the *Jupyter* extension also opens the notebooks;
> choose the course environment (`.venv`) with the kernel picker at the top right of the notebook,
> or with *Notebook: Select Notebook Kernel* `[src: vscode-jupyter]`. The course instructions use
> JupyterLab.

Notebook rules used in the course:

1. A notebook keeps variables in memory in the **kernel**. Running cells out of order gives
   results that nobody can reproduce. Before you trust a result, *Restart* the kernel and
   *Run All*: the notebook must run from top to bottom without errors.
2. Reusable code does not live in notebooks: it lives in the course package (§7), and notebooks
   import it.
3. If a cell seems to hang, *Interrupt* the kernel; if variables are in a strange state,
   *Restart* it (keys and menus in §3.1).

## 4. The Python subset used in the course

Work through notebook `python/notebooks/s00_python_101.ipynb`, §0–§1, while reading this table.
The reference is the official Python tutorial `[src: python-docs]`.

| Feature | Example | First used |
|---------|---------|------------|
| numbers, names, f-strings | `Q_flow = UA * dT`; `f"{Q_flow:.0f} W"` | S0 |
| lists, dicts, `for` loops, comprehensions | `for name in assets:`; `[x**2 for x in range(4)]` | S0 |
| functions with docstrings and keyword arguments | `heat_loss(UA=185.0, T_set=..., T_amb=...)` | S0 |
| frozen dataclasses for parameters | `ThermalZoneParams(C=1e7, UA=200.0)` | S1 |
| imports from the course package | `from energy_training.simulation import thermal_zone` | S1 |
| `try` / `except` to report an error | errors when a simulation fails | S0, S6 |

Not needed: classes beyond dataclasses, decorators other than `@dataclass`, async code,
writing packages.

## 5. The scientific libraries

The notebook §2–§5 covers each with the weather of the case-study house.

| Library | What it is for in the course | Learn in the notebook |
|---------|------------------------------|-----------------------|
| **NumPy** `[src: numpy-docs]` | arrays and vectorised arithmetic: model states, time grids | arrays, masks, copies vs views, float comparison |
| **pandas** `[src: pandas-docs]` | labelled tables and time series: weather, demands, results, cost tables | `read_csv`, time index, `.loc`, `resample`, `groupby`, time zones |
| **Matplotlib** `[src: matplotlib-docs]` | figures | `plt.subplots`, labelled axes with units, a second y axis |
| **SciPy** `[src: scipy-docs]` | algorithms: ODE solvers (S1–S2), optimization (S8) | a first fit with `scipy.optimize.curve_fit` |

The weather data are a **typical meteorological year** for Turin from PVGIS (European
Commission, Joint Research Centre) `[src: pvgis-5.3]`: one value per hour for a year built from
twelve representative months of different years. The notebook shows why this matters when you
read the time stamps.

## 6. Units

Python has no units, so the course follows one rule everywhere: **compute in SI** (K, W, J,
J/K, kg/s, Pa) and convert to °C, kWh or hours **only for display**. Names and comments carry the
unit (`UA = 185.0  # W/K`), and the names follow the course
[notation](../../docs/notation.md) (`T_amb` outdoor temperature, `Q_flow` heat flow rate). The helpers are `energy_training.utilities.celsius_to_kelvin` and
`kelvin_to_celsius`, and, for plots, `energy_training.plotting.style.degc` and `hours`.

## 7. The course package `energy_training`

All reusable code of the course is in one Python package in `python/src/energy_training/`.
`uv sync` installs it into the environment, so `import energy_training` works from any folder.

| Subpackage | Content |
|------------|---------|
| `utilities` | units, repository paths |
| `plotting` | course figure style, K → °C and s → h for display |
| `data` | input data of the case study (weather now; demand profiles later) |
| `simulation` | the Python versions of the course models (from Session 1) |

Each function has a docstring: in a notebook, `help(function)` or `function?` shows it.

The package is checked by **tests** in `python/tests/`. Run them in a terminal from the
course folder:

```bash
uv run pytest
```

It must end with a line like `NN passed`. Run it whenever something seems wrong: if the tests
pass, the environment is fine and the problem is in your code.

## 8. Tools used later in the course (read only)

You do not install or use these now. They are here so that the names are familiar.

| Tool | What it does | Session |
|------|--------------|---------|
| OpenModelica (OMEdit, `omc`) | writes, compiles and simulates Modelica models; exports FMUs | 3–5 |
| OMPython (optional) | drives OpenModelica from Python `[src: ompython]` | 4 (optional) |
| **FMPy** | reads and simulates FMUs (models exported from Modelica) from Python `[src: fmpy]` | 6–8 |
| `scipy.optimize.linprog`, `milp` | linear and mixed-integer optimization: operation and sizing of the house's assets `[src: scipy-docs]` | 8 |
| **CasADi** (optional extra) | nonlinear optimization with automatic derivatives; can import some FMUs `[src: casadi-docs]` | 8 (extension) |
| Pyomo, linopy | algebraic modelling languages for large optimization problems `[src: pyomo-docs]` `[src: linopy-docs]` | mentioned only |

CasADi is installed only if you want the Session 8 extension: `uv sync --extra casadi`.

## 9. Self-check

1. Run the notebook `python/notebooks/s00_python_101.ipynb` with *Restart* and *Run All*,
   without errors.
2. Do exercise **S0.1**: [exercises/session_00/S0.1_python_self_check.md](../../exercises/session_00/S0.1_python_self_check.md).
3. `uv run pytest` ends with "passed".

These three points close Session 0. If one of them fails and there is no time left in class,
note the exact error message and the step where it appeared, and bring it to Session 1.

## Common problems

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `uv: command not found` / not recognised | the terminal was opened before uv was installed | close and reopen the terminal |
| `ModuleNotFoundError: No module named 'energy_training'` in a notebook | JupyterLab was started without `uv run`, or from another Python installation (e.g. Anaconda) | close it; in the course folder start `uv run jupyter lab` (§3.1) |
| `jupyter` not recognised / `Failed to spawn: jupyter` | `uv sync` was not run, or the command was run outside the course folder | `cd` into the course folder, `uv sync`, then `uv run jupyter lab` |
| the browser shows "connection refused" / cannot reach `localhost` | JupyterLab is not running (its terminal was closed) | start `uv run jupyter lab` again |
| no browser tab opens, or the page asks for a password or token | the address was typed by hand, without the token | copy the full `http://localhost:...` address that the terminal prints |
| `ModuleNotFoundError` when running a script | the script was started with `python` instead of `uv run python` | use `uv run python ...` |
| `FileNotFoundError` for a data file | the command was run outside the course folder | `cd` into the course folder first |
| results differ slightly from the course material | different package versions | `uv sync` (do not upgrade packages) |
| a notebook works, but not after *Restart* + *Run All* | cells were run out of order, or a variable was defined in a deleted cell | fix the order; keep the notebook runnable from the top |
