within EnergyTraining.Interfaces;
connector HeatPort "Teaching thermal connector: temperature (potential) and heat flow rate (flow)"
  Modelica.Units.SI.Temperature T "Port temperature";
  flow Modelica.Units.SI.HeatFlowRate Q_flow
    "Heat flow rate, positive when flowing into the component";
  annotation (
    Icon(graphics={Rectangle(extent={{-100,100},{100,-100}}, lineColor={191,0,0},
          fillColor={191,0,0}, fillPattern=FillPattern.Solid)}),
    Documentation(info="<html>
<p>Teaching connector of Session 3. It has the same two variables as
<code>Modelica.Thermal.HeatTransfer.Interfaces.HeatPort</code> (MSL 4.1.0) and exists only to show
what a connector is. From Session 3 onward the course models use the MSL connector.</p>
<ul>
<li><code>T</code>: potential (non-flow) variable. Connecting ports makes their temperatures equal.</li>
<li><code>Q_flow</code>: flow variable. Connecting ports makes the heat flow rates sum to zero
(Modelica Language Specification 3.7, section 9.2), which is the energy balance of the
connection point.</li>
</ul>
<p>Sign convention: <code>Q_flow</code> is positive when heat flows from outside into the
component that owns the port (as in MSL).</p>
</html>"));
end HeatPort;
