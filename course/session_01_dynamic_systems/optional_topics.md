# Session 1 — optional advanced topics

Use only if the core content finishes early or the participant asks.

1. **Implicit Euler.** $T_{k+1} = T_k + h\,f(t_{k+1}, T_{k+1})$; for M01 solve for $T_{k+1}$ in
   closed form and show that $g = 1/(1 + h/\tau)$ is stable for every $h > 0$ — the key idea behind
   stiff solvers (Session 4).
2. **Time-varying ambient temperature.** Sinusoidal $T_{amb}(t)$ with a 24 h period: the zone
   follows with damped amplitude and a phase lag that depend on $\tau$ (first-order low-pass filter).
3. **Identifying τ from data.** Fit $\tau$ to a noisy step response with a straight line on
   $\ln|T - T_{ss}|$ — a first taste of parameter estimation (not covered further in the course).
4. **Matrix exponential.** For any input $u(t)$ the solution is
   $x(t) = e^{At}x_0 + \int_0^t e^{A(t-s)}Bu(s)\,ds$ `[src: astrom-murray-2021 Ch. 6]`; for M01 with
   constant inputs it reduces to the step response formula.
