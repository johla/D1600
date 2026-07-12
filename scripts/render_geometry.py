#!/usr/bin/env python3
from pathlib import Path
from string import Template
import json, yaml
root=Path(__file__).resolve().parents[1]
env=yaml.safe_load((root/'inputs/design-envelope.yaml').read_text())
c=env['chamber']
params={'chamber_diameter':c['internal_diameter_m'],'water_depth':c['water_depth_m'],'sump_depth':c['sump_depth_m'],
        'inlet_diameter':c['inlet_diameter_m'],'outlet_diameter':c['outlet_diameter_m'],'inlet_z':c['inlet_center_elevation_m'],
        'outlet_z':c['outlet_center_elevation_m'],'pipe_length':0.6,'mesh_min':0.02,'mesh_max':0.12}
t=Template((root/'geometry/gmsh/generic_d1600.geo.template').read_text())
out=root/'geometry/generated/baseline-d1600.geo'; out.write_text(t.substitute(params))
contract={
    'status':'generated_geometry_with_solver_boundary_contract',
    'parameters':params,
    'physical_groups':{'volumes':['fluid'],'surfaces':['inlet','outlet','walls']},
    'source':'inputs/design-envelope.yaml',
}
(root/'geometry/generated/geometry-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
print(out)
