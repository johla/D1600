import math
import unittest

import numpy as np

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


if __name__ == "__main__":
    unittest.main()
