#!/usr/bin/env python3
from pathlib import Path
import json, sys, hashlib
ROOT=Path(__file__).resolve().parents[1]

def load(name): return json.loads((ROOT/'data/v2'/name).read_text())
fonts=load('font_pairings.json'); comps=load('composition_recipes.json'); motions=load('motion_recipes.json'); threes=load('three_art_recipes.json')
brief=' '.join(sys.argv[1:]).lower().strip()
if not brief:
    print('usage: python tools/compose_spec.py "project brief"'); raise SystemExit(2)

def score(item, words):
    text=json.dumps(item,ensure_ascii=False).lower()
    s=sum(3 for w in words if w in text)
    # stable tie breaker—not "AI magic", just deterministic choice for CLI demo
    h=int(hashlib.sha1((brief+item.get('id','')).encode()).hexdigest()[:6],16)%1000
    return s + h/100000
words=[w for w in re_split(brief) if len(w)>2]
def pick(items): return max(items,key=lambda x:score(x,words))
def re_split(s):
    import re
    return re.findall(r'[a-z0-9çğıöşü]+',s)
font=pick(fonts); comp=pick(comps); motion=pick(motions)
use3d=any(w in brief for w in ['3d','webgl','three','model','product','cinematic','sahne'])
three=pick(threes) if use3d else None
spec={'brief':brief,'designDNA':{'note':'CLI bootstrap only; agent should refine'},'typography':font,'composition':comp,'motion':motion,'three':three,'quality':{'run':'data/v2/qa_rubric.json'},'warning':'This deterministic helper is a discovery bootstrap, not a substitute for art direction.'}
print(json.dumps(spec,indent=2,ensure_ascii=False))
