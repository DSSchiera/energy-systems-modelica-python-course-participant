within EnergyTraining.Systems;
model ZoneRC "M02: two-node (2R2C) zone, M01 with the envelope redeclared as a capacity between two resistances"
  extends EnergyTraining.Systems.ThermalZone(
    final C=C_z,
    final UA=1/(R_ze + R_ea),
    final T_start=T_z_start,
    redeclare EnergyTraining.Components.EnvelopeRC envelope(
      final C_e=C_e, final R_ze=R_ze, final R_ea=R_ea, final T_e_start=T_e_start));
  parameter Modelica.Units.SI.HeatCapacity C_z = 1.07*3.6e6
    "Heat capacity of the zone node (Bacher and Madsen 2011, Table 3: 1.07 kWh/K)";
  parameter Modelica.Units.SI.HeatCapacity C_e = 2.92*3.6e6
    "Heat capacity of the envelope node (Bacher and Madsen 2011, Table 3: 2.92 kWh/K)";
  parameter Modelica.Units.SI.ThermalResistance R_ze = 0.863e-3
    "Thermal resistance zone to envelope (Bacher and Madsen 2011, Table 3: 0.863 K/kW)";
  parameter Modelica.Units.SI.ThermalResistance R_ea = 4.54e-3
    "Thermal resistance envelope to ambient (Bacher and Madsen 2011, Table 3: 4.54 K/kW)";
  parameter Modelica.Units.SI.Temperature T_z_start = 293.15 "Initial zone temperature";
  parameter Modelica.Units.SI.Temperature T_e_start = 293.15 "Initial envelope temperature";
  Modelica.Units.SI.Temperature T_e = envelope.T_e "Envelope temperature";
  annotation (Documentation(info="<html>
<p><b>M02 ZoneRC</b> (course model lineage), the Modelica version of
<code>energy_training.simulation.zone_rc</code> (Session 2). Structure: deterministic part of
the two-state model of Bacher and Madsen (2011), without solar gains.</p>
<p>Built by <b>extending</b> M01 and <b>redeclaring</b> its envelope: the single conductance of
M01 is replaced by <code>EnvelopeRC</code>. <code>UA</code> is set to
<code>1/(R_ze + R_ea)</code>, the steady-state conductance of the two resistances in series; it
is not used by the redeclared envelope.</p>
<ul>
<li><b>System boundary:</b> building envelope.</li>
<li><b>Assumptions:</b> two lumped nodes with constant capacities, linear resistances, heater on
the zone node, no direct zone-to-ambient path, no solar gains.</li>
<li><b>States:</b> <code>zone.T</code> = T_z, <code>envelope.mass.T</code> = T_e [K].</li>
<li><b>Parameters:</b> <code>C_z</code>, <code>C_e</code> [J/K]; <code>R_ze</code>,
<code>R_ea</code> [K/W] (defaults: Bacher and Madsen 2011, Table 3, 120 m&sup2; house);
<code>T_z_start</code>, <code>T_e_start</code> [K].</li>
<li><b>Inputs:</b> <code>Q_flow</code> [W], <code>T_amb</code> [K]. <b>Output:</b> <code>T</code> = T_z [K].</li>
<li><b>Conservation equations:</b>
<code>C_z der(T_z) = (T_e - T_z)/R_ze + Q_flow</code>;
<code>C_e der(T_e) = (T_z - T_e)/R_ze + (T_amb - T_e)/R_ea</code>.</li>
<li><b>Initial conditions:</b> <code>T_z = T_z_start</code>, <code>T_e = T_e_start</code>.</li>
<li><b>Units:</b> SI.</li>
</ul>
</html>"));
end ZoneRC;
