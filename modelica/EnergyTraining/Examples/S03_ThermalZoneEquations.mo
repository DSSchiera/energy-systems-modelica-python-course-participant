within EnergyTraining.Examples;
model S03_ThermalZoneEquations "Session 3: M01 written as one model with equations"
  extends Modelica.Icons.Example;
  parameter Modelica.Units.SI.HeatCapacity C = 1.0e7 "Heat capacity (illustrative)";
  parameter Modelica.Units.SI.ThermalConductance UA = 200 "Heat-loss conductance (illustrative)";
  parameter Modelica.Units.SI.HeatFlowRate Q_flow = 4000 "Heater power";
  parameter Modelica.Units.SI.Temperature T_amb = 273.15 "Ambient temperature (0 degC)";
  parameter Modelica.Units.SI.Temperature T0 = 283.15 "Initial zone temperature (10 degC)";
  Modelica.Units.SI.Temperature T(displayUnit="degC") "Zone temperature";
  Modelica.Units.SI.Temperature T_exact(displayUnit="degC")
    "Analytic solution T_ss + (T0 - T_ss) exp(-t/tau)";
protected
  parameter Modelica.Units.SI.Time tau = C/UA "Time constant";
  parameter Modelica.Units.SI.Temperature T_ss = T_amb + Q_flow/UA "Equilibrium temperature";
initial equation
  T = T0;
equation
  C*der(T) = Q_flow - UA*(T - T_amb);
  T_exact = T_ss + (T0 - T_ss)*exp(-time/tau);
  annotation (
    experiment(StopTime=259200, Interval=600, Tolerance=1e-8),
    Documentation(info="<html>
<p>Session 3, first model: the M01 energy balance of Session 1 written directly as an equation,
with the guided-example values of Session 1 (C = 1e7 J/K and UA = 200 W/K, illustrative;
4 kW heater; 0 &deg;C outside; start at 10 &deg;C; 72 h). <code>T_exact</code> is the analytic step
response, for comparison.</p>
<ul>
<li><b>State:</b> <code>T</code> [K]. <b>Parameters:</b> <code>C</code>, <code>UA</code>,
<code>Q_flow</code>, <code>T_amb</code>, <code>T0</code>.</li>
<li><b>Equation:</b> <code>C der(T) = Q_flow - UA (T - T_amb)</code>.</li>
<li><b>Initial condition:</b> <code>initial equation T = T0</code>.</li>
</ul>
</html>"));
end S03_ThermalZoneEquations;
