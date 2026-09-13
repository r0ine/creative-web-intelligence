#!/usr/bin/env python3
import argparse,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
reg={x['id']:x for x in json.loads((root/'integrations/open-source/open_source_library_registry.json').read_text())['libraries']}
profiles=json.loads((root/'integrations/open-source/integration_profiles.json').read_text())['profiles']
ap=argparse.ArgumentParser(); ap.add_argument('query',nargs='+'); args=ap.parse_args()
q=' '.join(args.query).lower().split(); scored=[]
for p in profiles:
    blob=' '.join([p['id'],*p['intent'],p['reasoning']]).lower()
    score=sum(1 for t in q if t in blob)
    if score: scored.append((score,p))
for score,p in sorted(scored,key=lambda z:-z[0]):
    print(f"[{score}] {p['id']}")
    print(' required:', ', '.join(reg[x]['name'] for x in p['required']))
    print(' optional:', ', '.join(reg[x]['name'] for x in p['optional']))
    print(' why:', p['reasoning'])
    print()
