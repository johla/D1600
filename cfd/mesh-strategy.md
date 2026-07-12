# Mesh strategy obligations

Create at least coarse, medium and fine meshes generated from the same geometry parameters and refinement logic.

Refine deliberately at:

- inlet jet and expansion;
- outlet entrance;
- baffle/shield edges and minimum gaps;
- recirculation and vortex core regions;
- sediment-zone and bottom shield;
- particle collection boundaries.

Report cell count, non-orthogonality, skewness, aspect ratio, failed checks and local cell sizes. Mesh independence must use integral results—head loss, mass balance, velocity/shear monitors and particle efficiency—not only residuals.
