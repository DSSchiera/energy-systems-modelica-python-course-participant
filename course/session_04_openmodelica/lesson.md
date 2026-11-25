# Session 4 — OpenModelica Workflow and Numerical Modelling

**Canonical models:** M03 `StorageSystem` in Modelica; `EnergyTraining.Examples.Broken.*` ·
**Duration:** 150 min ([timetable](../../docs/syllabus.md#session-4--openmodelica-workflow-and-numerical-modelling)) ·
**Sources:** [source map](../../REFERENCES.md) · **Code:** `modelica/EnergyTraining`
(`Components.StorageTank`, `Systems.StorageSystem`, `Examples.S04_*`, `Examples.Broken`),
`energy_training.omc` (`runner`, `results`, `studies`) · **Notebook:**
`python/notebooks/s04_numerics_stiffness.ipynb`

## 1. Learning objectives

After this session the participant can:

1. describe what happens between a Modelica model and its simulation results: flattening,
   matching and sorting of the equations, algebraic loops and tearing, the number of states;
2. set up a simulation (stop time, output interval, solver, tolerance) and read the simulation
   log and its solver statistics;
3. state how many initial conditions a model needs, write them with `start`/`fixed` or
   `initial equation` (also in steady state), and recognise under- and over-specified
   initialization in the log;
4. explain what an event is, why a relation such as `T < T_set` creates one, why an ideal
   thermostat chatters, and write a hysteresis with `when`;
5. explain stiffness, choose between implicit and explicit solvers, and distinguish solver error
   (tolerance) from model error (number of nodes);
6. diagnose a failed or wrong simulation with a fixed checklist.

## 2. Prerequisite concepts

Sessions 1–3: M01–M03, explicit Euler and its stability limit $h < 2\tau$ for one mode (Session 1), node
count and numerical diffusion of M03 (Session 2), Modelica equations, connectors and the flat
model (Session 3). OpenModelica with MSL 4.1.0 installed ([setup](../../SETUP.md)).

## 3. Source map

Summary below; full list of sources in [REFERENCES.md](../../REFERENCES.md).
Language rules for initialization and events: `[src: modelica-spec-3.7]` (§8.3.5, §8.5, §8.6).
OpenModelica workflow, simulation flags, solvers and debugger: `[src: om-users-guide]`, and the
behaviour of OpenModelica 1.27.1 observed by running it `[src: om-release-1.27]`. Numerical
integration and stiffness: `[src: cellier-kofman-2006]`. Library components:
`[src: msl-4.1.0]`. M03 equations: Session 2 lesson §5.2.

## 4. Theory

### 4.1 From model to simulation

Simulating a model in OMEdit has three phases `[src: om-users-guide]`:

1. **Translation.** The front end *instantiates* the model into a flat list of variables and
   equations (Session 3). The back end analyses its structure and generates C code.
2. **Compilation** of the C code into a simulation executable.
3. **Simulation**: the executable computes the results. Re-simulating with changed parameter
   values repeats only this phase.

What the back end does with the flat equations:

- **Matching.** Each equation is assigned to the unknown it will compute. The derivatives
  `der(x)` of the states are unknowns; the states themselves are known at each instant, given
  by the integrator.
- **Sorting (BLT).** The equations are ordered so that each one only uses values already
  computed: a *block lower triangular* form. Most blocks are single assignments.
- **Algebraic loops.** A block of several equations that must be solved together. **Tearing**
  chooses a few *iteration variables*; the other unknowns of the block then follow one by one,
  and the remaining *residual* equations are solved for the iteration variables. A linear loop is
  solved directly; a nonlinear loop iteratively (Newton), starting from the **start values** of
  the iteration variables.
- **States and index.** Sometimes the equations constrain the states. Two heat capacities
  connected without a resistance must have the same temperature, so only one of them can be
  chosen freely. To obtain an ODE the tool may have to differentiate equations (**index
  reduction**) `[src: modelica-spec-3.7 §8.6]`, and it keeps fewer states than there are
  `der()` operators.

In this course's models the result is an ODE $\dot x = f(x, u, t)$ plus algebraic equations
evaluated along the way. The default solver integrates that ODE `[src: om-users-guide]`.

> **Simplification:** the matching, sorting and tearing algorithms themselves are not taught;
> the session uses only what the compiler reports about them (`[src: cellier-kofman-2006]` and
> `[src: fritzson-2014]` for the theory).

### 4.2 Simulation setup and log

| Setting | Meaning |
|---------|---------|
| start and stop time | simulated interval [s] |
| number of intervals, or interval | spacing of the output points; for **fixed-step** methods (`euler`, `rungekutta`) also the integration step `[src: om-users-guide]` |
| method | the integrator: `dassl` (default in 1.27.1), `ida`, `cvode`, `gbode`, `euler`, `rungekutta`, … |
| tolerance | error tolerance of the variable-step methods (default 1e-6) |

The values in a model's `experiment` annotation are used unless changed in the simulation
setup. With an adaptive method the output points are **interpolated** between the solver's own
steps: they do not force steps, and a small output interval does not make the result more
accurate `[src: om-users-guide]`.

**The log** says whether initialization and simulation succeeded, and lists warnings and errors.
More information is available with runtime flags (`-lv=LOG_STATS` for solver statistics,
`-lv=LOG_INIT` for initialization, `-lv=LOG_EVENTS` for events) and compiler flags
(`-d=initialization`) `[src: om-users-guide]`. OMEdit's **transformational debugger** shows the
equations after each transformation, with the variable each one solves for `[src: om-users-guide]`.

### 4.3 Initialization

At the initial time the derivatives are unknowns too. An ODE with $n$ states and $m$ algebraic
unknowns has $2n + m$ unknowns at initialization but only $n + m$ equations, so it needs
**$n$ additional initial equations** `[src: modelica-spec-3.7 §8.6.1]`. They come from:

- `fixed = true` on a state's start value, which adds `x = start`;
- an `initial equation` section, for example `T = T0`, or `der(T) = 0` for a **steady-state**
  start.

`start` alone (with `fixed = false`, the default for variables) is only a guess for iterative
solvers `[src: modelica-spec-3.7 §8.6]`.

A tool may treat a non-fixed start value as fixed, or remove a *consistent* redundant initial
equation, provided it reports a diagnostic `[src: modelica-spec-3.7 §8.6]`. OpenModelica 1.27.1
then warns:

- *The initial conditions are not fully specified*: a start value was used as an initial
  condition. If that start value is not set in the model, it is the default of the type, for
  example 288.15 K for `Modelica.Units.SI.Temperature` `[src: msl-4.1.0]`.
- *The initial conditions are over specified*: too many initial equations. If they contradict
  each other the simulation stops with *The initialization problem is inconsistent*.

### 4.4 Events

An expression such as `T < T_set` can change its value only at an **event**. During continuous
integration the solver keeps the value from the last event. When the underlying expression
`T - T_set` crosses zero, the integration is halted, the instant is located (root finding), the
relation and the equations that depend on it are updated, and the integration restarts
`[src: modelica-spec-3.7 §8.5]`. This keeps the equations smooth between events, as the
integrators require. `noEvent(...)` takes the relation literally instead, without an event; use
it only where both branches are smooth and valid on both sides.

**Time events** (`time >= t_stop`) can be scheduled in advance. **State events** (`T < T_set`)
must be found by root finding.

A `when` equation is active only at the instant its condition **becomes** true
`[src: modelica-spec-3.7 §8.3.5]`. Between those instants the variable keeps its previous
value, `pre(v)`. A **hysteresis** uses this: the heater switches off above $T_{set} + b/2$, on
below $T_{set} - b/2$, and keeps its state in between.

**Chattering.** With `Q_flow = if T < T_set then Q_max else 0` the zone warms up to $T_{set}$.
The heater switches off, $T$ falls, the relation is true again at once, and the heater switches
on. Every step is now an event. Physically the ideal thermostat switches infinitely fast.
Numerically, the solver crawls forward with tiny steps.

### 4.5 Stiffness and solver choice

A model is **stiff** when an explicit method has to take steps much smaller than the accuracy of
the result would require, because larger steps are **unstable**. This happens when the model has
fast modes (short time constants) and is simulated over a time much longer than they are
`[src: cellier-kofman-2006]` (textbook section to be confirmed). The fast modes decay
quickly, but the explicit step stays limited by them: for explicit Euler on a single mode,
$h < 2\tau$ (Session 1). Above the limit the numerical solution grows without bound, even if
nothing physical happens on that time scale. **Implicit** methods such as
the BDF methods in DASSL, IDA and CVODE have no such limit for modes that decay without
oscillating, like those of M03: they take steps as large as the accuracy allows. In return each step solves an equation system with the
Jacobian matrix `[src: om-users-guide]`.

The **tolerance** of an adaptive method controls the error made in each step (local error),
not the error of the final result, which builds up over many steps (global error). Halving the
tolerance does not halve the error at the end. Measure it against a reference.

## 5. Mathematical formulation

### 5.1 Initial equations of M01 and M03

M01 has one state, so one initial equation: $T(0) = T_0$, or a steady start
$\dot T(0) = 0$, which gives $T(0) = T_{amb} + \dot Q/UA$. M03 with $N$ nodes has $N$ states:
`StorageTank` sets every node to `T_start` with `fixed = true`. A model with two states, such as
M02, needs two initial equations, one per state, whichever form they take (question for G4.1:
what is the equilibrium of the envelope node?).

### 5.2 Hysteresis

With band $b$ and heater state $s \in \{\text{on}, \text{off}\}$:

$$s \leftarrow \text{off when } T > T_{set} + b/2, \qquad s \leftarrow \text{on when } T < T_{set} - b/2,\qquad \dot Q = \begin{cases}\dot Q_{max} & s = \text{on}\\ 0 & s = \text{off}\end{cases}$$

```modelica
when T > T_set + bandwidth/2 then
  heaterOn = false;
elsewhen T < T_set - bandwidth/2 then
  heaterOn = true;
end when;
Q_flow = if heaterOn then Q_max else 0;
```

### 5.3 Stiffness of M03

With constant inflow, the Jacobian of M03 (Session 2, without conduction) is lower bidiagonal,
with $-(1/\tau_n + 1/\tau_{loss})$ on the diagonal and $1/\tau_n$ below it. The node time
constant is $\tau_n = \rho V/(N\dot m)$; the standby-loss time constant
$\tau_{loss} = \rho V c_p/UA_{loss}$ = 174 h only shifts the diagonal slightly. For the 300 L
tank at 0.1 kg/s, simulated for 24 h:

| $N$ | 1 | 10 | 50 |
|-----|---|----|----|
| $\tau_n$ | 2987 s | 299 s | 60 s |
| 24 h / $\tau_n$ | 29 | 289 | 1446 |

All eigenvalues are equal, so the eigenvalue limit of explicit Euler is $h < 2\tau_n$. For this
chain of nodes it is **not sufficient**. One Euler step maps the node temperatures with the
matrix $(1 - r)I + rS$, $r = h/\tau_n$, $S$ = shift to the next node (losses neglected). Its
maximum-row-sum norm is $|1 - r| + r$, which is at most 1 only for $r \le 1$: **$h \le \tau_n$**
(the Courant condition of upwind advection). For $\tau_n < h < 2\tau_n$ errors are passed down the
chain of nodes and grow before they decay (derived here; observed below).

## 6. Guided example

1. **From equations to code** (notebook §1, OMEdit): M03 with $N$ = 10
   (`Examples.S04_StorageCharging`) has 37 equations, 10 states and no algebraic loop. Then
   `Examples.S04_AlgebraicLoops` (a two-layer wall without heat capacity, and a radiating wall)
   and `Examples.S04_TwoCapacities` (two capacities at one temperature).
2. **Simulation setup and log**: M03 in OMEdit with different solvers and tolerances; the solver
   statistics (notebook §2).
3. **Initialization**: count the initial equations of M01, M02, M03. In `S04_TwoCapacities`,
   fix the start value of the second capacity as well and read the error.
4. **Events**: the thermostat with and without hysteresis (figure below). The models themselves
   are in exercise G4.1.
5. **Stiffness**: M03 with $N$ = 1 … 50 and four solver settings (notebook §3).

## 7. Executable model/code

In OMEdit: *File → Open Model/Library File* `modelica/EnergyTraining/package.mo`. From Python:

```python
from energy_training.omc.runner import backend_info, simulate_variant

print(backend_info("EnergyTraining.Examples.S04_AlgebraicLoops", out_dir="output/s04"))
run = simulate_variant("EnergyTraining.Examples.S04_StorageCharging", {"N": 50},
                       out_dir="output/s04", stop_time=86400, interval=60, method="euler")
run.stats            # steps, f_calls, state_events, cpu_time, ...
run.result["storage.T_out"]
```

`backend_info` translates with the compiler flags `-d=backenddaeinfo,dumpLoops`;
`simulate_variant` compiles a variant with changed parameters (also array sizes such as `N`) and
returns result and statistics (`-lv=LOG_STATS`). Checks: `EnergyTraining.Validation.StorageVsPython`
(M03 in Modelica against Python, < 1e-4 K), `python/tests/test_omc.py`.

## 8. Results

![Thermostat without and with hysteresis](../../figures/generated/s04_chattering_vs_hysteresis.png)

![Solvers on M03 against the number of nodes](../../figures/generated/s04_solver_comparison.png)

## 9. Interpretation

- **What the compiler reports.** M03 with 10 nodes: 10 states, 21 single assignments, no loop;
  each node equation is solved for its derivative. The two-layer wall gives a **linear** torn
  system with one iteration variable (the temperature between the layers) and three inner
  variables. The radiating wall gives a **nonlinear** one, solved by Newton from the start value
  288.15 K. The two directly connected capacities give **one** state; fixing both start values
  makes OpenModelica 1.27.1 stop with *alias variables with conflicting fixed start values*.
- **Statistics.** M03 ($N$ = 10, 3 h, DASSL, tolerance 1e-6): 109 steps, 134 right-hand-side
  evaluations, 16 Jacobians, a few milliseconds of computing time. The 180 output points do
  not force steps.
- **Events.** The ideal thermostat produced 528 782 state events in 5000 s, and OpenModelica
  reported *Chattering detected around time 4764.8 … The zero-crossing was: T < T_set*. With a
  ±0.5 K hysteresis a whole day needs 45 state events and 22 switchings. Every crossing of a
  threshold is an event, including the crossings that change nothing.
- **Stiffness.** Over 24 h of charging, explicit Euler with $h$ = 300 s is wrong by 15 K at
  $N$ = 10 ($h \approx \tau_n$) and by 2·10⁷ K at $N$ = 15, although $h < 2\tau_n$ there: the
  eigenvalue limit alone does not predict the failure, $h \le \tau_n$ does. Classical
  Runge–Kutta (RK4), with a larger stability interval for a single mode, is wrong by 19 K at
  $N$ = 15 and blows up at $N$ = 20. With $h$ = 60 s Euler stays bounded up to $N$ = 50 but is wrong by up to 22 K.
  DASSL stays within 0.3–3·10⁻³ K for every $N$ with 97–180 evaluations, fewer than any
  explicit setting.
- **Which error matters?** With the default tolerance the solver error of M03 is about 10⁻³ K.
  The difference between $N$ = 10 and $N$ = 50 is several kelvin at the outlet (Session 2,
  numerical diffusion). For this model the number of nodes, a modelling choice, matters far more
  than the tolerance. Exercise I4.1 quantifies both.

### Debugging checklist

A failed or suspicious simulation is a **modelling question first**. Check, in this order:

1. **Formulation**: equations, signs, units; is the model balanced (*Check Model*)?
2. **Initialization**: one initial condition per state; warnings about unspecified or
   over-specified initial conditions; start values of the iteration variables of nonlinear
   loops.
3. **Scaling**: variables of very different magnitude (W and MW, Pa and bar). Nominal values.
4. **Algebraic loops**: their number and size (`-d=backenddaeinfo`); a division by a variable
   that can become zero.
5. **Discontinuities and events**: number of state events (`-lv=LOG_STATS`); chattering; a
   relation that compares with exactly the value a variable jumps to.
6. **Stiffness**: explicit solver, or a step size near the stability limit.
7. **Constraints**: `min`/`max` violations reported as assertions. A temperature below 0 K is
   usually a symptom of the problems above, not their cause.
8. **Solver configuration**: method, tolerance, maximum step, last.

## 10. Guided exercise

[G4.1 — Diagnose and fix broken models](../../exercises/session_04/G4.1_broken_models.md)

## 11. Independent exercise

[I4.1 — Convergence study on M03](../../exercises/session_04/I4.1_convergence_study.md)

## 12. Solutions

Solutions are added to the `solutions/` folder of this repository after the session.

## 13. Common errors

See [common_errors.md](common_errors.md).

## 14. Optional advanced topics

See [optional_topics.md](optional_topics.md).
