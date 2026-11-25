within EnergyTraining.Components;
model FixedTemperature "Teaching component: port at a fixed temperature (boundary condition)"
  parameter Modelica.Units.SI.Temperature T "Fixed temperature";
  EnergyTraining.Interfaces.HeatPort port
    annotation (Placement(transformation(extent={{90,-10},{110,10}})));
equation
  port.T = T;
  annotation (
    Icon(graphics={Rectangle(extent={{-90,60},{90,-60}}, lineColor={0,0,255},
          fillColor={159,159,223}, fillPattern=FillPattern.Solid),
        Text(extent={{-150,110},{150,70}}, textString="%name")}),
    Documentation(info="<html>
<p>Session 3 teaching component. MSL equivalent:
<code>Modelica.Thermal.HeatTransfer.Sources.FixedTemperature</code>.</p>
<ul>
<li><b>Boundary:</b> an ideal reservoir (here the ambient) at the port.</li>
<li><b>Assumptions:</b> the reservoir is so large that any heat flow leaves its temperature unchanged.</li>
<li><b>Boundary condition / equation:</b> <code>port.T = T</code>; <code>port.Q_flow</code> is whatever
the connected components require.</li>
<li><b>States:</b> none. <b>Parameter:</b> <code>T</code> [K]. <b>Inputs/outputs:</b> none.</li>
<li><b>Units:</b> SI (K, W).</li>
</ul>
</html>"));
end FixedTemperature;
