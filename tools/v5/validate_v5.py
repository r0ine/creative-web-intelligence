#!/usr/bin/env python3
"""CWI v5 structural validator.

Checks that all v5 doctrine and data files exist, that JSON files parse, and
that the authenticity_fingerprints.json catalog is well-formed.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors = []


def check_exists(rel):
    p = ROOT / rel
    if not p.exists():
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
    'README_V5.md',
    'START_HERE_V5.md',
    'RELEASE_NOTES_V5.md',
    'docs/V5_OVERVIEW.md',
    'v5/CORE_DOCTRINE.md',
    'v5/DIVIDER_POLICY.md',
    'v5/ANTI_AI_VISUAL_FINGERPRINTS.md',
    'v5/MOTION_GRAMMAR_V2.md',
    'v5/COMPOSITION_RESTRAINT.md',
    'v5/TYPOGRAPHY_FIRST_PREMIUM.md',
    'v5/DECORATION_VS_STRUCTURE.md',
    'v5/REST_ZONES.md',
    'v5/COLOR_RESTRAINT.md',
    'v5/QA_VISUAL_AUTHENTICITY.md',
    'prompts/v5/MASTER_META_PROMPT_V5.md',
    'prompts/v5/AUTHENTICITY_AUDIT_PROMPT.md',
    'directors/v5/AUTHENTICITY_DIRECTOR.md',
    'directors/v5/COMPOSITION_DIRECTOR_V5.md',
    'directors/v5/MOTION_DIRECTOR_V5.md',
    'directors/v5/QA_DIRECTOR_V5.md',
    'quality/V5_AUTHENTICITY_GATE.md',
    'tools/v5/authenticity_check.py',
    'tools/v5/validate_v5.py',
    'examples/v5/before_after_notes.md',
    'examples/v5/refactored_landing_spec.json',
]

REQUIRED_JSON = [
    'data/v5/authenticity_fingerprints.json',
    'data/v5/divider_decision_matrix.json',
    'data/v5/composition_restraint_checks.json',
    'data/v5/motion_grammar_v2_rules.json',
    'data/v5/rest_zone_recipes.json',
    'data/v5/decoration_vs_structure_tests.json',
]


for rel in REQUIRED_DOCS:
    check_exists(rel)

for rel in REQUIRED_JSON:
    check_json(rel)

catalog = check_json('data/v5/authenticity_fingerprints.json')
if catalog:
    if 'fingerprints' not in catalog:
        errors.append('catalog: missing "fingerprints" key')
    else:
        seen_ids = set()
        valid_sevs = {'blocker', 'high', 'medium', 'low'}
        for i, fp in enumerate(catalog['fingerprints']):
            for k in ('id', 'category', 'title', 'severity', 'description', 'why_ai', 'detection', 'correction'):
                if k not in fp:
                    errors.append(f'fingerprint[{i}] missing {k}')
            fid = fp.get('id')
            if fid in seen_ids:
                errors.append(f'duplicate fingerprint id: {fid}')
            seen_ids.add(fid)
            if fp.get('severity') not in valid_sevs:
                errors.append(f'{fid}: invalid severity {fp.get("severity")}')

divider = check_json('data/v5/divider_decision_matrix.json')
if divider:
    if 'hierarchy' not in divider:
        errors.append('divider matrix: missing "hierarchy" key')
    else:
        priorities = [h.get('priority') for h in divider['hierarchy']]
        if priorities != list(range(1, len(priorities) + 1)):
            errors.append(f'divider matrix: priorities not sequential 1..N: {priorities}')

motion = check_json('data/v5/motion_grammar_v2_rules.json')
if motion:
    if len(motion.get('blockers', [])) < 5:
        errors.append('motion rules: expected at least 5 hard blockers (MG-B01..B05)')

print(f'v5 required files: {len(REQUIRED_DOCS) + len(REQUIRED_JSON)}')
print(f'v5 errors: {len(errors)}')
for e in errors:
    print(f'  - {e}')
sys.exit(1 if errors else 0)
