import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("feedback_triage", ROOT / "tools/v9/feedback_triage.py")
TRIAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TRIAGE)


def run(text, answer=None):
    result = TRIAGE.analyse(text, answer)
    return result, [t["id"] for t in result["targets"]], [p["id"] for p in result["preserve"]]


class VagueFeedbackTests(unittest.TestCase):
    def test_vague_feedback_asks_where_before_changing_anything(self):
        result, targets, _ = run("içime sinmemiş")
        self.assertEqual(result["mode"], "ask-location")
        self.assertEqual(targets, [])
        self.assertEqual(result["questions"][0]["text"], "Neresi içine sinmedi?")
        options = result["questions"][0]["options"]
        self.assertEqual(options[0], "Arka plan ve zemin")
        self.assertIn(TRIAGE.GLOBAL_OPTION, options)

    def test_spelling_and_case_variants_are_equivalent(self):
        for text in ("içime sinmedi", "İÇİME SİNMEDİ", "icime sinmedi", "Içime sinmiyor", "doesn't feel right"):
            with self.subTest(text=text):
                self.assertEqual(run(text)[0]["mode"], "ask-location")

    def test_global_answer_starts_with_most_visible_surfaces(self):
        result, targets, _ = run("içime sinmedi", answer="genel")
        self.assertEqual(result["mode"], "global")
        self.assertEqual(targets, ["background", "hero", "palette"])
        self.assertEqual(result["questions"], [])

    def test_location_answer_focuses_only_that_surface(self):
        result, targets, _ = run("içime sinmedi", answer="arka plan")
        self.assertEqual((result["mode"], targets), ("located", ["background"]))

    def test_liked_part_before_but_is_preserved_and_skipped(self):
        result, targets, preserve = run("renkler güzel ama genel olarak olmamış")
        self.assertEqual(result["mode"], "global")
        self.assertEqual(preserve, ["palette"])
        self.assertNotIn("palette", targets)
        self.assertEqual(targets[:2], ["background", "hero"])

    def test_mixed_sentence_splits_keep_and_change(self):
        result, targets, preserve = run("başlık güzel, arka plan kalsın ama kartlar kalabalık")
        self.assertEqual(result["mode"], "located")
        self.assertEqual(targets, ["surfaces"])
        self.assertEqual(preserve, ["display-type", "background"])

    def test_negated_praise_is_not_treated_as_approval(self):
        for text in ("arka plan güzel değil", "arka plan iyi olmamış", "I don't like the background"):
            with self.subTest(text=text):
                result, targets, preserve = run(text)
                self.assertEqual((result["mode"], targets, preserve), ("located", ["background"], []))
        self.assertEqual(run("güzel olmamış")[0]["mode"], "ask-location")

    def test_colour_word_after_a_surface_is_an_attribute(self):
        self.assertEqual(run("arka plan rengi olmamış")[1], ["background"])
        self.assertEqual(run("başlık rengi soluk")[1], ["display-type"])
        self.assertEqual(run("renkler olmamış")[1], ["palette"])


class DirectionAndRevertTests(unittest.TestCase):
    def test_direction_without_location_asks_with_likely_surfaces(self):
        result, targets, _ = run("ucuz duruyor")
        self.assertEqual(result["mode"], "direction")
        self.assertEqual([d["id"] for d in result["directions"]], ["FB-02"])
        self.assertEqual(targets, ["palette", "display-type", "imagery"])
        self.assertEqual(result["questions"][0]["text"], "Bu his en çok nerede?")

    def test_global_direction_keeps_visibility_order_within_relevant_surfaces(self):
        _, targets, _ = run("genel olarak ucuz duruyor")
        self.assertEqual(targets, ["palette", "display-type", "imagery"])

    def test_revert_is_not_confused_with_dated_style(self):
        for text in ("eskisi daha iyiydi", "eski haline döndür", "geri al"):
            with self.subTest(text=text):
                self.assertEqual(run(text)[0]["mode"], "revert")
        result = run("eski moda duruyor")[0]
        self.assertEqual(result["mode"], "direction")
        self.assertEqual(result["matched"][0]["id"], "FB-10")

    def test_ai_generic_phrase_is_read_as_one_unit(self):
        result = run("AI gibi duruyor, her yerde var bu tasarım")[0]
        self.assertEqual([m["id"] for m in result["matched"]], ["FB-05"])
        self.assertEqual(result["mode"], "direction")


class OutcomeTests(unittest.TestCase):
    def test_approval_changes_nothing(self):
        for text in ("içime sindi, güzel olmuş", "arka plan güzel"):
            with self.subTest(text=text):
                result = run(text)[0]
                self.assertEqual((result["mode"], result["questions"], result["targets"]), ("approved", [], []))

    def test_unknown_text_asks_a_single_question(self):
        result = run("merhaba")[0]
        self.assertEqual(result["mode"], "unclear")
        self.assertEqual(len(result["questions"]), 1)

    def test_never_more_than_three_questions_and_always_report_files(self):
        samples = ("içime sinmedi", "ucuz", "geri al", "merhaba", "genel", "kartlar kalabalık", "arka plan güzel")
        for text in samples:
            with self.subTest(text=text):
                result = run(text)[0]
                self.assertLessEqual(len(result["questions"]), TRIAGE.MAX_QUESTIONS)
                self.assertIn("dosya yollarını", result["plan"][-1])

    def test_cli_text_output(self):
        import contextlib
        import io
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            self.assertEqual(TRIAGE.main(["içime", "sinmedi", "--answer", "genel"]), 0)
        self.assertIn("Mod: global", buffer.getvalue())
        self.assertIn("Arka plan ve zemin", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
