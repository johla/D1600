from pathlib import Path
import json, sys
import matplotlib.pyplot as plt
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from mft_d1600.optimize import sample_designs, campaign, pareto_front
from mft_d1600.surrogate import BASELINE, evaluate

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'reports/generated'; DATA=ROOT/'data/surrogate'; OPT=ROOT/'optimization'
for p in [OUT,DATA,OPT]: p.mkdir(parents=True,exist_ok=True)

df=campaign(sample_designs())
pareto=pareto_front(df)
df.to_csv(OPT/'surrogate-results.csv',index=False)
pareto.to_csv(OPT/'surrogate-pareto.csv',index=False)

# Grade-efficiency proxy for baseline and selected balanced candidate.
if len(pareto):
    norm=pareto.copy()
    score=(norm.weighted_capture_proxy
           -2.0*norm.head_loss_proxy_m
           -0.12*norm.overload_sediment_risk_proxy
           +0.10*norm.maintainability_proxy
           -0.05*norm.complexity)
    best=pareto.loc[score.idxmax()]
else: raise RuntimeError('No feasible surrogate designs')

from mft_d1600.surrogate import Design
fields=['tangentiality','center_baffle_ratio','shield_ratio','shield_gap_ratio','outlet_submergence_ratio','flow_distribution','complexity']
best_design=Design(**{f:float(best[f]) for f in fields})
rows=[]
for name,d in [('generic_baseline',BASELINE),('screened_candidate',best_design)]:
    for q in [10,20,40,80,120]:
        for p in [40,63,100,250]:
            r=evaluate(d,q,p); rows.append({'design':name,**r})
grade=pd.DataFrame(rows); grade.to_csv(DATA/'grade-efficiency-proxy.csv',index=False)

plt.figure(figsize=(8,5))
for name,group in grade[grade.flow_lps==40].groupby('design'):
    plt.plot(group.particle_um,100*group.capture_proxy,marker='o',label=name)
plt.xscale('log'); plt.xlabel('Particle diameter (µm)'); plt.ylabel('Capture proxy (%)'); plt.title('Reduced-order screening only — 40 L/s'); plt.grid(True,which='both'); plt.legend(); plt.tight_layout(); plt.savefig(OUT/'surrogate-grade-efficiency.png',dpi=180); plt.close()

plt.figure(figsize=(8,5))
feasible=df[df.feasible]
plt.scatter(feasible.head_loss_proxy_m,100*feasible.weighted_capture_proxy,s=8,alpha=.25,label='feasible screening designs')
plt.scatter(pareto.head_loss_proxy_m,100*pareto.weighted_capture_proxy,s=25,label='screening Pareto set')
plt.xlabel('Head-loss proxy at 80 L/s (m)'); plt.ylabel('Weighted capture proxy (%)'); plt.title('Reduced-order screening — not CFD'); plt.grid(True); plt.legend(); plt.tight_layout(); plt.savefig(OUT/'surrogate-pareto.png',dpi=180); plt.close()

summary={'model_class':'reduced_order_screening_not_CFD','sampled_designs':int(len(df)),'feasible_designs':int(df.feasible.sum()),'pareto_designs':int(len(pareto)),
         'baseline':df.iloc[0].to_dict(),'screened_candidate':best.to_dict()}
(OUT/'surrogate-summary.json').write_text(json.dumps(summary,indent=2,default=lambda x: bool(x) if hasattr(x,'item') and isinstance(x.item(),bool) else float(x) if hasattr(x,'item') else str(x))+'\n')
print(json.dumps({'sampled_designs':summary['sampled_designs'],'feasible_designs':summary['feasible_designs'],'pareto_designs':summary['pareto_designs'],'warning':summary['model_class']},indent=2))
