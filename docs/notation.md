# Notation and conventions

Fixed for the whole course. Slides, notes, code and Modelica models use these symbols.

## Units

- SI internally: K, W, J, J/K, W/K, kg, kg/s, Pa, s.
- °C only for display (axis labels, tables). Conversion: `energy_training.utilities.units`.
- Time axes in plots: hours (h) for building/storage dynamics, seconds for numerics demos.

## Symbols

| Symbol | Meaning | Unit | Code name (Python / Modelica) |
|--------|---------|------|-------------------------------|
| $t$ | time | s | `t` / `time` |
| $T$ | temperature (state of a lumped node) | K | `T` |
| $T_{amb}$ | ambient (outdoor) temperature | K | `T_amb` |
| $T_0$ | initial temperature | K | `T0` / `T_start` |
| $T_{set}$ | indoor set-point temperature | K | `T_set` |
| $G_h$, $G_{bn}$, $G_{dh}$ | global horizontal, beam normal, diffuse horizontal irradiance | W/m² | `G_h`, `G_bn`, `G_dh` |
| $H_h$ | horizontal irradiation (irradiance integrated over a period) | J/m² (kWh/m² for display) | `H_h` |
| $C$ | heat capacity of a lumped node | J/K | `C` |
| $UA$ | overall conductance (U·A) | W/K | `UA` |
| $R = 1/UA$ | thermal resistance | K/W | `R` |
| $\tau = C/UA = RC$ | time constant | s | `tau` |
| $\dot Q$ | heat flow rate | W | `Q_flow` |
| $\dot m$ | mass flow rate | kg/s | `m_flow` |
| $c_p$ | specific heat capacity at constant pressure | J/(kg·K) | `cp` |
| $h$ | specific enthalpy (fluid contexts, S2, S5) | J/kg | `h` |
| $h$ | integration step size (numerics contexts, S1, S4) — context disambiguates | s | `h` (argument of `explicit_euler`) |
| $h_c$ | convective heat-transfer coefficient | W/(m²·K) | `h_c` |
| $p$ | pressure | Pa | `p` |
| $P_{el}$ | electric power | W | `P_el` |
| $COP$ | coefficient of performance (heating) | – | `COP` |
| $\eta_{C}$ | fraction of Carnot COP achieved | – | `etaCarnot` |
| $x$ | state vector | – | `x` |
| $u$ | input vector | – | `u` |
| $y$ | output vector | – | `y` |
| $p$ (context) | parameter vector (optimization) | – | `theta` in Python to avoid clash with pressure |
| – | parameter *object* (frozen dataclass, e.g. `ThermalZoneParams`) | – | `p` in Session 1–2 code (never mixed with pressure there); optimization code uses `theta` for the vector |
| $T_z$, $T_e$ | zone and envelope node temperatures of M02 | K | `T_z`, `T_e` |
| $C_z$, $C_e$ | heat capacities of the M02 nodes | J/K | `C_z`, `C_e` |
| $R_{ze}$, $R_{ea}$ | resistances zone–envelope, envelope–ambient | K/W | `R_ze`, `R_ea` |
| $T_{in}$, $T_{out}$ | fluid inlet / outlet temperature | K | `T_in`, `T_out` |
| $T_{env}$ | temperature around a component (tank surroundings) | K | `T_env` |
| $T_k$ | temperature of node $k$ of a discretised component (node 1 at the top) | K | `T[k-1]` |
| $N$ | number of nodes of a discretised component | – | `N` |
| $V$ | volume | m³ | `V` |
| $\rho$ | density | kg/m³ | `rho` |
| $UA_{loss}$ | loss conductance of a component to its surroundings | W/K | `UA_loss` |
| $G$ | conductance between neighbouring nodes | W/K | `G` |
| $\varepsilon$, $NTU$, $C_r$ | heat-exchanger effectiveness, number of transfer units, capacity-rate ratio | – | `effectiveness`, `NTU`, `C_r` |
| $\varepsilon$ (context) | emissivity (radiation, S2) — context disambiguates | – | `eps` |
| $P$ | electric power of a component (PV output; battery input, > 0 when charging) | W | `P` |
| $A$ | area (PV panel) | m² | `A` |
| $f_{act}$, $\eta$ | active-cell fraction of a PV panel, PV conversion efficiency (Buildings names) | – | `fAct`, `eta` |
| $E_{max}$ | battery capacity | J (kWh for display) | `EMax` |
| $SOC$ | battery state of charge $\in [0, 1]$ | – | `SOC` |
| $\eta_{cha}$, $\eta_{dis}$ | battery charge and discharge efficiency (Buildings names) | – | `etaCha`, `etaDis` |

## Sign conventions

- Heat flow into a node is positive (consistent with MSL `HeatPort.Q_flow`, a flow variable positive into the component).
- Mass flow into a fluid port is positive (MSL `Modelica.Fluid` / Buildings convention).
