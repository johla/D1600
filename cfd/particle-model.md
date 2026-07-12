# Particle-model obligations

Initial route: dilute one-way Lagrangian particle tracking.

Must define and test:

- particle density, diameters and shape assumption;
- injection spatial/velocity distribution and duration;
- drag and gravity/buoyancy;
- turbulent dispersion model;
- timestep/integration controls;
- wall rebound/stick/escape rules;
- collection and outlet boundaries;
- tracking horizon and unresolved classification;
- count/mass weighting and random-seed repeatability.

Sensitivity must include injection count, random seed, timestep/integration and at least one alternative wall/dispersion assumption. CFD-only capture is not a certification claim.
