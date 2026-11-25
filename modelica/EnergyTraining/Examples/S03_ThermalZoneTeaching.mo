within EnergyTraining.Examples;
model S03_ThermalZoneTeaching "Session 3: M01 composed from the teaching components and connector"
  extends Modelica.Icons.Example;
  EnergyTraining.Components.ThermalMass zone(C=1.0e7, T_start=283.15) "Zone node"
    annotation (Placement(transformation(extent={{-10,20},{10,40}})));
  EnergyTraining.Components.ThermalConductance loss(G=200) "Heat loss UA"
    annotation (Placement(transformation(extent={{20,-10},{40,10}})));
  EnergyTraining.Components.FixedTemperature ambient(T=273.15) "Outdoor air at 0 degC"
    annotation (Placement(transformation(extent={{80,-10},{60,10}})));
  EnergyTraining.Components.HeatSource heater "Ideal heater"
    annotation (Placement(transformation(extent={{-50,-10},{-30,10}})));
  Modelica.Blocks.Sources.Constant heaterPower(k=4000) "Heater power [W]"
    annotation (Placement(transformation(extent={{-90,-10},{-70,10}})));
equation
  connect(heaterPower.y, heater.Q_flow)
    annotation (Line(points={{-69,0},{-52,0}}, color={0,0,127}));
  connect(heater.port, zone.port)
    annotation (Line(points={{-30,0},{0,0},{0,20}}, color={191,0,0}));
  connect(zone.port, loss.port_a)
    annotation (Line(points={{0,20},{0,0},{20,0}}, color={191,0,0}));
  connect(loss.port_b, ambient.port)
    annotation (Line(points={{40,0},{60,0}}, color={191,0,0}));
  annotation (
    experiment(StopTime=259200, Interval=600, Tolerance=1e-8),
    Documentation(info="<html>
<p>Session 3: the same M01 as <code>S03_ThermalZoneEquations</code>, now composed from the
teaching components <code>ThermalMass</code>, <code>ThermalConductance</code>,
<code>FixedTemperature</code> and <code>HeatSource</code>, all with the teaching connector
<code>EnergyTraining.Interfaces.HeatPort</code>. The node where three ports meet
(<code>heater.port</code>, <code>zone.port</code>, <code>loss.port_a</code>) gets the connection
equations: equal temperatures and heat flow rates that sum to zero. Together with the component
equations they give the M01 energy balance.</p>
</html>"));
end S03_ThermalZoneTeaching;
