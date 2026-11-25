within EnergyTraining.Interfaces;
partial model PartialHeatPath
  "Heat path between a zone and the ambient: two MSL heat ports, no equations"
  Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_a port_a "Zone side"
    annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
  Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_b port_b "Ambient side"
    annotation (Placement(transformation(extent={{90,-10},{110,10}})));
  annotation (
    Icon(graphics={Rectangle(extent={{-90,40},{90,-40}}, lineColor={0,0,0},
          fillColor={215,215,215}, fillPattern=FillPattern.Solid),
        Text(extent={{-150,90},{150,50}}, textString="%name")}),
    Documentation(info="<html>
<p>Constraining type of the replaceable <code>envelope</code> of
<code>EnergyTraining.Systems.ThermalZone</code>. Any model that extends this class can be put
in its place with <code>redeclare</code>: a single conductance (M01, <code>EnvelopeUA</code>) or a
conductance&ndash;capacity&ndash;conductance chain (M02, <code>EnvelopeRC</code>).</p>
<p>The class is <code>partial</code>: it declares the ports but no equations, so it cannot be
simulated on its own (Modelica Language Specification 3.7, section 4.4.2).</p>
</html>"));
end PartialHeatPath;
