# Course overview

**Title:** Dynamic Modelling, Modelica and Techno-Economic Optimization of Energy Systems
**Format:** individual advanced training, 20 h = 8 sessions × 2.5 h, plus a 2.5-h Python 101
(Session 0) extra to the 20 h: 22.5 contact hours
**Participant:** researcher with an engineering/technical background, new to Modelica

## Aim

Give the participant the *methodology* to build, debug and couple dynamic energy-system models,
and to **use them for decisions**: scenario analysis, optimization of design and operation, and
techno-economic assessment. At the end, they can read a library model (e.g. from the Buildings
library), know what equations it solves and why it may fail numerically, export it as an FMU,
drive it from Python, turn its results into costs, and optimize sizes and operation.

## Conceptual workflow (the spine of every session)

```
Physical system → assumptions → conservation laws → mathematical model → ODE / DAE
  → Modelica implementation → numerical simulation → FMU → Python
  → scenarios and KPIs → techno-economic assessment → optimization of design and operation
```

For every important example the course connects: physical system · assumptions ·
governing equations · Modelica representation · numerical implications · results ·
consequences for design, operation and cost.

## One case study, built piece by piece

One building is followed from the first session to the last: a single-family house in Turin
with thermal demand (space heating, hot water) and electrical demand (appliances).

```
           PV ──────────────┐
                            ▼
 grid ◄──► electrical bus ◄──► battery
                │   ▲
                ▼   │ appliances
           heat pump ──► storage tank ──► zone (space heating)
                                   └────► hot water draws
```

Sessions 1–4 build and debug its parts (zone, tank, PV, battery). Session 5 assembles the system
with a rule-based operating strategy. Session 6 turns it into an FMU driven from Python.
Session 7 turns simulation results into costs and scenarios. Session 8 optimizes sizes and
operation. Final question: *which sizes and which operation minimise the total cost, and how
robust is the answer?* See [model_lineage.md](model_lineage.md).

## Session map

| # | Session | Core question |
|---|---------|---------------|
| 0 | Python 101 (extra 2.5 h) | How do I set up and use Python, notebooks and data for this course? |
| 1 | Dynamic systems modelling | What is a state, and how does a thermal mass respond? |
| 2 | Energy systems modelling | How do conservation laws produce RC networks and storage models? |
| 3 | Modelica fundamentals | How does acausal, equation-based modelling express the same physics? |
| 4 | OpenModelica and numerics | What does the compiler/solver do, and how do I debug it? |
| 5 | Thermo-hydraulics, heat pumps, system assembly | How do fluid components and heat pumps work, and how is the case-study system assembled? |
| 6 | FMI/FMU and Python | How do I move the model out of the modelling tool and run scenarios? |
| 7 | Techno-economic assessment | How do simulation results become costs, and how do scenarios change the answer? |
| 8 | Optimization of design and operation | Which sizes and which operation minimise the cost? |

Details: [syllabus.md](syllabus.md) · [learning_outcomes.md](learning_outcomes.md) ·
[prerequisites.md](prerequisites.md).
