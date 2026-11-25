within EnergyTraining.Components;
model HeatSource "Teaching component: heat flow rate into the connected component, set by an input"
  Modelica.Blocks.Interfaces.RealInput Q_flow(unit="W")
    "Heat flow rate delivered through port"
    annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
  EnergyTraining.Interfaces.HeatPort port
    annotation (Placement(transformation(extent={{90,-10},{110,10}})));
equation
  port.Q_flow = -Q_flow;
  annotation (
    Icon(graphics={Rectangle(extent={{-90,40},{90,-40}}, lineColor={191,0,0},
          fillColor={255,255,255}, fillPattern=FillPattern.Solid),
        Line(points={{-60,0},{60,0}}, color={191,0,0}, arrow={Arrow.None,Arrow.Filled}),
        Text(extent={{-150,90},{150,50}}, textString="%name")}),
    Documentation(info="<html>
<p>Session 3 teaching component (an ideal heater). MSL equivalent:
<code>Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow</code> with the default
<code>alpha = 0</code>.</p>
<ul>
<li><b>Input:</b> <code>Q_flow</code> [W], heat delivered to the connected component.</li>
<li><b>Equation:</b> <code>port.Q_flow = -Q_flow</code>. The minus sign follows the flow
convention: <code>port.Q_flow</code> is positive <i>into</i> this component, and the heater
delivers heat <i>out of</i> it.</li>
<li><b>Boundary:</b> the heater; heat leaves only through <code>port</code>.</li>
<li><b>Assumptions:</b> ideal heater (no losses, no dynamics), the delivered heat equals the input.</li>
<li><b>States, parameters, outputs:</b> none.</li>
<li><b>Units:</b> SI (W).</li>
</ul>
</html>"));
end HeatSource;
