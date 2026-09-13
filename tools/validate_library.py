#!/usr/bin/env python3
from pathlib import Path
import json, sys
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
    data=json.loads(path.read_text())
    if not isinstance(data,list): errors.append(f'{kind}: expected list'); continue
    for i,item in enumerate(data):
        if kind not in ('compat',):
            rid=item.get('id')
            if not rid: errors.append(f'{kind}[{i}]: missing id')
            elif rid in seen: errors.append(f'duplicate id: {rid}')
            else: seen.add(rid)
for e in json.loads(files['compat'].read_text()):
    if e.get('relation') not in {'good','caution','avoid'}: errors.append(f'bad relation: {e}')
print(f'validated IDs: {len(seen)}')
print(f'errors: {len(errors)}')
for e in errors[:50]: print('-',e)
sys.exit(1 if errors else 0)
