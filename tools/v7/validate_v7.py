#!/usr/bin/env python3
"""v7 girişlerini ve eski sürümün doğrulayıcısını çalıştırır."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = (
    'START_HERE_V7.md', 'README_V7.md', 'RELEASE_NOTES_V7.md',
    'README.en.md', 'RELEASE_NOTES_V7.en.md',
    'docs/INSTALL_TR.md', 'docs/INSTALL_EN.md',
    'runtime/reference/pixel-compare.mjs',
    'examples/v7/reference-compare/index.html',
    'examples/v7/reference-compare/style.css',
    'examples/v7/reference-compare/app.mjs',
    'tests/pixel-compare.test.mjs',
    'quality/V7_VISUAL_CALIBRATION.md',
    'tools/v7/audit_visual_defaults.mjs',
    'tools/v7/install_codex_skill.py',
    'tests/visual-defaults.test.mjs',
    'tests/test_skill_install.py',
)


def main():
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        for path in missing:
            print(f'Eksik v7 dosyası: {path}', file=sys.stderr)
        return 1

    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    if manifest.get('version') not in {'7.0', '8.0'} or not manifest.get('v7'):
        print('manifest.json v7 bilgisi eksik.', file=sys.stderr)
        return 1

    for command in (
        [sys.executable, str(ROOT / 'tools/v6/validate_v6.py')],
        ['node', '--test', str(ROOT / 'tests/pixel-compare.test.mjs')],
        ['node', '--test', str(ROOT / 'tests/visual-defaults.test.mjs')],
        ['node', str(ROOT / 'tools/v7/audit_visual_defaults.mjs'), str(ROOT / 'examples/v7/reference-compare')],
    ):
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            return result.returncode

    print('v7 doğrulaması geçti.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
