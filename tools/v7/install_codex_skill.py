#!/usr/bin/env python3
"""Kütüphaneyi ve /crative-web kısayolunu Codex becerilerine kurar."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def install_skills(source_root: Path, skills_dir: Path) -> tuple[Path, Path]:
    source_root = source_root.resolve()
    skills_dir = skills_dir.resolve()
    if skills_dir == source_root or source_root in skills_dir.parents:
        raise ValueError('Beceri dizini kaynak deponun içinde olamaz.')

    main_skill = skills_dir / 'creative-web-intelligence'
    shortcut = skills_dir / 'crative-web'

    def omit_nested_shortcut(directory: str, names: list[str]) -> set[str]:
        excluded = {name for name in names if name in {'.git', '__pycache__', 'node_modules'}}
        if Path(directory).resolve() == source_root:
            excluded.add('skills')
        return excluded

    shutil.copytree(source_root, main_skill, dirs_exist_ok=True, ignore=omit_nested_shortcut)
    duplicate = main_skill / 'skills' / 'crative-web' / 'SKILL.md'
    if duplicate.is_file():
        duplicate.unlink()

    shortcut.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_root / 'skills' / 'crative-web' / 'SKILL.md', shortcut / 'SKILL.md')
    return main_skill, shortcut


def main() -> int:
    parser = argparse.ArgumentParser(description='Creative Web Intelligence becerilerini Codex içine kurar.')
    parser.add_argument('--skills-dir', type=Path, default=Path.home() / '.codex' / 'skills',
                        help='Codex becerilerinin bulunduğu dizin')
    args = parser.parse_args()
    main_skill, shortcut = install_skills(ROOT, args.skills_dir)
    print(f'Kütüphane: {main_skill}')
    print(f'Kısayol: {shortcut}')
    print('Yeni sohbette /crative-web ardından tasarım isteğini yaz.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
