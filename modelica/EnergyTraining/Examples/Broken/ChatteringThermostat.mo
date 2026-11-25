within EnergyTraining.Examples.Broken;
model ChatteringThermostat "M01 with an on/off thermostat (deliberate error)"
  extends Modelica.Icons.Example;
  import SI = Modelica.Units.SI;
  parameter SI.HeatCapacity C = 1.0e7 "Zone heat capacity (illustrative)";
  parameter SI.ThermalConductance UA = 200 "Heat-loss conductance (illustrative)";
  parameter SI.Temperature T_amb = 273.15 "Ambient temperature (0 degC)";
  parameter SI.HeatFlowRate Q_max = 6000 "Heater power when on";
  parameter SI.Temperature T_set = 293.15 "Set point (20 degC)";
  SI.Temperature T(start=292.15, fixed=true, displayUnit="degC") "Zone temperature";
  SI.HeatFlowRate Q_flow "Heater power";
equation
  Q_flow = if T < T_set then Q_max else 0;
  C*der(T) = Q_flow - UA*(T - T_amb);
  annotation (
    experiment(StopTime=5000, Interval=10, Tolerance=1e-6),
    Documentation(info="<html>
<p><b>Deliberately broken</b> (Session 4, G4.1). Intended case: M01 (Session 1) heated by an
on/off heater controlled by a thermostat, starting at 19 &deg;C. The run is short (5000 s) on
purpose.</p>
<ul>
<li><b>System boundary:</b> the heated zone as one node.</li>
<li><b>Assumptions:</b> uniform zone temperature; constant capacity; ideal on/off heater;
constant ambient temperature.</li>
<li><b>State:</b> <code>T</code> [K]. <b>Parameters:</b> <code>C</code> [J/K], <code>UA</code>
[W/K] (illustrative, Session 1), <code>T_amb</code>, <code>T_set</code> [K], <code>Q_max</code>
[W].</li>
<li><b>Inputs:</b> none. <b>Outputs:</b> <code>T</code>, <code>Q_flow</code>.</li>
<li><b>Conservation equation:</b> <code>C der(T) = Q_flow - UA (T - T_amb)</code>.</li>
<li><b>Initial condition:</b> <code>T = 19 &deg;C</code>.</li>
<li><b>Boundary conditions:</b> ambient air at the constant temperature <code>T_amb</code>.</li>
<li><b>Units:</b> SI.</li>
</ul>
</html>"));
end ChatteringThermostat;
