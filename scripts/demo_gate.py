#!/usr/bin/env python3
from pathlib import Path
import json,sys,hashlib
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'evidence/evidence-matrix.json').read_text())
errors=[]
for c in data['criteria']:
    if c['status']!='pass': errors.append(f"{c['id']} status {c['status']}")
    for rel in c['evidence']:
        p=root/rel
        if not p.exists(): errors.append(f"{c['id']} missing {rel}")
        elif p.is_file() and p.stat().st_size==0: errors.append(f"{c['id']} empty {rel}")
        elif p.is_dir() and not any(p.iterdir()): errors.append(f"{c['id']} empty directory {rel}")
    rp=root/c['evidence_record']
    if not rp.exists(): errors.append(f"{c['id']} missing evidence record")
    else:
        try: r=json.loads(rp.read_text())
        except Exception as e: errors.append(f"{c['id']} invalid evidence record: {e}"); continue
        if r.get('status')!='pass' or r.get('criterion_id')!=c['id']: errors.append(f"{c['id']} evidence record not pass/mismatched")
        if not r.get('release_revision') or not r.get('verifications'): errors.append(f"{c['id']} weak evidence record")
        review=r.get('independent_review',{})
        if c['requires_independent_review'] and (not review.get('review_path') or review.get('open_critical')!=0 or review.get('open_high')!=0): errors.append(f"{c['id']} independent review incomplete")
        nc=r.get('negative_control',{})
        if c['requires_negative_control'] and (not nc.get('method') or not nc.get('restoration_verified')): errors.append(f"{c['id']} negative control incomplete")
if errors:
    print('C1 DEMO GATE: FAIL')
    for e in errors: print('-',e)
    print(f'\n{len(errors)} unsatisfied conditions. Continue the root loop.')
    sys.exit(1)
print('C1 DEMO GATE: PASS')
