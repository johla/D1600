# Reproducible environment

The bootstrap Python surrogate runs in the current environment. C1 requires a pinned container or reproducible installation containing:

- OpenFOAM distribution/version;
- Gmsh;
- ParaView/pvpython;
- Python and locked dependencies;
- optional optimization libraries;
- exact OS/container image digest.

The root agent must choose and smoke-test the toolchain rather than mixing OpenFOAM distributions silently.
