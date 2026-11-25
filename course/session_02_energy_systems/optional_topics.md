# Session 2 — optional advanced topics

- **More nodes in the building model.** Bacher & Madsen add heater, sensor and medium nodes and
  select among models with likelihood-ratio tests `[src: bacher-madsen-2011]`.
- **Solar gains.** Add $A_w\,\Phi_s$ to the zone node and $A_e\,\Phi_s$ to the envelope node, as in
  the source model `[src: bacher-madsen-2011]`.
- **Effective conductivity and mixing in tanks.** Real tanks lose stratification by conduction in
  the water and the wall and by inlet mixing; library tanks model these and correct numerical
  dissipation `[src: buildings-14.0.0]`.
- **Variable properties.** Over 20–80 °C the density of water changes by a few percent; the course
  keeps constant properties like `Buildings.Media.Water` `[src: buildings-14.0.0]`.
- **Heat exchanger dynamics.** Give the exchanger walls and fluid hold-up a capacity and compare
  with the ε-NTU result during a step in the flow.
