#!/usr/bin/env python3
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'evidence/evidence-matrix.json').read_text())
print(f"Terminal: {data['terminal_state']}\n")
for c in data['criteria']:
    missing=[p for p in c['evidence'] if not (root/p).exists()]
    rec=not (root/c['evidence_record']).exists()
    count=len(missing)+(1 if rec else 0)
    label={'pass':'PASS','active':'WORK','missing':'TODO','blocked':'BLOCK'}[c['status']]
    print(f"[{label:5}] {c['id']} {c['name']}"+(f"; missing evidence items: {count}" if count else ''))
notpass=[c for c in data['criteria'] if c['status']!='pass']
if notpass:
    c=next((x for x in notpass if x['status']=='active'),notpass[0])
    print(f"\nNext criterion: {c['id']} — {c['name']}")
    for p in c['evidence']+[c['evidence_record']]:
        if not (root/p).exists(): print(f"  missing: {p}")
