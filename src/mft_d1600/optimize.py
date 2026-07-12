from __future__ import annotations
from dataclasses import asdict
import numpy as np
import pandas as pd
from .surrogate import Design, evaluate, BASELINE

def sample_designs(n=2000, seed=1600):
    rng=np.random.default_rng(seed)
    designs=[BASELINE]
    for _ in range(n-1):
        designs.append(Design(
          tangentiality=float(rng.uniform(0,1)),
          center_baffle_ratio=float(rng.uniform(0.05,0.45)),
          shield_ratio=float(rng.uniform(0.20,0.80)),
          shield_gap_ratio=float(rng.uniform(0.03,0.20)),
          outlet_submergence_ratio=float(rng.uniform(0.05,0.70)),
          flow_distribution=float(rng.uniform(0.2,1.0)),
          complexity=float(rng.uniform(0,1))))
    return designs

def campaign(designs, flows=(10,20,40,80), particles=(40,63,100,250), weights=(0.10,0.40,0.30,0.20), overload=120):
    rows=[]
    for idx,d in enumerate(designs):
        per=[]
        for q in flows:
            for p,w in zip(particles,weights):
                r=evaluate(d,q,p); r['weight']=w; per.append(r)
        overload_rows=[evaluate(d,overload,p) for p in particles]
        weighted_capture=np.mean([sum(x['capture_proxy']*x['weight'] for x in per if x['flow_lps']==q) for q in flows])
        design_flow=max(flows)
        design_rows=[x for x in per if x['flow_lps']==design_flow]
        row={'design_id':idx,**asdict(d),'weighted_capture_proxy':weighted_capture,
             'head_loss_proxy_m':max(x['head_loss_proxy_m'] for x in design_rows),
             'overload_sediment_risk_proxy':max(x['sediment_risk_proxy'] for x in overload_rows),
             'maintainability_proxy':min(x['maintainability_proxy'] for x in per),
             'feasible':all(x['feasible'] for x in per+overload_rows)}
        rows.append(row)
    return pd.DataFrame(rows)

def pareto_front(df):
    feasible=df[df.feasible].copy()
    objectives=np.column_stack([-feasible.weighted_capture_proxy.values,
                                feasible.head_loss_proxy_m.values,
                                feasible.overload_sediment_risk_proxy.values,
                                -feasible.maintainability_proxy.values,
                                feasible.complexity.values])
    keep=np.ones(len(feasible),dtype=bool)
    for i in range(len(feasible)):
        if not keep[i]: continue
        dominated=np.all(objectives <= objectives[i],axis=1)&np.any(objectives<objectives[i],axis=1)
        if np.any(dominated): keep[i]=False
    return feasible.iloc[np.where(keep)[0]].copy().sort_values(['weighted_capture_proxy','head_loss_proxy_m'],ascending=[False,True])
