within EnergyTraining.Validation;
model ZoneRCvsPython "M02 heater step, compared with the Python model of Session 2"
  extends EnergyTraining.Examples.S03_ZoneRCStep;
  annotation (
    experiment(StopTime=345600, Interval=600, Tolerance=1e-8),
    Documentation(info="<html><p>Validation model, not teaching content. Case: M02 heater step of <code>Examples.S03_ZoneRCStep</code> (96 h). No new equations:
the models, states, parameters and units are those of the instantiated examples.</p>
<p>Pass criterion (course result checks): <code>zone.T</code> and <code>zone.T_e</code> within 1e-4 K of
<code>energy_training.simulation.zone_rc.simulate</code> at every output point.</p></html>"));
end ZoneRCvsPython;
