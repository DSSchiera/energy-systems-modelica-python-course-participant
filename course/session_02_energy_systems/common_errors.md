# Session 2 — common errors

| Symptom | Cause | Fix / teaching point |
|---------|-------|----------------------|
| Tank energy grows although no heat is added | advection written as $\dot m c_p T_{in}$ without the outflow term | only enthalpy *differences* count: $\dot m c_p (T_{up} - T_k)$ per node |
| Energy balance residual is large and depends on the output step | the inflow jumps between samples (trapezoid rule smears each jump) | put jumps on the output grid, use a finer grid, or compare with the smear bound $\Delta P\,\Delta t/2$ |
| Wrong outlet temperature after flow reversal | upstream node not switched with the flow direction | the inlet node is node 1 for $\dot m > 0$ and node $N$ for $\dot m < 0$ |
| Conduction changes the total energy | conduction added to one node but not subtracted from the neighbour | write each internal flow once and apply it with opposite signs |
| A node becomes hotter than the inlet water (impossible physically) | tolerances too loose: at SciPy's defaults (rtol 1e-3) the charging run with $N$ = 50 overshoots by about 2 K | set `rtol`, `atol` explicitly (the course functions use 1e-8) |
| The run takes very long with many nodes | stiffness: node time constant ≪ loss time constant | use `method="BDF"` for large $N$; Session 4 explains why |
| Time constants read as $R_{ze}C_z$ and $R_{ea}C_e$ | coupled nodes: the modes are eigenvalues of $A$, not single RC products | compute `np.linalg.eigvals(A)` |
| Equilibrium of M02 computed with $R_{ea}$ only | the zone sees both resistances in series | $T_z = T_{amb} + \dot Q(R_{ze} + R_{ea})$ |
| kWh/K values used as J/K | unit conversion of published parameters | 1 kWh/K = 3.6·10⁶ J/K; 1 K/kW = 10⁻³ K/W |
| Cold water entering at the top "sinks" in reality but not in the model | M03 has no buoyancy model | charge hot water from the top, cold from the bottom; library tanks add mixing for inversions |
| Negative heat flow from the ε-NTU function, or a `ValueError` | inlet temperatures swapped, or $C_r$ computed as $C_{max}/C_{min}$ | $C_r = C_{min}/C_{max} \le 1$; hot inlet first |
