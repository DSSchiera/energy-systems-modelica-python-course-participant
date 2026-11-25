within EnergyTraining.Examples.Broken;
model MissingInitialCondition "M02 heater step that should start in equilibrium (deliberate error)"
  extends Modelica.Icons.Example;
  import SI = Modelica.Units.SI;
  parameter SI.HeatCapacity C_z = 1.07*3.6e6 "Zone heat capacity (1.07 kWh/K)";
  parameter SI.HeatCapacity C_e = 2.92*3.6e6 "Envelope heat capacity (2.92 kWh/K)";
  parameter SI.ThermalResistance R_ze = 0.863e-3 "Zone-envelope resistance (0.863 K/kW)";
  parameter SI.ThermalResistance R_ea = 4.54e-3 "Envelope-ambient resistance (4.54 K/kW)";
  parameter SI.Temperature T_amb = 273.15 "Ambient temperature (0 degC)";
  parameter SI.HeatFlowRate Q_before = 1000 "Heater power before the step (equilibrium)";
  parameter SI.HeatFlowRate Q_after = 4000 "Heater power from t = 0";
  SI.Temperature T_z(displayUnit="degC") "Zone temperature";
  SI.Temperature T_e(displayUnit="degC") "Envelope temperature";
initial equation
  T_z = T_amb + Q_before*(R_ze + R_ea);
equation
  C_z*der(T_z) = Q_after - (T_z - T_e)/R_ze;
  C_e*der(T_e) = (T_z - T_e)/R_ze - (T_e - T_amb)/R_ea;
  annotation (
    experiment(StopTime=345600, Interval=600, Tolerance=1e-6),
    Documentation(info="<html>
<p><b>Deliberately broken</b> (Session 4, G4.1). Intended case: the Session 2 guided example of
M02, starting in equilibrium with <code>Q_before</code>, heater at <code>Q_after</code> from t = 0,
96 h; reference result: <code>EnergyTraining.Examples.S03_ZoneRCStep</code>.</p>
<ul>
<li><b>System boundary:</b> zone air and internal mass (node z), building envelope (node e).</li>
<li><b>Assumptions:</b> two lumped nodes; ideal heater; constant ambient temperature.</li>
<li><b>States:</b> <code>T_z</code>, <code>T_e</code> [K].</li>
<li><b>Parameters:</b> Bacher and Madsen (2011), Table 3 (SI units); <code>T_amb</code> [K],
<code>Q_before</code>, <code>Q_after</code> [W].</li>
<li><b>Inputs:</b> none (constant heater power and ambient temperature).
<b>Outputs:</b> <code>T_z</code>, <code>T_e</code>.</li>
<li><b>Conservation equations:</b> <code>C_z der(T_z) = Q - (T_z - T_e)/R_ze</code>,
<code>C_e der(T_e) = (T_z - T_e)/R_ze - (T_e - T_amb)/R_ea</code>.</li>
<li><b>Initial conditions:</b> intended: equilibrium with <code>Q_before</code>.</li>
<li><b>Boundary conditions:</b> ambient air at the constant temperature <code>T_amb</code>.</li>
<li><b>Units:</b> SI.</li>
</ul>
</html>"));
end MissingInitialCondition;
