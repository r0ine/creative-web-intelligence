#!/usr/bin/env python3
"""Depodaki Markdown dosyalarında kırık göreli bağlantıları bulur."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r'^(```|~~~).*?^\1', re.S | re.M)
LINK = re.compile(r'\]\(<?([^)\s>]+)>?(?:\s+"[^"]*")?\)')


def markdown_files():
    try:
        listed = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '*.md'], cwd=ROOT, capture_output=True,
                                text=True, check=True).stdout.split()
        return [ROOT / name for name in listed]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in ROOT.rglob('*.md') if '.git' not in p.parts and 'node_modules' not in p.parts]


def broken_links(path):
    text = FENCE.sub('', path.read_text(encoding='utf-8'))
    for target in LINK.findall(text):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
            continue
        relative = target.split('#', 1)[0].split('?', 1)[0]
        if relative and not (path.parent / relative).exists():
            yield target


def main():
    problems = [(p.relative_to(ROOT).as_posix(), t) for p in markdown_files() for t in broken_links(p)]
    for source, target in problems:
        print(f'{source}: {target}', file=sys.stderr)
    print(f'Markdown bağlantı denetimi: {len(problems)} kırık bağlantı.')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
