within EnergyTraining.Examples;
model S04_StorageCharging "Session 4: M03 charged with hot water (Session 2 guided example)"
  extends Modelica.Icons.Example;
  parameter Integer N(min=1) = 10 "Number of nodes (structural: recompile to change)";
  parameter Modelica.Units.SI.MassFlowRate m_flow = 0.1 "Charging mass flow rate";
  parameter Modelica.Units.SI.Temperature T_in = 333.15 "Inlet temperature (60 degC)";
  parameter Modelica.Units.SI.Temperature T_env = 293.15 "Surroundings (20 degC)";
  EnergyTraining.Systems.StorageSystem storage(N=N, T_start=303.15)
    "M03, 300 L, starting at 30 degC"
    annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
  Modelica.Blocks.Sources.Constant pump(k=m_flow) "Mass flow rate [kg/s]"
    annotation (Placement(transformation(extent={{-60,40},{-40,60}})));
  Modelica.Blocks.Sources.Constant inlet(k=T_in) "Inlet temperature [K]"
    annotation (Placement(transformation(extent={{-60,0},{-40,20}})));
  Modelica.Blocks.Sources.Constant room(k=T_env) "Surroundings temperature [K]"
    annotation (Placement(transformation(extent={{-60,-40},{-40,-20}})));
equation
  connect(pump.y, storage.m_flow)
    annotation (Line(points={{-39,50},{-20,50},{-20,6},{-12,6}}, color={0,0,127}));
  connect(inlet.y, storage.T_in)
    annotation (Line(points={{-39,10},{-26,10},{-26,0},{-12,0}}, color={0,0,127}));
  connect(room.y, storage.T_env)
    annotation (Line(points={{-39,-30},{-20,-30},{-20,-6},{-12,-6}}, color={0,0,127}));
  annotation (
    experiment(StopTime=10800, Interval=60, Tolerance=1e-6),
    Documentation(info="<html>
<p>Session 4: M03 (<code>EnergyTraining.Systems.StorageSystem</code>) with the Session 2 guided
example: 300 L tank at 30 &deg;C, charged from the top with 0.1 kg/s at 60 &deg;C, surroundings
at 20 &deg;C, 3 h. Used for the solver and node-count studies of Session 4 (I4.1).</p>
<ul>
<li><b>System boundary:</b> the water in the 300 L tank.</li>
<li><b>Assumptions:</b> N fully mixed layers of equal mass, plug flow between them (upwind),
equal loss conductance per layer, no conduction between layers (G = 0), no buoyancy
correction (details: <code>EnergyTraining.Components.StorageTank</code>).</li>
<li><b>States:</b> <code>storage.tank.T[1..N]</code> [K].</li>
<li><b>Conservation equation</b> (node k, charging from the top, T_0 = T_in):
<code>C_node der(T[k]) = m_flow cp (T[k-1] - T[k]) - UA_loss/N (T[k] - T_env)</code>.</li>
<li><b>Boundary conditions:</b> inlet flow and temperature at the top, surroundings at
T_env.</li>
<li><b>Parameters:</b> <code>N</code> [-]; tank values are the illustrative defaults of M03.</li>
<li><b>Initial conditions:</b> every node at 30 &deg;C.</li>
<li><b>Inputs (constant sources):</b> <code>m_flow</code> [kg/s], <code>T_in</code> [K],
<code>T_env</code> [K]. <b>Output:</b> <code>storage.T_out</code> [K].</li>
<li><b>Units:</b> SI.</li>
</ul>
<p>Time scales: mean residence time rho V / m_flow = 0.83 h; node time constant
rho V / (N m_flow) = 5.0 min for N = 10; standby-loss time constant rho V cp / UA_loss = 174 h.</p>
</html>"));
end S04_StorageCharging;
