from __future__ import annotations
from dataclasses import dataclass, asdict
import math
import numpy as np
from .physics import settling_velocity_ferguson_church, velocity_head, inlet_velocity

@dataclass(frozen=True)
class Design:
    tangentiality: float
    center_baffle_ratio: float
    shield_ratio: float
    shield_gap_ratio: float
    outlet_submergence_ratio: float
    flow_distribution: float
    complexity: float

    def validate(self):
        ranges={
            'tangentiality':(0,1), 'center_baffle_ratio':(0.05,0.45),
            'shield_ratio':(0.20,0.80), 'shield_gap_ratio':(0.03,0.20),
            'outlet_submergence_ratio':(0.05,0.70), 'flow_distribution':(0.2,1.0),
            'complexity':(0,1)}
        for name,(lo,hi) in ranges.items():
            value=getattr(self,name)
            if not lo <= value <= hi: raise ValueError(f'{name} outside [{lo}, {hi}]')

    def as_dict(self): return asdict(self)

BASELINE=Design(0.0,0.05,0.20,0.20,0.05,0.30,0.0)

def evaluate(design: Design, flow_lps: float, particle_um: float, *, chamber_diameter=1.6,
             water_depth=2.0, inlet_diameter=0.30, rho=998.0, particle_density=2650.0,
             nu=1.004e-6, gravity=9.81, max_head_loss_m=0.15,
             minimum_gap_m=0.075, minimum_access_m=0.4):
    """Transparent screening surrogate.

    The functional form is intentionally conservative and heuristic. It exists to test
    experiment plumbing and rank ideas before CFD, never to substantiate product performance.
    """
    design.validate()
    q=flow_lps/1000.0
    ws=float(settling_velocity_ferguson_church(particle_um*1e-6,particle_density,rho,nu,gravity))
    area=math.pi*chamber_diameter**2/4
    vin=inlet_velocity(q,inlet_diameter)

    # Effective settling opportunity and explicit penalties.
    residence=max(0.15, design.flow_distribution*(1.0-0.35*design.center_baffle_ratio))
    path_enhancement=1 + 1.25*design.tangentiality + 0.75*design.center_baffle_ratio + 0.85*design.shield_ratio
    outlet_optimum=math.exp(-((design.outlet_submergence_ratio-0.38)/0.28)**2)
    turbulence=1 + 0.45*(vin/0.5)**1.35*(0.35+design.tangentiality**1.7)
    ideal_number=ws*area/q
    capture=1-math.exp(-ideal_number*residence*path_enhancement*(0.55+0.45*outlet_optimum)/turbulence)
    capture=float(np.clip(capture,0,0.995))

    # Head-loss proxy through a geometry-dependent K coefficient.
    restriction=max(0.0,(0.10-design.shield_gap_ratio))/0.10
    k=0.55 + 1.5*design.tangentiality**2 + 0.8*design.center_baffle_ratio**2 + 1.8*restriction**2 + 0.25*design.complexity
    head_loss=k*velocity_head(q,inlet_diameter,gravity)

    # Dimensionless near-bed disturbance/washout risk proxy at this flow.
    shield_protection=0.25+1.5*design.shield_ratio*(0.4+design.center_baffle_ratio)
    jet_coupling=(0.45+0.55*(1-design.outlet_submergence_ratio))*((vin/0.5)**2)
    sediment_risk=float(np.clip(jet_coupling/(1+shield_protection),0,4))

    physical_gap=design.shield_gap_ratio*chamber_diameter
    access=chamber_diameter*(1-design.shield_ratio)/2
    constraints={
      'head_loss': head_loss <= max_head_loss_m,
      'minimum_gap': physical_gap >= minimum_gap_m,
      'cleaning_access': access >= minimum_access_m,
    }
    feasible=all(constraints.values())
    maintainability=float(np.clip(min(physical_gap/minimum_gap_m,access/minimum_access_m)/2,0,1))
    return {
      'flow_lps':flow_lps,'particle_um':particle_um,'settling_velocity_m_s':ws,
      'capture_proxy':capture,'head_loss_proxy_m':head_loss,'sediment_risk_proxy':sediment_risk,
      'maintainability_proxy':maintainability,'feasible':feasible,**{f'constraint_{k}':v for k,v in constraints.items()}}
