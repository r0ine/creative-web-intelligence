import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True,
                          encoding='utf-8', errors='replace', timeout=60, check=False)


class LegacyToolSmokeTests(unittest.TestCase):
    def test_compose_spec_builds_spec_from_brief(self):
        result = run('tools/compose_spec.py', 'editorial portfolio with webgl product sahne')
        self.assertEqual(result.returncode, 0, result.stderr)
        spec = json.loads(result.stdout)
        for key in ('typography', 'composition', 'motion'):
            self.assertTrue(spec[key]['id'])
        self.assertIsNotNone(spec['three'])

    def test_compose_spec_is_deterministic_and_skips_3d_without_cue(self):
        first = run('tools/compose_spec.py', 'quiet editorial studio')
        second = run('tools/compose_spec.py', 'quiet editorial studio')
        self.assertEqual(first.stdout, second.stdout)
        self.assertIsNone(json.loads(first.stdout)['three'])

    def test_compose_spec_without_brief_prints_usage(self):
        result = run('tools/compose_spec.py')
        self.assertEqual(result.returncode, 2)
        self.assertIn('usage', result.stdout)

    def test_search_tools_return_hits(self):
        for args, expected in (
            (('tools/search_capabilities.py', 'editorial'), 'font-'),
            (('tools/search_scroll_recipes.py', 'pin'), 'scroll-'),
            (('tools/v3_1/query_recipes.py', 'variable'), '::'),
            (('tools/select_external_library.py', 'scroll'), ''),
        ):
            with self.subTest(args=args):
                result = run(*args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(expected, result.stdout)
                self.assertTrue(result.stdout.strip())

    def test_link_checker_passes_on_repository(self):
        result = run('tools/check_links.py')
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
