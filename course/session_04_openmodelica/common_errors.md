# Session 4 — common errors

| Symptom | Cause | Fix / teaching point |
|---------|-------|----------------------|
| Warning *The initial conditions are not fully specified*; the run succeeds but the first hours look wrong | fewer initial equations than states: the tool used a start value (or the type default, 288.15 K for `Modelica.Units.SI.Temperature`) | one initial condition per state: `fixed = true` or an `initial equation`; check the initial values in the result |
| *The initial conditions are over specified*, then *The initialization problem is inconsistent* | `fixed = true` and an `initial equation` (for example `der(T) = 0`) for the same state | keep one: for a steady-state start, `der(T) = 0` with `fixed = false` |
| *alias variables with conflicting fixed start values* | two variables forced equal (directly connected capacities) with different fixed start values | fix one start value only: the connection makes them one state |
| The simulation hardly advances; *Chattering detected … The zero-crossing was: …* | a switching condition that flips back immediately (ideal thermostat) | a hysteresis (`when`/`elsewhen`, or `Modelica.Blocks.Logical.OnOffController`) or a continuous controller |
| Simulation slow, result file huge | many events, each written to the result file | count state events with `-lv=LOG_STATS`; remove the cause, not the output |
| *division by zero at time …, where divisor b expression is: …* | a steady-state formula divides by a flow that becomes zero | model the stored mass (a state), or switch the term off with a threshold |
| A switch that should act when a flow stops does not act | the relation compares with exactly the value the variable jumps to (`m_flow > 0` with `m_flow` jumping to 0) | compare with a threshold away from that value |
| Temperatures below 0 K, *Variable violating min constraint* | explicit fixed-step solver above its stability limit (or wrong signs) | implicit solver (DASSL), or a step below the stability limit of the fastest mode ($2\tau$ for one mode, $\tau_n$ for the M03 chain of nodes) |
| Results do not change when the output interval is made smaller | for adaptive solvers the output points are interpolated | change the tolerance (or the model) to change the accuracy |
| A new value of `N` needs a new translation | `N` sets array sizes: a structural parameter, fixed when the model is translated (re-simulating only repeats the last phase) | change it in the model (or with a modifier, `simulate_variant`) and translate again |
| Smaller tolerance, but the tank result still disagrees with the measurement | the error is in the model (number of nodes, mixing), not in the solver | separate solver error (tolerance study) from model error (node study), I4.1 |
