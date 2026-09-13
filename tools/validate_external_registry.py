#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'integrations'/'open-source'/'open_source_library_registry.json'
d=json.loads(p.read_text())
ids=set(); errs=[]
for x in d['libraries']:
    if x['id'] in ids: errs.append('duplicate id '+x['id'])
    ids.add(x['id'])
    for k in ['id','name','repo','category','license','redistribution','integration','priority','best_for','avoid_when','notes']:
        if k not in x: errs.append(f"{x.get('id','?')}: missing {k}")
    if x['priority']=='restricted' and 'allowed' in x['redistribution'].lower():
        errs.append(f"{x['id']}: restricted but redistribution says allowed")
print(f'external libraries: {len(d["libraries"])}')
print(f'errors: {len(errs)}')
for e in errs: print('-',e)
raise SystemExit(1 if errs else 0)
