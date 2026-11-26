within EnergyTraining.Validation;
model ThermalZoneForms
  "M01 in four forms (equations, teaching components, MSL components, block diagram) against the analytic solution"
  extends Modelica.Icons.Example;
  EnergyTraining.Examples.S03_ThermalZoneEquations equations "M01 as one equation";
  EnergyTraining.Examples.S03_ThermalZoneTeaching teaching "M01 from teaching components";
  EnergyTraining.Examples.S03_ThermalZoneMSL msl "M01 from MSL components";
  EnergyTraining.Examples.S03_ThermalZoneBlocks blocks "M01 as a block diagram";
  Real err_equations(unit="K") = abs(equations.T - equations.T_exact);
  Real err_teaching(unit="K") = abs(teaching.zone.T - equations.T_exact);
  Real err_msl(unit="K") = abs(msl.zone.T - equations.T_exact);
  Real err_blocks(unit="K") = abs(blocks.zone.y - equations.T_exact);
  annotation (
    experiment(StopTime=259200, Interval=600, Tolerance=1e-8),
    Documentation(info="<html><p>Validation model, not teaching content. Case: M01 as equation, teaching components, MSL components and block diagram, Session 1 guided example (72 h). No new equations:
the models, states, parameters and units are those of the instantiated examples.</p>
<p>Pass criterion (course result checks): every error below 1e-4 K over 72 h.</p></html>"));
end ThermalZoneForms;
