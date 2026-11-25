# Session 1 — common errors

| Symptom | Cause | Fix / teaching point |
|---------|-------|----------------------|
| Steady state 273 K too high/low | mixing °C and K in $T - T_{amb}$ or initial value | compute in K everywhere; convert only when plotting (`energy_training.plotting.style.degc`) |
| Time axis in seconds labelled as hours | forgot `/3600` | use `hours()`; keep SI internally |
| Temperature grows without bound | sign error: `+UA*(T - T_amb)` | energy balance: loss leaves the node → minus sign; check that `rhs` is 0 at $T_{ss}$ |
| Euler result oscillates | $h > \tau$ | compute $g = 1 - h/\tau$; reduce $h$ |
| `solve_ivp` result "slightly off" vs analytic | default rtol = 1e-3 | set `rtol`, `atol` explicitly |
| Kink missing at the heater switch / small error after a switch | solver stepped over the input jump | pass the jump times (`breakpoints` or a `piecewise_constant` Signal) |
| `solve_ivp` returns `y` of shape (1, n) and plotting fails | state vector is 2-D | use `sol.y[0]` |
| Energy in J reported as kWh | missing `/3.6e6` | 1 kWh = 3.6·10⁶ J |
| "C" confused between heat capacity and output matrix | notation clash | the course writes $C_y$ for the output matrix in state-space formulas ([notation](../../docs/notation.md)) |
