import unittest
import pandas as pd
from mft_d1600.optimize import pareto_front, sample_designs
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
    def test_sampling_is_bounded_and_includes_baseline(self):
        designs=sample_designs(n=12,seed=1600)
        self.assertEqual(len(designs),12)
        self.assertEqual(designs[0],BASELINE)
    def test_pareto_front_filters_infeasible_and_dominated_rows(self):
        rows=[
            {'design_id':0,'weighted_capture_proxy':.8,'head_loss_proxy_m':.05,
             'overload_sediment_risk_proxy':.4,'maintainability_proxy':.8,'complexity':.2,'feasible':True},
            {'design_id':1,'weighted_capture_proxy':.7,'head_loss_proxy_m':.06,
             'overload_sediment_risk_proxy':.5,'maintainability_proxy':.7,'complexity':.3,'feasible':True},
            {'design_id':2,'weighted_capture_proxy':.9,'head_loss_proxy_m':.08,
             'overload_sediment_risk_proxy':.3,'maintainability_proxy':.7,'complexity':.4,'feasible':True},
            {'design_id':3,'weighted_capture_proxy':1.0,'head_loss_proxy_m':.01,
             'overload_sediment_risk_proxy':.1,'maintainability_proxy':1.0,'complexity':.1,'feasible':False},
        ]
        front=pareto_front(pd.DataFrame(rows))
        self.assertEqual(set(front.design_id),{0,2})
