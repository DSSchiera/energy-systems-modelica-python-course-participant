---
title: "Session 3 — Modelica Fundamentals"
subtitle: "Dynamic Modelling, Modelica and Techno-Economic Optimization of Energy Systems"
---

# Objectives

- **Equations** instead of assignments: what the compiler must do
- **M01 in Modelica**: same numbers as Python
- **Connectors**: potential and flow variables; what `connect` generates
- **Library components** (MSL): read them, then use them
- `partial`, `extends`, `replaceable`, `redeclare`: **M01 → M02**
- **Blocks** with inputs and outputs: simplified PV and battery

# Roadmap

- S1–S2 — M01, M02, M03 in Python
- **S3 — the same models in Modelica** ← today
- S4 — how OpenModelica compiles and solves; debugging
- S5 — heat pump + storage + zone + PV + battery (M05, Buildings library)
- S6–S8 — FMU and scenarios, costs, optimal design and operation

# Python: assignments

$$\dot T = \frac{1}{C}\bigl(\dot Q - UA\,(T - T_{amb})\bigr)$$

- You decide **what is computed from what**
- You write the **right-hand side** and call the solver
- A new node = a new `rhs` and a new state vector

# Modelica: equations

$$C\,\frac{dT}{dt} = \dot Q - UA\,(T - T_{amb})$$

- An equation states that two expressions are **equal**
- No order between equations
- The **compiler** flattens, sorts and solves them (Session 4)
- The same component works whatever it is connected to

# Block diagram or schematic?

- **Block diagram**: outputs feed inputs; information flows one way
- **Schematic**: components share **ports**; heat may flow either way
- Modelica has both: `block` (inputs and outputs only) and physical `model`s with connectors
- The physical style is called **acausal**

# M01 as one Modelica model

```modelica
parameter SI.HeatCapacity C = 1.0e7;
parameter SI.ThermalConductance UA = 200;
SI.Temperature T;
initial equation
  T = T0;
equation
  C*der(T) = Q_flow - UA*(T - T_amb);
```

- `SI` = `Modelica.Units.SI` · file: `Examples/S03_ThermalZoneEquations.mo`

# M01: Modelica = Python

![](../../figures/generated/s03_m01_python_vs_modelica.png)

# Connectors

- A connector lists the variables two components **share** at a port
- Thermal port: temperature $T$ and heat flow rate $\dot Q$

```modelica
connector HeatPort
  SI.Temperature T;
  flow SI.HeatFlowRate Q_flow;
end HeatPort;
```

- `flow` marks the **flow** variable; $\dot Q$ > 0 **into** the component

# What `connect` generates

- **Potential** (non-flow) variables: equal, $T_a = T_b = T_c$
- **Flow** variables: sum to zero, $\dot Q_a + \dot Q_b + \dot Q_c = 0$
- The zero sum = **energy balance** of the connection point (no storage)
- An unconnected flow variable is set to **zero**

# Teaching components

- `ThermalMass`: $T = T_{port}$, $\;C\,\dot T = \dot Q_{port}$
- `ThermalConductance`: $\dot Q = G\,(T_a - T_b)$, $\;\dot Q_a = \dot Q$, $\;\dot Q_b = -\dot Q$
- `FixedTemperature`: $T_{port} = T_{fixed}$
- `HeatSource`: $\dot Q_{port} = -\dot Q_{in}$
- Why the minus sign?

# M01 from components: the flat model

- `connect(heater.port, zone.port)`, `connect(zone.port, loss.port_a)`, `connect(loss.port_b, ambient.port)`
- Generated: `zone.port.T = loss.port_a.T`, `zone.port.T = heater.port.T`
- Generated: `heater.port.Q_flow + loss.port_a.Q_flow + zone.port.Q_flow = 0`
- 14 unknowns, 14 equations: a **balanced** model
- Remove the trivial equations → $C\,\dot T = \dot Q - G\,(T - T_{amb})$

# The Modelica Standard Library

- `Modelica.Thermal.HeatTransfer`: `HeatCapacitor`, `ThermalConductor`, `FixedTemperature`, `PrescribedTemperature`, `PrescribedHeatFlow`
- Same equations as the teaching components (read the source!)
- `HeatCapacitor` adds `der_T`; `PrescribedHeatFlow` adds an optional temperature coefficient
- M01 in the course library: `EnergyTraining.Systems.ThermalZone`

# Packages and files

- A package is a folder: `EnergyTraining/Components/ThermalMass.mo`
- First line: `within EnergyTraining.Components;`
- `package.order`: order in the library browser
- Full names: `EnergyTraining.Systems.ThermalZone`, `Modelica.Units.SI.Temperature`

# Classes

- `model`: the general modelling class
- `block`: inputs and outputs only (signals)
- `connector`: variables at a port, no equations
- `record`: data
- `package`: a library of classes and constants

# `partial` and `extends`

- `partial model PartialHeatPath`: two heat ports, **no equations**
- Cannot be simulated: it is incomplete on purpose
- `model EnvelopeUA extends PartialHeatPath` + one `ThermalConductor`
- `extends` inherits elements and equations; modifiers change parameters

# `replaceable` and `redeclare`

```modelica
replaceable EnvelopeUA envelope(UA=UA)
  constrainedby PartialHeatPath;
```

- `replaceable`: the type of `envelope` may change later
- `constrainedby`: every replacement must be a **subtype** of it (at least the same ports)
- `redeclare`: put another component in its place

# M02 = M01 with another envelope

```modelica
model ZoneRC
  extends ThermalZone(
    C=C_z,
    redeclare EnvelopeRC envelope(
      C_e=C_e, R_ze=R_ze, R_ea=R_ea));
```

- `EnvelopeRC`: conductance – capacity – conductance
- One state more, **no connection changed** (shortened; full code in `Systems/ZoneRC.mo`)

# M02: Modelica = Python

![](../../figures/generated/s03_m02_python_vs_modelica.png)

# Inputs and outputs

- `Modelica.Blocks.Interfaces.RealInput`, `RealOutput`: signals with a direction
- `ThermalZone` has inputs $\dot Q$, $T_{amb}$ and output $T$
- Sources (`Constant`, `CombiTimeTable`) and sensors join signals to the physical network
- M06 (Session 6): the system with top-level inputs and outputs, exported as an FMU

# Simplified PV and battery (I3.1)

- PV: $P = A\,f_{act}\,\eta\,G_h$ (horizontal panel; code name `G`)
- Battery: $E_{max}\,\dot{SOC} = P_{act}$
- Charging ($P > 0$): $P_{act} = \eta_{cha}P$; discharging: $P_{act} = P/\eta_{dis}$
- Same equations as the Buildings components of Session 5
- **No limits** on $SOC$: why not?

# Python and Modelica

- **Model**: right-hand side vs equations in any order
- **Sorting and solving**: the modeller vs the compiler
- **Node balance**: written by hand vs generated by `connect`
- **M01 → M02**: new `rhs` vs one `redeclare`
- **Solver**: `solve_ivp` vs DASSL by default

# Common errors

- Heater sign: `port.Q_flow = Q_flow` cools the zone
- Unconnected ports: the model runs, the result is wrong
- No start value: the MSL mass starts at 20 °C
- `start` without `fixed = true`: only a guess (warning)
- `Modelica.SIunits` in old examples → `Modelica.Units.SI`
- Python and Modelica differ by 10⁻⁵ K: tolerances, not a bug

# Exercises

- **G3.1** (guided, 20 min): M02 from MSL components; compare with Python (< 0.01 K)
- **I3.1** (independent, 10 min): `SimplePV` and `SimpleBattery` blocks; one April day in Turin
- Files: `exercises/session_03/`

# Key takeaways

- Modelica models are **equations**; the compiler sorts and solves them
- `connect`: equal **potentials**, **flows** summing to zero
- Read the **library** source, then reuse it
- `replaceable` + `redeclare`: change the structure, keep the connections
- Next: what the compiler does, and what to do when it fails — **Session 4**
