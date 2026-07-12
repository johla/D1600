import unittest
from mft_d1600.surrogate import BASELINE, Design, evaluate
class SurrogateTests(unittest.TestCase):
    def test_larger_particle_has_higher_capture_proxy(self):
        a=evaluate(BASELINE,40,40)['capture_proxy']; b=evaluate(BASELINE,40,250)['capture_proxy']
        self.assertGreater(b,a)
    def test_higher_flow_reduces_capture_proxy(self):
        a=evaluate(BASELINE,10,63)['capture_proxy']; b=evaluate(BASELINE,80,63)['capture_proxy']
        self.assertGreater(a,b)
    def test_negative_control_restriction_breaks_head_loss_constraint(self):
        broken=Design(.9,.4,.7,.03,.2,.8,.9)
        result=evaluate(broken,120,63)
        self.assertFalse(result['constraint_head_loss'])
    def test_negative_control_access_breaks_constraint(self):
        broken=Design(.3,.2,.8,.1,.3,.6,.4)
        result=evaluate(broken,20,63)
        self.assertFalse(result['constraint_cleaning_access'])
