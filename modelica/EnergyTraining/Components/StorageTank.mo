within EnergyTraining.Components;
model StorageTank "Hot-water tank as N fully mixed nodes with a prescribed through-flow (M03)"
  import SI = Modelica.Units.SI;
  parameter SI.Volume V = 0.3 "Tank volume (illustrative)";
  parameter Integer N(min=1) = 10 "Number of fully mixed nodes (node 1 at the top)";
  parameter SI.ThermalConductance UA_loss = 2.0
    "Total heat-loss conductance through the insulation (illustrative)";
  parameter SI.ThermalConductance G = 0
    "Conductance across each interface between neighbouring nodes (0: no conduction)";
  parameter SI.Density rho = 995.586 "Density of water (Buildings.Media.Water)";
  parameter SI.SpecificHeatCapacity cp = 4184 "Specific heat capacity of water (Buildings.Media.Water)";
  parameter SI.Temperature T_start = 303.15 "Initial temperature of every node";
  final parameter SI.Mass m_node = rho*V/N "Water mass of one node";
  final parameter SI.HeatCapacity C_node = m_node*cp "Heat capacity of one node";

  Modelica.Blocks.Interfaces.RealInput m_flow(unit="kg/s")
    "Mass flow rate through the tank; > 0: in at the top, out at the bottom (charging)"
    annotation (Placement(transformation(extent={{-140,20},{-100,60}})));
  Modelica.Blocks.Interfaces.RealInput T_in(unit="K") "Temperature of the entering water"
    annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
  Modelica.Blocks.Interfaces.RealOutput T_out(unit="K", displayUnit="degC")
    "Temperature of the leaving water"
    annotation (Placement(transformation(extent={{100,-10},{120,10}})));
  Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_a port_env
    "Surroundings of the tank (heat losses)"
    annotation (Placement(transformation(extent={{-10,-110},{10,-90}})));

  SI.Temperature T[N](each start=T_start, each fixed=true, each displayUnit="degC")
    "Node temperatures, node 1 at the top";
  SI.HeatFlowRate Q_loss "Heat flow rate from the tank to the surroundings";
protected
  SI.HeatFlowRate Q_cond[N + 1]
    "Conduction into node k from node k-1 (Q_cond[1] and Q_cond[N+1] are the closed ends)";
equation
  Q_cond[1] = 0;
  Q_cond[N + 1] = 0;
  for k in 2:N loop
    Q_cond[k] = G*(T[k - 1] - T[k]);
  end for;
  for k in 1:N loop
    C_node*der(T[k]) =
      cp*max(m_flow, 0)*((if k == 1 then T_in else T[k - 1]) - T[k])
      + cp*max(-m_flow, 0)*((if k == N then T_in else T[k + 1]) - T[k])
      + Q_cond[k] - Q_cond[k + 1]
      - UA_loss/N*(T[k] - port_env.T);
  end for;
  Q_loss = sum(UA_loss/N*(T[k] - port_env.T) for k in 1:N);
  port_env.Q_flow = -Q_loss;
  T_out = if m_flow >= 0 then T[N] else T[1];
  annotation (
    Icon(graphics={Rectangle(extent={{-60,90},{60,-90}}, lineColor={0,0,0},
          fillColor={255,85,85}, fillPattern=FillPattern.VerticalCylinder),
        Line(points={{-60,30},{60,30}}, color={0,0,0}, pattern=LinePattern.Dash),
        Line(points={{-60,-30},{60,-30}}, color={0,0,0}, pattern=LinePattern.Dash),
        Text(extent={{-150,140},{150,100}}, textString="%name"),
        Text(extent={{-60,10},{60,-10}}, textString="N = %N")}),
    Documentation(info="<html>
<p><b>M03 storage tank</b> (course model lineage), the Modelica version of
<code>energy_training.simulation.storage</code> (Session 2). Same equations, same parameter names
and default values.</p>
<ul>
<li><b>System boundary:</b> the water inside the tank wall.</li>
<li><b>Assumptions:</b> <code>N</code> horizontal layers of equal mass, each fully mixed (node 1
at the top); incompressible water with constant <code>rho</code> and <code>cp</code>; plug flow
between layers, the water entering a node has the temperature of the upstream node (upwind);
the inflow always enters the end node; equal loss conductance <code>UA_loss/N</code> per node;
optional conduction <code>G</code> between neighbours; no buoyancy correction.</li>
<li><b>States:</b> <code>T[1..N]</code> [K].</li>
<li><b>Parameters:</b> <code>V</code> [m3], <code>N</code> [-], <code>UA_loss</code> [W/K],
<code>G</code> [W/K] (illustrative values), <code>rho</code> [kg/m3], <code>cp</code>
[J/(kg K)] (Buildings.Media.Water constants), <code>T_start</code> [K].</li>
<li><b>Inputs:</b> <code>m_flow</code> [kg/s] (sign gives the direction),
<code>T_in</code> [K].</li>
<li><b>Outputs:</b> <code>T_out</code> [K]: bottom node when charging (<code>m_flow</code> &ge; 0),
top node otherwise. Heat port <code>port_env</code>: temperature of the surroundings, heat flow
rate <code>-Q_loss</code> into the tank.</li>
<li><b>Conservation equation</b> (node k, charging; T_0 = T_in):
<code>C_node der(T[k]) = m_flow cp (T[k-1] - T[k]) + Q_cond[k] - Q_cond[k+1]
- UA_loss/N (T[k] - T_env)</code>, with <code>C_node = rho V cp / N</code>.</li>
<li><b>Initial conditions:</b> <code>T[k] = T_start</code> for every node.</li>
<li><b>Boundary conditions:</b> inlet temperature and mass flow rate imposed; surroundings at the
temperature of <code>port_env</code>; no conduction through the top and bottom
(<code>Q_cond[1] = Q_cond[N+1] = 0</code>).</li>
<li><b>Units:</b> SI.</li>
</ul>
<p><code>N</code> sets the size of the arrays, so it is a structural parameter: changing it means
compiling the model again (Session 4).</p>
</html>"));
end StorageTank;
