import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / 'tools/v6/validate_v6.py'
spec = importlib.util.spec_from_file_location('validate_v6', VALIDATOR)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

MEDIA = 'data/v6/media_decision_matrix.json'
PROFILES = 'data/v6/cinematic_profiles.json'
FINGERPRINTS = 'data/v6/cinematic_anti_ai_fingerprints.json'
THREE_D = 'data/v6/three_d_decision_matrix.json'
SCHEMA = 'schemas/v6/media_plan.schema.json'


class CatalogTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.originals = {}
        for relative in validator.REQUIRED_JSON:
            payload = json.loads((ROOT / relative).read_text(encoding='utf-8'))
            self.originals[relative] = payload
            self.write(relative, payload)

    def write(self, relative, payload):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding='utf-8')

    def changed(self, relative, path, replacement):
        payload = copy.deepcopy(self.originals[relative])
        if path:
            parent = payload
            for key in path[:-1]:
                parent = parent[key]
            parent[path[-1]] = replacement
        else:
            payload = replacement
        self.write(relative, payload)
        try:
            return validator.check_catalogs(self.root)
        finally:
            self.write(relative, self.originals[relative])

    def test_current_catalogs_pass(self):
        self.assertEqual([], validator.check_catalogs(self.root))

    def test_restricted_sources_cannot_be_marked_for_library_redistribution(self):
        errors = self.changed('data/v6/creative_sources.json', ('sources', 0, 'libraryRedistribution'), 'license-notice')
        self.assertTrue(any('react-bits' in error for error in errors))

    def test_21st_source_requires_official_platform_handoff(self):
        errors = self.changed('data/v6/creative_sources.json', ('sources', 1, 'access'), 'scrape')
        self.assertTrue(any('21st' in error for error in errors))

    def test_import_has_no_output_or_subprocess(self):
        imported = importlib.util.module_from_spec(spec)
        output = io.StringIO()
        with patch('subprocess.run') as run, contextlib.redirect_stdout(output):
            spec.loader.exec_module(imported)
        self.assertEqual('', output.getvalue())
        run.assert_not_called()

    def test_empty_and_wrong_root_types_fail(self):
        for relative in validator.REQUIRED_JSON:
            for invalid in ({}, [], None, True, 9, 'catalog'):
                with self.subTest(file=relative, invalid=invalid):
                    self.assertTrue(self.changed(relative, (), invalid))

    def test_invalid_json_is_reported(self):
        (self.root / MEDIA).write_text('{', encoding='utf-8')
        self.assertTrue(any(MEDIA in error for error in validator.check_catalogs(self.root)))

    def test_missing_file_is_reported(self):
        (self.root / THREE_D).unlink()
        self.assertTrue(any(THREE_D in error for error in validator.check_catalogs(self.root)))

    def test_wrong_nested_types_do_not_crash(self):
        fields = (
            (MEDIA, ('medium_spectrum',)), (MEDIA, ('downgrade_chains',)),
            (PROFILES, ('performance_budget_tiers',)), (PROFILES, ('mobile_tier_mapping',)),
            (PROFILES, ('frame_sequence_profiles',)), (PROFILES, ('camera_patterns',)),
            (FINGERPRINTS, ('fingerprints',)), (THREE_D, ('optimization_targets',)),
            (SCHEMA, ('$defs',)),
        )
        for relative, path in fields:
            for invalid in ([], {}, None, True, 'invalid', 4):
                with self.subTest(file=relative, path=path, invalid=invalid):
                    self.assertTrue(self.changed(relative, path, invalid))

    def test_empty_lists_and_nonobject_records_fail(self):
        for relative, path in (
            (MEDIA, ('medium_spectrum',)), (FINGERPRINTS, ('fingerprints',)),
            (PROFILES, ('camera_patterns', 'vocabulary')),
            (PROFILES, ('frame_sequence_profiles', 'tiers')),
        ):
            for invalid in ([], [None], ['entry'], [True], [[]]):
                with self.subTest(file=relative, path=path, invalid=invalid):
                    self.assertTrue(self.changed(relative, path, invalid))

    def test_duplicate_ids_fail(self):
        for relative, path in (
            (MEDIA, ('medium_spectrum',)), (FINGERPRINTS, ('fingerprints',)),
            (PROFILES, ('camera_patterns', 'vocabulary')),
            (PROFILES, ('camera_patterns', 'hard_rejects')),
            (PROFILES, ('frame_sequence_profiles', 'tiers')),
        ):
            entries = self.originals[relative]
            for field in path:
                entries = entries[field]
            with self.subTest(file=relative, path=path):
                errors = self.changed(relative, path, entries + [entries[0]])
                self.assertTrue(any('yinelenen kimlik' in error for error in errors))

    def test_unhashable_identifiers_fail_without_exception(self):
        for relative, collection in ((MEDIA, 'medium_spectrum'), (FINGERPRINTS, 'fingerprints')):
            for invalid in ({'id': 1}, [1], None):
                with self.subTest(file=relative, invalid=invalid):
                    self.assertTrue(self.changed(relative, (collection, 0, 'id'), invalid))

    def test_unknown_media_references_fail(self):
        for relative, path in (
            (MEDIA, ('downgrade_chains', '3d')),
            (MEDIA, ('interaction_to_medium', 'view_only')),
            (MEDIA, ('camera_freedom_to_medium', 'fixed_camera_path')),
            (PROFILES, ('asset_fallback_hierarchy', '3d')),
        ):
            with self.subTest(file=relative, path=path):
                errors = self.changed(relative, path, ['unknown-medium'])
                self.assertTrue(any('bilinmeyen medya' in error for error in errors))

    def test_image_formats_are_not_media_references(self):
        errors = self.changed(PROFILES, ('asset_fallback_hierarchy', 'image'), ['avif', 'webp', 'jpeg'])
        self.assertEqual([], errors)

    def test_invalid_budget_values_fail(self):
        for field in validator.BUDGET_FIELDS:
            for invalid in (-1, True, False, '2', None, float('nan'), float('inf'), 10 ** 400):
                with self.subTest(field=field, invalid=invalid):
                    errors = self.changed(PROFILES, ('performance_budget_tiers', 'rich', field), invalid)
                    self.assertTrue(any(field in error for error in errors))

    def test_fractional_runtime_counts_fail(self):
        for field in ('draw_calls', 'concurrent_animations'):
            with self.subTest(field=field):
                self.assertTrue(self.changed(PROFILES, ('performance_budget_tiers', 'rich', field), 1.5))

    def test_invalid_mobile_mappings_fail(self):
        for desktop, mobile in (('rich', 'rich'), ('standard', 'rich'), ('lean', 'standard'),
                                ('cinematic', 'unknown'), ('rich', []), ('rich', True)):
            with self.subTest(desktop=desktop, mobile=mobile):
                errors = self.changed(PROFILES, ('mobile_tier_mapping', desktop), mobile)
                self.assertTrue(any('mobile_tier_mapping' in error for error in errors))

    def test_more_conservative_mobile_mapping_passes(self):
        self.assertEqual([], self.changed(PROFILES, ('mobile_tier_mapping', 'rich'), 'lean'))

    def test_missing_tier_and_missing_budget_fail(self):
        profiles = copy.deepcopy(self.originals[PROFILES])
        del profiles['performance_budget_tiers']['standard']
        del profiles['performance_budget_tiers']['rich']['glb_kb']
        del profiles['mobile_tier_mapping']['lean']
        errors = self.changed(PROFILES, (), profiles)
        for field in ('performance_budget_tiers.standard', 'rich.glb_kb', 'mobile_tier_mapping.lean'):
            self.assertTrue(any(field in error for error in errors))

    def test_invalid_three_d_targets_fail(self):
        for limits in ({'target': 6000, 'hard_limit': 5000}, {'target': True, 'hard_limit': 5000},
                       {'target': 2000, 'hard_limit': -1}, []):
            with self.subTest(limits=limits):
                self.assertTrue(self.changed(THREE_D, ('optimization_targets', 'glb_size_kb'), limits))

    def test_invalid_sequence_limits_fail(self):
        for path in (
            ('frame_sequence_profiles', 'resolution', 'mobile', 'width'),
            ('frame_sequence_profiles', 'transfer_limits', 'mobile_per_sequence_kb'),
            ('frame_sequence_profiles', 'runtime_limits', 'decoded_frame_cache_mb'),
        ):
            with self.subTest(path=path):
                self.assertTrue(self.changed(PROFILES, path, -1))

    def test_schema_enum_drift_fails(self):
        for path in (('$defs', 'tier', 'enum'), ('$defs', 'medium', 'enum'),
                     ('$defs', 'moment', 'properties', 'purpose', 'enum')):
            with self.subTest(path=path):
                self.assertTrue(self.changed(SCHEMA, path, ['unknown']))

    def test_schema_metric_drift_fails(self):
        for path, replacement in (
            (('$defs', 'metrics', 'properties'), {'initial_payload_kb': {'type': 'number'}}),
            (('$defs', 'metrics', 'required'), ['initial_payload_kb']),
        ):
            with self.subTest(path=path):
                self.assertTrue(self.changed(SCHEMA, path, replacement))


if __name__ == '__main__':
    unittest.main()
