#!/usr/bin/env python3
import json, pathlib, sys
root=pathlib.Path(__file__).resolve().parents[1]
q=' '.join(sys.argv[1:]).lower().strip()
recipes=json.loads((root/'data/v2/scroll_recipes.json').read_text())
if not q:
    print('usage: python tools/search_scroll_recipes.py <query>'); raise SystemExit(2)
terms=q.split()
scored=[]
for r in recipes:
    hay=' '.join([r['name'],r['category'],r['intent'],' '.join(r['recommendedTech']),' '.join(r['compatibilityTags'])]).lower()
    score=sum(hay.count(t) for t in terms)
    if score: scored.append((score,r))
for score,r in sorted(scored,key=lambda x:(-x[0],x[1]['id']))[:20]:
    print(f"{r['id']} | {r['category']} | {r['name']} | cost {r['performanceCost']}/5 | {', '.join(r['recommendedTech'])}")
