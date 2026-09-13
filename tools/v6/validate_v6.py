#!/usr/bin/env python3
"""CWI v6 structural validator.

Checks that all v6 files exist, JSON parses, cinematic fingerprint catalog
is well-formed, and v5 validator still passes.
"""
from __future__ import annotations
import json, sys, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors = []


def check_exists(rel):
    if not (ROOT / rel).exists():
        errors.append(f'missing: {rel}')
        return False
    return True


def check_json(rel):
    if not check_exists(rel):
        return None
    try:
        return json.loads((ROOT / rel).read_text(encoding='utf-8'))
    except Exception as e:
        errors.append(f'invalid JSON {rel}: {e}')
        return None


REQUIRED_DOCS = [
    'README_V6.md',
    'START_HERE_V6.md',
    'RELEASE_NOTES_V6.md',
    'docs/V6_OVERVIEW.md',
    'v6/CORE_DOCTRINE.md',
    'v6/MEDIA_DECISION_ENGINE.md',
    'v6/THREE_D_DIRECTOR.md',
    'v6/FRAME_SEQUENCE_DIRECTOR.md',
    'v6/CAMERA_DIRECTOR.md',
    'v6/BLENDER_WEB_PIPELINE.md',
    'v6/ASSET_DNA.md',
    'v6/PERFORMANCE_BUDGET_ENGINE.md',
    'v6/MOBILE_MEDIA_STRATEGY.md',
    'v6/CINEMATIC_ANTI_AI_FINGERPRINTS.md',
    'prompts/v6/MASTER_META_PROMPT_V6.md',
    'directors/v6/MEDIA_DIRECTOR.md',
    'directors/v6/CINEMATIC_QA_DIRECTOR.md',
    'quality/V6_CINEMATIC_GATES.md',
    'tools/v6/validate_v6.py',
    'examples/v6/media_decision_walkthrough.md',
]

REQUIRED_JSON = [
    'data/v6/media_decision_matrix.json',
    'data/v6/three_d_decision_matrix.json',
    'data/v6/cinematic_anti_ai_fingerprints.json',
    'data/v6/cinematic_profiles.json',
]

for rel in REQUIRED_DOCS:
    check_exists(rel)

for rel in REQUIRED_JSON:
    check_json(rel)

catalog = check_json('data/v6/cinematic_anti_ai_fingerprints.json')
if catalog:
    if 'fingerprints' not in catalog:
        errors.append('cinematic catalog: missing "fingerprints" key')
    else:
        seen_ids = set()
        valid_sevs = {'blocker', 'high', 'medium', 'low'}
        for i, fp in enumerate(catalog['fingerprints']):
            for k in ('id', 'category', 'title', 'severity', 'description', 'why_ai', 'detection', 'correction'):
                if k not in fp:
                    errors.append(f'cinematic fingerprint[{i}] missing {k}')
            fid = fp.get('id')
            if fid in seen_ids:
                errors.append(f'duplicate cinematic fingerprint id: {fid}')
            seen_ids.add(fid)
            if fp.get('severity') not in valid_sevs:
                errors.append(f'{fid}: invalid severity {fp.get("severity")}')

media = check_json('data/v6/media_decision_matrix.json')
if media:
    if 'medium_spectrum' not in media:
        errors.append('media decision matrix: missing "medium_spectrum"')
    if 'downgrade_chains' not in media:
        errors.append('media decision matrix: missing "downgrade_chains"')

profiles = check_json('data/v6/cinematic_profiles.json')
if profiles:
    for key in ('frame_sequence_profiles', 'camera_patterns', 'performance_budget_tiers', 'asset_fallback_hierarchy'):
        if key not in profiles:
            errors.append(f'cinematic profiles: missing "{key}"')

v5_validator = ROOT / 'tools/v5/validate_v5.py'
if v5_validator.exists():
    result = subprocess.run([sys.executable, str(v5_validator)], capture_output=True, text=True, cwd=str(ROOT))
    if result.returncode != 0:
        errors.append(f'v5 validator FAILED:\n{result.stdout}')
else:
    errors.append('v5 validator not found')

v4_validator = ROOT / 'tools/v4/validate_v4.py'
if v4_validator.exists():
    result = subprocess.run([sys.executable, str(v4_validator)], capture_output=True, text=True, cwd=str(ROOT))
    if result.returncode != 0:
        errors.append(f'v4 validator FAILED:\n{result.stdout}')

v32_validator = ROOT / 'tools/v3_2/validate_v3_2.py'
if v32_validator.exists():
    result = subprocess.run([sys.executable, str(v32_validator)], capture_output=True, text=True, cwd=str(ROOT))
    if result.returncode != 0:
        errors.append(f'v3.2 validator FAILED:\n{result.stdout}')

print(f'v6 required files: {len(REQUIRED_DOCS) + len(REQUIRED_JSON)}')
print(f'v6 errors: {len(errors)}')
for e in errors:
    print(f'  - {e}')
sys.exit(1 if errors else 0)
