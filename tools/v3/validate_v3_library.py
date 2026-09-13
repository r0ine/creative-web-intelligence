import json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
expected={
 'data/v3/scroll_recipes_advanced.json':120,
 'data/v3/motion_token_matrix.json':72,
 'data/v3/backend_recipes.json':120,
 'data/v3/reference_recreation_recipes.json':72,
 'data/v3/fullstack_integration_recipes.json':60,
 'data/v3/qa_checks.json':96,
 'data/v3/media_runtime_recipes.json':48,
}
errors=[]
for rel,count in expected.items():
    p=root/rel
    try: data=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'{rel}: {e}'); continue
    if not isinstance(data,list) or len(data)!=count: errors.append(f'{rel}: expected {count}, got {len(data) if isinstance(data,list) else "not-list"}')
    ids=[x.get('id') for x in data if isinstance(x,dict)]
    if len(ids)!=len(set(ids)): errors.append(f'{rel}: duplicate ids')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print('v3 library validation OK')
