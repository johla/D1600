# CFD workstream

The repository intentionally does not pretend that an unpinned OpenFOAM template is a validated case.

C1 requires the root agent to select an exact OpenFOAM distribution and create generated cases from `inputs/design-envelope.yaml` and design parameters. The case generator must control:

- boundaries and reference pressures;
- flow rate/velocity profile and turbulence quantities;
- turbulence model and wall treatment;
- solver controls and monitored integrals;
- particle injection, forces, dispersion and wall interaction;
- collection/outlet/unresolved accounting;
- consistent post-processing and provenance.

Start with hydraulics, then particles. Do not optimize against a case that has not passed convergence, conservation and mesh evidence.
