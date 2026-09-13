#!/usr/bin/env python3
from pathlib import Path
import json, sys
root=Path(__file__).resolve().parents[2]
required=[
 'README_V3_2.md','docs/V3_2_OVERVIEW.md','directors/v3_2/COLOR_DIRECTOR.md','directors/v3_2/TYPOGRAPHY_DIRECTOR.md','directors/v3_2/MOTION_DIRECTOR.md',
 'color/v3_2/SANZO_WADA_COLOR_INTELLIGENCE.md','motion/v3_2/ANTI_AI_MOTION_GRAMMAR.md','anti-ai/v3_2/VISUAL_FINGERPRINT_GATE.md','quality/V3_2_VISUAL_DIRECTION_GATE.md',
 'data/v3_2/wada_source_registry.json','data/v3_2/font_taxonomy.json','data/v3_2/motion_grammar_recipes.json','data/v3_2/visual_fingerprint_checks.json'
]
errs=[]
for rel in required:
    if not (root/rel).exists(): errs.append('missing '+rel)
for p in (root/'data/v3_2').glob('*.json'):
    try: json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: errs.append(f'invalid json {p.relative_to(root)}: {e}')
for p in (root/'schemas/v3_2').glob('*.json'):
    try: json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: errs.append(f'invalid schema json {p.relative_to(root)}: {e}')
if errs:
    print('\n'.join(errs)); sys.exit(1)
print('v3.2 validation PASS')
