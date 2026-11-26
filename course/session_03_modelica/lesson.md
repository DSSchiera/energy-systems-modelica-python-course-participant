# Session 3 — Modelica Fundamentals

**Canonical models:** M01 `ThermalZone`, M02 `ZoneRC` in Modelica · **Duration:** 150 min ([timetable](../../docs/syllabus.md#session-3--modelica-fundamentals)) ·
**Sources:** [source map](../../REFERENCES.md) · **Code:** `modelica/EnergyTraining` (`Interfaces`,
`Components`, `Systems.ThermalZone`, `Systems.ZoneRC`, `Examples.S03_*`),
`energy_training.omc` · **Notebook:** `python/notebooks/s03_python_vs_modelica.ipynb`

## 1. Learning objectives

After this session the participant can:

1. explain the difference between assignment-based (causal) and equation-based (acausal)
   modelling, and what a Modelica compiler must do before a model can be simulated;
2. write a Modelica model with `parameter`, typed variables (`Modelica.Units.SI`), `der()`,
   `initial equation` and an `experiment` annotation, simulate it and obtain the same result as
   the Python model of Session 1;
3. use units and physical types, and let the tool find a unit error;
4. define a connector with an across (potential) and a through (flow) variable, write the
   equations that `connect` generates and count unknowns and equations of a component and of a
   flat model;
5. compose a model from components, and replace teaching components by their Modelica Standard
   Library (MSL) equivalents after reading their source;
6. change parameters with modifications (`final`, `each`), and use `partial`, `extends`,
   `replaceable` and `redeclare` to change the structure of a model (M01 → M02) without
   rewriting it;
7. write the same model as an equation, as a component network and as a block diagram, and say
   when each form is the right one;
8. write `block`s with `RealInput`/`RealOutput` (simplified PV and battery) and connect them to
   time series.

## 2. Prerequisite concepts

Sessions 1–2 (M01, M02, state, energy balance of a node, RC networks); OpenModelica installed
with MSL 4.1.0 ([setup](../../SETUP.md)).

**Pre-reading (about 60 min)**, *Modelica by Example* by M. Tiller, free online
`[src: modelica-by-example]`:

1. [Basic Equations → Simple First Order System](https://mbe.modelica.university/behavior/equations/first_order/):
   `der`, descriptions, `initial equation`, steady-state start, `experiment`;
2. [Basic Equations → Getting Physical](https://mbe.modelica.university/behavior/equations/physical/):
   Newton's law of cooling — almost exactly our M01 — with parameters, units and physical types;
3. [Basic Equations → Equations](https://mbe.modelica.university/behavior/equations/equations/)
   (review page);
4. [Connectors](https://mbe.modelica.university/components/connectors/) and
   [Connectors → Simple Domains](https://mbe.modelica.university/components/connectors/simple_domains/).

The book was written for MSL 3.2.2: where it writes `Modelica.SIunits`, MSL 4.1.0 (used in this
course) has `Modelica.Units.SI`; `Modelica.SIunits.Conversions` became `Modelica.Units.Conversions`.
Book code needs this rename before it runs here.

## 3. Source map

Summary below; full list of sources in [REFERENCES.md](../../REFERENCES.md).
Main tutorial: *Modelica by Example* `[src: modelica-by-example]` — the reading map below sends you
to the section that explains each topic. Second tutorial: P. Fritzson's OpenModelica tutorial of the
2025 Modelica Conference `[src: fritzson-tutorial-2025]` (cited by PDF page). Language rules:
`[src: modelica-spec-3.7]`. Library components: `[src: msl-4.1.0]`
(`Modelica.Thermal.HeatTransfer`, `Modelica.Blocks`, `Modelica.Units.SI`). PV and battery equations of
the library used from Session 5: `[src: buildings-14.0.0]`. M02 parameters: `[src: bacher-madsen-2011]`.

| Lesson | *Modelica by Example* (https://mbe.modelica.university/…) | Fritzson tutorial (PDF page) | Specification 3.7 |
|--------|------------------------------------------------------------|------------------------------|-------------------|
| §4.1 equations | `behavior/equations/first_order/`, `…/equations/` | 17, 136 (acausality); 30, 137 (translation) | ch. 8 |
| §4.2 variables and attributes | `behavior/equations/variables/`, `…/initialization/` | 139 | §4.5, §4.9.1, §8.6 |
| §4.3 units and types | `behavior/equations/physical/`, `components/packages/fqn/`, `…/nimport/` | – | §4.9.1, ch. 19 |
| §4.4 causal and acausal | `components/components/block_comps/` | 25, 185 | §4.7 |
| §4.5 connectors | `components/connectors/simple_domains/`, `…/connector_def/` | 186–188 | §9.1, §9.3 |
| §4.6 connections and balance | `components/components/heat_transfer/`, `…/component_models/` | 189–190, 194 | §9.2, §4.8 |
| §4.7 classes and packages | `components/packages/organizing/`, `…/importing/`, `…/package_def/` | 144 | §4.7, ch. 13 |
| §4.8 modifications | `behavior/equations/variables/` (modifications), `components/subsystems/modifications/`, `…/propagation/` | 151 | §7.2 |
| §4.9 inheritance, replaceable | `behavior/equations/population/` (avoiding repetition), `components/architectures/int_vs_imp/`, `…/replaceable/` | 147, 191 | §4.4.2, §7.1, §7.3 |

## 4. Theory

### 4.1 Equations, not assignments

In Python, M01 is a function that **computes** $\dot T$ from $T$ and the inputs: the modeller
decides which quantity is computed from which (a *causal* formulation). A Modelica model is a set
of **equations**: there is no order between them, and an equation states that two expressions are
equal, not that the left side is assigned `[src: modelica-spec-3.7 §8.3.1]`. Writing
`C*der(T) = Q_flow - UA*(T - T_amb)` or `Q_flow = C*der(T) + UA*(T - T_amb)` is the same model.
*Modelica by Example* insists on writing equations in their textbook form and leaving the
rearrangement to the tool `[src: modelica-by-example, Basic Equations → An Electrical Example]`. Fritzson's example is a
resistor, $R\,i = v$: the same equation can be used to compute $i$, $v$ or $R$, and which one is
decided only when the resistor is connected in a circuit — this is what makes a component reusable
`[src: fritzson-tutorial-2025 p. 17]`.

Before simulation the compiler **flattens** the model (replaces every component by its equations,
adds the equations of the connections), **sorts** the equations and **solves** each one for the
variable it determines, so that a numerical solver receives a causal form again
`[src: fritzson-tutorial-2025 p. 30]`. Session 4 opens this box in OpenModelica; today it is
enough to know that these steps exist and that they are why components can be written without
knowing how they will be connected.

### 4.2 Variables, parameters and their attributes

A declaration gives a variable a **type** and a **variability** `[src: modelica-spec-3.7 §4.5]`:

- a `constant` never changes and is fixed when the model is translated (π, $\sigma$);
- a `parameter` is constant during a simulation and may change between simulations ($C$, $UA$);
- a variable without prefix may change at any time ($T$).

A `Real` has **attributes**, set in parentheses `[src: modelica-spec-3.7 §4.9.1]`
`[src: modelica-by-example, Basic Equations → Variables]`:

| Attribute | Meaning |
|-----------|---------|
| `unit` | unit used in the equations, e.g. `"K"`, `"W/K"` |
| `displayUnit` | unit shown in plots and dialogs, e.g. `"degC"`; never changes the equations |
| `start` | initial value — of a state, if `fixed = true`; otherwise only a guess |
| `fixed` | `true`: the start value must hold at $t_0$; default `true` for parameters, `false` for variables |
| `min`, `max` | bounds the value must respect |
| `nominal` | typical size, used for scaling and for relative tolerances |

A **state** needs one initial condition: `T(start = T0, fixed = true)` or an `initial equation`
`T = T0`, which are equivalent `[src: modelica-spec-3.7 §8.6]`. An initial equation can also say
something else, e.g. a steady start `der(T) = 0` `[src: modelica-by-example, Basic Equations →
Simple First Order System]`. Without either, the tool chooses the initial value from `start` and
warns (Session 4).

### 4.3 Units and physical types

`Real T(unit = "K")` attaches a unit to a variable; the unit strings follow SI
`[src: modelica-spec-3.7 ch. 19]`. Writing the attributes every time is tedious, so a **type**
collects them once: MSL 4.1.0 defines `Modelica.Units.SI.Temperature` as a `Real` with
`unit = "K"`, `displayUnit = "degC"`, `min = 0`, `start = 288.15` and `nominal = 300`, and
`ThermalConductance` with `unit = "W/K"` `[src: msl-4.1.0]`. Declaring
`Modelica.Units.SI.Temperature T` gives `T` all of these
`[src: modelica-by-example, Basic Equations → Getting Physical]`. A temperature *difference* has
its own type, `TemperatureDifference` (unit K, no lower bound), marked as a relative quantity, so a
tool converting it to °C ignores the 273.15 K offset `[src: msl-4.1.0]`
`[src: modelica-spec-3.7 §18.10, annotation absoluteValue]`.

With units, the tool can check every equation: both sides must have the same unit, so an
equation that is legal syntax but physically wrong is caught
`[src: modelica-by-example, Packages → Referencing Package Contents]`. OpenModelica 1.27.1
checks units when a model is **checked** (`checkModel`; in OMEdit: *Check Model*) and
reports an inconsistent equation as a warning, naming the two sides and their units; the plain
`simulate` command runs the same model without that warning, and a variable declared as a plain
`Real` without unit is not checked at all (observed by execution, 2026-11-26). Units are therefore
a cheap test: check the model, then simulate it.

> **Simplification:** this course writes values in SI inside models (K, W, J/K) and uses °C only for
> display (`displayUnit`) and in plots. *Modelica by Example* recommends the same practice
> `[src: modelica-by-example, Packages → Importing Physical Types]`.

`nominal` matters for the solver too: the specification reserves it for scaling and relative
tolerances `[src: modelica-spec-3.7 §4.9.1]`. M01 with `T` of type `SI.Temperature` (nominal
300 K) has a largest error of 1.4·10⁻⁵ K over the 72 h run; the same equation with a plain `Real`
(nominal 1) 3.4·10⁻⁶ K, and the two swap when only `nominal` is swapped (OpenModelica 1.27.1,
DASSL, tolerance 10⁻⁸, observed by execution). Both errors are tiny; the point is that a type is
more than a label.

### 4.4 Causal and acausal composition

A **block diagram** connects outputs to inputs: information flows in one direction, and the
diagram is the solved form of the equations. A physical **schematic** connects ports where several
components share variables: a wall does not know whether heat will flow in or out. Modelica
supports both. Blocks (`block`) have only inputs and outputs `[src: modelica-spec-3.7 §4.7]`;
physical components have connectors without a direction. Fritzson shows the same RLC circuit as a
Modelica schematic and as a signal-flow diagram, and notes that only the first is easy to read as a
physical model `[src: fritzson-tutorial-2025 p. 25]`; the signal-flow diagram shows instead how the
solution is computed.
*Modelica by Example* solves one cooling problem in three ways — one equation, acausal components,
block diagram — and notes that the block diagram must be redrawn whenever the physical topology
changes `[src: modelica-by-example, Components → Block Diagram Components]`. §5.3 does the same with
M01.

### 4.5 Connectors: across and through variables

A connector lists the variables that two components share at a port. Each physical domain has a
pair: an **across** (potential) variable, whose differences drive the exchange, and a **through**
(flow) variable, the rate at which a conserved quantity crosses the port
`[src: modelica-by-example, Connectors]` `[src: fritzson-tutorial-2025 pp. 187–188]`:

| Domain | Across (potential) | Through (flow) | Conserved quantity |
|--------|--------------------|----------------|--------------------|
| thermal | temperature $T$ [K] | heat flow rate $\dot Q$ [W] | energy |
| electrical | voltage $v$ [V] | current $i$ [A] | charge |
| translational | position $s$ [m] | force $f$ [N] | momentum |
| rotational | angle $\varphi$ [rad] | torque $\tau$ [N·m] | angular momentum |

*Modelica by Example* gives two rules for the choice: the through variable is the time derivative
of a conserved quantity, and the across variable is the lowest derivative that appears in the
component laws (position, not velocity) `[src: modelica-by-example, Connectors → Simple Domains]`.
In Modelica the through variable gets the prefix `flow` `[src: modelica-spec-3.7 §9.1]`. Sign
convention: a flow variable is **positive into the component** (MSL `HeatPort`
`[src: msl-4.1.0]`; `[src: fritzson-tutorial-2025 p. 187]`).

### 4.6 Connections, connection sets and balanced models

`connect(a, b)` puts the two connectors in one **connection set**; several `connect` statements on
the same port extend the set. For each set the compiler generates `[src: modelica-spec-3.7 §9.2]`
`[src: fritzson-tutorial-2025 pp. 189–190]`:

- for the **potential** variables: equality, $T_a = T_b = T_c$;
- for the **flow** variables: a zero sum, $\dot Q_a + \dot Q_b + \dot Q_c = 0$.

With the sign convention, the zero sum is the energy balance of the connection point, which stores
no energy: a connection has neither heat capacity nor thermal resistance
`[src: modelica-by-example, Components → Heat Transfer Components]`. A flow variable of a port that
is not connected is set to zero `[src: modelica-spec-3.7 §9.2]`: the model still runs, as if the
port were insulated.

A simulation model must be **balanced**: as many equations as unknowns
`[src: modelica-spec-3.7 §4.8]`. Each component is checked on its own, which lets an author know
how many equations to write without knowing the connections. A practical rule for components with
simple connectors: write **one equation per across/through pair, plus one per local variable,
plus one per output** (the connection supplies the rest) `[src: modelica-by-example, Components → Component Models]`.
`ThermalConductance` has two ports and one local variable $\dot Q$, so it needs three equations
(§5.2).

### 4.7 Classes and packages

- **Specialized classes** `[src: modelica-spec-3.7 §4.7]`: `model` (general), `block` (inputs and
  outputs only), `connector` (no equations), `record` (data), `type` (a predefined type with
  attributes, e.g. `Temperature`), `package` (a library of classes), `function`.
- **Packages** map to folders: `EnergyTraining/Components/ThermalMass.mo` starts with
  `within EnergyTraining.Components;`; a folder package has a `package.mo`, and the optional
  `package.order` lists the classes in the order the library browser shows them
  `[src: modelica-spec-3.7 §13.4]` `[src: modelica-by-example, Packages]`.
- **Names**: a full name starts from the top package (`Modelica.Units.SI.Temperature`).
  `import SI = Modelica.Units.SI;` makes the short name `SI.Temperature` available inside a class;
  the other forms are `import Modelica.Units.SI.Temperature;`, `import Modelica.Units.SI.{Temperature, Power};`
  and `import Modelica.Units.SI.*;` `[src: modelica-spec-3.7 §13.2]`. *Modelica by Example*
  advises against the last one: it hides where a name comes from
  `[src: modelica-by-example, Packages → Importing]`; it also notes that graphical editors write
  full names anyway `[src: modelica-by-example, Packages → Importing Physical Types]`.

### 4.8 Modifications and `final`

A **modification** changes a parameter or an attribute where a component is declared or inherited
`[src: modelica-spec-3.7 §7.2]`:

```modelica
Modelica.Thermal.HeatTransfer.Components.HeatCapacitor zone(C = 1e7, T(start = 283.15, fixed = true));
```

`C = 1e7` sets a parameter; `T(start = …, fixed = true)` modifies the attributes of a variable
inside the component (a nested modification). Modifications can also be written on `extends`
clauses (§4.9). For an array of components, `each` applies one modification to every element:
`HeatCapacitor layer[5](each C = 2e5)` `[src: modelica-spec-3.7 §7.2.5]`.

A system model usually passes its own parameters down to its components — *Modelica by Example*
calls this **propagation**: `ThermalZone` declares `C` and `UA` once and writes
`zone(final C = C)` `[src: modelica-by-example, Subsystems → Propagation]`. **`final`** forbids any
further modification of that value `[src: modelica-spec-3.7 §7.2.6]`, so a user cannot set
`zone.zone.C` to something different from `zone.C` by mistake: one value, one place.

### 4.9 Inheritance and replaceable components

- **`extends`** inherits all elements and equations of a base class; modifications on the
  `extends` clause change its parameters `[src: modelica-spec-3.7 §7.1]`
  `[src: modelica-by-example, Basic Equations → Lotka-Volterra Systems]`.
- **`partial`** marks an incomplete class (for example, ports without equations); it can be a base
  class but cannot be simulated `[src: modelica-spec-3.7 §4.4.2]`. *Modelica by Example* calls such a
  class an **interface** and the classes that complete it **implementations**
  `[src: modelica-by-example, Architectures → Interfaces and Implementations]`.
- **`replaceable`** marks a component whose type can be changed later with **`redeclare`**; the
  replacement must be compatible with the **constraining type** (`constrainedby`)
  `[src: modelica-spec-3.7 §7.3]`. The constraining type is the plug every replacement must fit
  `[src: modelica-by-example, Architectures → Configuration Management]`. Where modifications
  belong: when the declaration has a `constrainedby` clause, a modification written on the
  declaration (`envelope(final UA = UA)` in §5.4) belongs to the default component and is gone after
  a `redeclare`; a modification written on the `constrainedby` clause is applied to every
  replacement `[src: modelica-spec-3.7 §7.3.2]`.

### 4.10 Teaching components and library components

The course writes a component itself only when writing it is the lesson (today: `HeatPort`,
`ThermalMass`, `ThermalConductance`, `FixedTemperature`, `HeatSource`). After that it uses the
validated library: MSL `Modelica.Thermal.HeatTransfer` here, the Buildings library from Session 5.
Reading the library source is part of using it.

## 5. Mathematical formulation

### 5.1 M01 as one Modelica equation

```modelica
model S03_ThermalZoneEquations
  parameter Modelica.Units.SI.HeatCapacity C = 1.0e7 "illustrative";
  parameter Modelica.Units.SI.ThermalConductance UA = 200 "illustrative";
  parameter Modelica.Units.SI.HeatFlowRate Q_flow = 4000;
  parameter Modelica.Units.SI.Temperature T_amb = 273.15;
  parameter Modelica.Units.SI.Temperature T0 = 283.15;
  Modelica.Units.SI.Temperature T "Zone temperature";
initial equation
  T = T0;
equation
  C*der(T) = Q_flow - UA*(T - T_amb);
  annotation (experiment(StopTime = 259200, Interval = 600, Tolerance = 1e-8));
end S03_ThermalZoneEquations;
```

(Shortened: the file also computes the analytic solution.) `der(T)` is the time derivative
`[src: modelica-spec-3.7 §3.7.4]`. Units: J/K · K/s = W on the left, W − W/K · K = W on the
right. The `experiment` annotation stores the simulation settings with the model; annotations
carry information for tools, not equations `[src: modelica-by-example, Basic Equations → Simple
First Order System]`.

### 5.2 Components, generated equations and the count

| Component | Unknowns | Equations written | Rule: pairs + locals + outputs |
|-----------|----------|-------------------|----------------------|
| `ThermalMass` | $T$, $T_{port}$, $\dot Q_{port}$ | $T = T_{port}$, $C\,\dot T = \dot Q_{port}$ | 1 + 1 = 2 |
| `ThermalConductance` | $\dot Q$, $T_a$, $\dot Q_a$, $T_b$, $\dot Q_b$ | $\dot Q = G\,(T_a - T_b)$, $\dot Q_a = \dot Q$, $\dot Q_b = -\dot Q$ | 2 + 1 = 3 |
| `FixedTemperature` | $T_{port}$, $\dot Q_{port}$ | $T_{port} = T_{fixed}$ | 1 + 0 = 1 |
| `HeatSource` | $T_{port}$, $\dot Q_{port}$ (input $\dot Q_{in}$ given) | $\dot Q_{port} = -\dot Q_{in}$ (the heater delivers heat *out of* itself) | 1 + 0 = 1 |
| `Constant` (MSL source) | output $y$ | $y = k$ | 0 + 0 + 1 output = 1 |

In each component, the equations written plus one per through variable (supplied by the
connection) equal the unknowns. `S03_ThermalZoneTeaching` connects the four components and the
constant source for the heater power. At the node where heater, mass and conductance meet,
`connect` adds $T_{heater} = T_{mass} = T_{a}$ and $\dot Q_{heater} + \dot Q_{mass} + \dot Q_{a} = 0$.
Count for the flat model: 14 unknowns; 8 component equations (2 + 3 + 1 + 1 + 1 for the constant
source) and 6 connection equations (1 for the signal, 3 at the zone node, 2 at the ambient node) —
14 equations, a **balanced** model. Eliminating the trivial equations gives
$C\,\dot T = \dot Q_{in} - G\,(T - T_{amb})$: M01 again.

### 5.3 M01 as a block diagram

`S03_ThermalZoneBlocks` draws M01 with MSL blocks (`Modelica.Blocks`): a `Feedback` computes
$T - T_{amb}$, a `Gain` multiplies it by $UA$, a second `Feedback` subtracts the loss from the
heater power, and an `Integrator` with gain $1/C$ returns $T$. The diagram is the solved form
$T(t) = T_0 + \int_0^t (\dot Q - UA\,(T - T_{amb}))/C\,\mathrm d t$ — the Python right-hand side of
Session 1 drawn as boxes. The signals of `Modelica.Blocks` are plain `Real` numbers: the units are
not declared and cannot be checked.

| | Equation (§5.1) | Components (§5.2) | Block diagram (§5.3) |
|---|---|---|---|
| Who chooses the causality | compiler | compiler | modeller |
| Units checked | yes | yes | no (plain signals) |
| Add a second capacity (M02) | rewrite the equations | one component more, or a `redeclare` | redraw the loop |
| Best for | one balance, quick tests | physical systems | controllers, signal processing |

### 5.4 M02 by redeclaration

M01 (`Systems.ThermalZone`) has a replaceable heat path from zone to ambient:

```modelica
replaceable EnergyTraining.Components.EnvelopeUA envelope(final UA=UA)
  constrainedby EnergyTraining.Interfaces.PartialHeatPath;
```

M02 (`Systems.ZoneRC`) extends M01 and puts an envelope with heat capacity in its place:

```modelica
extends EnergyTraining.Systems.ThermalZone(
  final C=C_z, final UA=1/(R_ze + R_ea), final T_start=T_z_start,
  redeclare EnergyTraining.Components.EnvelopeRC envelope(
    final C_e=C_e, final R_ze=R_ze, final R_ea=R_ea, final T_e_start=T_e_start));
```

`EnvelopeRC` is conductance $1/R_{ze}$ – capacity $C_e$ – conductance $1/R_{ea}$; with the
connection equations it gives the two M02 equations of Session 2
`[src: bacher-madsen-2011]`. The number of states changes from 1 to 2; no connection changes. The
`final` modifications propagate the M02 parameters to the inherited M01 (§4.8).

### 5.5 Simplified PV and battery (I3.1)

PV: $P = A\,f_{act}\,\eta\,G_h$ (in the code the input keeps the Buildings name `G`); battery: $E_{max}\,\dot{SOC} = P_{act}$ with
$P_{act} = \eta_{cha}P$ for $P > 0$ (charging) and $P/\eta_{dis}$ otherwise. These are the
equations of the Buildings library components used from Session 5 (`PartialPV`, battery
`Charge`), which also do **not** keep $SOC$ in [0, 1] `[src: buildings-14.0.0]`.

> **Simplification:** in I3.1 the panel is horizontal (irradiance on the panel = $G_h$),
> without temperature or inverter losses; sizes and load are illustrative.

## 6. Guided example

1. **M01 as one model, step by step** (`Examples.S03_ThermalZoneEquations`), following *Getting
   Physical* `[src: modelica-by-example]`: the equation with `Real` variables; then parameters;
   then SI types; then a deliberate unit error found by *Check Model*; then the initial equation
   and the `experiment` annotation. Values of the Session 1 guided example: $C$ = 10⁷ J/K and
   $UA$ = 200 W/K (illustrative), 4 kW from 10 °C at 0 °C outside, 72 h.
2. **M01 from teaching components** (`Examples.S03_ThermalZoneTeaching`): count unknowns and
   equations, then print the flat model. **Then from MSL components** (`Systems.ThermalZone`,
   used by `Examples.S03_ThermalZoneMSL`): open
   `Modelica.Thermal.HeatTransfer.Components.HeatCapacitor` and compare it with `ThermalMass`.
3. **M02 by modification, `extends` and `redeclare`** (`Systems.ZoneRC`, `Examples.S03_ZoneRCStep`): the
   Session 2 guided example, heater 1 → 4 kW from equilibrium, parameters of the 120 m² house
   `[src: bacher-madsen-2011]`.
4. **M01 as a block diagram** (`Examples.S03_ThermalZoneBlocks`): same numbers; what is lost.

## 7. Executable model/code

In OMEdit: *File → Open Model/Library File* `modelica/EnergyTraining/package.mo`, then check and
simulate the examples. From Python (local OpenModelica, or the course Docker image):

```python
from energy_training.omc.results import read_result
from energy_training.omc.runner import flatten, simulate

run = simulate("EnergyTraining.Examples.S03_ZoneRCStep", out_dir="output/s03")
df = read_result(run.csv)                       # time index [s], one column per variable
print(flatten("EnergyTraining.Examples.S03_ThermalZoneTeaching", out_dir="output/s03"))
```

Checks: `EnergyTraining.Validation.ThermalZoneForms` (the four forms of M01 against the analytic
solution) and `ZoneRCvsPython`, simulated with result criteria by the course checks;
`python/tests/test_omc.py`.

## 8. Results

![M01 in Python and Modelica](../../figures/generated/s03_m01_python_vs_modelica.png)

![M02 in Python and Modelica](../../figures/generated/s03_m02_python_vs_modelica.png)

## 9. Interpretation

- **Same model, same numbers.** M01 in Modelica (`S03_ThermalZoneEquations`) differs from the
  exact solution by at most 1.4·10⁻⁵ K over 72 h (OpenModelica's default solver DASSL, tolerance
  10⁻⁸ from the `experiment` annotation); Python's RK45 at rtol = atol = 10⁻⁸ by 7.5·10⁻⁷ K. Both
  are integration errors, not model differences: tighten or loosen the tolerance and they change.
- **Four forms, one model.** The equation, the teaching components, the MSL components and the
  block diagram give the same differential equation after the compiler has removed the trivial
  equations. Simulated together in `Validation.ThermalZoneForms` (the figure in §8), all four have
  the same largest error, 5.3·10⁻⁶ K: smaller than the 1.4·10⁻⁵ K of the equation model alone,
  because the solver's error control now includes the integrator state of the block diagram, a
  plain `Real` with `nominal = 1` (§4.3); the other three forms together give 1.4·10⁻⁵ K
  (observed by execution).
- **M02.** The Modelica `ZoneRC` follows the Python M02 within 1.2·10⁻⁵ K ($T_z$) and 7·10⁻⁶ K
  ($T_e$) over 96 h. The redeclared envelope added a state; the zone, heater, ambient and their
  connections were reused unchanged.
- **What `connect` buys.** In Python each new node meant rewriting `rhs` and the state vector.
  In Modelica the node balance is generated by `connect`, so models grow by adding components.
- **What types buy.** A unit error is found by *Check Model* before any simulation; a block
  diagram, whose signals have no units, cannot be checked this way.
- **Inputs and outputs.** Sources and sensors (`RealInput`, `RealOutput`) join the causal world of
  signals (weather, set points, controllers) to the acausal physical network. M06 in Session 6 is
  M05 with top-level inputs and outputs.

| | Python (Sessions 1–2) | Modelica (Session 3) |
|---|---|---|
| Model written as | right-hand side $\dot x = f(x, u)$ | equations, any order |
| Sorting and solving | by the modeller | by the compiler |
| Node energy balance | written by hand | generated by `connect` |
| Units | comments and names | types, checked by the tool |
| M01 → M02 | new `rhs`, new state vector | one `redeclare` |
| Solver | `solve_ivp` (RK45, BDF, …) | DASSL by default (Session 4) |

## 10. Guided exercise

[G3.1 — M02 from library components](../../exercises/session_03/G3.1_zone_rc_composition.md)

## 11. Independent exercise

[I3.1 — Simplified PV and battery blocks](../../exercises/session_03/I3.1_pv_battery_blocks.md)

## 12. Solutions

Solutions are added to the `solutions/` folder of this repository after the session.

## 13. Common errors

See [common_errors.md](common_errors.md).

## 14. Optional advanced topics

See [optional_topics.md](optional_topics.md).
