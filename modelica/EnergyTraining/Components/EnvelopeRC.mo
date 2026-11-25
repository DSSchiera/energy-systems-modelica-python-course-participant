within EnergyTraining.Components;
model EnvelopeRC
  "Envelope with heat capacity: conductance 1/R_ze, capacity C_e, conductance 1/R_ea (the envelope node of M02)"
  extends EnergyTraining.Interfaces.PartialHeatPath;
  parameter Modelica.Units.SI.HeatCapacity C_e "Heat capacity of the envelope node";
  parameter Modelica.Units.SI.ThermalResistance R_ze "Thermal resistance zone to envelope";
  parameter Modelica.Units.SI.ThermalResistance R_ea "Thermal resistance envelope to ambient";
  parameter Modelica.Units.SI.Temperature T_e_start "Initial envelope temperature";
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor zoneToEnvelope(final G=1/R_ze)
    annotation (Placement(transformation(extent={{-60,-10},{-40,10}})));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor mass(
    final C=C_e, T(start=T_e_start, fixed=true)) "Envelope node (heavy construction)"
    annotation (Placement(transformation(extent={{-10,0},{10,20}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor envelopeToAmbient(final G=1/R_ea)
    annotation (Placement(transformation(extent={{40,-10},{60,10}})));
  Modelica.Units.SI.Temperature T_e = mass.T "Envelope temperature";
equation
  connect(port_a, zoneToEnvelope.port_a)
    annotation (Line(points={{-100,0},{-60,0}}, color={191,0,0}));
  connect(zoneToEnvelope.port_b, mass.port)
    annotation (Line(points={{-40,0},{0,0}}, color={191,0,0}));
  connect(mass.port, envelopeToAmbient.port_a)
    annotation (Line(points={{0,0},{40,0}}, color={191,0,0}));
  connect(envelopeToAmbient.port_b, port_b)
    annotation (Line(points={{60,0},{100,0}}, color={191,0,0}));
  annotation (Documentation(info="<html>
<p>Envelope node of M02 (two-state model of Bacher and Madsen, 2011, deterministic part): the
zone exchanges heat with a heavy envelope node, which exchanges heat with the ambient.</p>
<ul>
<li><b>Boundary:</b> building envelope between the zone (<code>port_a</code>) and the ambient
(<code>port_b</code>).</li>
<li><b>Assumptions:</b> one lumped envelope node, constant capacity, linear resistances, no solar
gains.</li>
<li><b>State:</b> <code>mass.T</code> = T_e [K]. <b>Inputs/outputs:</b> none (heat ports only).</li>
<li><b>Parameters:</b> <code>C_e</code> [J/K], <code>R_ze</code>, <code>R_ea</code> [K/W],
<code>T_e_start</code> [K].</li>
<li><b>Equation:</b> <code>C_e der(T_e) = (T_z - T_e)/R_ze + (T_amb - T_e)/R_ea</code>, from the
MSL components and the connection equations.</li>
<li><b>Initial condition:</b> <code>T_e = T_e_start</code>.</li>
<li><b>Units:</b> SI.</li>
</ul>
</html>"));
end EnvelopeRC;
