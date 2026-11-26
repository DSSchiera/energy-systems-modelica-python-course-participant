# Learning outcomes

Verbs follow Bloom's revised taxonomy. Each outcome is assessed by at least one exercise.

## Course-level outcomes

By the end of the course the participant can:

- **CO0** Set up a Python environment and use notebooks, NumPy, pandas and Matplotlib to load,
  process and plot energy time series (Session 0, assessed by S0.1 in class).
- **CO1** Formulate a lumped dynamic model of a thermal/hydronic energy system from
  physical assumptions and conservation laws, identifying states, inputs, outputs, parameters.
- **CO2** Implement such a model both causally (Python ODE) and acausally (Modelica), and
  explain the difference.
- **CO3** Build, simulate and debug Modelica models in OpenModelica, diagnosing
  initialization, event, algebraic-loop and stiffness problems from logs.
- **CO4** Assemble thermo-hydraulic systems from established libraries (MSL, Buildings) and
  judge when a teaching model is enough and when a validated library component is needed.
- **CO6** Assess an energy system techno-economically: turn simulation results into costs
  (CAPEX, OPEX, annuity, NPV, LCOE/LCOH) and design scenario and sensitivity analyses.
- **CO5** Export models as FMUs and run, parameterize, drive and analyse them from Python.
- **CO7** Formulate and solve design and operation optimization problems (heuristic search,
  LP/MILP), validate their results on the dynamic model, and explain what a linear surrogate
  misses and when nonlinear tools (e.g. CasADi) are needed.

## Session-level outcomes

| Session | The participant can… | CO |
|---------|----------------------|----|
| 0 | install the course environment; run a notebook; use NumPy, pandas and Matplotlib on a weather time series; name the role of FMPy, OMPython, `scipy.optimize` and CasADi | CO0 |
| 1 | define state, input, output, parameter; derive and solve the first-order thermal model analytically and numerically; compute and interpret τ and steady state; write a model in state-space form | CO1, CO2 |
| 2 | write mass and energy balances for closed and open control volumes; build RC networks; model a stratified tank with N nodes; verify a global energy balance; argue model fidelity | CO1 |
| 3 | write equation-based Modelica models; use connectors with potential/flow variables; compose, extend and redeclare components; use MSL thermal components; write simple input/output components (PV, battery); compare causal and acausal formulations | CO2 |
| 4 | configure and run simulations in OMEdit; explain the compilation pipeline at a conceptual level; diagnose and fix initialization, event and solver issues; choose solver and tolerance | CO3 |
| 5 | explain fluid connectors and stream variables; simulate a pump–pipe–load loop with Buildings components; model a heat pump with a Carnot-fraction COP; build the electrical side from Buildings library components (PV, battery, loads, grid) and a weather reader; complete the case-study system with a rule-based operating strategy (district heating is discussed, not assessed) | CO4 |
| 6 | distinguish Model Exchange and Co-Simulation; export an FMU from OpenModelica; inspect, simulate and drive it with input data from Python; run scenario batches and compute energy KPIs | CO5 |
| 7 | compute annualised costs, NPV and LCOE/LCOH from simulation results; run what-if and sensitivity analyses; compare designs with a parametric sweep under rule-based operation | CO6 |
| 8 | formulate dispatch and sizing problems as LP/MILP; solve them with SciPy; validate an optimal schedule on the FMU and explain the mismatch; compare heuristic and mathematical-programming design | CO7 |
