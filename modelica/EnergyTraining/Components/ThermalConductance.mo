within EnergyTraining.Components;
model ThermalConductance
  "Teaching component: heat flow between two ports, Q_flow = G (T_a - T_b), no storage"
  parameter Modelica.Units.SI.ThermalConductance G "Thermal conductance";
  Modelica.Units.SI.HeatFlowRate Q_flow "Heat flow rate from port_a to port_b";
  EnergyTraining.Interfaces.HeatPort port_a
    annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
  EnergyTraining.Interfaces.HeatPort port_b
    annotation (Placement(transformation(extent={{90,-10},{110,10}})));
equation
  Q_flow = G*(port_a.T - port_b.T);
  port_a.Q_flow = Q_flow;
  port_b.Q_flow = -Q_flow;
  annotation (
    Icon(graphics={Rectangle(extent={{-90,30},{90,-30}}, lineColor={0,0,0},
          fillColor={192,192,192}, fillPattern=FillPattern.Backward),
        Text(extent={{-150,80},{150,40}}, textString="%name")}),
    Documentation(info="<html>
<p>Session 3 teaching component. MSL equivalent:
<code>Modelica.Thermal.HeatTransfer.Components.ThermalConductor</code>.</p>
<ul>
<li><b>Boundary:</b> the conducting element between <code>port_a</code> and <code>port_b</code>.</li>
<li><b>Assumptions:</b> linear conductance, no heat storage (what enters at a leaves at b).</li>
<li><b>States:</b> none. <b>Parameter:</b> <code>G</code> [W/K].</li>
<li><b>Equations:</b> <code>Q_flow = G (port_a.T - port_b.T)</code>; <code>port_a.Q_flow = Q_flow</code>;
<code>port_b.Q_flow = -Q_flow</code>.</li>
<li><b>Inputs/outputs:</b> none (heat ports only). <b>Units:</b> SI.</li>
</ul>
</html>"));
end ThermalConductance;
