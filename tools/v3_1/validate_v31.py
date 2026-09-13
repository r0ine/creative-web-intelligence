from pathlib import Path
import json, sys
root=Path(__file__).resolve().parents[2]
required={
 'data/v3_1/typography_recipes.json':200,
 'data/v3_1/scroll_recipes_precision.json':160,
 'data/v3_1/backend_security_recipes.json':180,
 'data/v3_1/api_contract_patterns.json':100,
 'data/v3_1/secret_key_patterns.json':80,
 'data/v3_1/encryption_decisions.json':60,
 'data/v3_1/security_qa_checks.json':160,
 'data/v3_1/typography_qa_checks.json':120,
 'data/v3_1/scroll_qa_checks.json':120,
 'data/v3_1/font_pairing_strategies.json':120,
 'data/v3_1/scroll_transition_matrix.json':120,
}
errors=[]
for rel,count in required.items():
    p=root/rel
    try:d=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'{rel}: {e}'); continue
    if len(d)!=count: errors.append(f'{rel}: expected {count}, got {len(d)}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('v3.1 machine-readable sets validated:',sum(required.values()),'records')
