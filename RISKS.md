# Risk register

| ID | Risk | Consequence | Detection | Mitigation | Gate |
|---|---|---|---|---|---|
| K-001 | Generic geometry solves the wrong MFT problem | impressive but irrelevant demo | design-envelope review | MFT owner supplies constraints, not necessarily proprietary CAD | C1-01 |
| K-002 | RANS misses dominant unsteady vortex behavior | wrong rankings | transient comparison | URANS selected cases and route switch | C1-05/C1-09 |
| K-003 | Particle-wall interaction overstates capture | false efficiency | accounting/model sensitivity | conservative wall rules and physical plan | C1-06/C1-14 |
| K-004 | 63 µm sediment is non-spherical/cohesive | absolute claims invalid | model limitation review | PSD/density/shape sensitivity; no certification claim | C1-06 |
| K-005 | Mesh passes quality but misses jets/gaps | false convergence | local and mesh sensitivity | three meshes and monitored integrals | C1-04/C1-09 |
| K-006 | Optimizer exploits solver failures/coarse cases | bogus Pareto front | runtime red-team | failed cases penalized, holdout high-fidelity reruns | C1-10/C1-11 |
| K-007 | Sediment washout proxy is too weak | unsafe candidate | overload review | reinjection cases and C2 hydraulic test | C1-08/C1-14 |
| K-008 | Maintainability omitted | unbuildable/unserviceable geometry | constraint checker | hard clearances/access/removability | C1-12 |
| K-009 | Proprietary design/IP copied | legal/trust harm | source audit | clean generic baseline and private input isolation | always |
| K-010 | Compute cost overwhelms small-company workflow | demo not reusable | campaign telemetry | fidelity ladder, caching and surrogate-assisted search | C1-10 |
