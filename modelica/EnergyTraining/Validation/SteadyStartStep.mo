within EnergyTraining.Validation;
model SteadyStartStep
  "M01 with steady-state and fixed start, ambient step (time event), against the analytic solution"
  extends Modelica.Icons.Example;
  EnergyTraining.Examples.S04_SteadyStartStep ex "Example under test";
  Real err_steady(unit="K") = abs(ex.T_steady - T_steady_exact);
  Real err_fixed(unit="K") = abs(ex.T_fixed - T_fixed_exact);
  Modelica.Units.SI.Temperature T_steady_exact = if time < ex.t_step then T_ss_before
    else T_ss_after + (T_ss_before - T_ss_after)*exp(-(time - ex.t_step)/tau)
    "Analytic solution of the steady start";
  Modelica.Units.SI.Temperature T_fixed_exact = if time < ex.t_step
    then T_ss_before + (ex.T0 - T_ss_before)*exp(-time/tau)
    else T_ss_after + (T_fixed_step - T_ss_after)*exp(-(time - ex.t_step)/tau)
    "Analytic solution of the fixed start";
protected
  parameter Modelica.Units.SI.Time tau = ex.C/ex.UA "Time constant";
  parameter Modelica.Units.SI.Temperature T_ss_before = ex.T_amb_before + ex.Q_flow/ex.UA;
  parameter Modelica.Units.SI.Temperature T_ss_after = ex.T_amb_after + ex.Q_flow/ex.UA;
  parameter Modelica.Units.SI.Temperature T_fixed_step =
    T_ss_before + (ex.T0 - T_ss_before)*exp(-ex.t_step/tau) "Fixed start at the step";
  annotation (
    experiment(StopTime=259200, Interval=600, Tolerance=1e-8),
    Documentation(info="<html><p>Validation model, not teaching content. Case:
<code>Examples.S04_SteadyStartStep</code> (72 h, ambient step after 24 h) against the analytic step
responses of M01. No new physics: states, parameters and units are those of the example.</p>
<p>Pass criterion (course result checks): both errors below 1e-4 K over 72 h (tolerance 1e-8),
and the steady start at 20 &deg;C within 1e-6 K.</p></html>"));
end SteadyStartStep;
