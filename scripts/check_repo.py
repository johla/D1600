#!/usr/bin/env python3
from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[1]
required=['README.md','GOAL.md','SCOUT.md','EVIDENCE_MATRIX.md','ROUTES.md','TASKS.md','DECISIONS.md','RISKS.md','OPEN_QUESTIONS.md','inputs/design-envelope.yaml','evidence/evidence-matrix.json','agent/MASTER_PROMPT.md','reports/generated/surrogate-summary.json','geometry/generated/baseline-d1600.geo']
missing=[x for x in required if not (root/x).exists()]
if missing:
    print('Missing:',*missing,sep='\n- '); sys.exit(1)
s=json.loads((root/'reports/generated/surrogate-summary.json').read_text())
assert s['model_class']=='reduced_order_screening_not_CFD'
assert s['sampled_designs']>=1000 and s['feasible_designs']>0 and s['pareto_designs']>0
m=json.loads((root/'evidence/evidence-matrix.json').read_text())
assert m['terminal_state']=='C1_DEMO_READY' and len(m['criteria'])==16
assert 'make demo-gate' in (root/'agent/MASTER_PROMPT.md').read_text()
print('Repository and reduced-order bootstrap checks passed.')
print('The surrogate is explicitly NOT CFD evidence. Run make demo-gate for project status.')
