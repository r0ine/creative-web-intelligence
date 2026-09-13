#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
q=' '.join(sys.argv[1:]).lower().strip()
if not q:
    print('usage: python tools/search_capabilities.py <query>'); raise SystemExit(2)
for f in ['font_pairings.json','composition_recipes.json','motion_recipes.json','three_art_recipes.json']:
    data=json.loads((ROOT/'data/v2'/f).read_text())
    hits=[]
    for item in data:
        text=json.dumps(item,ensure_ascii=False).lower()
        if all(term in text for term in q.split()): hits.append(item)
    if hits:
        print('\n##',f)
        for h in hits[:10]: print(h.get('id'), '-', h.get('name') or h.get('heading') or h.get('concept'), '|', h.get('family') or h.get('world'))
