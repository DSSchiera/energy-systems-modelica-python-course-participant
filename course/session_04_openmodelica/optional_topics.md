# Session 4 — optional advanced topics

- **The transformational debugger.** Simulate a model with OMEdit's transformational debugger
  and follow an equation from the flat model to the form in which it is solved; the
  `-d=infoXmlOperations` flag records every transformation `[src: om-users-guide]`.
- **Index reduction.** Connect two `HeatCapacitor`s through a `ThermalConductor` whose
  conductance tends to infinity, and compare the solver statistics with
  `Examples.S04_TwoCapacities`: a very stiff model versus one state less
  `[src: cellier-kofman-2006]` (section to be confirmed).
- **Other solvers.** Repeat the stiffness study with `ida`, `cvode` and the explicit and implicit
  Runge–Kutta methods of `gbode` (`-gbm=...`); compare steps and Jacobian evaluations
  `[src: om-users-guide]`.
- **Initial values from a previous simulation.** OpenModelica can take the initial values (or
  the guesses of the initial equations) from an earlier result file, useful for long warm-up
  periods of building models `[src: om-users-guide]`.
- **`smooth` and `noEvent`.** Rewrite the upwind term of M03 with `noEvent(max(m_flow, 0))` and
  count the state events of a flow reversal with and without it `[src: modelica-spec-3.7 §8.5]`.
