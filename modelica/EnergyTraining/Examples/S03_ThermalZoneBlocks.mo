within EnergyTraining.Examples;
model S03_ThermalZoneBlocks "Session 3: M01 as a block diagram (integrator, gain, feedback)"
  extends Modelica.Icons.Example;
  parameter Modelica.Units.SI.HeatCapacity C = 1.0e7 "Heat capacity (illustrative)";
  parameter Modelica.Units.SI.ThermalConductance UA = 200 "Heat-loss conductance (illustrative)";
  parameter Modelica.Units.SI.Temperature T0 = 283.15 "Initial zone temperature (10 degC)";

  Modelica.Blocks.Sources.Constant heaterPower(k=4000) "Heater power [W]"
    annotation (Placement(transformation(extent={{-100,20},{-80,40}})));
  Modelica.Blocks.Sources.Constant outdoor(k=273.15) "Ambient temperature [K]"
    annotation (Placement(transformation(extent={{-100,-60},{-80,-40}})));
  Modelica.Blocks.Math.Feedback net "Net heat flow rate Q_flow - UA (T - T_amb) [W]"
    annotation (Placement(transformation(extent={{-50,20},{-30,40}})));
  Modelica.Blocks.Continuous.Integrator zone(
    k=1/C, initType=Modelica.Blocks.Types.Init.InitialOutput, y_start=T0)
    "Zone temperature T [K]: integral of net/C"
    annotation (Placement(transformation(extent={{0,20},{20,40}})));
  Modelica.Blocks.Math.Feedback dT "Temperature difference T - T_amb [K]"
    annotation (Placement(transformation(extent={{30,-60},{10,-40}})));
  Modelica.Blocks.Math.Gain loss(k=UA) "Heat loss UA (T - T_amb) [W]"
    annotation (Placement(transformation(extent={{-10,-60},{-30,-40}})));
equation
  connect(heaterPower.y, net.u1)
    annotation (Line(points={{-79,30},{-48,30}}, color={0,0,127}));
  connect(net.y, zone.u)
    annotation (Line(points={{-31,30},{-2,30}}, color={0,0,127}));
  connect(zone.y, dT.u1)
    annotation (Line(points={{21,30},{50,30},{50,-50},{28,-50}}, color={0,0,127}));
  connect(outdoor.y, dT.u2)
    annotation (Line(points={{-79,-50},{-60,-50},{-60,-80},{20,-80},{20,-58}}, color={0,0,127}));
  connect(dT.y, loss.u)
    annotation (Line(points={{11,-50},{-8,-50}}, color={0,0,127}));
  connect(loss.y, net.u2)
    annotation (Line(points={{-31,-50},{-40,-50},{-40,22}}, color={0,0,127}));
  annotation (
    experiment(StopTime=259200, Interval=600, Tolerance=1e-8),
    Documentation(info="<html>
<p>Session 3: the same M01 as <code>S03_ThermalZoneEquations</code>, drawn as a block diagram with
Modelica Standard Library 4.1.0 blocks (<code>Modelica.Blocks</code>). The diagram is the solved
form of the energy balance, <code>T = T0 + integral of (Q_flow - UA (T - T_amb))/C</code>: the
modeller has chosen the causality (which quantity is computed from which), as in the Python
right-hand side of Session 1.</p>
<ul>
<li><b>System boundary:</b> the zone (air and internal mass) as one node, as in M01.</li>
<li><b>Assumptions:</b> those of M01: uniform temperature, constant <code>C</code> and
<code>UA</code>, ideal heater.</li>
<li><b>State:</b> <code>zone.y</code> = T [K], the output of the integrator.</li>
<li><b>Parameters:</b> <code>C</code> [J/K], <code>UA</code> [W/K] (illustrative, as in Session 1),
<code>T0</code> [K].</li>
<li><b>Inputs (constant sources):</b> heater 4000 W, ambient 273.15 K. <b>Output:</b>
<code>zone.y</code> [K].</li>
<li><b>Conservation equation:</b> <code>C der(T) = Q_flow - UA (T - T_amb)</code>, written as
<code>der(zone.y) = net.y/C</code> by the integrator with gain <code>1/C</code>.</li>
<li><b>Initial condition:</b> <code>zone.y = T0</code> (<code>initType = InitialOutput</code>).</li>
<li><b>Boundary condition:</b> ambient temperature from <code>outdoor</code>.</li>
<li><b>Units:</b> SI. The signals of <code>Modelica.Blocks</code> are plain <code>Real</code>
numbers without units, so the units given in brackets are a convention of this diagram and are
not checked by the tool.</li>
</ul>
<p>Compare with <code>S03_ThermalZoneTeaching</code>: a second capacity (M02) means adding
components and connections there, or one <code>redeclare</code> (<code>Systems.ZoneRC</code>), but
redrawing the loop here.</p>
</html>"));
end S03_ThermalZoneBlocks;
