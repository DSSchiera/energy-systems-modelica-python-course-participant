within EnergyTraining.Examples;
model S04_TwoCapacities "Session 4: two heat capacities connected directly have one state"
  extends Modelica.Icons.Example;
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor air(
    C=1.0e6, T(start=293.15, fixed=true)) "Zone air (illustrative capacity)"
    annotation (Placement(transformation(extent={{-50,0},{-30,20}})));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor furniture(C=4.0e6)
    "Furniture and internal walls, at the air temperature (illustrative capacity)"
    annotation (Placement(transformation(extent={{-10,0},{10,20}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor loss(G=200)
    "Envelope (illustrative, as M01)"
    annotation (Placement(transformation(extent={{20,-20},{40,0}})));
  Modelica.Thermal.HeatTransfer.Sources.FixedTemperature ambient(T=273.15) "Outdoor air"
    annotation (Placement(transformation(extent={{80,-20},{60,0}})));
equation
  connect(air.port, furniture.port)
    annotation (Line(points={{-40,0},{0,0}}, color={191,0,0}));
  connect(furniture.port, loss.port_a)
    annotation (Line(points={{0,0},{0,-10},{20,-10}}, color={191,0,0}));
  connect(loss.port_b, ambient.port)
    annotation (Line(points={{40,-10},{60,-10}}, color={191,0,0}));
  annotation (
    experiment(StopTime=259200, Interval=600, Tolerance=1e-6),
    Documentation(info="<html>
<p>Session 4: two heat capacities connected to the same port, without a resistance between
them. The connection makes their temperatures equal, so the two equations
<code>C der(T) = port.Q_flow</code> describe one degree of freedom: the compiler keeps one state
(<code>-d=backenddaeinfo</code> reports it) and computes the other temperature from it. Giving
<b>both</b> start values <code>fixed=true</code> over-specifies the initial conditions.</p>
<ul>
<li><b>System boundary:</b> zone air and furniture, at one temperature.</li>
<li><b>Assumptions:</b> perfect thermal contact between air and furniture; one conductance to
the outdoor air; no heater.</li>
<li><b>States:</b> one temperature (two <code>der</code> operators).</li>
<li><b>Parameters:</b> capacities <code>air.C</code>, <code>furniture.C</code> [J/K],
<code>loss.G</code> [W/K] (illustrative), <code>ambient.T</code> [K].</li>
<li><b>Inputs:</b> none. <b>Outputs:</b> <code>air.T</code> = <code>furniture.T</code> [K].</li>
<li><b>Conservation equation:</b> (C_air + C_furniture) der(T) = -G (T - T_amb) after
elimination.</li>
<li><b>Initial condition:</b> <code>air.T</code> = 20 &deg;C.</li>
<li><b>Boundary conditions:</b> outdoor air at 0 &deg;C (<code>ambient</code>).</li>
<li><b>Units:</b> SI.</li>
</ul>
</html>"));
end S04_TwoCapacities;
