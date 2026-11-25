# Software setup (Windows)

Do this once before Session 1 (about 30–45 min, mostly downloads). The same steps work on macOS
and Linux; differences are noted. Use the versions below: the course results were produced with
them.

| Software | Version | Used from |
|----------|---------|-----------|
| uv (Python and package manager) | current release | Session 1 |
| Python | 3.12 (installed by uv) | Session 1 |
| OpenModelica with OMEdit | 1.27.1 | Session 3 (install it now anyway) |
| Modelica Standard Library | 4.1.0 | Session 3 |
| Modelica Buildings Library | 14.0.0 | Session 5 |

## 1. Get the course files

Either install Git for Windows (<https://git-scm.com/download/win>) and clone this repository,
or download it as a ZIP from the repository page and extract it. As a precaution, use a folder
whose path has no spaces or accented characters (for example `C:\course`).

## 2. Install uv

Open **PowerShell** and run (official command from <https://docs.astral.sh/uv/getting-started/installation/>):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternative: `winget install --id=astral-sh.uv -e`. On macOS/Linux:
`curl -LsSf https://astral.sh/uv/install.sh | sh`. Close and reopen PowerShell afterwards.

## 3. Create the Python environment

In PowerShell, inside the course folder:

```powershell
uv sync
uv run pytest
```

`uv sync` downloads Python 3.12 and the exact package versions in `uv.lock` into a local `.venv`
folder. `uv run pytest` must end with a line like `NN passed`.

## 4. Open the notebooks

Either:

- **JupyterLab:** `uv run jupyter lab`, then open `python/notebooks/s00_python_101.ipynb`; or
- **VS Code** with the *Python* and *Jupyter* extensions: open the course folder, open the
  notebook and select the kernel from `.venv`.

Run all cells once: they must complete without errors. The Session 0 guide
(`course/session_00_python_101/guide.md`) explains notebooks and the environment in more detail.

## 5. Install OpenModelica (needed from Session 3)

1. Download OpenModelica **1.27.1** for Windows from
   <https://openmodelica.org/download/download-windows/> and install it with the default options.
2. Start **OMEdit**. Install the Modelica Standard Library **4.1.0** from
   *File → Manage Libraries → Install Library*.
3. Open the course library: *File → Open Model/Library File(s)* →
   `modelica/EnergyTraining/package.mo`.
4. In the library browser, open `EnergyTraining.Validation.SmokeTest` and run
   *Simulation → Simulate*. The simulation must finish without errors.

From Session 3 some Python scripts and notebooks run OpenModelica themselves (module
`energy_training.omc`). They use the `omc` program of this installation, found on `PATH` or in
the folder named by the `OPENMODELICAHOME` environment variable. If MSL 4.1.0 is missing they ask
OpenModelica to install it (a download). A Docker-based alternative exists for the instructors and
is not needed for the course.

The Buildings library is installed in Session 5; the instructions will be given then.

## Problems?

Note the exact error message and the step where it appeared, and bring it to the next session.
First things to check: PowerShell was reopened after installing uv; the course folder path has no
spaces or non-ASCII characters.

<!-- Provenance (development repository): uv commands from uv-docs (checked 2026-11-18);
     OpenModelica 1.27.1 for Windows from om-download-windows; OMEdit menu paths from
     om-users-guide, OMEdit chapter (checked 2026-11-18). Steps to be confirmed in the Windows
     dry run. -->
