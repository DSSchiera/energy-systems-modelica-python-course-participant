# Syllabus

Nine sessions of 2.5 h each: Session 0 (Python 101) plus the 8 core sessions (20 h).
Each session combines theory, guided modelling on your own machine and exercises.
Model IDs refer to [model_lineage.md](model_lineage.md).

---

## Session 0 — Python 101

**Contact session, extra to the 20 h core.**
**Canonical material:** the guide in `course/session_00_python_101/`, the notebook
`python/notebooks/s00_python_101.ipynb` and exercise S0.1, on the Turin weather data.
Before the session the participant installs the environment ([SETUP.md](../SETUP.md) up to "open the notebooks", about 30–45 min, mostly downloads).

**Content**
- Course map and the case-study building; why Python next to Modelica
- The working environment: uv, the course package `energy_training`, notebooks and scripts in JupyterLab
- The Python subset used in the course; NumPy arrays
- pandas time series on the Turin typical year; Matplotlib and the course plotting pattern; units (SI in the computation, °C and kWh for display)
- SciPy: fit of the annual temperature cycle; a first steady-state estimate of the house's heat demand
- Exercise S0.1 (Python self-check); tools met later in the course

---

## Session 1 — Dynamic Systems Modelling Fundamentals

**Canonical model:** M01 `ThermalZone` (single thermal mass), implemented in **Python first**.

**Content**
- Static vs dynamic systems; states, inputs, outputs, parameters; lumped modelling and its validity
- M01: energy balance $C\,\dot T = \dot Q - UA\,(T - T_{amb})$, equilibrium, time constant $\tau = C/UA$, analytic step response
- Numerical integration in Python: explicit Euler written by hand, `scipy.integrate.solve_ivp`; step size, tolerance and stability
- State-space form, linearity and superposition; preview of two-state models (M02) and of DAEs
- Exercises G1.1 (step response) and I1.1 (heater schedule and energy use)

## Session 2 — Energy Systems Modelling Fundamentals

**Canonical models:** M02 `ZoneRC` (2 nodes), M03 `Storage` (N-node tank), Python.

**Content**
- Conservation laws and control volumes; mass and energy balances for open systems with enthalpy flows
- Heat transfer modes, thermal resistance and capacitance, the electrical analogy
- M02: zone air + building mass (2R2C) in state-space form, simulated in Python
- M03: storage tank with N mixed nodes and a through-flow; global energy balance check
- Simple heat exchangers (ε-NTU); dynamic vs steady-state component models; model fidelity and numerical diffusion
- Exercises G2.1 (energy balance of M03) and I2.1 (dominant time constants of M02)

## Session 3 — Modelica Fundamentals

**Canonical models:** M01 and M02 re-implemented in Modelica (teaching components + MSL). **Main reference:** *Modelica by Example* (pre-reading and section-by-section reading map in the lesson), with the Fritzson OpenModelica tutorial (2025).

**Content**
- Equation-based vs assignment-based modelling; acausal vs causal; what the compiler does
- M01 as a single Modelica model: parameters, SI types and units, `der()`, `initial equation`, `experiment`
- Connectors (across and through variables), teaching components, balanced models
- The Modelica Standard Library heat-transfer package; packages, `within`, `import`
- Modifications, inheritance and replaceable components; M02 by composition
- Three formulations of M01 (equations, components, block diagram); Python vs Modelica
- Exercises G3.1 (M02 from components) and I3.1 (simplified PV and battery components)

## Session 4 — OpenModelica Workflow and Numerical Modelling

**Canonical models:** M03 `Storage` in Modelica; M01 with a steady start and a time-dependent disturbance (`Examples.S04_SteadyStartStep`); `EnergyTraining.Examples.Broken.*`. **Main reference** for initialization and events: *Modelica by Example* (pre-reading and reading map in the lesson), with the Fritzson OpenModelica tutorial (2025); solvers and tools: OpenModelica User's Guide.

**Content**
- From model to simulation: flattening, structural analysis, index, algebraic loops and tearing
- The OMEdit workflow and the simulation log
- Initialization: initial equations, `start`/`fixed`, over- and under-determined initial systems; steady start and a disturbance
- Events and discontinuities: time and state events, `noEvent`, `when`/`pre`; thermostat chattering vs hysteresis
- Stiffness and solver choice; tolerances; CPU time vs accuracy
- Exercises G4.1 (diagnose broken models) and I4.1 (convergence study); a debugging checklist

## Session 5 — Thermo-Hydraulic Systems, Heat Pumps and System Assembly

**Canonical models:** M04 `HydronicLoop` (Buildings library, fluid view), M05 `BuildingEnergySystem`
(case study: heat pump + thermal storage + zone + PV + battery, thermal/power domain).

**Content**
- Fluid connectors and stream variables; media models; pumps, pipes, valves; pressure reference
- The Buildings library; M04 hydronic loop: flow, temperature and pressure drop
- Heat pump fundamentals (Carnot COP, fraction-of-Carnot model); district heating in brief
- M05: the case-study energy system (heat pump, tank, zone, PV, battery, grid) on a winter and a summer day
- Rule-based operation as the baseline for Sessions 7–8
- Exercises G5.1 (daily COP and PV self-consumption) and I5.1 (pump flow and pipe length)

## Session 6 — FMI/FMU and Python Integration

**Canonical model:** M06 `BuildingEnergySystemFMU` (M05 with top-level inputs/outputs and size parameters).

**Content**
- FMI architecture: FMU contents, Model Exchange vs Co-Simulation, causality and variability, FMI 2.0 vs 3.0
- Export of M06 from OpenModelica; `modelDescription.xml`
- Simulating the FMU from Python with FMPy; cross-check with OpenModelica
- Input data with pandas and energy KPIs (grid import/export, self-consumption, self-sufficiency, seasonal COP)
- Scenario runner: batches of simulations; representative days vs a full year
- Exercises G6.1 (KPI table for a set of asset sizes) and I6.1 (Co-Simulation with a battery rule in Python)

## Session 7 — Techno-Economic Assessment and Scenario Analysis

**Canonical experiment:** M07 techno-economic assessment of the case study (Python `economics` on M06 results).

**Content**
- Techno-economic framework: CAPEX, OPEX, replacements, discount rate, annuity, NPV, LCOE/LCOH, payback; tariff structures
- From simulation results to cash flows for a reference system and its variants
- Scenario design: what-if analysis, one-at-a-time sensitivity, tornado chart; uncertainty of cost data
- Design by heuristics: parametric sweeps of sizes with rule-based operation and their limits
- Exercises G7.1 (NPV and LCOE of four configurations) and I7.1 (sensitivity of the best PV/battery size)

## Session 8 — Optimization of Design and Operation

**Canonical experiments:** M08a operational dispatch (LP/MILP), M08b design optimization (sizing).

**Content**
- Optimization problem anatomy: variables, objective, constraints; LP, MILP, NLP; heuristics vs mathematical programming
- M08a: operational dispatch on representative days with `scipy.optimize`; cost vs rule-based operation
- Linear surrogate vs dynamic model; replaying the optimal schedule on the FMU
- M08b: joint sizing and dispatch as a MILP; comparison with the Session 7 sweep; outlook on nonlinear models
- Exercises G8.1 (dispatch under different tariffs) and I8.1 (extension); course wrap-up
