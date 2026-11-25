within ;
package EnergyTraining "Teaching library for the course Dynamic Modelling, Modelica and Techno-Economic Optimization of Energy Systems"
  extends Modelica.Icons.Package;

  annotation (
    uses(Modelica(version="4.1.0")),
    version="0.1.0-dev",
    Documentation(info="<html>
<p>Teaching library. Models in this package are written for <b>clarity</b>, not as
replacements for validated libraries (Modelica Standard Library, Buildings).
See <code>docs/model_lineage.md</code> for the canonical model family M01&ndash;M08.</p>
<ul>
<li><code>Components</code>: teaching components (thermal mass, storage, simple heat pump)</li>
<li><code>Systems</code>: assembled canonical systems</li>
<li><code>Controls</code>: rule-based operating strategies used in Session 5</li>
<li><code>Examples</code>: runnable experiments referenced by lessons</li>
<li><code>Validation</code>: models with a known answer, simulated automatically to check the installation and the library</li>
</ul>
</html>"));
end EnergyTraining;
