from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.v7.install_codex_skill import install_skills


class SkillInstallTests(unittest.TestCase):
    def test_installs_main_skill_and_single_shortcut(self):
        with TemporaryDirectory() as workspace:
            root = Path(workspace)
            source = root / 'source'
            (source / 'skills' / 'crative-web').mkdir(parents=True)
            (source / 'SKILL.md').write_text('main', encoding='utf-8')
            (source / 'skills' / 'crative-web' / 'SKILL.md').write_text('shortcut', encoding='utf-8')
            (source / 'reference-engine').mkdir()
            (source / 'reference-engine' / 'README.md').write_text('reference', encoding='utf-8')

            skills_dir = root / 'installed'
            duplicate = skills_dir / 'creative-web-intelligence' / 'skills' / 'crative-web' / 'SKILL.md'
            duplicate.parent.mkdir(parents=True)
            duplicate.write_text('old shortcut', encoding='utf-8')

            main_skill, shortcut = install_skills(source, skills_dir)
            self.assertEqual((main_skill / 'SKILL.md').read_text(encoding='utf-8'), 'main')
            self.assertEqual((shortcut / 'SKILL.md').read_text(encoding='utf-8'), 'shortcut')
            self.assertEqual((main_skill / 'reference-engine' / 'README.md').read_text(encoding='utf-8'), 'reference')
            self.assertFalse(duplicate.exists())

    def test_rejects_installation_inside_source(self):
        with TemporaryDirectory() as workspace:
            source = Path(workspace)
            with self.assertRaises(ValueError):
                install_skills(source, source / 'skills')


if __name__ == '__main__':
    unittest.main()
