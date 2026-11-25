package S04_G1_Fixes "G4.1: your fixes of the broken models in EnergyTraining.Examples.Broken"
  model MissingInitialCondition "Fix of Broken.MissingInitialCondition"
    extends EnergyTraining.Examples.Broken.MissingInitialCondition;
  // TODO: add what is missing (an extended model may add equations of any kind)
    annotation (experiment(StopTime=345600, Interval=600, Tolerance=1e-6));
  end MissingInitialCondition;

  model OverdeterminedInitialization "Fix of Broken.OverdeterminedInitialization"
    extends EnergyTraining.Examples.Broken.OverdeterminedInitialization;
    // TODO: a modifier in the extends clause can change an attribute of an inherited variable,
    //       for example: extends ...(T(start=290)). Which attribute must change here?
    annotation (experiment(StopTime=259200, Interval=600, Tolerance=1e-6));
  end OverdeterminedInitialization;

  model Thermostat "Fix of Broken.ChatteringThermostat: on/off heater with hysteresis"
    extends Modelica.Icons.Example;
    import SI = Modelica.Units.SI;
    parameter SI.HeatCapacity C = 1.0e7 "Zone heat capacity (illustrative)";
    parameter SI.ThermalConductance UA = 200 "Heat-loss conductance (illustrative)";
    parameter SI.Temperature T_amb = 273.15 "Ambient temperature (0 degC)";
    parameter SI.HeatFlowRate Q_max = 6000 "Heater power when on";
    parameter SI.Temperature T_set = 293.15 "Set point (20 degC)";
    parameter SI.TemperatureDifference bandwidth = 1 "Hysteresis band around T_set";
    SI.Temperature T(start=292.15, fixed=true, displayUnit="degC") "Zone temperature";
    SI.HeatFlowRate Q_flow "Heater power";
    Boolean heaterOn(start=true, fixed=true) "Heater state";
  equation
    // TODO: switch heaterOn off above T_set + bandwidth/2 and on below T_set - bandwidth/2
    //       (a when-equation with elsewhen), then set Q_flow from heaterOn.
    C*der(T) = Q_flow - UA*(T - T_amb);
    annotation (experiment(StopTime=86400, Interval=60, Tolerance=1e-6));
  end Thermostat;
end S04_G1_Fixes;
