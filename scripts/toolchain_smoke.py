#!/usr/bin/env python3
from __future__ import annotations

import importlib
import json
import platform
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/generated/toolchain-smoke.json"


def command_version(command: list[str], pattern: str | None = None) -> dict:
    result = subprocess.run(command, text=True, capture_output=True, timeout=30)
    text = (result.stdout + result.stderr).strip()
    match = re.search(pattern, text) if pattern else None
    version = match.group(1) if match else (text.splitlines()[0] if text else "unknown")
    return {
        "command": command,
        "return_code": result.returncode,
        "version": version,
        "passed": result.returncode == 0,
    }


def main() -> None:
    packages = {}
    for name in ("numpy", "scipy", "pandas", "matplotlib", "yaml"):
        module = importlib.import_module(name)
        packages[name] = getattr(module, "__version__", "bundled")

    checks = {
        "gmsh": command_version(["gmsh", "--version"]),
        "openfoam": command_version([
            "bash", "-lc",
            "source /usr/share/openfoam/etc/bashrc >/dev/null 2>&1 || true; simpleFoam -help",
        ]),
        "paraview": command_version(
            ["xvfb-run", "-a", "paraview", "--version"], r"paraview version\s+(\S+)"
        ),
    }
    # OpenFOAM 1912 prints an empty banner version but exposes its build in package metadata.
    package = subprocess.run(
        ["dpkg-query", "-W", "-f=${Version}", "openfoam"],
        text=True,
        capture_output=True,
        timeout=30,
    )
    checks["openfoam"]["version"] = package.stdout.strip()
    checks["openfoam"]["passed"] &= package.returncode == 0

    with tempfile.TemporaryDirectory(prefix="d1600-toolchain-") as temp:
        temp_path = Path(temp)
        mesh = Path(temp) / "smoke.msh"
        gmsh = subprocess.run(
            ["gmsh", str(ROOT / "geometry/generated/baseline-d1600.geo"), "-3",
             "-setnumber", "Mesh.CharacteristicLengthMin", "0.08",
             "-setnumber", "Mesh.CharacteristicLengthMax", "0.24",
             "-format", "msh2", "-o", str(mesh)],
            text=True, capture_output=True, timeout=120,
        )
        checks["gmsh_mesh_smoke"] = {
            "return_code": gmsh.returncode,
            "mesh_bytes": mesh.stat().st_size if mesh.exists() else 0,
            "passed": gmsh.returncode == 0 and mesh.exists() and mesh.stat().st_size > 0,
        }
        malformed = temp_path / "malformed.geo"
        malformed.write_text('SetFactory("OpenCASCADE"); Cylinder(1) = {broken};\n')
        rejected = subprocess.run(
            ["gmsh", str(malformed), "-3", "-format", "msh2",
             "-o", str(temp_path / "malformed.msh")],
            text=True, capture_output=True, timeout=30,
        )
        negative_control = {
            "method": "malformed Gmsh input must return nonzero",
            "failure_detected": rejected.returncode != 0,
            "restoration_verified": checks["gmsh_mesh_smoke"]["passed"],
        }

    report = {
        "claim_class": "review_result",
        "platform": platform.platform(),
        "python": platform.python_version(),
        "python_packages": packages,
        "checks": checks,
        "negative_control": negative_control,
        "passed": (
            all(item["passed"] for item in checks.values())
            and negative_control["failure_detected"]
            and negative_control["restoration_verified"]
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    if not report["passed"]:
        raise SystemExit("Toolchain smoke failed; inspect reports/generated/toolchain-smoke.json")
    print(OUT)


if __name__ == "__main__":
    main()
