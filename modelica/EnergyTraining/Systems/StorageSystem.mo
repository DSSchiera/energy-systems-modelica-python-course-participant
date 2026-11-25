within EnergyTraining.Systems;
model StorageSystem "M03: hot-water storage tank with prescribed through-flow and surroundings"
  import SI = Modelica.Units.SI;
  parameter SI.Volume V = 0.3 "Tank volume (illustrative)";
  parameter Integer N(min=1) = 10 "Number of fully mixed nodes";
  parameter SI.ThermalConductance UA_loss = 2.0 "Total heat-loss conductance (illustrative)";
  parameter SI.ThermalConductance G = 0 "Conductance between neighbouring nodes";
  parameter SI.Temperature T_start = 303.15 "Initial temperature of every node";

  Modelica.Blocks.Interfaces.RealInput m_flow(unit="kg/s")
    "Mass flow rate; > 0: in at the top (charging)"
    annotation (Placement(transformation(extent={{-140,40},{-100,80}})));
  Modelica.Blocks.Interfaces.RealInput T_in(unit="K") "Inlet temperature"
    annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
  Modelica.Blocks.Interfaces.RealInput T_env(unit="K") "Temperature of the surroundings"
    annotation (Placement(transformation(extent={{-140,-80},{-100,-40}})));
  Modelica.Blocks.Interfaces.RealOutput T_out(unit="K", displayUnit="degC")
    "Outlet temperature"
    annotation (Placement(transformation(extent={{100,-10},{120,10}})));

  EnergyTraining.Components.StorageTank tank(
    final V=V, final N=N, final UA_loss=UA_loss, final G=G, final T_start=T_start)
    "N-node tank"
    annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature surroundings
    "Room around the tank"
    annotation (Placement(transformation(extent={{-40,-60},{-20,-40}})));
equation
  connect(m_flow, tank.m_flow)
    annotation (Line(points={{-120,60},{-60,60},{-60,4},{-12,4}}, color={0,0,127}));
  connect(T_in, tank.T_in)
    annotation (Line(points={{-120,0},{-60,0},{-60,-4},{-12,-4}}, color={0,0,127}));
  connect(T_env, surroundings.T)
    annotation (Line(points={{-120,-60},{-80,-60},{-80,-50},{-42,-50}}, color={0,0,127}));
  connect(surroundings.port, tank.port_env)
    annotation (Line(points={{-20,-50},{0,-50},{0,-10}}, color={191,0,0}));
  connect(tank.T_out, T_out)
    annotation (Line(points={{11,0},{110,0}}, color={0,0,127}));
  annotation (
    Icon(graphics={Rectangle(extent={{-100,100},{100,-100}}, lineColor={0,0,0},
          fillColor={255,255,255}, fillPattern=FillPattern.Solid),
        Rectangle(extent={{-40,80},{40,-80}}, lineColor={0,0,0},
          fillColor={255,85,85}, fillPattern=FillPattern.VerticalCylinder),
        Text(extent={{-150,150},{150,110}}, textString="%name")}),
    Documentation(info="<html>
<p><b>M03 StorageSystem</b> (course model lineage): the tank of
<code>EnergyTraining.Components.StorageTank</code> with the temperature of its surroundings
imposed by an input. Same model as <code>energy_training.simulation.storage</code> (Session 2).</p>
<ul>
<li><b>System boundary:</b> the water in the tank (see <code>StorageTank</code>).</li>
<li><b>Assumptions:</b> those of <code>StorageTank</code>; the surroundings are an ideal
temperature source.</li>
<li><b>States:</b> <code>tank.T[1..N]</code> [K].</li>
<li><b>Parameters:</b> <code>V</code> [m3], <code>N</code> [-], <code>UA_loss</code> [W/K],
<code>G</code> [W/K] (illustrative values), <code>T_start</code> [K].</li>
<li><b>Inputs:</b> <code>m_flow</code> [kg/s], <code>T_in</code> [K], <code>T_env</code> [K].</li>
<li><b>Output:</b> <code>T_out</code> [K].</li>
<li><b>Conservation equations:</b> one energy balance per node (see <code>StorageTank</code>).</li>
<li><b>Initial conditions:</b> every node at <code>T_start</code>.</li>
<li><b>Boundary conditions:</b> inlet flow and temperature, surroundings temperature.</li>
<li><b>Units:</b> SI.</li>
</ul>
</html>"));
end StorageSystem;
