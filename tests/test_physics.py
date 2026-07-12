import unittest
from mft_d1600.physics import settling_velocity_ferguson_church
class PhysicsTests(unittest.TestCase):
    def test_velocity_increases_with_size(self):
        vals=settling_velocity_ferguson_church([40e-6,63e-6,100e-6,250e-6])
        self.assertTrue(all(a<b for a,b in zip(vals,vals[1:])))
    def test_63um_plausible_screening_range(self):
        value=float(settling_velocity_ferguson_church(63e-6))
        self.assertGreater(value,0.001)
        self.assertLess(value,0.01)
    def test_invalid_density_rejected(self):
        with self.assertRaises(ValueError): settling_velocity_ferguson_church(63e-6,particle_density=900)
