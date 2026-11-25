within EnergyTraining.Systems;
model ThermalZone "M01: one lumped zone with heater, heat loss to ambient through a replaceable envelope"
  parameter Modelica.Units.SI.HeatCapacity C = 1.0e7
    "Heat capacity of the zone node (illustrative)";
  parameter Modelica.Units.SI.ThermalConductance UA = 200
    "Overall heat-loss conductance (illustrative)";
  parameter Modelica.Units.SI.Temperature T_start = 283.15 "Initial zone temperature";

  Modelica.Blocks.Interfaces.RealInput Q_flow(unit="W") "Heater power"
    annotation (Placement(transformation(extent={{-140,20},{-100,60}})));
  Modelica.Blocks.Interfaces.RealInput T_amb(unit="K") "Ambient temperature"
    annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
  Modelica.Blocks.Interfaces.RealOutput T(unit="K", displayUnit="degC") "Zone temperature"
    annotation (Placement(transformation(extent={{100,-10},{120,10}})));

  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor zone(
    final C=C, T(start=T_start, fixed=true)) "Zone node (air and internal mass)"
    annotation (Placement(transformation(extent={{-10,20},{10,40}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow heater "Ideal heater"
    annotation (Placement(transformation(extent={{-60,30},{-40,50}})));
  replaceable EnergyTraining.Components.EnvelopeUA envelope(final UA=UA)
    constrainedby EnergyTraining.Interfaces.PartialHeatPath "Heat path from zone to ambient"
    annotation (Placement(transformation(extent={{10,-10},{30,10}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature ambient "Outdoor air"
    annotation (Placement(transformation(extent={{70,-50},{50,-30}})));
  Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor sensor
    annotation (Placement(transformation(extent={{40,40},{60,60}})));
equation
  connect(Q_flow, heater.Q_flow)
    annotation (Line(points={{-120,40},{-60,40}}, color={0,0,127}));
  connect(heater.port, zone.port)
    annotation (Line(points={{-40,40},{-20,40},{-20,20},{0,20}}, color={191,0,0}));
  connect(zone.port, envelope.port_a)
    annotation (Line(points={{0,20},{0,0},{10,0}}, color={191,0,0}));
  connect(envelope.port_b, ambient.port)
    annotation (Line(points={{30,0},{40,0},{40,-40},{50,-40}}, color={191,0,0}));
  connect(T_amb, ambient.T)
    annotation (Line(points={{-120,-40},{-80,-40},{-80,-70},{80,-70},{80,-40},{72,-40}},
      color={0,0,127}));
  connect(zone.port, sensor.port)
    annotation (Line(points={{0,20},{30,20},{30,50},{40,50}}, color={191,0,0}));
  connect(sensor.T, T)
    annotation (Line(points={{61,50},{80,50},{80,0},{110,0}}, color={0,0,127}));
  annotation (
    Icon(graphics={Rectangle(extent={{-100,100},{100,-100}}, lineColor={0,0,0},
          fillColor={255,255,255}, fillPattern=FillPattern.Solid),
        Polygon(points={{-60,0},{0,60},{60,0},{-60,0}}, lineColor={0,0,0},
          fillColor={255,170,85}, fillPattern=FillPattern.Solid),
        Rectangle(extent={{-50,0},{50,-60}}, lineColor={0,0,0},
          fillColor={255,170,85}, fillPattern=FillPattern.Solid),
        Text(extent={{-150,150},{150,110}}, textString="%name")}),
    Documentation(info="<html>
<p><b>M01 ThermalZone</b> (course model lineage), the Modelica version of
<code>energy_training.simulation.thermal_zone</code> (Session 1), assembled from Modelica Standard
Library 4.1.0 thermal components.</p>
<ul>
<li><b>System boundary:</b> the heated zone (air and internal mass) as one node.</li>
<li><b>Assumptions:</b> uniform zone temperature, constant capacity <code>C</code>; ideal heater;
heat leaves through the replaceable <code>envelope</code> (default: one conductance
<code>UA</code>, no storage).</li>
<li><b>State:</b> <code>zone.T</code> [K] (plus the states of a redeclared envelope).</li>
<li><b>Parameters:</b> <code>C</code> [J/K], <code>UA</code> [W/K] (illustrative values, as in
Session 1), <code>T_start</code> [K].</li>
<li><b>Inputs:</b> <code>Q_flow</code> [W] heater power, <code>T_amb</code> [K] ambient
temperature.</li>
<li><b>Output:</b> <code>T</code> [K] zone temperature.</li>
<li><b>Conservation equation</b> (default envelope):
<code>C der(T) = Q_flow - UA (T - T_amb)</code>.</li>
<li><b>Initial condition:</b> <code>zone.T = T_start</code>.</li>
<li><b>Boundary condition:</b> ambient temperature imposed by <code>ambient</code>.</li>
<li><b>Units:</b> SI.</li>
</ul>
<p><code>envelope</code> is <code>replaceable</code> with constraining type
<code>EnergyTraining.Interfaces.PartialHeatPath</code>. <code>EnergyTraining.Systems.ZoneRC</code>
(M02) redeclares it as <code>EnvelopeRC</code>.</p>
</html>"));
end ThermalZone;
