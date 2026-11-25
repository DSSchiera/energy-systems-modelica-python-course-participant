# Session 3 — optional advanced topics

- **Arrays of components.** Build an $N$-node wall from `HeatCapacitor[N]` and `ThermalConductor[N+1]`
  with a `for` loop of `connect` statements; *Modelica by Example* covers spatially distributed
  heat transfer `[src: modelica-by-example]`.
- **State space in Modelica.** Write M02 as `der(x) = A*x + B*u` with matrix parameters and
  compare it with the component model `[src: modelica-by-example]`.
- **Selective model extension.** Modelica 3.7 can remove an inherited element or connection
  (`extends B(break D)`, `break connect(a, b)`) instead of redeclaring it
  `[src: modelica-spec-3.7 §7.4]`.
- **Reading a CSV file into a table.** Replace the inline irradiance table of I3.1 by
  `CombiTimeTable` with `tableOnFile = true`, `tableName` and `fileName`, reading a text file
  written from Python `[src: msl-4.1.0]`.
