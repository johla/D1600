from __future__ import annotations
import numpy as np

def settling_velocity_ferguson_church(diameter_m, particle_density=2650.0, fluid_density=998.0,
                                       kinematic_viscosity=1.004e-6, gravity=9.81,
                                       c1=18.0, c2=1.0):
    """Settling-velocity screening correlation for natural particles.

    This is an analytical screening model, not CFD or a certification model.
    """
    d=np.asarray(diameter_m,dtype=float)
    if np.any(d <= 0): raise ValueError('diameter must be positive')
    if particle_density <= fluid_density: raise ValueError('particle must be denser than fluid for settling')
    relative=(particle_density-fluid_density)/fluid_density
    return relative*gravity*d*d/(c1*kinematic_viscosity + np.sqrt(0.75*c2*relative*gravity*d**3))

def inlet_velocity(flow_m3_s, diameter_m):
    if flow_m3_s <= 0 or diameter_m <= 0: raise ValueError('flow and diameter must be positive')
    return flow_m3_s/(np.pi*diameter_m**2/4)

def velocity_head(flow_m3_s, diameter_m, gravity=9.81):
    v=inlet_velocity(flow_m3_s,diameter_m)
    return v*v/(2*gravity)
