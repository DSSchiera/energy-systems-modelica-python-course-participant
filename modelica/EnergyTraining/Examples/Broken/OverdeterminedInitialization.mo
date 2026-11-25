within EnergyTraining.Examples.Broken;
model OverdeterminedInitialization "M01 that should start in steady state (deliberate error)"
  extends Modelica.Icons.Example;
  import SI = Modelica.Units.SI;
  parameter SI.HeatCapacity C = 1.0e7 "Zone heat capacity (illustrative)";
  parameter SI.ThermalConductance UA = 200 "Heat-loss conductance (illustrative)";
  parameter SI.Temperature T_amb = 273.15 "Ambient temperature (0 degC)";
  parameter SI.HeatFlowRate Q_flow = 4000 "Heater power";
  parameter SI.Temperature T_start = 283.15 "Guess of the initial zone temperature";
  SI.Temperature T(start=T_start, fixed=true, displayUnit="degC") "Zone temperature";
initial equation
  der(T) = 0;
equation
  C*der(T) = Q_flow - UA*(T - T_amb);
  annotation (
    experiment(StopTime=259200, Interval=600, Tolerance=1e-6),
    Documentation(info="<html>
<p><b>Deliberately broken</b> (Session 4, G4.1). Intended case: M01 (Session 1) starting in
<b>steady state</b> with the heater on, 72 h; the zone temperature should stay constant at
T_amb + Q_flow/UA = 20 &deg;C.</p>
<ul>
<li><b>System boundary:</b> the heated zone as one node.</li>
<li><b>Assumptions:</b> uniform zone temperature; constant capacity; ideal heater; constant
ambient temperature.</li>
<li><b>State:</b> <code>T</code> [K]. <b>Parameters:</b> <code>C</code> [J/K], <code>UA</code>
[W/K] (illustrative, Session 1), <code>T_amb</code> [K], <code>Q_flow</code> [W],
<code>T_start</code> [K].</li>
<li><b>Inputs:</b> none. <b>Output:</b> <code>T</code>.</li>
<li><b>Conservation equation:</b> <code>C der(T) = Q_flow - UA (T - T_amb)</code>.</li>
<li><b>Initial condition:</b> intended: steady state.</li>
<li><b>Boundary conditions:</b> ambient air at the constant temperature <code>T_amb</code>.</li>
<li><b>Units:</b> SI.</li>
</ul>
</html>"));
end OverdeterminedInitialization;
