# Syllabus and detailed timetable

Budget: 8 × 150 min. Each timetable is planned for 140 min (130 min contact + one 10-min break),
leaving a **10-min buffer** per session for overruns, installation issues and questions.
Targets: theory 25–30 %, guided modelling 40–50 %, exercises/discussion 20–30 %.

Legend: **T** theory · **G** guided modelling (instructor-led, participant follows on own machine) ·
**E** exercise · **D** discussion/wrap-up. Model IDs refer to [model_lineage.md](model_lineage.md).

---

## Pre-course module — Python 101 (self-paced, outside the 20 h)

About 4–6 h of self-study before Session 1: a guide in `course/session_00_python_101/` and the
notebook `python/notebooks/s00_python_101.ipynb`. Content:
install the environment (uv, VS Code, Jupyter) and run the course tests (`uv run pytest`); the Python subset used
in the course (types, functions, dataclasses, modules, the course package); NumPy arrays;
pandas time series (read, resample, plot the Turin weather data; demand profiles follow in Session 6); Matplotlib; SciPy; notebooks
vs scripts; a map of the ecosystem used later (FMPy, OMPython, `scipy.optimize`, CasADi,
algebraic modelling languages). The opening block of Session 1 includes a short check.

---

## Session 1 — Dynamic Systems Modelling Fundamentals

**Canonical model:** M01 `ThermalZone` (single thermal mass), implemented in **Python first**.

| min | Type | Content |
|-----|------|---------|
| 0–10 | D | Course map and the case-study building; the conceptual workflow; short check of the Session 0 set-up |
| 10–30 | T | Static vs dynamic systems; states, inputs, outputs, parameters; lumped modelling and its validity (Biot number as a rule of thumb) |
| 30–50 | T | Derive M01: $C\,\dot T = \dot Q - UA\,(T - T_{amb})$. Equilibrium $T_{ss} = T_{amb} + \dot Q/UA$, time constant $\tau = C/UA$, analytic step response |
| 50–60 | G | Python: right-hand-side function, explicit Euler written by hand |
| 60–70 | — | Break |
| 70–90 | G | `scipy.integrate.solve_ivp`; compare with analytic solution; effect of step size and tolerance; stability of explicit Euler ($\Delta t < 2\tau$) |
| 90–105 | T | State-space form $\dot x = Ax + Bu$, $y = Cx + Du$; linearity, superposition; preview: two states (M02); preview: what a DAE is (algebraic variable $\dot Q_{loss}$ kept as unknown) |
| 105–135 | E | G1.1 step response & reading τ from a plot; I1.1 heater schedule (piecewise input) and energy use |
| 135–140 | D | Takeaways; bridge to Session 2 |

## Session 2 — Energy Systems Modelling Fundamentals

**Canonical models:** M02 `ZoneRC` (2 nodes), M03 `Storage` (N-node tank), Python.

| min | Type | Content |
|-----|------|---------|
| 0–5 | D | Recap: M01 and its limits |
| 5–30 | T | Conservation laws; control volumes; mass balance; energy balance for an open system with enthalpy flows; when $\dot m c_p (T_{in}-T)$ is valid (incompressible, constant $c_p$) |
| 30–45 | T | Heat transfer modes; conduction/convection/linearized radiation → thermal resistance; thermal capacitance; the electrical analogy |
| 45–60 | G | M02: zone air + building mass (2R2C); write the state-space matrices; simulate in Python |
| 60–70 | — | Break |
| 70–95 | G | M03: storage tank with N mixed nodes and a through-flow; energy balance per node; check global energy balance numerically |
| 95–110 | T | Simple heat exchangers (ε-NTU, steady-state); dynamic vs steady-state component models; model fidelity: what to keep, what to drop; how N changes the dynamics (numerical diffusion) |
| 110–135 | E | G2.1 energy-balance check on M03; I2.1 identify which time constants of M02 dominate the response |
| 135–140 | D | Bridge to Modelica: "what if we only wrote the equations, not the solver?" |

## Session 3 — Modelica Fundamentals

**Canonical models:** M01 and M02 re-implemented in Modelica (teaching components + MSL). **Main reference:** *Modelica by Example* (pre-reading and section-by-section reading map in the lesson), with the Fritzson OpenModelica tutorial (2025).

| min | Type | Content |
|-----|------|---------|
| 0–5 | D | Recap; install check (OMEdit opens, MSL 4.1.0 loads) |
| 5–20 | T | Equation-based vs assignment-based modelling ($R\,i = v$ used three ways); acausal vs causal; what the compiler must do (flatten, sort, solve) |
| 20–42 | G | M01 as a single `model`, step by step as in *Modelica by Example* (Getting Physical): `parameter`, SI types and units (`checkModel` finds a unit error), `der()`, `initial equation`, `experiment`; compare with Session 1 Python result (same numbers) |
| 42–60 | T/G | Connectors: across and through variables, domain table; teaching `HeatPort`, `ThermalMass`, `ThermalConductance`, `FixedTemperature`, `HeatSource`; compose M01; connection sets and the count of unknowns and equations (balanced model) |
| 60–70 | — | Break |
| 70–78 | G | MSL `Modelica.Thermal.HeatTransfer`: `HeatCapacitor` source next to `ThermalMass`; packages, `within`, `import` |
| 78–98 | T/G | Modifications, `final` and propagation, `each`; `partial`, `extends`, `replaceable`/`redeclare` (swap a loss model); build M02 by composition |
| 98–106 | T/G | Three formulations of M01 — equation, components, block diagram (`S03_ThermalZoneBlocks`); which one when; Python vs Modelica table |
| 106–136 | E | G3.1 build M02 from components and match Python M02; I3.1 write simplified PV and battery components (`RealInput`/`RealOutput`, state of charge; limits come after S4), a language exercise; Session 5 uses the Buildings library versions |
| 136–140 | D | Key takeaways; bridge to Session 4 |

## Session 4 — OpenModelica Workflow and Numerical Modelling

**Canonical models:** M03 `Storage` in Modelica; M01 with a steady start and a time-dependent disturbance (`Examples.S04_SteadyStartStep`); `EnergyTraining.Examples.Broken.*`. **Main reference** for initialization and events: *Modelica by Example* (pre-reading and reading map in the lesson), with the Fritzson OpenModelica tutorial (2025); solvers and tools: OpenModelica User's Guide.

| min | Type | Content |
|-----|------|---------|
| 0–5 | D | Recap |
| 5–25 | T | From model to simulation: flattening, structural analysis (matching, BLT), index, algebraic loops and tearing; what ends up as ODE / DAE |
| 25–33 | G | OMEdit workflow, short: one simulation of M03 with `-lv=LOG_STATS`; reading the log; output interval ≠ accuracy (solver and tolerance changes: notebook §2, at home) |
| 33–50 | T/G | Initialization: one initial equation per state, `start`/`fixed`, `initial equation`; over/under-determined initial systems (demo: two directly connected capacities; the Broken examples are diagnosed in G4.1) |
| 50–60 | G | Steady start and a disturbance at a given time: M01 started with `der(T) = 0`, ambient step after 24 h, against a fixed start (`S04_SteadyStartStep`); the step as an event |
| 60–70 | — | Break |
| 70–90 | T/G | Events and discontinuities: time and state events, zero crossings, why an `if` does not guard `sqrt`, `noEvent`; `when`, `pre`; thermostat chattering vs hysteresis (figure; the Broken model is diagnosed in G4.1) |
| 90–105 | T/G | Stiffness and solver choice: M03 with N = 1 … 50; DASSL/IDA vs explicit Euler; tolerances; CPU time vs accuracy |
| 105–135 | E | G4.1 diagnose and fix three broken models from their logs; I4.1 convergence study on M03 |
| 135–140 | D | Debugging checklist |

## Session 5 — Thermo-Hydraulic Systems, Heat Pumps and System Assembly

**Canonical models:** M04 `HydronicLoop` (Buildings library, fluid view), M05 `BuildingEnergySystem`
(case study: heat pump + thermal storage + zone + PV + battery, thermal/power domain).

| min | Type | Content |
|-----|------|---------|
| 0–5 | D | Recap; where the case-study building is now |
| 5–25 | T | Fluid connectors: $p$, $\dot m$ (flow), $h$ as stream variable; why stream connectors exist (flow reversal, mixing); media models; pumps, pipes (pressure drop, delay, heat loss), valves; pressure reference |
| 25–45 | G | Tour of the Buildings library; M04 pump → pipe → heated load → return (pre-built): simulate; inspect $\dot m$, $T$, $\Delta p$; library vs teaching model |
| 45–60 | T | Heat pump fundamentals: Carnot COP, fraction-of-Carnot model, COP vs source/sink temperature; district heating in brief: topology, temperature levels, where heat pumps sit |
| 60–70 | — | Break |
| 70–95 | G | M05 (pre-assembled; a winter and a summer day of the Turin weather file, provided demand tables): heat pump charges the tank (M03), tank feeds the zone (M02) and hot-water draws; PV, battery, appliances and grid from the Buildings electrical library, weather from the Buildings reader; participants wire the electrical components to the grid |
| 95–105 | T/G | Rule-based operation: participants add the heat-pump hysteresis on the tank temperature and the battery self-consumption rule; why this is the baseline for Sessions 7–8 |
| 105–135 | E | G5.1 daily COP and PV self-consumption of M05 for two tank set points (winter and summer day); I5.1 pump flow and pipe length in M04 vs return temperature |
| 135–140 | D | Takeaways; bridge: inputs, outputs and sizes become the FMU interface |

## Session 6 — FMI/FMU and Python Integration

**Canonical model:** M06 `BuildingEnergySystemFMU` (M05 with top-level inputs/outputs and size parameters).

| min | Type | Content |
|-----|------|---------|
| 0–5 | D | Recap |
| 5–30 | T | FMI architecture; FMU contents; Model Exchange vs Co-Simulation; who owns the solver; communication step; causality/variability; FMU lifecycle; FMI 2.0 vs 3.0 |
| 30–45 | G | Export M06 with OpenModelica (`buildModelFMU` / OMEdit); inspect `modelDescription.xml` |
| 45–60 | G | FMPy: inspect variables, simulate, set parameters (asset sizes), read results; cross-check against the native OpenModelica result |
| 60–70 | — | Break |
| 70–90 | G | Input data with pandas: Turin weather and PV (typical year), demand profiles; input trajectories; energy KPIs (grid import/export, self-consumption, self-sufficiency, seasonal COP) |
| 90–105 | G | Scenario runner: a batch of what-if simulations; representative days vs a full year (run time vs accuracy of the KPIs) |
| 105–135 | E | G6.1 KPI table for a set of asset sizes; I6.1 step the Co-Simulation FMU with a battery rule written in Python |
| 135–140 | D | Bridge: energy KPIs are not yet costs |

## Session 7 — Techno-Economic Assessment and Scenario Analysis

**Canonical experiment:** M07 techno-economic assessment of the case study (Python `economics` on M06 results).

| min | Type | Content |
|-----|------|---------|
| 0–5 | D | Recap |
| 5–30 | T | Techno-economic framework: system boundary, CAPEX, fixed/variable OPEX, replacements, lifetime, discount rate, annuity (capital recovery factor), NPV, LCOE/LCOH, payback; tariff structures (energy, power, time-of-use, feed-in); cost-data sources and uncertainty |
| 30–50 | G | From simulation results to cash flows: annual costs and NPV of a reference system (heat pump + grid) and of variants with PV, tank and battery |
| 50–60 | T | Scenario design: what-if analysis, one-at-a-time sensitivity, tornado chart, scenario matrices; uncertainty of cost data |
| 60–70 | — | Break |
| 70–90 | G | What-if: flat vs time-of-use tariff, PV size, battery size; tornado chart of NPV |
| 90–105 | T/G | Design by heuristics: parametric sweep of sizes with rule-based operation; trade-off between cost and self-sufficiency; limits of sweeps (dimensions, operation fixed by rules) |
| 105–135 | E | G7.1 NPV and LCOE of four configurations; I7.1 sensitivity of the best PV/battery size to discount rate and electricity price |
| 135–140 | D | Bridge: the rules decide the operation — what if the operation were optimal too? |

## Session 8 — Optimization of Design and Operation

**Canonical experiments:** M08a operational dispatch (LP/MILP), M08b design optimization (sizing).

| min | Type | Content |
|-----|------|---------|
| 0–5 | D | Recap |
| 5–25 | T | Optimization problem anatomy: decision variables, objective, constraints; LP, MILP, NLP; local vs global; heuristics vs mathematical programming |
| 25–50 | G | M08a dispatch on representative days: heat pump, tank and battery as linear models, grid prices; a provided problem builder on `scipy.optimize.linprog`/`milp` (participants change tariffs and sizes, then read the matrices); cost vs rule-based operation |
| 50–60 | T | Linear surrogate vs dynamic model: what is lost (COP vs temperature, stratification, losses) |
| 60–70 | — | Break |
| 70–90 | G | Replay the optimal schedule on the FMU: model mismatch; cost gap rule-based vs optimal vs replayed |
| 90–110 | T/G | M08b design optimization: MILP joint sizing and dispatch (annualised CAPEX + OPEX), binary decisions (install or not, no simultaneous charge/discharge); compare with the Session 7 sweep; outlook (one slide): nonlinear models and CasADi |
| 110–130 | E | G8.1 optimal dispatch under time-of-use vs flat tariff; I8.1 (extension) joint sizing with another battery cost, or the CasADi nonlinear COP extension |
| 130–140 | D | Course wrap-up: workflow recap, where to go next (Buildings, CasADi, algebraic modelling languages) |

---

## Time accounting

Each timetable sums to 130 min of contact + 10 min break + 10 min buffer = 150 min. Mixed **T/G** blocks count
half theory, half guided. Course-wide split (v2, computed from the tables): ~33 % theory,
~37 % guided modelling, ~22 % exercises, ~9 % recap/discussion. Theory is above the 25–30 %
target and guided modelling below 40–50 % (v1 was similar: 34 % / 36 %); when the lessons are
written, theory blocks should turn into guided work where the notebook can carry the argument.

Sessions 5 and 8 are the densest: Session 5 uses pre-built M04 and M05, Session 8 a provided
problem builder, and the Session 8 independent exercise is extension work.
