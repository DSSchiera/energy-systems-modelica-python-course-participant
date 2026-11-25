within EnergyTraining.Validation;
model SmokeTest "Toolchain check: first-order decay with known analytic solution"
  extends Modelica.Icons.Example;
  parameter Modelica.Units.SI.Time tau = 10 "Time constant";
  parameter Real x0 = 1 "Initial value";
  Real x(start = x0, fixed = true) "State";
  Real x_exact "Analytic solution x0*exp(-t/tau)";
  Real err "Absolute error";
equation
  tau*der(x) = -x;
  x_exact = x0*exp(-time/tau);
  err = abs(x - x_exact);
  annotation (
    experiment(StopTime=50, Tolerance=1e-8),
    Documentation(info="<html><p>Not teaching content. Verifies that omc, the
Modelica Standard Library and the validation script work. Pass criterion:
<code>max(err) &lt; 1e-5</code>.</p></html>"));
end SmokeTest;
