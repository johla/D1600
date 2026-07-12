# Reproducible environment

The generic C1 study is pinned to Ubuntu 24.04 amd64 packages. Install the
system tools and Python environment with:

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  gmsh=4.12.1+ds1-1.1build2 \
  openfoam=1912.200626-2build3 \
  paraview=5.11.2+dfsg-6build5
python -m pip install -r requirements.txt
make toolchain-smoke
```

`environment/toolchain-lock.yaml` is the machine-readable lock. The smoke test
imports every Python dependency, executes Gmsh, loads the OpenFOAM command-line
environment and starts ParaView under a virtual display. The generated JSON
records observed versions and a small mesh-generation result.

The Ubuntu packages are pinned rather than a container image. Reproduction on
another distribution requires a new lock and sensitivity review; silently
mixing OpenFOAM distributions is not supported.
