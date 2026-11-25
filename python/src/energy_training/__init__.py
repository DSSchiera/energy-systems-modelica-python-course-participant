"""energy_training — Python package of the course
'Dynamic Modelling, Modelica and Techno-Economic Optimization of Energy Systems'.

Subpackages
-----------
simulation   : causal ODE implementations of the canonical models (M01-M03) and solvers
omc          : thin wrappers to run OpenModelica (omc) scripts and read results
fmu          : FMU inspection, simulation, input trajectories and scenario batches (FMPy)
data         : weather and demand profiles of the case study (planned)
economics    : costs, tariffs, NPV, levelised costs, KPIs (planned)
optimization : dispatch and sizing (LP/MILP) for the case study (planned)
plotting     : consistent course figure style
utilities    : units, paths, result I/O
"""

__version__ = "0.1.0.dev0"
