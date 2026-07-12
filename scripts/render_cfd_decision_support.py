#!/usr/bin/env python3
"""Render annotated pre-CFD decision-support views from the frozen design envelope."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import yaml
from matplotlib import colormaps
from mpl_toolkits.mplot3d.art3d import Line3DCollection

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "reports/generated"
HYDRAULICS_NAME = "cfd-hydraulics-preview-3d.png"
PARTICLES_NAME = "cfd-particle-preview-3d.png"

BACKGROUND = "#07111d"
PANEL = "#0b1928"
TEXT = "#f3f8fb"
MUTED = "#91a8b7"
CYAN = "#65dcff"
ORANGE = "#ff9f43"


def load_case(envelope_path: Path, surrogate_path: Path, flow_lps: float) -> dict:
    """Load geometry, operating-point, and explicitly labelled surrogate values."""
    envelope = yaml.safe_load(envelope_path.read_text())
    chamber = envelope["chamber"]
    fluid = envelope["fluid"]
    q = flow_lps / 1000
    pipe_area = math.pi * chamber["inlet_diameter_m"] ** 2 / 4

    particle_rows = []
    with surrogate_path.open(newline="") as stream:
        for row in csv.DictReader(stream):
            if row["design"] == "generic_baseline" and float(row["flow_lps"]) == flow_lps:
                particle_rows.append(
                    {
                        "diameter_um": float(row["particle_um"]),
                        "settling_velocity_m_s": float(row["settling_velocity_m_s"]),
                        "capture_proxy": float(row["capture_proxy"]),
                    }
                )
    if not particle_rows:
        raise ValueError(f"No generic-baseline surrogate rows for {flow_lps:g} L/s")

    return {
        "radius": chamber["internal_diameter_m"] / 2,
        "bottom": -chamber["sump_depth_m"],
        "top": chamber["water_depth_m"],
        "pipe_radius": chamber["inlet_diameter_m"] / 2,
        "pipe_length": chamber["pipe_length_m"],
        "inlet_z": chamber["inlet_center_elevation_m"],
        "outlet_z": chamber["outlet_center_elevation_m"],
        "flow_lps": flow_lps,
        "inlet_velocity_m_s": q / pipe_area,
        "volume_m3": math.pi * (chamber["internal_diameter_m"] / 2) ** 2
        * (chamber["water_depth_m"] + chamber["sump_depth_m"]),
        "density_kg_m3": fluid["density_kg_m3"],
        "particles": sorted(particle_rows, key=lambda row: row["diameter_um"]),
    }


def _style_3d(axis, case: dict, *, azimuth: float = -58) -> None:
    radius = case["radius"]
    extent = radius + case["pipe_length"] + 0.08
    axis.set(
        xlim=(-extent, extent),
        ylim=(-radius * 1.08, radius * 1.08),
        zlim=(case["bottom"] - 0.04, case["top"] + 0.08),
    )
    axis.set_box_aspect((2 * extent, 1.7 * radius, case["top"] - case["bottom"]))
    axis.set_axis_off()
    axis.set_proj_type("persp", focal_length=0.88)
    axis.view_init(elev=22, azim=azimuth)
    axis.set_facecolor(BACKGROUND)


def _draw_shell(axis, case: dict) -> None:
    radius = case["radius"]
    theta = np.linspace(0.17 * np.pi, 1.83 * np.pi, 100)
    z = np.linspace(case["bottom"], case["top"], 34)
    theta_grid, z_grid = np.meshgrid(theta, z)
    axis.plot_surface(
        radius * np.cos(theta_grid),
        radius * np.sin(theta_grid),
        z_grid,
        color="#8cb4c8",
        alpha=0.10,
        linewidth=0,
        shade=True,
    )
    ring = np.linspace(0, 2 * np.pi, 180)
    for elevation, alpha in ((case["bottom"], 0.4), (case["top"], 0.75)):
        axis.plot(
            radius * np.cos(ring),
            radius * np.sin(ring),
            np.full_like(ring, elevation),
            color="#c8dce5",
            alpha=alpha,
            linewidth=1.2,
        )

    for start, stop, elevation, color in (
        (-radius - case["pipe_length"], -radius, case["inlet_z"], ORANGE),
        (radius, radius + case["pipe_length"], case["outlet_z"], CYAN),
    ):
        x = np.linspace(start, stop, 20)
        angle = np.linspace(0, 2 * np.pi, 36)
        x_grid, angle_grid = np.meshgrid(x, angle)
        axis.plot_surface(
            x_grid,
            case["pipe_radius"] * np.cos(angle_grid),
            elevation + case["pipe_radius"] * np.sin(angle_grid),
            color=color,
            alpha=0.32,
            linewidth=0,
        )


def _flow_lines(case: dict) -> list[tuple[np.ndarray, np.ndarray]]:
    """Create deterministic analytical paths and local speed proxies for visualization."""
    radius = case["radius"]
    inlet_velocity = case["inlet_velocity_m_s"]
    paths = []
    for index in range(34):
        t = np.linspace(0, 1, 150)
        phase = 2 * np.pi * index / 34
        radial = radius * (0.18 + 0.66 * ((index % 7) / 6))
        x = (radius + case["pipe_length"]) * (2 * t - 1)
        window = np.sin(np.pi * t) ** 1.25
        y = radial * np.sin(phase + 1.15 * np.pi * t) * window
        z_seed = case["inlet_z"] + 0.11 * np.sin(phase)
        z = z_seed - (0.22 + 0.20 * radial / radius) * window + 0.04 * np.sin(
            phase + 2 * np.pi * t
        )
        speed = inlet_velocity * (
            0.16 + 0.84 * (np.exp(-12 * t) + np.exp(-12 * (1 - t)))
        )
        speed += inlet_velocity * 0.12 * np.cos(phase) ** 2 * window
        paths.append((np.column_stack((x, y, z)), speed))
    return paths


def _add_header(figure, title: str, subtitle: str, flow_lps: float) -> None:
    figure.text(0.045, 0.94, title, color=TEXT, fontsize=24, fontweight="bold")
    figure.text(0.046, 0.905, subtitle, color=MUTED, fontsize=11)
    figure.text(
        0.955,
        0.94,
        f"GENERIC D1600  ·  {flow_lps:g} L/s",
        color=CYAN,
        fontsize=10,
        fontweight="bold",
        ha="right",
    )


def _add_evidence_banner(figure) -> None:
    figure.text(
        0.5,
        0.025,
        "PRE-CFD ANALYTICAL VISUALIZATION  ·  NOT SOLVER, CONVERGENCE, OR PRODUCT-PERFORMANCE EVIDENCE",
        color="#ffcc80",
        fontsize=9,
        fontweight="bold",
        ha="center",
        bbox={"boxstyle": "round,pad=0.55", "facecolor": "#2b2115", "edgecolor": "#785d2e"},
    )


def render_hydraulics(case: dict, output: Path, dpi: int = 220) -> Path:
    figure = plt.figure(figsize=(16, 9), facecolor=BACKGROUND)
    main = figure.add_axes((0.025, 0.08, 0.72, 0.80), projection="3d")
    _style_3d(main, case)
    _draw_shell(main, case)

    cmap = colormaps["turbo"]
    vmax = case["inlet_velocity_m_s"]
    for points, speed in _flow_lines(case):
        segments = np.stack((points[:-1], points[1:]), axis=1)
        collection = Line3DCollection(
            segments,
            cmap=cmap,
            norm=plt.Normalize(0, vmax),
            linewidth=1.5,
            alpha=0.82,
        )
        collection.set_array(speed[:-1])
        main.add_collection3d(collection)

    main.text(-1.35, -0.08, 1.82, "INLET\njet", color=ORANGE, fontsize=9, fontweight="bold")
    main.text(0.88, -0.05, 1.82, "OUTLET", color=CYAN, fontsize=9, fontweight="bold")
    main.text(-0.25, -0.72, -0.37, "LOW-ENERGY\nSUMP", color="#94b7c5", fontsize=8)

    panel = figure.add_axes((0.76, 0.10, 0.205, 0.75), facecolor=PANEL)
    panel.set_axis_off()
    q = case["flow_lps"] / 1000
    residence = case["volume_m3"] / q
    dynamic_head = case["inlet_velocity_m_s"] ** 2 / (2 * 9.81)
    metrics = (
        ("INLET VELOCITY", f"{case['inlet_velocity_m_s']:.2f} m/s"),
        ("VELOCITY HEAD", f"{dynamic_head * 1000:.1f} mm"),
        ("WET VOLUME", f"{case['volume_m3']:.2f} m³"),
        ("NOMINAL V/Q", f"{residence:.0f} s"),
    )
    panel.text(0.08, 0.94, "OPERATING POINT", transform=panel.transAxes, color=TEXT,
               fontsize=12, fontweight="bold")
    for index, (label, value) in enumerate(metrics):
        y = 0.83 - index * 0.15
        panel.text(0.08, y, label, transform=panel.transAxes, color=MUTED, fontsize=8)
        panel.text(0.08, y - 0.06, value, transform=panel.transAxes, color=TEXT,
                   fontsize=17, fontweight="bold")
    panel.text(0.08, 0.22, "DECISION CUES", transform=panel.transAxes, color=TEXT,
               fontsize=11, fontweight="bold")
    panel.text(
        0.08,
        0.16,
        "• Resolve inlet-jet decay\n• Quantify short circuiting\n• Verify sump shear\n• Compare pressure loss",
        transform=panel.transAxes,
        color="#bfd0d9",
        fontsize=9,
        linespacing=1.65,
        va="top",
    )

    scalar = plt.cm.ScalarMappable(norm=plt.Normalize(0, vmax), cmap=cmap)
    color_axis = figure.add_axes((0.10, 0.105, 0.38, 0.018))
    colorbar = figure.colorbar(scalar, cax=color_axis, orientation="horizontal")
    colorbar.set_label("Analytical local velocity proxy (m/s)", color=MUTED, fontsize=8)
    colorbar.ax.tick_params(colors=MUTED, labelsize=8)
    colorbar.outline.set_edgecolor("#486173")

    _add_header(
        figure,
        "HYDRAULIC FLOW FIELD · 3D CUTAWAY",
        "Velocity-scaled analytical paths identify the regions CFD must resolve",
        case["flow_lps"],
    )
    _add_evidence_banner(figure)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=dpi, facecolor=BACKGROUND)
    plt.close(figure)
    return output


def _particle_paths(case: dict, diameter_um: float, count: int = 15):
    row = next(row for row in case["particles"] if row["diameter_um"] == diameter_um)
    radius = case["radius"]
    paths = []
    for index in range(count):
        t = np.linspace(0, 1, 120)
        phase = 2 * np.pi * index / count
        x = (radius + case["pipe_length"]) * (2 * t - 1)
        window = np.sin(np.pi * t)
        y = radius * (0.13 + 0.42 * (index % 4) / 3) * np.sin(phase + np.pi * t) * window
        normalized_settling = row["settling_velocity_m_s"] / case["particles"][-1][
            "settling_velocity_m_s"
        ]
        drop = (0.12 + 1.65 * normalized_settling) * t ** 1.35
        z = case["inlet_z"] - drop + 0.08 * np.sin(phase + 2 * np.pi * t) * window
        z = np.maximum(z, case["bottom"] + 0.02)
        paths.append(np.column_stack((x, y, z)))
    return row, paths


def render_particles(case: dict, output: Path, dpi: int = 220) -> Path:
    figure = plt.figure(figsize=(16, 9), facecolor=BACKGROUND)
    colors = {40.0: "#65dcff", 63.0: "#70f0b0", 100.0: "#ffd166", 250.0: "#ff7d55"}
    diameters = [row["diameter_um"] for row in case["particles"]]

    for panel_index, diameter in enumerate(diameters):
        left = 0.025 + (panel_index % 2) * 0.48
        bottom = 0.51 if panel_index < 2 else 0.08
        axis = figure.add_axes((left, bottom, 0.46, 0.37), projection="3d")
        _style_3d(axis, case, azimuth=-61)
        _draw_shell(axis, case)
        row, paths = _particle_paths(case, diameter)
        for path in paths:
            axis.plot(
                path[:, 0], path[:, 1], path[:, 2], color=colors[diameter],
                linewidth=1.25, alpha=0.72,
            )
            axis.scatter(
                path[::18, 0], path[::18, 1], path[::18, 2], color=colors[diameter],
                s=max(3, diameter / 24), alpha=0.85, depthshade=False,
            )
        axis.text2D(
            0.04,
            0.92,
            f"{diameter:g} µm",
            transform=axis.transAxes,
            color=colors[diameter],
            fontsize=14,
            fontweight="bold",
        )
        axis.text2D(
            0.04,
            0.83,
            f"settling {row['settling_velocity_m_s'] * 1000:.1f} mm/s  ·  "
            f"capture proxy {row['capture_proxy'] * 100:.1f}%",
            transform=axis.transAxes,
            color="#c5d4dc",
            fontsize=8,
        )

    _add_header(
        figure,
        "PARTICLE FATE · SIZE-CLASS COMPARISON",
        "Settling-scaled trajectories expose the capture challenge before Lagrangian CFD",
        case["flow_lps"],
    )
    figure.text(
        0.5,
        0.475,
        "Increasing settling response  →  validate capture / escape / unresolved accounting independently",
        color=MUTED,
        fontsize=9,
        ha="center",
    )
    _add_evidence_banner(figure)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=dpi, facecolor=BACKGROUND)
    plt.close(figure)
    return output


def render_all(output_dir: Path, flow_lps: float = 40, dpi: int = 220) -> list[Path]:
    case = load_case(
        ROOT / "inputs/design-envelope.yaml",
        ROOT / "data/surrogate/grade-efficiency-proxy.csv",
        flow_lps,
    )
    return [
        render_hydraulics(case, output_dir / HYDRAULICS_NAME, dpi),
        render_particles(case, output_dir / PARTICLES_NAME, dpi),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--flow-lps", type=float, default=40)
    parser.add_argument("--dpi", type=int, default=220)
    args = parser.parse_args()
    for output in render_all(args.output_dir, args.flow_lps, args.dpi):
        print(output)


if __name__ == "__main__":
    main()
