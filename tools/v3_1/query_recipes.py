from pathlib import Path
import json, sys
root=Path(__file__).resolve().parents[2]/'data'/'v3_1'
q=' '.join(sys.argv[1:]).lower().strip()
if not q:
    print('usage: python tools/v3_1/query_recipes.py <keywords>'); raise SystemExit(1)
hits=[]
for p in root.glob('*.json'):
    try:data=json.loads(p.read_text(encoding='utf-8'))
    except:continue
    if not isinstance(data,list):continue
    for item in data:
        blob=json.dumps(item,ensure_ascii=False).lower()
        score=sum(1 for token in q.split() if token in blob)
        if score:hits.append((score,p.name,item.get('id','?'),item))
for score,file,id_,item in sorted(hits,key=lambda x:-x[0])[:20]:
    print(f'[{score}] {file} :: {id_}')
    print(json.dumps(item,ensure_ascii=False,indent=2)[:1200])
