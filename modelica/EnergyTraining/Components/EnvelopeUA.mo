within EnergyTraining.Components;
model EnvelopeUA "Envelope as a single conductance UA (the heat loss path of M01)"
  extends EnergyTraining.Interfaces.PartialHeatPath;
  parameter Modelica.Units.SI.ThermalConductance UA "Overall heat-loss conductance";
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor conductor(final G=UA)
    "Zone to ambient"
    annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
equation
  connect(port_a, conductor.port_a)
    annotation (Line(points={{-100,0},{-10,0}}, color={191,0,0}));
  connect(conductor.port_b, port_b)
    annotation (Line(points={{10,0},{100,0}}, color={191,0,0}));
  annotation (Documentation(info="<html>
<p>Heat loss path of M01, built from one MSL <code>ThermalConductor</code>.</p>
<ul>
<li><b>Boundary:</b> building envelope between the zone (<code>port_a</code>) and the ambient
(<code>port_b</code>).</li>
<li><b>Assumptions:</b> linear conductance, no heat storage in the envelope.</li>
<li><b>Equations:</b> <code>Q_flow = UA (port_a.T - port_b.T)</code>; <code>port_a.Q_flow = Q_flow</code>,
<code>port_b.Q_flow = -Q_flow</code>.</li>
<li><b>States:</b> none. <b>Parameter:</b> <code>UA</code> [W/K]. <b>Inputs/outputs:</b> none.</li>
<li><b>Units:</b> SI.</li>
</ul>
</html>"));
end EnvelopeUA;
