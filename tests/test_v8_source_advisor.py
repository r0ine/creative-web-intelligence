import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("source_advisor", ROOT / "tools/v8/source_advisor.py")
ADVISOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADVISOR)


class SourceAdvisorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources, cls.findings = ADVISOR.load_catalog()

    def test_every_requested_source_has_profile(self):
        self.assertEqual(len(self.sources), 46)
        self.assertEqual(sum(s["kind"] == "repository" for s in self.sources.values()), 41)
        self.assertEqual(sum(s["access"] == "unverified" for s in self.sources.values()), 2)

    def test_next_3d_recommendation_is_one_reference_and_compatible_pair(self):
        result = ADVISOR.recommend(self.sources, self.findings, "portfolio", "next", "3d")
        self.assertIsNotNone(result["firstReference"])
        support = {item["id"] for item in result["supportingStudies"]}
        self.assertEqual(support, {"pmndrs/react-three-fiber", "pmndrs/drei"})
        self.assertFalse(any(issue["code"] == "missing-3d-renderer" for issue in result["conflicts"]))

    def test_two_motion_engines_and_two_ui_foundations_conflict(self):
        ids = ["greensock/gsap", "framer/motion", "shadcn-ui/ui", "saadeghi/daisyui"]
        issues = ADVISOR.conflicts([self.sources[sid] for sid in ids], "react")
        codes = {issue["code"] for issue in issues}
        self.assertIn("multiple-motion-owners", codes)
        self.assertIn("multiple-ui-foundations", codes)
        self.assertIn("custom-license-review", codes)

    def test_multiple_site_shells_and_gpl_are_exposed(self):
        ids = ["gothsec/dark-minimal", "surjithctly/astroship"]
        issues = ADVISOR.conflicts([self.sources[sid] for sid in ids], "astro")
        self.assertIn("multiple-shells", {issue["code"] for issue in issues})
        self.assertIn("copyleft-review", {issue["code"] for issue in issues})

    def test_drei_without_renderer_is_blocked(self):
        issues = ADVISOR.conflicts([self.sources["pmndrs/drei"]], "react")
        self.assertIn("missing-3d-renderer", {issue["code"] for issue in issues})

    def test_unavailable_source_is_never_selected(self):
        result = ADVISOR.recommend(self.sources, self.findings, "portfolio", "react", "none")
        self.assertNotEqual(result["firstReference"]["id"], "javascript-mastery-pro/threejs-portfolio")
        card = ADVISOR.source_brief(self.sources["aceternity/aceternity-ui"], self.findings)
        self.assertEqual(card["access"], "unverified")
        self.assertEqual(card["reuse"], "blocked-until-license-verified")

    def test_non_react_3d_does_not_add_react_renderer(self):
        result = ADVISOR.recommend(self.sources, self.findings, "landing", "astro", "3d")
        self.assertEqual(result["supportingStudies"], [])
        self.assertTrue(any("runtime/three" in step for step in result["workflow"]))


if __name__ == "__main__":
    unittest.main()
