# Approach registry

| ID | Crux | Route | Mechanism | Principal risk | Verification | Status |
|---|---|---|---|---|---|---|
| R-01 | Geometry | Gmsh/OpenCASCADE parametric solids | scripted booleans and physical groups | fragile booleans/small gaps | geometry validity + mesh smoke tests | ACTIVE |
| R-02 | Geometry | CadQuery/OpenCASCADE | Python parametric CAD and STEP export | package availability/meshing handoff | containerized smoke test and STEP comparison | CANDIDATE |
| R-03 | Flow | steady incompressible RANS baseline | economical design screening | misses unsteady vortex/short-circuit behavior | compare selected cases to transient URANS | ACTIVE |
| R-04 | Flow | transient URANS throughout | resolves unsteadiness | expensive optimization loop | convergence/cost/value comparison | CANDIDATE |
| R-05 | Particles | one-way Lagrangian tracking | dilute PSD, explicit trajectories | turbulence dispersion/wall interaction uncertainty | count/timestep/model sensitivity | ACTIVE |
| R-06 | Particles | Eulerian scalar/settling classes | robust concentration fields | numerical diffusion and less trajectory detail | benchmark against Lagrangian cases | CANDIDATE |
| R-07 | Sediment security | near-bed shear + reinjection proxy | screens washout risk | not a cohesive-bed model | overload sensitivity + physical-test plan | ACTIVE |
| R-08 | Sediment security | coupled CFD-DEM/bed model | richer resuspension physics | cost/calibration/parameter uncertainty | only reopen after C1 evidence demands | BLOCKED |
| R-09 | Search | surrogate-assisted multi-objective optimization | reduced CFD calls | surrogate exploitation | holdout CFD validation and failed-run penalties | ACTIVE |
| R-10 | Search | evolutionary direct CFD search | simple objective truth | large compute cost | pilot budget comparison | CANDIDATE |

Update routes with concrete evidence and reopen conditions. Do not retain a route merely because it was selected first.
