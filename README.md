# MFT D1600 Autonomous Separator Lab

An agentic CFD and design-search repository for a **passive, compact D1600 stormwater particle separator**.

The current mission is not to produce a colorful CFD image. It is to produce a reproducible computational design study that compares a generic D1600 baseline with agent-generated passive internals and returns a defensible Pareto set for physical testing.

## Product thesis

```text
geometry + gravity + controlled hydraulics
instead of
pumps + continuous energy + moving parts + disposable filters
```

MFT publicly focuses on hydraulic control and treatment of stormwater, including compact separators targeting 63 µm particles. The exact D1600 geometry, flow envelope and proprietary product knowledge are not assumed here. They enter later through controlled inputs.

## Terminal states

### C1 — computational demonstration release: current mission

A specific immutable revision contains:

- a parameterized generic D1600 baseline and design family;
- pinned CFD/meshing/post-processing toolchain;
- verified geometry and mesh generation;
- converged baseline flow solutions across the agreed flow envelope;
- mesh-independence and mass-balance evidence;
- Lagrangian particle-grade efficiency for specified particle classes;
- overload and retained-sediment security proxies;
- automated design search producing a Pareto frontier;
- independent adversarial reviews;
- reproducible visualizations and an engineering report;
- an explicit physical hydraulic-test plan.

The project-level return gate is:

```bash
make demo-gate
```

### C2 — physically calibrated product-development loop: later

Hydraulic rig data calibrates or falsifies the CFD, after which the runtime searches the local design family again. C2 is not required to complete C1.

## Executable bootstrap already included

The repository contains a clearly labelled **reduced-order screening model**, not fake CFD. It calculates particle settling velocities, screens a generic D1600 parameter space and produces a preliminary Pareto set. This gives the agent an executable baseline and tests while OpenFOAM/Gmsh cases are built.

```bash
make check
make surrogate
make geometry-render
make cfd-renders
make status
make demo-gate
```

`make geometry-render` creates a high-resolution transparent cutaway at
`reports/generated/baseline-geometry-3d.png`. The image is generated directly
from `inputs/design-envelope.yaml`, so updated dimensions remain reproducible.

`make cfd-renders` adds two annotated, presentation-quality 3D decision-support
views at `reports/generated/cfd-*-preview-3d.png`. They combine the frozen
geometry, operating envelope, and reduced-order particle screening data. The
figures are deliberately marked as **pre-CFD analytical visualizations**: they
identify inlet-jet, short-circuiting, sump-shear, pressure-loss, and
particle-accounting questions for subsequent solver runs, but are not CFD or
product-performance evidence.

`make demo-gate` initially fails with the exact computational evidence still required. That failure is the agent's project work queue, not a stopping state.

## Start the agentic run

Open the repository in Scout/Sol and paste `agent/MASTER_PROMPT.md`.
