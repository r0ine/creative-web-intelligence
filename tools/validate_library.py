#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
files={
 'font':ROOT/'data/v2/font_pairings.json',
 'composition':ROOT/'data/v2/composition_recipes.json',
 'motion':ROOT/'data/v2/motion_recipes.json',
 'three':ROOT/'data/v2/three_art_recipes.json',
 'compat':ROOT/'data/v2/compatibility_graph.json',
 'qa':ROOT/'data/v2/qa_rubric.json',
}
errors=[]
seen=set()
for kind,path in files.items():
    data=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data,list): errors.append(f'{kind}: expected list'); continue
    for i,item in enumerate(data):
        if kind not in ('compat',):
            rid=item.get('id')
            if not rid: errors.append(f'{kind}[{i}]: missing id')
            elif rid in seen: errors.append(f'duplicate id: {rid}')
            else: seen.add(rid)
scroll_ids={r['id'] for r in json.loads((ROOT/'data/v2/scroll_recipes.json').read_text(encoding='utf-8'))}
recipe_ids=seen|scroll_ids
edges=json.loads(files['compat'].read_text(encoding='utf-8'))
pairs=set()
for e in edges:
    if e.get('relation') not in {'good','caution','avoid'}: errors.append(f'bad relation: {e}')
    pair=frozenset((e.get('a'),e.get('b')))
    if len(pair)<2: errors.append(f'self edge: {e}')
    elif pair in pairs: errors.append(f'duplicate edge: {e["a"]} <-> {e["b"]}')
    pairs.add(pair)
    # Unprefixed endpoints are abstract traits (e.g. glass-heavy); prefixed ones must name a recipe.
    for end in (e.get('a'),e.get('b')):
        if re.fullmatch(r'(font|comp|motion|three|qa|scroll)-\d+',end or '') and end not in recipe_ids:
            errors.append(f'unknown recipe in edge: {end}')
stats=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))['stats']
for key,kind in {'fontPairings':'font','compositionRecipes':'composition','motionRecipes':'motion','threeArtRecipes':'three','compatibilityEdges':'compat','qaChecks':'qa'}.items():
    actual=len(json.loads(files[kind].read_text(encoding='utf-8')))
    if stats.get(key)!=actual: errors.append(f'manifest.json stats.{key}={stats.get(key)} but data has {actual}')
print(f'validated IDs: {len(seen)}')
print(f'errors: {len(errors)}')
for e in errors[:50]: print('-',e)
sys.exit(1 if errors else 0)
