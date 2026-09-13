#!/usr/bin/env python3
import json, argparse
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
REG = HERE/'integrations'/'open-source'/'open_source_library_registry.json'

def main():
    ap=argparse.ArgumentParser(description='Search external creative-web integrations')
    ap.add_argument('query', nargs='+')
    ap.add_argument('--framework', default='')
    ap.add_argument('--allow-restricted', action='store_true')
    args=ap.parse_args()
    q=' '.join(args.query).lower().split()
    data=json.loads(REG.read_text())['libraries']
    out=[]
    for x in data:
        if not args.allow_restricted and x.get('priority')=='restricted':
            continue
        blob=' '.join([x['id'],x['name'],*x.get('category',[]),*x.get('best_for',[]),x.get('notes','')]).lower()
        score=sum(2 if t in x['id'].lower() or t in x['name'].lower() else 1 for t in q if t in blob)
        if args.framework and args.framework.lower() not in [f.lower() for f in x.get('framework',[])]:
            score-=2
        if score>0: out.append((score,x))
    for score,x in sorted(out,key=lambda z:(-z[0],z[1]['name']))[:15]:
        print(f"{score:>2}  {x['id']:<24} {x['name']}  [{x['license']}]  {x['integration']}")
        print('    best:', '; '.join(x.get('best_for',[])[:3]))
        print('    note:', x.get('notes',''))
if __name__=='__main__': main()
