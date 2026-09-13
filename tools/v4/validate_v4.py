#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[2]
errors=[]

def read(rel):
    try: return json.loads((ROOT/rel).read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'{rel}: {e}'); return None

sources=read('data/v4/source_registry.json') or []
ids=set()
for i,s in enumerate(sources):
    for k in ('id','name','category','access','automation','licenseModel','guardrails'):
        if k not in s: errors.append(f'source[{i}] missing {k}')
    if s.get('id') in ids: errors.append(f"duplicate source id {s.get('id')}")
    ids.add(s.get('id'))
    if s.get('automation') in {'restricted_no_generic_scrape','do-not-scrape-or-automate-without-consent'} and s.get('access')=='public_api':
        errors.append(f"restricted source incorrectly marked public_api: {s.get('id')}")

for rel in ['data/v4/icon_family_profiles.json','data/v4/icon_decision_matrix.json','data/v4/asset_decision_matrix.json','data/v4/source_license_policies.json','data/v4/design_resource_taxonomy.json']:
    read(rel)

required=[
 'prompts/v4/MASTER_META_PROMPT_V4.md','directors/v4/SOURCE_INTELLIGENCE_DIRECTOR.md','directors/v4/ICON_DIRECTOR.md','directors/v4/ASSET_DIRECTOR.md','source-intelligence/LICENSE_AND_PROVENANCE_GATE.md','tools/v4/source_intelligence.py','quality/V4_SOURCE_ASSET_GATE.md'
]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'missing {rel}')

print(f'v4 sources: {len(sources)}')
print(f'v4 errors: {len(errors)}')
for e in errors: print('-',e)
sys.exit(1 if errors else 0)
