import json, argparse
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--name',required=True)
p.add_argument('--backend',action='store_true')
p.add_argument('--reference-mode',choices=['none','inspired','structure-close','pixel-close','behavior-close'],default='none')
p.add_argument('--out',default='creative-build-spec-v3.json')
a=p.parse_args()

spec={
  'project':a.name,
  'reference':None if a.reference_mode=='none' else {'mode':a.reference_mode,'sources':[],'viewports':[],'unknowns':[]},
  'creative':{'designDNA':{},'typography':{},'color':{},'composition':{},'motion':{},'scroll':{},'three':None},
  'backendRequired':a.backend,
  'backend':{} if a.backend else None,
  'integration':[],
  'quality':{'viewports':[],'accessibility':{},'performance':{},'fidelity':{},'security':{}}
}
Path(a.out).write_text(json.dumps(spec,indent=2),encoding='utf-8')
print(a.out)
