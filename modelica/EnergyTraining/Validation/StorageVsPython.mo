within EnergyTraining.Validation;
model StorageVsPython "M03 charging, compared with the Python model of Session 2"
  extends EnergyTraining.Examples.S04_StorageCharging;
  annotation (
    experiment(StopTime=10800, Interval=60, Tolerance=1e-8),
    Documentation(info="<html><p>Validation model, not teaching content. Case: M03 charging of
<code>Examples.S04_StorageCharging</code> (N = 10, 3 h). No new equations: system boundary,
assumptions, states, parameters, inputs, outputs, conservation equations, initial and boundary
conditions and units are those of the instantiated example (documented there and in
<code>EnergyTraining.Components.StorageTank</code>).</p>
<p>Pass criterion (course result checks): every node temperature within 1e-4 K of
<code>energy_training.simulation.storage.simulate</code> at every output point.</p></html>"));
end StorageVsPython;
