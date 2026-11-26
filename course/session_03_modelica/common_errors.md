# Session 3 — common errors

| Symptom | Cause | Fix / teaching point |
|---------|-------|----------------------|
| The zone gets colder when the heater is on | sign of the heat source: `port.Q_flow = Q_flow` | a port flow variable is positive *into* the component; a heater delivers heat out of itself: `port.Q_flow = -Q_flow` |
| The model simulates but the temperatures stay constant | ports not connected: an unconnected flow variable is set to zero | check every port in the diagram; "it runs" is not "it is right" — compare with a reference (G3.1 script) |
| "Too many equations" / "too few equations" | a component equation missing or written twice, or a connector variable without `flow` | count unknowns and equations of each component; potential variables are equal across a connection, flow variables sum to zero |
| `checkModel` (OMEdit: *Check Model*) warns that an equation is "INCONSISTENT due to specified unit information" | a typo that is legal syntax, e.g. missing parentheses `Q_flow - UA*T - T_amb` | read the two sub-expressions and units in the warning; fix the equation. `simulate` alone does not report it: check first |
| No unit warning, but the result is wrong | variables declared as plain `Real`, or a block diagram (signals carry no units) | declare physical variables with `Modelica.Units.SI` types; compare with a reference |
| `der(T)` written as an assignment `der(T) := ...` | assignment syntax belongs to `algorithm` sections | in an `equation` section use `=` |
| The mass starts at 20 °C (293.15 K) whatever you meant | no start value given: MSL `HeatCapacitor` has `T(start = 293.15)` | set the initial temperature: `T(start = T0, fixed = true)` or an `initial equation` |
| Warning "The initial conditions are not fully specified" | `start` without `fixed = true` is only a guess; the tool picks the initial values itself | give each state one initial condition: `fixed = true` or an `initial equation` (Session 4) |
| Both `fixed = true` and an `initial equation` for the same variable | over-determined initialization (Session 4) | give one initial condition per state |
| "Trying to override final element C" | the parameter was set `final` (e.g. `zone.zone.C` inside `ThermalZone`) | change the parameter of the enclosing model (`zone.C`); `final` keeps one value in one place |
| "Non-array modification … possibly due to missing 'each'" | a scalar modification on an array of components | `HeatCapacitor layer[5](each C = 2e5)` |
| After a `redeclare`: "Parameter envelope.UA has neither value nor start value" | the modification `envelope(final UA = UA)` was written on the replaceable declaration, and the redeclaration replaces it | write it in the `redeclare` (as `ZoneRC` does), or on the `constrainedby` clause |
| A `partial` model cannot be simulated | partial classes are incomplete by design | simulate a model that extends it, or an example |
| `redeclare` rejected | the component is not `replaceable`, or the new type does not fit the constraining type | declare it `replaceable ... constrainedby ...`; the new class must be a subtype of the constraining type (at least its ports, with the same types; it may add more) |
| Python and Modelica differ by about 10⁻⁵ K | different solvers and tolerances | integration error, not a model error; change the tolerance and watch the difference change |
| `Modelica.SIunits` not found (code from *Modelica by Example* or older books) | MSL 4.x renamed it to `Modelica.Units.SI` (and `Modelica.SIunits.Conversions` to `Modelica.Units.Conversions`) | use `Modelica.Units.SI` |
| A `block` with a physical connector fails | blocks may only have `input`/`output` connector variables | use a `model` for components with heat ports |
| Battery SOC above 1 or below 0 | the I3.1 battery, like the library one, has no limits | expected today; limits need events and an operating rule (Sessions 4–5) |
