# C1 evidence matrix

The machine source of truth is `evidence/evidence-matrix.json`.

| ID | Criterion | Required evidence |
|---|---|---|
| C1-01 | Design envelope frozen | D1600 geometry, flow/particle envelope, constraints, objective definitions and independent review |
| C1-02 | Reproducible toolchain | Pinned OpenFOAM/Gmsh/ParaView/Python environment and smoke tests |
| C1-03 | Parametric geometry valid | Machine-generated baseline/design family, watertightness, physical groups, maintenance/manufacturing constraints |
| C1-04 | Mesh strategy verified | Quality thresholds, local refinement, three meshes, `checkMesh` and mesh-independence plan |
| C1-05 | Baseline hydraulics verified | All operating points, convergence, mass balance, head loss, residence/short-circuit metrics |
| C1-06 | Particle model verified | Particle properties, injection/accounting, boundary interactions and numerical sensitivity |
| C1-07 | Grade-efficiency envelope complete | 40/63/100/250 µm across approved flows with confidence/sensitivity evidence |
| C1-08 | Overload and sediment security assessed | Overload flow, near-bed shear/velocity and retained-particle/washout proxy |
| C1-09 | Mesh/model sensitivity passed | Mesh, turbulence, particle count, timestep and key-boundary sensitivity |
| C1-10 | Agentic experiment runtime verified | Case registry, retries, failure diagnosis, provenance, no reward from failed cases |
| C1-11 | Multi-objective search complete | Constrained campaign, Pareto frontier and reproducible candidate selection |
| C1-12 | Maintainability/manufacturability enforced | Access, blockage, minimum gaps, removable parts and D1600 envelope constraints |
| C1-13 | Visual/report artifacts reproducible | Automated figures, animations, tables and engineering report from release data |
| C1-14 | Physical validation plan complete | Scale/full-size rig, instrumentation, PSD, flow, sampling and CFD calibration plan |
| C1-15 | Final adversarial audit passed | Independent hydraulic/numerical/product/manufacturing critique resolved |
| C1-16 | Immutable release assembled | Revision, environment, case inventory and SHA-256 manifest |
