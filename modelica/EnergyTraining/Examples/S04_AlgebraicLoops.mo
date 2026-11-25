within EnergyTraining.Examples;
model S04_AlgebraicLoops "Session 4: M01 with walls that create a linear and a nonlinear algebraic loop"
  extends Modelica.Icons.Example;
  import SI = Modelica.Units.SI;
  parameter SI.HeatCapacity C = 1.0e7 "Zone heat capacity (illustrative, as M01)";
  parameter SI.ThermalConductance G_layer = 400
    "Conductance of each wall layer (two in series = UA 200 W/K of M01)";
  parameter SI.HeatFlowRate Q_flow = 4000 "Heater power";
  parameter SI.Temperature T_amb = 273.15 "Ambient temperature (0 degC)";

  // Zone A: wall of two conductive layers, no heat capacity in the wall -> linear loop
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor zoneA(C=C, T(start=283.15, fixed=true))
    "Zone with a two-layer wall"
    annotation (Placement(transformation(extent={{-50,40},{-30,60}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor layerA1(G=G_layer) "Inner layer"
    annotation (Placement(transformation(extent={{-20,20},{0,40}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor layerA2(G=G_layer) "Outer layer"
    annotation (Placement(transformation(extent={{20,20},{40,40}})));
  Modelica.Thermal.HeatTransfer.Sources.FixedHeatFlow heaterA(Q_flow=Q_flow) "Heater"
    annotation (Placement(transformation(extent={{-90,20},{-70,40}})));
  Modelica.Thermal.HeatTransfer.Sources.FixedTemperature ambientA(T=T_amb) "Outdoor air"
    annotation (Placement(transformation(extent={{80,20},{60,40}})));

  // Zone B: conductive layer, then radiation to the surroundings -> nonlinear loop
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor zoneB(C=C, T(start=283.15, fixed=true))
    "Zone whose outer surface radiates"
    annotation (Placement(transformation(extent={{-50,-20},{-30,0}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor layerB1(G=G_layer) "Wall layer"
    annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
  Modelica.Thermal.HeatTransfer.Components.BodyRadiation surfaceB(Gr=2)
    "Radiation of the outer surface (illustrative Gr = 2 m2)"
    annotation (Placement(transformation(extent={{20,-40},{40,-20}})));
  Modelica.Thermal.HeatTransfer.Sources.FixedHeatFlow heaterB(Q_flow=Q_flow) "Heater"
    annotation (Placement(transformation(extent={{-90,-40},{-70,-20}})));
  Modelica.Thermal.HeatTransfer.Sources.FixedTemperature ambientB(T=T_amb) "Surroundings"
    annotation (Placement(transformation(extent={{80,-40},{60,-20}})));
equation
  connect(heaterA.port, zoneA.port)
    annotation (Line(points={{-70,30},{-40,30},{-40,40}}, color={191,0,0}));
  connect(zoneA.port, layerA1.port_a)
    annotation (Line(points={{-40,40},{-40,30},{-20,30}}, color={191,0,0}));
  connect(layerA1.port_b, layerA2.port_a)
    annotation (Line(points={{0,30},{20,30}}, color={191,0,0}));
  connect(layerA2.port_b, ambientA.port)
    annotation (Line(points={{40,30},{60,30}}, color={191,0,0}));
  connect(heaterB.port, zoneB.port)
    annotation (Line(points={{-70,-30},{-40,-30},{-40,-20}}, color={191,0,0}));
  connect(zoneB.port, layerB1.port_a)
    annotation (Line(points={{-40,-20},{-40,-30},{-20,-30}}, color={191,0,0}));
  connect(layerB1.port_b, surfaceB.port_a)
    annotation (Line(points={{0,-30},{20,-30}}, color={191,0,0}));
  connect(surfaceB.port_b, ambientB.port)
    annotation (Line(points={{40,-30},{60,-30}}, color={191,0,0}));
  annotation (
    experiment(StopTime=259200, Interval=600, Tolerance=1e-6),
    Documentation(info="<html>
<p>Session 4: two independent versions of M01 (Session 1) whose walls create algebraic loops,
to show what the compiler does with them (tearing). Translate with the omc debug flags
<code>backenddaeinfo,dumpLoops</code> (<code>energy_training.omc.runner.backend_info</code>).</p>
<ul>
<li><b>System boundary:</b> each zone (air and internal mass) as one node; the wall layers have
no heat capacity.</li>
<li><b>Assumptions:</b> zone A loses heat through two conductive layers in series; zone B through
one conductive layer and radiation from the outer surface (MSL <code>BodyRadiation</code>,
Q = sigma Gr (T_a^4 - T_b^4)); constant heater power and ambient temperature.</li>
<li><b>States:</b> <code>zoneA.T</code>, <code>zoneB.T</code> [K].</li>
<li><b>Parameters:</b> <code>C</code> [J/K], <code>G_layer</code> [W/K] (illustrative),
<code>surfaceB.Gr</code> [m2] (illustrative), <code>Q_flow</code> [W], <code>T_amb</code> [K].</li>
<li><b>Inputs:</b> none. <b>Outputs:</b> zone temperatures; the wall-interface temperatures
<code>layerA1.port_b.T</code> and <code>layerB1.port_b.T</code> are the unknowns of the loops.</li>
<li><b>Conservation equations:</b> <code>C der(T) = Q_flow - Q_wall</code> for each zone; at each
wall interface the heat flow rates of the two layers are equal (no storage).</li>
<li><b>Initial conditions:</b> both zones at 10 &deg;C.</li>
<li><b>Boundary conditions:</b> ambient at 0 &deg;C.</li>
<li><b>Units:</b> SI.</li>
</ul>
<p>Zone A behaves exactly as M01 with UA = 200 W/K: the two layers in series have
G_layer/2 = 200 W/K.</p>
</html>"));
end S04_AlgebraicLoops;
