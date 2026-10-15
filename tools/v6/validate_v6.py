#!/usr/bin/env python3
"""v6 kataloglarını ve önceki sürümlerin doğrulayıcılarını denetler."""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIERS = ('lean', 'standard', 'rich', 'cinematic')
BUDGET_FIELDS = (
    'initial_payload_kb', 'total_page_media_mb', 'frame_sequences_kb',
    'glb_kb', 'texture_memory_mb', 'draw_calls', 'concurrent_animations',
)
REQUIRED_DOCS = [
    'README_V6.md', 'START_HERE_V6.md', 'RELEASE_NOTES_V6.md',
    'docs/V6_OVERVIEW.md', 'v6/CORE_DOCTRINE.md', 'v6/MEDIA_DECISION_ENGINE.md',
    'v6/THREE_D_DIRECTOR.md', 'v6/FRAME_SEQUENCE_DIRECTOR.md',
    'v6/CAMERA_DIRECTOR.md', 'v6/BLENDER_WEB_PIPELINE.md', 'v6/ASSET_DNA.md',
    'v6/PERFORMANCE_BUDGET_ENGINE.md', 'v6/MOBILE_MEDIA_STRATEGY.md',
    'v6/CINEMATIC_ANTI_AI_FINGERPRINTS.md', 'prompts/v6/MASTER_META_PROMPT_V6.md',
    'directors/v6/MEDIA_DIRECTOR.md', 'directors/v6/CINEMATIC_QA_DIRECTOR.md',
    'quality/V6_CINEMATIC_GATES.md', 'tools/v6/validate_v6.py',
    'examples/v6/media_decision_walkthrough.md', 'tools/v6/audit_media_plan.py',
    'tools/v6/README.md',
    'runtime/media/README.md', 'runtime/media/video-prompt.mjs',
    'runtime/media/source-selection.mjs', 'runtime/media/background-video.mjs',
    'runtime/media/sequence-manifest.mjs', 'tools/v6/creative_media.mjs',
    'tools/v6/video_to_web.py', 'source-intelligence/CREATIVE_COMPONENT_WORKFLOW.md',
    'source-intelligence/REACT_BITS_INTEGRATION.md', 'examples/v6/media-studio/index.html',
    'examples/v6/media-studio/studio.mjs', 'examples/v6/media-studio/style.css',
    'reference-engine/BRIEF_TO_REFERENCE.md', 'reference-recreation/REFERENCE_RECREATION_ENGINE.md',
    'reference-recreation/PIXEL_CLOSE_QA.md',
    'examples/v6/reference-first/reference-preview.html', 'examples/v6/reference-first/reference-note.md',
]
REQUIRED_JSON = [
    'data/v6/media_decision_matrix.json', 'data/v6/three_d_decision_matrix.json',
    'data/v6/cinematic_anti_ai_fingerprints.json', 'data/v6/cinematic_profiles.json',
    'schemas/v6/media_plan.schema.json', 'examples/v6/media_plan.json',
    'examples/v6/over_budget_media_plan.json',
    'data/v6/creative_sources.json',
]


class CatalogCheck:
    def __init__(self):
        self.errors = []

    def object(self, value, path):
        if not isinstance(value, dict) or not value:
            self.errors.append(f'{path}: boş olmayan bir nesne bekleniyor')
            return {}
        return value

    def array(self, value, path):
        if not isinstance(value, list) or not value:
            self.errors.append(f'{path}: boş olmayan bir liste bekleniyor')
            return []
        return value

    def text(self, value, path):
        if not isinstance(value, str) or not value.strip():
            self.errors.append(f'{path}: boş olmayan metin bekleniyor')
            return None
        return value

    def strings(self, value, path):
        entries = []
        for index, item in enumerate(self.array(value, path)):
            entry = self.text(item, f'{path}[{index}]')
            if entry is not None:
                if entry in entries:
                    self.errors.append(f'{path}: yinelenen değer: {entry}')
                entries.append(entry)
        return entries

    def records(self, value, path, id_key='id'):
        seen = set()
        entries = []
        for index, item in enumerate(self.array(value, path)):
            item_path = f'{path}[{index}]'
            entry = self.object(item, item_path)
            identifier = self.text(entry.get(id_key), f'{item_path}.{id_key}')
            if identifier is not None:
                if identifier in seen:
                    self.errors.append(f'{path}: yinelenen kimlik: {identifier}')
                seen.add(identifier)
            entries.append((entry, item_path))
        return entries

    def number(self, value, path, positive=False):
        try:
            valid = (type(value) in (int, float) and math.isfinite(value)
                     and value >= 0 and (not positive or value > 0))
        except OverflowError:
            valid = False
        if not valid:
            self.errors.append(f'{path}: geçersiz sayısal sınır: {value!r}')
            return False
        return True

    def references(self, value, path, medium_ids, skip=()):
        for name, chain in self.object(value, path).items():
            entries = self.strings(chain, f'{path}.{name}')
            if name not in skip:
                for medium in entries:
                    if medium not in medium_ids:
                        self.errors.append(f'{path}.{name}: bilinmeyen medya: {medium}')


def check_media(matrix, check):
    entries = check.records(matrix.get('medium_spectrum'), 'medium_spectrum')
    medium_ids = set()
    for medium, path in entries:
        if isinstance(medium.get('id'), str):
            medium_ids.add(medium['id'])
        for field in ('cost', 'when'):
            check.text(medium.get(field), f'{path}.{field}')
    for field in ('decision_steps', 'valid_purposes', 'invalid_purposes'):
        check.strings(matrix.get(field), field)
    for field in ('downgrade_chains', 'interaction_to_medium', 'camera_freedom_to_medium'):
        check.references(matrix.get(field), field, medium_ids)
    return medium_ids


def check_profiles(profiles, medium_ids, check):
    budgets = check.object(profiles.get('performance_budget_tiers'), 'performance_budget_tiers')
    for tier in TIERS:
        path = f'performance_budget_tiers.{tier}'
        limits = check.object(budgets.get(tier), path)
        for field in BUDGET_FIELDS:
            check.number(limits.get(field), f'{path}.{field}')
            if field in ('draw_calls', 'concurrent_animations') and type(limits.get(field)) is not int:
                check.errors.append(f'{path}.{field}: tam sayı bekleniyor')
    for tier in budgets.keys() - set(TIERS):
        check.errors.append(f'performance_budget_tiers: bilinmeyen katman: {tier}')

    mapping = check.object(profiles.get('mobile_tier_mapping'), 'mobile_tier_mapping')
    for desktop in TIERS:
        mobile = mapping.get(desktop)
        if not isinstance(mobile, str) or mobile not in TIERS:
            check.errors.append(f'mobile_tier_mapping.{desktop}: bilinmeyen katman: {mobile!r}')
        elif TIERS.index(mobile) > max(0, TIERS.index(desktop) - 1):
            check.errors.append(f'mobile_tier_mapping.{desktop}: mobil katman en az bir basamak düşmeli')
    for tier in mapping.keys() - set(TIERS):
        check.errors.append(f'mobile_tier_mapping: bilinmeyen masaüstü katmanı: {tier}')

    check.references(profiles.get('asset_fallback_hierarchy'), 'asset_fallback_hierarchy', medium_ids, skip=('image',))
    sequence = check.object(profiles.get('frame_sequence_profiles'), 'frame_sequence_profiles')
    for tier, path in check.records(sequence.get('tiers'), 'frame_sequence_profiles.tiers'):
        check.number(tier.get('frames_per_vh'), f'{path}.frames_per_vh', positive=True)
        check.text(tier.get('use_when'), f'{path}.use_when')
    check.strings(sequence.get('format_priority'), 'frame_sequence_profiles.format_priority')
    resolution = check.object(sequence.get('resolution'), 'frame_sequence_profiles.resolution')
    for device in ('desktop', 'tablet', 'mobile'):
        path = f'frame_sequence_profiles.resolution.{device}'
        dimensions = check.object(resolution.get(device), path)
        for field in ('width', 'dpr'):
            check.number(dimensions.get(field), f'{path}.{field}', positive=True)
    sequence_fields = {
        'transfer_limits': ('desktop_per_sequence_kb', 'mobile_per_sequence_kb'),
        'runtime_limits': ('decoded_frame_cache_mb', 'concurrent_sequences', 'first_meaningful_frame_ms'),
    }
    for section, fields in sequence_fields.items():
        path = f'frame_sequence_profiles.{section}'
        limits = check.object(sequence.get(section), path)
        for field in fields:
            check.number(limits.get(field), f'{path}.{field}')
    loading = check.object(sequence.get('loading_strategy'), 'frame_sequence_profiles.loading_strategy')
    check.number(loading.get('preload_window_frames'), 'loading_strategy.preload_window_frames')
    for field in ('poster_first', 'progressive_in_scroll_order', 'frame_skipping_on_fast_scroll', 'use_createImageBitmap'):
        if not isinstance(loading.get(field), bool):
            check.errors.append(f'loading_strategy.{field}: boolean bekleniyor')

    camera = check.object(profiles.get('camera_patterns'), 'camera_patterns')
    for move, path in check.records(camera.get('vocabulary'), 'camera_patterns.vocabulary', id_key='move'):
        check.text(move.get('communicates'), f'{path}.communicates')
        if 'max_arc_deg' in move:
            check.number(move['max_arc_deg'], f'{path}.max_arc_deg')
    for reject, path in check.records(camera.get('hard_rejects'), 'camera_patterns.hard_rejects'):
        for field in ('pattern', 'correction'):
            check.text(reject.get(field), f'{path}.{field}')
    scroll = check.object(camera.get('scroll_camera_rules'), 'camera_patterns.scroll_camera_rules')
    for field in ('max_total_rotation_deg', 'rest_within_timeline_pct'):
        check.number(scroll.get(field), f'camera_patterns.scroll_camera_rules.{field}')


def check_three_d(matrix, check):
    for field in ('justified_when', 'not_justified_when'):
        check.strings(matrix.get(field), f'three_d.{field}')
    choices = check.object(matrix.get('realtime_vs_prerendered'), 'three_d.realtime_vs_prerendered')
    for field in ('choose_realtime', 'choose_prerendered'):
        check.strings(choices.get(field), f'three_d.realtime_vs_prerendered.{field}')
    technologies = check.object(matrix.get('technology_selection'), 'three_d.technology_selection')
    for name, description in technologies.items():
        check.text(description, f'three_d.technology_selection.{name}')
    targets = check.object(matrix.get('optimization_targets'), 'three_d.optimization_targets')
    for field in ('glb_size_kb', 'texture_memory_mb', 'draw_calls', 'triangle_count'):
        path = f'three_d.optimization_targets.{field}'
        limits = check.object(targets.get(field), path)
        target_valid = check.number(limits.get('target'), f'{path}.target')
        limit_valid = check.number(limits.get('hard_limit'), f'{path}.hard_limit')
        if target_valid and limit_valid and limits['target'] > limits['hard_limit']:
            check.errors.append(f'{path}: hedef sert sınırı aşamaz')
    check.text(matrix.get('final_test'), 'three_d.final_test')


def check_schema(schema, matrix, check):
    definitions = check.object(schema.get('$defs'), 'schema.$defs')
    for name, expected in (
        ('tier', list(TIERS)),
        ('medium', [item.get('id') for item in matrix.get('medium_spectrum', []) if isinstance(item, dict)]
         if isinstance(matrix.get('medium_spectrum'), list) else []),
    ):
        definition = check.object(definitions.get(name), f'schema.$defs.{name}')
        values = check.strings(definition.get('enum'), f'schema.$defs.{name}.enum')
        if values != expected:
            check.errors.append(f'schema.$defs.{name}.enum: katalogla aynı sırada olmalı')
    moment = check.object(definitions.get('moment'), 'schema.$defs.moment')
    properties = check.object(moment.get('properties'), 'schema.$defs.moment.properties')
    purpose = check.object(properties.get('purpose'), 'schema.$defs.moment.properties.purpose')
    purposes = check.strings(purpose.get('enum'), 'schema.$defs.moment.properties.purpose.enum')
    expected_purposes = []
    for field in ('valid_purposes', 'invalid_purposes'):
        if isinstance(matrix.get(field), list):
            expected_purposes.extend(matrix[field])
    if purposes != expected_purposes:
        check.errors.append('schema purpose.enum: katalog amaçlarıyla aynı sırada olmalı')
    metrics = check.object(definitions.get('metrics'), 'schema.$defs.metrics')
    fields = check.object(metrics.get('properties'), 'schema.$defs.metrics.properties')
    required = check.strings(metrics.get('required'), 'schema.$defs.metrics.required')
    if set(fields) != set(BUDGET_FIELDS) or set(required) != set(BUDGET_FIELDS):
        check.errors.append('schema metrics: properties ve required yedi bütçe alanını içermeli')


def check_creative_sources(catalog, check):
    allowed_roles = {'hero', 'background', 'scroll', 'gallery', 'template', 'primitives'}
    identifiers = set()
    for source, path in check.records(catalog.get('sources'), 'creative_sources.sources'):
        identifier = source.get('id')
        if isinstance(identifier, str):
            identifiers.add(identifier)
        for field in ('name', 'url', 'license', 'licenseUrl', 'summary', 'acquisition', 'adaptation'):
            check.text(source.get(field), f'{path}.{field}')
        for field, allowed in [('roles', allowed_roles), ('frameworks', {'react', 'vanilla'})]:
            for choice in check.strings(source.get(field), f'{path}.{field}'):
                if choice not in allowed:
                    check.errors.append(f'{path}.{field}: bilinmeyen seçim: {choice}')
        redistribution = source.get('libraryRedistribution')
        if redistribution not in ('blocked', 'verify-per-item', 'license-notice'):
            check.errors.append(f'{path}.libraryRedistribution: geçersiz kullanım koşulu')
        if identifier == 'react-bits' and redistribution != 'blocked':
            check.errors.append('react-bits: kütüphane içinde yeniden dağıtım kapalı olmalı')
        if identifier == '21st' and source.get('access') != 'official-copy-prompt':
            check.errors.append('21st: resmi platform handoff yolu gerekli')
    if not {'react-bits', '21st', 'cwi-native'} <= identifiers:
        check.errors.append('creative_sources: temel kaynaklar eksik')


def check_catalogs(root=ROOT):
    root = Path(root)
    check = CatalogCheck()
    catalogs = {}
    for relative in REQUIRED_JSON:
        try:
            catalog = json.loads((root / relative).read_text(encoding='utf-8'))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            check.errors.append(f'{relative}: okunamadı: {error}')
            continue
        catalogs[Path(relative).stem] = check.object(catalog, relative)
        if relative.startswith('data/v6/') and isinstance(catalog, dict) and catalog.get('version') != '6.0':
            check.errors.append(f'{relative}: version alanı 6.0 olmalı')

    media = catalogs.get('media_decision_matrix')
    medium_ids = check_media(media, check) if media else set()
    profiles = catalogs.get('cinematic_profiles')
    if profiles:
        check_profiles(profiles, medium_ids, check)
    three_d = catalogs.get('three_d_decision_matrix')
    if three_d:
        check_three_d(three_d, check)
    fingerprints = catalogs.get('cinematic_anti_ai_fingerprints')
    if fingerprints:
        for fingerprint, path in check.records(fingerprints.get('fingerprints'), 'fingerprints'):
            for field in ('category', 'title', 'description', 'why_ai', 'correction'):
                check.text(fingerprint.get(field), f'{path}.{field}')
            severity = fingerprint.get('severity')
            if not isinstance(severity, str) or severity not in ('blocker', 'high', 'medium', 'low'):
                check.errors.append(f'{path}.severity: geçersiz önem derecesi')
            for signal, description in check.object(fingerprint.get('detection'), f'{path}.detection').items():
                check.text(description, f'{path}.detection.{signal}')
    schema = catalogs.get('media_plan.schema')
    if schema:
        check_schema(schema, media or {}, check)
    sources = catalogs.get('creative_sources')
    if sources:
        check_creative_sources(sources, check)
    return check.errors


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    errors = check_catalogs()
    errors.extend(f'Eksik dosya: {relative}' for relative in REQUIRED_DOCS if not (ROOT / relative).is_file())
    for relative in ('tools/v5/validate_v5.py', 'tools/v4/validate_v4.py', 'tools/v3_2/validate_v3_2.py'):
        validator = ROOT / relative
        if not validator.is_file():
            errors.append(f'Eksik doğrulayıcı: {relative}')
            continue
        completed = subprocess.run(
            [sys.executable, str(validator)], capture_output=True, text=True,
            encoding='utf-8', errors='replace', cwd=ROOT,
        )
        if completed.returncode:
            errors.append(f'{relative} başarısız:\n{completed.stdout}{completed.stderr}')
    print(f'v6 dosya sayısı: {len(REQUIRED_DOCS) + len(REQUIRED_JSON)}')
    print(f'v6 hata sayısı: {len(errors)}')
    for error in errors:
        print(f'  - {error}')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
