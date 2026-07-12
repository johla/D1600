import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class DesignEnvelopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.envelope = yaml.safe_load((ROOT / "inputs/design-envelope.yaml").read_text())

    def test_scope_is_frozen_generic_demo(self):
        self.assertEqual(
            self.envelope["status"], "frozen_generic_c1_demo_not_product_claims"
        )
        self.assertTrue(self.envelope["constraints"]["passive_only"])
        self.assertFalse(self.envelope["constraints"]["powered_components_allowed"])

    def test_operating_envelope_is_ordered_and_complete(self):
        hydraulics = self.envelope["hydraulics"]
        self.assertEqual(hydraulics["flow_points_lps"], sorted(hydraulics["flow_points_lps"]))
        self.assertGreater(hydraulics["overload_flow_lps"], max(hydraulics["flow_points_lps"]))
        self.assertEqual(self.envelope["particles"]["diameters_um"], [40, 63, 100, 250])
        self.assertAlmostEqual(sum(self.envelope["particles"]["weighting"]), 1.0)

    def test_geometry_and_evidence_thresholds_are_physical(self):
        chamber = self.envelope["chamber"]
        self.assertEqual(chamber["internal_diameter_m"], 1.6)
        self.assertLess(chamber["inlet_diameter_m"], chamber["internal_diameter_m"])
        self.assertLess(chamber["outlet_diameter_m"], chamber["internal_diameter_m"])
        self.assertGreater(self.envelope["constraints"]["minimum_internal_gap_m"], 0)
        for threshold in self.envelope["evidence_thresholds"].values():
            self.assertGreater(threshold, 0)


if __name__ == "__main__":
    unittest.main()
