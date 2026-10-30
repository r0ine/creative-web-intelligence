#!/usr/bin/env python3
"""Kütüphanenin bütün doğrulayıcılarını tek komutla çalıştırır.

v10 doğrulayıcısı v9 → v8 → v7 → v6 → v5, v4, v3.2 zincirini kapsar; geri kalanlar burada eklenir.
"""

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    ('Markdown bağlantıları', 'tools/check_links.py'),
    ('v2 tarif ve uyumluluk grafiği', 'tools/validate_library.py'),
    ('v2 scroll tarifleri', 'tools/validate_scroll_library.py'),
    ('Harici kütüphane kaydı', 'tools/validate_external_registry.py'),
    ('v3', 'tools/v3/validate_v3_library.py'),
    ('v3.1', 'tools/v3_1/validate_v31.py'),
    ('v10 zinciri (v9, v8, v7, v6, v5, v4, v3.2)', 'tools/v10/validate_v10.py'),
)


def main():
    failed = []
    for label, script in CHECKS:
        print(f'\n== {label} ({script})', flush=True)
        started = time.monotonic()
        code = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=False).returncode
        print(f'-- {"GEÇTİ" if code == 0 else f"BAŞARISIZ (çıkış {code})"} · {time.monotonic() - started:.1f} sn', flush=True)
        if code:
            failed.append(label)
    print(f'\n{len(CHECKS) - len(failed)}/{len(CHECKS)} doğrulama geçti.')
    if failed:
        print('Başarısız: ' + ', '.join(failed), file=sys.stderr)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
