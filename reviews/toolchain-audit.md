# C1-02 independent toolchain audit

## Scope and reviewer

An independent repository-analysis run audited the environment lock,
installation instructions, smoke script and retained smoke report.

## Result

**Pass — no open critical or high finding after disposition.**

- Ubuntu architecture, Python dependencies, Gmsh, OpenFOAM and ParaView are
  pinned to exact package versions.
- The retained smoke report records observed versions and successful process
  return codes.
- The smoke generates a non-empty mesh, invokes the OpenFOAM CLI in its runtime
  environment and starts ParaView under a virtual display.
- A malformed Gmsh input is rejected and a valid mesh is regenerated,
  satisfying failure detection and restoration.

The initial audit identified missing review/evidence records and a missing
negative control. The records now exist and the negative control is executable
in `scripts/toolchain_smoke.py`.

## Residual non-critical risk

The reproducibility route uses version-pinned Ubuntu packages rather than an
image digest. Repository availability can change; reproducing on another
distribution requires a new lock and sensitivity review.
