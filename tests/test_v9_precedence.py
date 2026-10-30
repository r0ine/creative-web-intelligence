import contextlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load("validate_v9", "tools/v9/validate_v9.py")
PRECEDENCE = load("precedence", "tools/v9/precedence.py")
IGNORED = shutil.ignore_patterns(".git", "examples", "runtime", "node_modules", "__pycache__", "tests", "tools")


class RepositoryStateTests(unittest.TestCase):
    def test_repository_has_no_feedback_or_precedence_errors(self):
        self.assertEqual(VALIDATOR.check_feedback(), [])
        self.assertEqual(VALIDATOR.check_precedence(), [])

    def test_every_superseded_director_points_to_its_winner(self):
        register = PRECEDENCE.load()
        for domain in register["domains"]:
            for path in domain["superseded"]:
                with self.subTest(path=path):
                    lines = PRECEDENCE.describe_file(path, register)
                    self.assertIn(domain["winner"], lines[0])

    def test_record_lookup_reports_conflict_and_resolution(self):
        register = PRECEDENCE.load()
        lines = PRECEDENCE.describe_record("font-029", register)
        self.assertTrue(lines[0].startswith("CF-007"))
        self.assertIn("Mono", lines[1])
        self.assertIn("bilinen bir çakışmada yok", PRECEDENCE.describe_record("scroll-001", register)[0])

    def test_all_open_conflicts_currently_affect_records(self):
        register = PRECEDENCE.load()
        for conflict in register["conflicts"]:
            with self.subTest(conflict=conflict["id"]):
                self.assertTrue(PRECEDENCE.affected(conflict))

    def test_cli_domain_lookup(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            self.assertEqual(PRECEDENCE.main(["--domain", "motion"]), 0)
        self.assertIn("directors/v5/MOTION_DIRECTOR_V5.md", buffer.getvalue())
        self.assertIn("yerini aldı: directors/motion/MOTION_DIRECTOR.md", buffer.getvalue())


class GrowthGuardTests(unittest.TestCase):
    """Kütüphane büyürken eklenen çelişkili içeriğin doğrulayıcıda yakalandığını sınar."""

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.root = Path(self.scratch.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=IGNORED)

    def tearDown(self):
        self.scratch.cleanup()

    def edit_json(self, relative, change):
        path = self.root / relative
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def replace(self, relative, old, new):
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def assert_error(self, errors, fragment):
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_unregistered_new_director_fails(self):
        (self.root / "directors/v9").mkdir(parents=True)
        (self.root / "directors/v9/LAYOUT_DIRECTOR.md").write_text("# LAYOUT DIRECTOR\n", encoding="utf-8")
        self.assert_error(VALIDATOR.check_precedence(self.root), "directors/v9/LAYOUT_DIRECTOR.md: director öncelik kaydında")

    def test_superseded_director_without_pointer_fails(self):
        self.replace("directors/motion/MOTION_DIRECTOR.md", "Öncelik (v9)", "Not")
        self.assert_error(VALIDATOR.check_precedence(self.root), "directors/motion/MOTION_DIRECTOR.md: başında geçerli dosyayı")

    def test_new_catalog_reusing_an_existing_id_fails(self):
        target = self.root / "data/v9/new_catalog.json"
        target.write_text(json.dumps({"version": "9.0", "items": [{"id": "font-001"}]}), encoding="utf-8")
        self.assert_error(VALIDATOR.check_precedence(self.root), "kimlik çakışması: 'font-001'")

    def test_fixed_old_data_must_be_marked_resolved(self):
        old = "cubic-bezier(0.34, 1.56, 0.64, 1)"
        self.replace("directors/v5/MOTION_DIRECTOR_V5.md", old, "cubic-bezier(0.22, 1, 0.36, 1)")
        self.assert_error(VALIDATOR.check_precedence(self.root), "CF-008: eski taraf artık")

        def resolve(data):
            next(c for c in data["conflicts"] if c["id"] == "CF-008")["status"] = "resolved"
        self.edit_json("data/v9/rule_precedence.json", resolve)
        self.assertEqual(VALIDATOR.check_precedence(self.root), [])

    def test_removed_newer_evidence_fails(self):
        self.replace("v6/ASSET_DNA.md", "No bounce, no overshoot", "Bounce is fine")
        self.assert_error(VALIDATOR.check_precedence(self.root), "CF-008: yeni taraftaki kanıt")

    def test_same_feedback_phrase_with_two_meanings_fails(self):
        def duplicate(data):
            next(e for e in data["entries"] if e["id"] == "FB-03")["phrases"].append("Ucuz*")
        self.edit_json("data/v9/feedback_lexicon.json", duplicate)
        self.assert_error(VALIDATOR.check_feedback(self.root), "iki anlama bağlı")

    def test_phrase_containing_a_contrast_word_fails(self):
        def add(data):
            data["entries"][0]["phrases"].append("güzel ama değil")
        self.edit_json("data/v9/feedback_lexicon.json", add)
        self.assert_error(VALIDATOR.check_feedback(self.root), "bağlaç içeriyor")

    def test_direction_pointing_to_unknown_surface_fails(self):
        def add(data):
            data["entries"][1]["likelySurfaces"].append("sidebar")
        self.edit_json("data/v9/feedback_lexicon.json", add)
        self.assert_error(VALIDATOR.check_feedback(self.root), "bilinmeyen yüzey sidebar")


if __name__ == "__main__":
    unittest.main()
