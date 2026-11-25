within EnergyTraining.Components;
model ThermalMass "Teaching component: lumped heat capacity, C der(T) = port.Q_flow"
  parameter Modelica.Units.SI.HeatCapacity C "Heat capacity";
  parameter Modelica.Units.SI.Temperature T_start "Initial temperature";
  Modelica.Units.SI.Temperature T(start=T_start, fixed=true) "Temperature of the mass";
  EnergyTraining.Interfaces.HeatPort port
    annotation (Placement(transformation(extent={{-10,-110},{10,-90}})));
equation
  T = port.T;
  C*der(T) = port.Q_flow;
  annotation (
    Icon(graphics={Ellipse(extent={{-70,70},{70,-70}}, lineColor={191,0,0},
          fillColor={255,170,85}, fillPattern=FillPattern.Solid),
        Text(extent={{-150,120},{150,80}}, textString="%name")}),
    Documentation(info="<html>
<p>Session 3 teaching component, written with the teaching connector
<code>EnergyTraining.Interfaces.HeatPort</code>. MSL equivalent:
<code>Modelica.Thermal.HeatTransfer.Components.HeatCapacitor</code>.</p>
<ul>
<li><b>Boundary:</b> the lumped body; heat enters only through <code>port</code>.</li>
<li><b>Assumptions:</b> uniform temperature, constant heat capacity.</li>
<li><b>State:</b> <code>T</code> [K]. <b>Parameters:</b> <code>C</code> [J/K], <code>T_start</code> [K].</li>
<li><b>Equation:</b> energy balance <code>C der(T) = port.Q_flow</code> (heat flow positive into the mass).</li>
<li><b>Initial condition:</b> <code>T = T_start</code> (<code>fixed=true</code>).</li>
<li><b>Inputs/outputs:</b> none (heat port only). <b>Units:</b> SI.</li>
</ul>
</html>"));
end ThermalMass;
