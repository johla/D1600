# Objectives and constraints

## Frozen generic demonstration envelope

`inputs/design-envelope.yaml` is frozen for the generic C1 computational
demonstration. Its dimensions, flow points, particle classes, weights, head-loss
limit and access constraints are assumptions chosen for an interrogable
non-proprietary experiment. They are not approved MFT product inputs or
performance claims. Any later protected/product envelope creates a new study
revision and invalidates direct reuse of these rankings.

## Multi-objective formulation

The runtime must preserve a Pareto set rather than collapse the problem prematurely into one opaque score.

Primary objectives:

- particle capture by diameter and flow;
- annual/weighted captured mass once a storm/PSD distribution is supplied;
- low head loss;
- low short-circuiting;
- low near-bed disturbance at overload;
- sufficient sediment storage and access;
- low geometric/manufacturing complexity.

Hard constraints:

- every solid stays within the D1600 chamber;
- minimum gaps and cleaning access pass;
- inlet/outlet remain unobstructed;
- no powered or moving components;
- head loss below the frozen limit;
- geometry and mesh generation succeed;
- solver and particle accounting pass evidence thresholds.

A candidate with a failed CFD case is infeasible, not high-performing. Missing particles are unresolved, not captured.
