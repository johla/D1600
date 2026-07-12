# Terminal truth — C1 computational demonstration

## Exact proposition

Transform this repository into an independently reproducible computational engineering release demonstrating that an agentic runtime can search, simulate, falsify and rank passive internal geometries for a D1600 stormwater particle separator.

A competent engineer must be able to reproduce the release and answer:

1. What exact D1600 geometry and operating envelope were studied?
2. Do the flow solutions converge and conserve mass?
3. Are results insensitive enough to mesh refinement and solver choices?
4. What proportion of each specified particle class exits, settles or remains unresolved?
5. What happens at normal, design and overload flows?
6. Which geometries form the Pareto frontier for capture, head loss, sediment security, compactness and maintainability?
7. Which 2–3 candidates deserve physical hydraulic testing, and why?
8. What claims remain outside CFD evidence?

The project is complete only when `make demo-gate` exits 0 against one immutable release revision.

## Fixed scope

- Chamber nominal internal diameter: **1.600 m**.
- Passive operation: gravity and hydraulic geometry only.
- No pumps, powered moving parts or disposable filter media.
- Stormwater as the carrier phase.
- Target particle classes include **40, 63, 100 and 250 µm**.
- Generic, non-proprietary baseline until approved MFT inputs are supplied.
- Primary outputs: particle grade-efficiency curves, head loss, mass balance, residence/short-circuit metrics, sediment-zone shear proxy, maintainability constraints and Pareto candidates.

## Semantic closure

- **D1600** means a nominal 1.600 m internal chamber diameter unless a supplied manufacturing drawing states otherwise.
- **Baseline** means an explicitly parameterized generic chamber without undisclosed proprietary internals.
- **Captured particle** means the computational particle reaches a defined collection boundary and remains there under the model's interaction rules.
- **Escaped particle** means it crosses the outlet boundary.
- **Unresolved particle** means neither condition occurs within the specified tracking horizon; it must not be silently counted as captured.
- **Efficiency** means injected mass or count captured divided by injected mass or count, reported per particle class and operating point.
- **Sediment security** is a pre-fabrication proxy derived from near-bed velocity/shear and particle re-entrainment tests; it is not a certified washout claim.
- **Compact** means the design stays inside the D1600 envelope and obeys maintenance/manufacturing constraints.
- **CFD-verified** means geometry, mesh, solver, convergence, conservation, sensitivity and post-processing evidence all pass their defined criteria.
- **Demo-ready** means the complete reproducible study and report pass the machine evidence gate; it does not mean certified product performance.

## Initial computational envelope

The bootstrap uses provisional exploration values only:

- flow points: 10, 20, 40 and 80 L/s;
- overload point: 120 L/s;
- water depth: 2.0 m;
- inlet/outlet diameter: 0.30 m;
- particle density: 2650 kg/m³;
- water near 15 °C.

These are not MFT product claims. The agent must replace or ratify them through `inputs/design-envelope.yaml` before CFD freeze.

## Required C1 evidence

- Pinned toolchain and reproducible environment.
- Geometry generation from machine-readable parameters.
- Geometry validity and mesh-quality reports.
- Baseline CFD at all approved operating points.
- Residual, continuity and integral convergence evidence.
- At least three systematically refined meshes and a mesh-independence conclusion.
- Particle-tracking sensitivity to injection count, timestep/integration settings and turbulence dispersion assumptions.
- Grade-efficiency results for all particle/flow combinations.
- Head loss and hydraulic capacity.
- Overload run and sediment-security assessment.
- Automated design campaign with failed-run recovery and retained provenance.
- Pareto frontier and 2–3 physically testable candidates.
- Independent red-team reviews and resolved critical findings.
- Reproducible figures, animations and engineering report.
- Hydraulic physical-test plan for C2.

## What does not count

- a prompt, plan, literature review or architecture document;
- a reduced-order surrogate presented as CFD;
- one successful solver run;
- velocity contours without convergence and mass-balance evidence;
- particle tracks without complete injection/accounting statistics;
- a single particle diameter or flow rate presented as the general result;
- comparing designs on different meshes, models or boundary assumptions without justification;
- improving nominal capture while ignoring head loss, overload, resuspension or maintenance;
- treating particles still in the domain as captured;
- a mesh that merely passes `checkMesh` but lacks local adequacy/sensitivity evidence;
- an optimizer exploiting solver failures, coarse meshes or changed constraints;
- copied proprietary geometry without authorization;
- absolute product/certification claims based only on CFD;
- stopping after geometry, baseline CFD, optimization or report generation;
- reporting `BLOCKED` for a missing local tool before attempting installation, a container, HPC/remote execution or a viable equivalent route.

## Hard return gate

Return `DEMO_READY` only when:

```bash
make check
make demo-gate
```

both exit 0 and the final independent review has no unresolved critical/high finding.

Otherwise continue. Return `BLOCKED` only when an exact C1 criterion is impossible after materially different routes have been attempted and documented. A blocked result must identify the smallest external capability or protected MFT input required while continuing all independent work.
