model S03_G1_ZoneRC "G3.1: M02 composed from Modelica Standard Library thermal components (starting file)"
  extends Modelica.Icons.Example;
  // M02 parameters: Bacher and Madsen (2011), Table 3, converted to SI
  parameter Modelica.Units.SI.HeatCapacity C_z = 1.07*3.6e6 "Zone node";
  parameter Modelica.Units.SI.HeatCapacity C_e = 2.92*3.6e6 "Envelope node";
  parameter Modelica.Units.SI.ThermalResistance R_ze = 0.863e-3 "Zone to envelope";
  parameter Modelica.Units.SI.ThermalResistance R_ea = 4.54e-3 "Envelope to ambient";
  // Session 2 guided example: equilibrium at 1 kW, heater at 4 kW from t = 0, 0 degC outside
  parameter Modelica.Units.SI.HeatFlowRate Q_before = 1000 "Heater power before the step";
  parameter Modelica.Units.SI.HeatFlowRate Q_after = 4000 "Heater power from t = 0";
  parameter Modelica.Units.SI.Temperature T_amb = 273.15 "Ambient temperature";

  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor zone(
    C=C_z, T(start=T_amb + Q_before*(R_ze + R_ea), fixed=true)) "Zone node";
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor envelope(
    C=C_e, T(start=T_amb + Q_before*R_ea, fixed=true)) "Envelope node";
  // TODO 1: declare the two conductances (Modelica.Thermal.HeatTransfer.Components.ThermalConductor),
  //         the heater (Modelica.Thermal.HeatTransfer.Sources.FixedHeatFlow) and the ambient
  //         (Modelica.Thermal.HeatTransfer.Sources.FixedTemperature).
equation
  // TODO 2: connect the components so that the network is the M02 schematic of Session 2.
  annotation (experiment(StopTime=345600, Interval=600, Tolerance=1e-8));
end S03_G1_ZoneRC;
