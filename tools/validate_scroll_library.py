#!/usr/bin/env python3
import json, pathlib, sys
root=pathlib.Path(__file__).resolve().parents[1]
recipes=json.loads((root/'data/v2/scroll_recipes.json').read_text())
ids=[x['id'] for x in recipes]
errors=[]
if len(recipes)!=100: errors.append(f'expected 100 recipes, got {len(recipes)}')
if len(ids)!=len(set(ids)): errors.append('duplicate scroll recipe ids')
required={'id','category','name','trigger','mapping','intent','recommendedTech','mobileStrategy','reducedMotion','performanceCost','salience'}
for i,r in enumerate(recipes):
    missing=required-r.keys()
    if missing: errors.append(f'{r.get("id",i)} missing {sorted(missing)}')
    if r.get('performanceCost') not in range(1,6): errors.append(f'{r.get("id")} invalid performanceCost')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'OK: {len(recipes)} scroll recipes, {len(set(r["category"] for r in recipes))} categories, unique IDs')
