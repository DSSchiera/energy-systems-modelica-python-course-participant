within EnergyTraining.Examples;
model S03_ThermalZoneMSL "Session 3: M01 from Modelica Standard Library components (EnergyTraining.Systems.ThermalZone)"
  extends Modelica.Icons.Example;
  EnergyTraining.Systems.ThermalZone zone(C=1.0e7, UA=200, T_start=283.15) "M01"
    annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
  Modelica.Blocks.Sources.Constant heaterPower(k=4000) "Heater power [W]"
    annotation (Placement(transformation(extent={{-60,20},{-40,40}})));
  Modelica.Blocks.Sources.Constant outdoor(k=273.15) "Ambient temperature [K]"
    annotation (Placement(transformation(extent={{-60,-40},{-40,-20}})));
equation
  connect(heaterPower.y, zone.Q_flow)
    annotation (Line(points={{-39,30},{-20,30},{-20,4},{-12,4}}, color={0,0,127}));
  connect(outdoor.y, zone.T_amb)
    annotation (Line(points={{-39,-30},{-20,-30},{-20,-4},{-12,-4}}, color={0,0,127}));
  annotation (
    experiment(StopTime=259200, Interval=600, Tolerance=1e-8),
    Documentation(info="<html>
<p>Session 3: M01 as the library model <code>EnergyTraining.Systems.ThermalZone</code>, built
from MSL 4.1.0 <code>Modelica.Thermal.HeatTransfer</code> components, driven by two constant
sources with the values of the Session 1 guided example.</p>
<ul>
<li><b>Model:</b> M01 (see <code>EnergyTraining.Systems.ThermalZone</code> for boundary, assumptions,
equations); state <code>zone.zone.T</code> [K].</li>
<li><b>Parameters:</b> C = 1e7 J/K, UA = 200 W/K (illustrative), T_start = 283.15 K.</li>
<li><b>Inputs (constant sources):</b> heater 4000 W, ambient 273.15 K. <b>Output:</b> <code>zone.T</code> [K].</li>
<li><b>Expected result:</b> the analytic step response, equilibrium 20 &deg;C, time constant 13.9 h.</li>
</ul>
</html>"));
end S03_ThermalZoneMSL;
