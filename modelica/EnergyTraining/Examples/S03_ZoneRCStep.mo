within EnergyTraining.Examples;
model S03_ZoneRCStep "Session 3: M02 heater step 1 kW to 4 kW from equilibrium (Session 2 guided example)"
  extends Modelica.Icons.Example;
  parameter Modelica.Units.SI.HeatFlowRate Q_before = 1000 "Heater power before the step";
  parameter Modelica.Units.SI.HeatFlowRate Q_after = 4000 "Heater power from t = 0";
  parameter Modelica.Units.SI.Temperature T_amb = 273.15 "Ambient temperature (0 degC)";
  EnergyTraining.Systems.ZoneRC zone(
    T_z_start=T_amb + Q_before*(zone.R_ze + zone.R_ea),
    T_e_start=T_amb + Q_before*zone.R_ea) "M02, starting in equilibrium with Q_before"
    annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
  Modelica.Blocks.Sources.Constant heaterPower(k=Q_after) "Heater power [W]"
    annotation (Placement(transformation(extent={{-60,20},{-40,40}})));
  Modelica.Blocks.Sources.Constant outdoor(k=T_amb) "Ambient temperature [K]"
    annotation (Placement(transformation(extent={{-60,-40},{-40,-20}})));
equation
  connect(heaterPower.y, zone.Q_flow)
    annotation (Line(points={{-39,30},{-20,30},{-20,4},{-12,4}}, color={0,0,127}));
  connect(outdoor.y, zone.T_amb)
    annotation (Line(points={{-39,-30},{-20,-30},{-20,-4},{-12,-4}}, color={0,0,127}));
  annotation (
    experiment(StopTime=345600, Interval=600, Tolerance=1e-8),
    Documentation(info="<html>
<p>Session 3: M02 (<code>EnergyTraining.Systems.ZoneRC</code>, parameters of Bacher and Madsen
2011) with the Session 2 guided example: equilibrium at 1 kW and 0 &deg;C, heater at 4 kW from
t = 0, 96 h. The Python result of <code>energy_training.simulation.zone_rc.simulate</code> for the
same case is the reference (checked by <code>EnergyTraining.Validation.ZoneRCvsPython</code>).</p>
<ul>
<li><b>Model:</b> M02 (see <code>EnergyTraining.Systems.ZoneRC</code> for boundary, assumptions,
equations); states T_z, T_e [K].</li>
<li><b>Parameters:</b> Bacher and Madsen (2011), Table 3; <code>Q_before</code>, <code>Q_after</code> [W],
<code>T_amb</code> [K].</li>
<li><b>Initial conditions:</b> equilibrium with <code>Q_before</code>:
T_z = T_amb + Q_before (R_ze + R_ea), T_e = T_amb + Q_before R_ea.</li>
<li><b>Inputs (constant sources):</b> heater <code>Q_after</code>, ambient <code>T_amb</code>.
<b>Outputs:</b> <code>zone.T</code>, <code>zone.T_e</code> [K].</li>
</ul>
</html>"));
end S03_ZoneRCStep;
