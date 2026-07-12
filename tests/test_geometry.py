import math
from pathlib import Path
import tempfile
import unittest

import numpy as np

from scripts.render_geometry_3d import load_dimensions, render
from scripts.render_cfd_decision_support import load_case, render_all
from scripts.validate_geometry import connected_tetra_components, tetra_quality


class GeometryMetricTests(unittest.TestCase):
    def test_regular_tetrahedron_has_unit_mean_ratio(self):
        points = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.5, math.sqrt(3) / 2, 0.0],
            [0.5, math.sqrt(3) / 6, math.sqrt(2 / 3)],
        ])
        volume, quality = tetra_quality(points)
        self.assertAlmostEqual(volume, math.sqrt(2) / 12)
        self.assertAlmostEqual(quality, 1.0)

    def test_degenerate_tetrahedron_has_zero_quality(self):
        points = np.zeros((4, 3))
        volume, quality = tetra_quality(points)
        self.assertEqual(volume, 0)
        self.assertEqual(quality, 0)

    def test_disconnected_tetrahedra_are_detected(self):
        tetrahedra = [[1, 2, 3, 4], [4, 5, 6, 7], [8, 9, 10, 11]]
        self.assertEqual(connected_tetra_components(tetrahedra), 2)

    def test_render_dimensions_follow_design_envelope(self):
        root = Path(__file__).resolve().parents[1]
        dimensions = load_dimensions(root / "inputs/design-envelope.yaml")
        self.assertEqual(dimensions["radius"], 0.8)
        self.assertEqual(dimensions["bottom"], -0.5)
        self.assertEqual(dimensions["top"], 2.0)
        self.assertEqual(dimensions["pipe_length"], 0.6)

    def test_render_writes_nonempty_png(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "render.png"
            render(output, dpi=40)
            self.assertTrue(output.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
            self.assertGreater(output.stat().st_size, 10_000)

    def test_decision_support_case_uses_frozen_inputs(self):
        root = Path(__file__).resolve().parents[1]
        case = load_case(
            root / "inputs/design-envelope.yaml",
            root / "data/surrogate/grade-efficiency-proxy.csv",
            40,
        )
        self.assertAlmostEqual(case["inlet_velocity_m_s"], 0.5659, places=4)
        self.assertEqual([row["diameter_um"] for row in case["particles"]], [40, 63, 100, 250])

    def test_decision_support_renders_write_nonempty_pngs(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            outputs = render_all(Path(temporary_directory), flow_lps=40, dpi=35)
            self.assertEqual(len(outputs), 2)
            for output in outputs:
                self.assertTrue(output.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
                self.assertGreater(output.stat().st_size, 10_000)


if __name__ == "__main__":
    unittest.main()
