within EnergyTraining.Examples;
model S04_SteadyStartStep
  "Session 4: M01 started in steady state, then a step in the ambient temperature (time event)"
  extends Modelica.Icons.Example;
  import SI = Modelica.Units.SI;
  parameter SI.HeatCapacity C = 1.0e7 "Heat capacity (illustrative)";
  parameter SI.ThermalConductance UA = 200 "Heat-loss conductance (illustrative)";
  parameter SI.HeatFlowRate Q_flow = 4000 "Heater power";
  parameter SI.Temperature T_amb_before = 273.15 "Ambient temperature before the step (0 degC)";
  parameter SI.Temperature T_amb_after = 263.15 "Ambient temperature after the step (-10 degC)";
  parameter SI.Time t_step = 86400 "Time of the step (24 h)";
  parameter SI.Temperature T0 = 283.15 "Initial temperature of the zone with a fixed start (10 degC)";
  SI.Temperature T_amb(displayUnit="degC") "Ambient temperature";
  SI.Temperature T_steady(displayUnit="degC") "Zone started in steady state";
  SI.Temperature T_fixed(displayUnit="degC") "Same zone started at T0";
initial equation
  der(T_steady) = 0 "steady-state start";
  T_fixed = T0 "fixed start";
equation
  T_amb = if time < t_step then T_amb_before else T_amb_after "time event at t_step";
  C*der(T_steady) = Q_flow - UA*(T_steady - T_amb);
  C*der(T_fixed) = Q_flow - UA*(T_fixed - T_amb);
  annotation (
    experiment(StopTime=259200, Interval=600, Tolerance=1e-6),
    Documentation(info="<html>
<p>Session 4: the M01 energy balance of Session 1, twice, with the same disturbance: the ambient
temperature drops by 10 K after 24 h. <code>T_steady</code> starts in equilibrium
(<code>der(T_steady) = 0</code>), so its response shows only the disturbance.
<code>T_fixed</code> starts at 10 &deg;C, so its initial transient and the response to the step
overlap. The condition <code>time &lt; t_step</code> depends on time only: by the language a <b>time
event</b>, which a tool may schedule in advance (OpenModelica 1.27.1 locates it by root finding,
as a state event; lesson &sect;4.4). Either way the integrator stops at the step and restarts. After <i>Cooling Revisited</i> in
<i>Modelica by Example</i> (Tiller), rewritten for M01.</p>
<ul>
<li><b>System boundary:</b> the zone (air and internal mass) as one node, as in M01; two copies
that differ only in their initial condition.</li>
<li><b>Assumptions:</b> those of M01: uniform temperature, constant <code>C</code> and
<code>UA</code>, ideal heater at constant power; ambient temperature as a step.</li>
<li><b>States:</b> <code>T_steady</code>, <code>T_fixed</code> [K].</li>
<li><b>Parameters:</b> <code>C</code> [J/K], <code>UA</code> [W/K] (illustrative, as in
Session 1), <code>Q_flow</code> [W], <code>T_amb_before</code>, <code>T_amb_after</code>,
<code>T0</code> [K], <code>t_step</code> [s].</li>
<li><b>Inputs:</b> none (the ambient temperature is a function of time). <b>Outputs:</b>
<code>T_steady</code>, <code>T_fixed</code>, <code>T_amb</code>.</li>
<li><b>Conservation equation:</b> <code>C der(T) = Q_flow - UA (T - T_amb)</code> for each copy.</li>
<li><b>Initial conditions:</b> <code>der(T_steady) = 0</code>, which gives
<code>T_steady = T_amb_before + Q_flow/UA</code> = 20 &deg;C; <code>T_fixed = T0</code>.</li>
<li><b>Boundary condition:</b> ambient temperature 0 &deg;C, -10 &deg;C from <code>t_step</code>.</li>
<li><b>Units:</b> SI.</li>
</ul>
</html>"));
end S04_SteadyStartStep;
