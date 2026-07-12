#!/usr/bin/env python3
"""Create a presentation-quality cutaway render of the generic D1600 geometry."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import yaml
from matplotlib.colors import LightSource

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "reports/generated/baseline-geometry-3d.png"


def load_dimensions(path: Path) -> dict[str, float]:
    chamber = yaml.safe_load(path.read_text())["chamber"]
    return {
        "radius": chamber["internal_diameter_m"] / 2,
        "bottom": -chamber["sump_depth_m"],
        "top": chamber["water_depth_m"],
        "pipe_radius": chamber["inlet_diameter_m"] / 2,
        "inlet_z": chamber["inlet_center_elevation_m"],
        "outlet_z": chamber["outlet_center_elevation_m"],
        "pipe_length": chamber["pipe_length_m"],
    }


def _vertical_cylinder(radius: float, bottom: float, top: float, cutaway: bool = False):
    start, stop = (0.16 * np.pi, 1.84 * np.pi) if cutaway else (0, 2 * np.pi)
    theta = np.linspace(start, stop, 120)
    z = np.linspace(bottom, top, 50)
    theta, z = np.meshgrid(theta, z)
    return radius * np.cos(theta), radius * np.sin(theta), z


def _horizontal_cylinder(
    start: float, stop: float, radius: float, elevation: float
):
    x = np.linspace(start, stop, 45)
    theta = np.linspace(0, 2 * np.pi, 64)
    x, theta = np.meshgrid(x, theta)
    return x, radius * np.cos(theta), elevation + radius * np.sin(theta)


def _style_axis(axis, dimensions: dict[str, float]) -> None:
    radius = dimensions["radius"]
    limit = radius + dimensions["pipe_length"] + 0.12
    axis.set(
        xlim=(-limit, limit),
        ylim=(-limit, limit),
        zlim=(dimensions["bottom"] - 0.08, dimensions["top"] + 0.18),
    )
    vertical_range = dimensions["top"] - dimensions["bottom"] + 0.26
    axis.set_box_aspect((2 * limit, 2 * limit, vertical_range))
    axis.set_axis_off()
    axis.set_proj_type("persp", focal_length=0.9)
    axis.view_init(elev=23, azim=-58)
    axis.set_facecolor("#08121f")


def render(output: Path, dpi: int = 220) -> Path:
    dimensions = load_dimensions(ROOT / "inputs/design-envelope.yaml")
    radius = dimensions["radius"]
    bottom = dimensions["bottom"]
    top = dimensions["top"]
    pipe_radius = dimensions["pipe_radius"]
    light = LightSource(azdeg=315, altdeg=42)

    figure = plt.figure(figsize=(13.2, 8), facecolor="#08121f")
    axis = figure.add_subplot(111, projection="3d")
    _style_axis(axis, dimensions)

    # The translucent shell leaves a front window to expose the fluid domain.
    x, y, z = _vertical_cylinder(radius, bottom, top, cutaway=True)
    axis.plot_surface(
        x, y, z, color="#a8c1cf", alpha=0.19, linewidth=0, shade=True,
        lightsource=light, antialiased=True,
    )

    # Water and sump are shown as a second, slightly inset volume.
    x, y, z = _vertical_cylinder(radius * 0.975, bottom + 0.025, top - 0.03, cutaway=True)
    axis.plot_surface(
        x, y, z, color="#159ddb", alpha=0.34, linewidth=0, shade=True,
        lightsource=light, antialiased=True,
    )

    theta = np.linspace(0.16 * np.pi, 1.84 * np.pi, 160)
    radial = np.linspace(0, radius * 0.975, 55)
    theta, radial = np.meshgrid(theta, radial)
    axis.plot_surface(
        radial * np.cos(theta), radial * np.sin(theta), np.full_like(theta, top - 0.03),
        color="#70d8ff", alpha=0.52, linewidth=0, shade=True, lightsource=light,
    )

    for start, stop, elevation, color in (
        (-radius - dimensions["pipe_length"], -radius, dimensions["inlet_z"], "#ed8b3a"),
        (radius, radius + dimensions["pipe_length"], dimensions["outlet_z"], "#5fd0ef"),
    ):
        x, y, z = _horizontal_cylinder(start, stop, pipe_radius, elevation)
        axis.plot_surface(
            x, y, z, color=color, alpha=0.9, linewidth=0, shade=True,
            lightsource=light, antialiased=True,
        )

    ring_theta = np.linspace(0, 2 * np.pi, 240)
    for elevation, alpha in ((bottom, 0.55), (top, 0.9)):
        axis.plot(
            radius * np.cos(ring_theta), radius * np.sin(ring_theta),
            np.full_like(ring_theta, elevation), color="#d5e4ea",
            linewidth=2.1, alpha=alpha,
        )

    axis.text(
        -radius - dimensions["pipe_length"] - 0.04, 0, dimensions["inlet_z"] + 0.25,
        "INLET", color="#ffb36f", fontsize=10, fontweight="bold", ha="center",
    )
    axis.text(
        radius + dimensions["pipe_length"] + 0.04, 0, dimensions["outlet_z"] + 0.25,
        "OUTLET", color="#81e6ff", fontsize=10, fontweight="bold", ha="center",
    )
    figure.text(
        0.055, 0.91, "GENERIC D1600", color="white", fontsize=27, fontweight="bold",
    )
    figure.text(
        0.057, 0.865, "Hydraulic geometry · transparent cutaway",
        color="#91a8b7", fontsize=13,
    )
    figure.text(
        0.057, 0.075,
        "Ø 1.60 m   •   2.50 m wet depth   •   Ø 0.30 m inlet / outlet",
        color="#91a8b7", fontsize=11,
    )
    figure.text(
        0.945, 0.075, "GENERIC BASELINE · SI UNITS",
        color="#557083", fontsize=9, ha="right",
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=dpi, facecolor=figure.get_facecolor(), bbox_inches="tight")
    plt.close(figure)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--dpi", type=int, default=220)
    args = parser.parse_args()
    print(render(args.output, args.dpi))


if __name__ == "__main__":
    main()
