within EnergyTraining.Examples.Broken;
model DivisionByZero "Electric flow heater whose pump stops (deliberate error, G4.1 extension)"
  extends Modelica.Icons.Example;
  import SI = Modelica.Units.SI;
  parameter SI.SpecificHeatCapacity cp = 4184 "Specific heat capacity of water";
  parameter SI.HeatFlowRate Q_flow = 5000 "Heater power (always on)";
  parameter SI.Temperature T_in = 303.15 "Inlet temperature (30 degC)";
  parameter SI.MassFlowRate m_flow_nominal = 0.1 "Pump flow rate while the pump runs";
  parameter SI.Time t_stop = 1800 "Time at which the pump stops";
  SI.MassFlowRate m_flow "Mass flow rate through the heater";
  SI.Temperature T_out(displayUnit="degC") "Outlet temperature";
equation
  m_flow = if time < t_stop then m_flow_nominal else 0;
  T_out = T_in + Q_flow/(m_flow*cp);
  annotation (
    experiment(StopTime=3600, Interval=10, Tolerance=1e-6),
    Documentation(info="<html>
<p><b>Deliberately broken</b> (Session 4, G4.1 extension). Intended case: an electric heater on a
water flow, as at the inlet of the M03 tank; the pump stops after 30 min, the heater stays on.</p>
<ul>
<li><b>System boundary:</b> the water flowing through the heater.</li>
<li><b>Assumptions:</b> steady-state energy balance of the flow (no water stored in the
heater); constant <code>cp</code>; heater always on.</li>
<li><b>States:</b> none. <b>Parameters:</b> <code>cp</code> [J/(kg K)], <code>Q_flow</code> [W],
<code>T_in</code> [K], <code>m_flow_nominal</code> [kg/s], <code>t_stop</code> [s].</li>
<li><b>Inputs:</b> none (pump schedule inside the model). <b>Outputs:</b> <code>m_flow</code>,
<code>T_out</code>.</li>
<li><b>Conservation equation:</b> <code>m_flow cp (T_out - T_in) = Q_flow</code>.</li>
<li><b>Initial conditions:</b> none (no states).</li>
<li><b>Boundary conditions:</b> inlet temperature <code>T_in</code>; mass flow rate from the pump
schedule.</li>
<li><b>Units:</b> SI.</li>
</ul>
</html>"));
end DivisionByZero;
