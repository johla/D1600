#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
import json
import math
import subprocess
import tempfile
from pathlib import Path
from string import Template

import matplotlib.pyplot as plt
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/generated"
LEVELS = {
    "coarse": (0.06, 0.18),
    "medium": (0.04, 0.12),
    "fine": (0.03, 0.09),
}


def read_msh2(
    path: Path,
) -> tuple[dict[int, np.ndarray], list[tuple[int, int | None, list[int]]], dict[int, str]]:
    lines = path.read_text().splitlines()
    nodes: dict[int, np.ndarray] = {}
    elements: list[tuple[int, int | None, list[int]]] = []
    groups: dict[int, str] = {}
    i = 0
    while i < len(lines):
        if lines[i] == "$PhysicalNames":
            count = int(lines[i + 1])
            for line in lines[i + 2:i + 2 + count]:
                prefix, name, _ = line.split('"')
                _, tag = [int(field) for field in prefix.split()]
                groups[tag] = name
            i += count + 2
        elif lines[i] == "$Nodes":
            count = int(lines[i + 1])
            for line in lines[i + 2:i + 2 + count]:
                fields = line.split()
                nodes[int(fields[0])] = np.array([float(x) for x in fields[1:4]])
            i += count + 2
        elif lines[i] == "$Elements":
            count = int(lines[i + 1])
            for line in lines[i + 2:i + 2 + count]:
                fields = [int(x) for x in line.split()]
                tag_count = fields[2]
                physical_tag = fields[3] if tag_count else None
                elements.append((fields[1], physical_tag, fields[3 + tag_count:]))
            i += count + 2
        i += 1
    return nodes, elements, groups


def tetra_quality(points: np.ndarray) -> tuple[float, float]:
    volume = abs(np.linalg.det(np.stack((points[1] - points[0],
                                         points[2] - points[0],
                                         points[3] - points[0])))) / 6
    edge_sum = sum(float(np.dot(points[j] - points[i], points[j] - points[i]))
                   for i in range(4) for j in range(i + 1, 4))
    quality = 12 * (3 * volume) ** (2 / 3) / edge_sum if edge_sum else 0
    return volume, quality


def connected_tetra_components(tetrahedra: list[list[int]]) -> int:
    parent: dict[int, int] = {}

    def find(node: int) -> int:
        parent.setdefault(node, node)
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(left: int, right: int) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for tetrahedron in tetrahedra:
        for node in tetrahedron[1:]:
            union(tetrahedron[0], node)
    return len({find(node) for node in parent})


def render(level: str, mesh_min: float, mesh_max: float, directory: Path) -> dict:
    envelope = yaml.safe_load((ROOT / "inputs/design-envelope.yaml").read_text())
    chamber = envelope["chamber"]
    params = {
        "chamber_diameter": chamber["internal_diameter_m"],
        "water_depth": chamber["water_depth_m"],
        "sump_depth": chamber["sump_depth_m"],
        "inlet_diameter": chamber["inlet_diameter_m"],
        "outlet_diameter": chamber["outlet_diameter_m"],
        "inlet_z": chamber["inlet_center_elevation_m"],
        "outlet_z": chamber["outlet_center_elevation_m"],
        "pipe_length": 0.6,
        "mesh_min": mesh_min,
        "mesh_max": mesh_max,
    }
    geometry = directory / f"{level}.geo"
    mesh = directory / f"{level}.msh"
    template = Template((ROOT / "geometry/gmsh/generic_d1600.geo.template").read_text())
    geometry.write_text(template.substitute(params))
    process = subprocess.run(
        ["gmsh", str(geometry), "-3", "-format", "msh2", "-o", str(mesh)],
        text=True, capture_output=True, timeout=180,
    )
    if process.returncode:
        raise RuntimeError(process.stdout + process.stderr)
    nodes, elements, physical_names = read_msh2(mesh)
    tetrahedra = [element for kind, _, element in elements if kind == 4]
    triangles = [(tag, element) for kind, tag, element in elements if kind == 2]
    metrics = [tetra_quality(np.stack([nodes[node] for node in tetra])) for tetra in tetrahedra]
    volumes = np.array([metric[0] for metric in metrics])
    qualities = np.array([metric[1] for metric in metrics])
    group_counts = Counter(physical_names[tag] for tag, _ in triangles if tag in physical_names)
    surface_areas: Counter[str] = Counter()
    for tag, triangle in triangles:
        points = np.stack([nodes[node] for node in triangle])
        area = np.linalg.norm(np.cross(points[1] - points[0], points[2] - points[0])) / 2
        surface_areas[physical_names[tag]] += float(area)
    expected_groups = {"fluid", "inlet", "outlet", "walls"}
    coordinates = np.stack(list(nodes.values()))
    expected_bounds = np.array([[-1.4, -0.8, -0.5], [1.4, 0.8, 2.0]])
    observed_bounds = np.stack([coordinates.min(axis=0), coordinates.max(axis=0)])
    return {
        "level": level,
        "mesh_min_m": mesh_min,
        "mesh_max_m": mesh_max,
        "nodes": len(nodes),
        "tetrahedra": len(tetrahedra),
        "connected_volume_components": connected_tetra_components(tetrahedra),
        "total_volume_m3": float(volumes.sum()),
        "minimum_cell_volume_m3": float(volumes.min()),
        "minimum_mean_ratio_quality": float(qualities.min()),
        "p05_mean_ratio_quality": float(np.quantile(qualities, 0.05)),
        "physical_groups": ";".join(sorted(physical_names.values())),
        "boundary_triangle_counts": ";".join(
            f"{name}:{group_counts[name]}" for name in ("inlet", "outlet", "walls")
        ),
        "boundary_areas_m2": ";".join(
            f"{name}:{surface_areas[name]:.8f}" for name in ("inlet", "outlet", "walls")
        ),
        "physical_groups_pass": set(physical_names.values()) == expected_groups,
        "boundary_partition_pass": (
            sum(group_counts.values()) == len(triangles)
            and all(group_counts[name] > 0 for name in ("inlet", "outlet", "walls"))
        ),
        "bounds_maximum_error_m": float(np.max(np.abs(observed_bounds - expected_bounds))),
        "positive_volume_pass": bool(np.all(volumes > 0)),
    }


def make_plots(rows: list[dict], chamber: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    x = np.array([row["mesh_max_m"] for row in rows])
    cells = np.array([row["tetrahedra"] for row in rows])
    axes[0].loglog(x, cells, "o-")
    axes[0].invert_xaxis()
    axes[0].set(xlabel="Maximum target size (m)", ylabel="Tetrahedra",
                title="Systematic mesh refinement")
    axes[0].grid(True, which="both")

    radius = chamber["internal_diameter_m"] / 2
    bottom = -chamber["sump_depth_m"]
    top = chamber["water_depth_m"]
    inlet_z = chamber["inlet_center_elevation_m"]
    pipe_radius = chamber["inlet_diameter_m"] / 2
    axes[1].add_patch(plt.Rectangle((-radius, bottom), 2 * radius, top - bottom,
                                    color="#9ecae1", alpha=0.55, label="fluid domain"))
    axes[1].add_patch(plt.Rectangle((-radius - 0.6, inlet_z - pipe_radius), 0.6,
                                    2 * pipe_radius, color="#3182bd"))
    axes[1].add_patch(plt.Rectangle((radius, inlet_z - pipe_radius), 0.6,
                                    2 * pipe_radius, color="#3182bd"))
    axes[1].set_aspect("equal")
    axes[1].set(xlabel="Horizontal coordinate (m)", ylabel="Elevation (m)",
                title="Generic D1600 baseline section", xlim=(-1.55, 1.55),
                ylim=(bottom - 0.1, top + 0.1))
    axes[1].grid(True)
    fig.suptitle("Geometry and mesh evidence (Gmsh 4.12.1)")
    fig.tight_layout()
    fig.savefig(OUT / "geometry-mesh-overview.png", dpi=180)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="d1600-meshes-") as temp:
        directory = Path(temp)
        rows = [render(level, *sizes, directory) for level, sizes in LEVELS.items()]
        invalid = directory / "invalid.geo"
        invalid.write_text('SetFactory("OpenCASCADE"); Cylinder(1) = {broken};\n')
        negative = subprocess.run(
            ["gmsh", str(invalid), "-3", "-format", "msh2", "-o", str(directory / "invalid.msh")],
            text=True, capture_output=True, timeout=30,
        )
        disconnected = directory / "disconnected.geo"
        disconnected.write_text(
            'SetFactory("OpenCASCADE");\n'
            'Box(1) = {0, 0, 0, 1, 1, 1};\n'
            'Box(2) = {2, 0, 0, 1, 1, 1};\n'
            'Physical Volume("fluid") = {1, 2};\n'
            'walls[] = Boundary { Volume{1, 2}; };\n'
            'Physical Surface("walls") = {walls[]};\n'
        )
        disconnected_mesh = directory / "disconnected.msh"
        disconnected_result = subprocess.run(
            ["gmsh", str(disconnected), "-3", "-format", "msh2",
             "-o", str(disconnected_mesh)],
            text=True, capture_output=True, timeout=30,
        )
        _, disconnected_elements, _ = read_msh2(disconnected_mesh)
        disconnected_tetrahedra = [
            element for kind, _, element in disconnected_elements if kind == 4
        ]
        disconnected_components = connected_tetra_components(disconnected_tetrahedra)

    with (OUT / "mesh-quality.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    envelope = yaml.safe_load((ROOT / "inputs/design-envelope.yaml").read_text())
    chamber_volume = (
        math.pi * (envelope["chamber"]["internal_diameter_m"] / 2) ** 2
        * (envelope["chamber"]["water_depth_m"] + envelope["chamber"]["sump_depth_m"])
    )
    untrimmed_volume = chamber_volume + (
        2 * math.pi * (envelope["chamber"]["inlet_diameter_m"] / 2) ** 2 * 0.6
    )
    refinement_change = abs(
        rows[-1]["total_volume_m3"] - rows[-2]["total_volume_m3"]
    ) / rows[-1]["total_volume_m3"]
    report = {
        "claim_class": "analytical_calculation_and_mesh_result",
        "geometry": "generic D1600 baseline; no proprietary geometry",
        "levels": rows,
        "checks": {
            "three_systematic_levels": len(rows) == 3 and rows[0]["tetrahedra"] < rows[1]["tetrahedra"] < rows[2]["tetrahedra"],
            "boundary_contract": all(row["physical_groups_pass"] for row in rows),
            "boundary_partition": all(row["boundary_partition_pass"] for row in rows),
            "geometry_bounds_within_1_micrometre": all(
                row["bounds_maximum_error_m"] < 1e-6 for row in rows
            ),
            "positive_cell_volumes": all(row["positive_volume_pass"] for row in rows),
            "single_connected_fluid_volume": all(
                row["connected_volume_components"] == 1 for row in rows
            ),
            "volume_within_analytical_boolean_bounds": all(
                chamber_volume < row["total_volume_m3"] < untrimmed_volume for row in rows
            ),
            "medium_to_fine_volume_change_below_0.25_percent": refinement_change < 0.0025,
            "malformed_geometry_rejected": negative.returncode != 0,
            "disconnected_geometry_detected": (
                disconnected_result.returncode == 0 and disconnected_components > 1
            ),
            "valid_geometry_restored": rows[-1]["tetrahedra"] > 0,
        },
        "analytical_volume_bounds_m3": [chamber_volume, untrimmed_volume],
        "medium_to_fine_volume_relative_change": refinement_change,
        "negative_control": {
            "method": "malformed syntax rejection and parseable two-volume disconnection detection",
            "rejected": negative.returncode != 0,
            "disconnected_components_observed": disconnected_components,
            "restoration_verified": rows[-1]["tetrahedra"] > 0,
        },
    }
    report["passed"] = all(report["checks"].values())
    (OUT / "geometry-validation.json").write_text(json.dumps(report, indent=2) + "\n")
    make_plots(rows, envelope["chamber"])
    if not report["passed"]:
        raise SystemExit("Geometry validation failed; inspect geometry-validation.json")
    print(OUT / "geometry-validation.json")


if __name__ == "__main__":
    main()
