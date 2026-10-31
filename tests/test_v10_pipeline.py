"""build_from_reference ve check_site komut testleri."""

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_TOOL = ROOT / "tools" / "v10" / "build_from_reference.py"
CHECK_TOOL = ROOT / "tools" / "v10" / "check_site.py"
TEST_SITE = ROOT / "examples" / "v10" / "test-site"


class BuildFromReferenceDryRunTests(unittest.TestCase):
    def test_dry_run_shows_steps(self):
        r = subprocess.run(
            [sys.executable, "-I", str(BUILD_TOOL), "--dry-run", "https://www.example.com"],
            capture_output=True, encoding="utf-8", timeout=30)
        self.assertEqual(r.returncode, 0)
        self.assertIn("Pipeline", r.stdout)
        self.assertIn("wget", r.stdout)
        self.assertIn("font_coverage", r.stdout)

    def test_dry_run_with_content(self):
        r = subprocess.run(
            [sys.executable, "-I", str(BUILD_TOOL), "--dry-run",
             "https://www.example.com", "--content", "https://my-site.com"],
            capture_output=True, encoding="utf-8", timeout=30)
        self.assertEqual(r.returncode, 0)
        self.assertIn("content.json", r.stdout)

    def test_dry_run_without_content(self):
        r = subprocess.run(
            [sys.executable, "-I", str(BUILD_TOOL), "--dry-run", "https://www.example.com"],
            capture_output=True, encoding="utf-8", timeout=30)
        self.assertIn("atlanıyor", r.stdout)


class CheckSiteTests(unittest.TestCase):
    def test_check_site_no_write(self):
        r = subprocess.run(
            [sys.executable, "-I", str(CHECK_TOOL), str(TEST_SITE), "--no-write"],
            capture_output=True, encoding="utf-8", timeout=120)
        self.assertEqual(r.returncode, 0)
        self.assertIn("analyze_reference", r.stdout)
        self.assertIn("authenticity_check", r.stdout)
        self.assertIn("Kapsam ve sınırlar", r.stdout)

    def test_check_site_json_format(self):
        r = subprocess.run(
            [sys.executable, "-I", str(CHECK_TOOL), str(TEST_SITE), "--no-write", "--format", "json"],
            capture_output=True, encoding="utf-8", timeout=120)
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertIn("results", data)
        tools = [item["tool"] for item in data["results"]]
        self.assertIn("analyze_reference", tools)
        self.assertIn("authenticity_check", tools)

    def test_check_site_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "index.html").write_text(
                '<!doctype html><html lang="tr"><head><meta charset="utf-8">'
                '<title>Test</title></head><body><h1>Merhaba</h1></body></html>',
                encoding="utf-8")
            (site / "style.css").write_text("body { color: #000; background: #fff; }", encoding="utf-8")
            r = subprocess.run(
                [sys.executable, "-I", str(CHECK_TOOL), str(site)],
                capture_output=True, encoding="utf-8", timeout=120)
            self.assertTrue((site / "check-report.md").is_file())

    def test_check_nonexistent_target(self):
        r = subprocess.run(
            [sys.executable, "-I", str(CHECK_TOOL), "/nonexistent/path"],
            capture_output=True, encoding="utf-8", timeout=30)
        self.assertNotEqual(r.returncode, 0)


class BuildSpecMdTests(unittest.TestCase):
    def test_build_spec_md_format(self):
        sys.path.insert(0, str(ROOT / "tools" / "v10"))
        from build_from_reference import build_spec_md
        spec = {
            "reference": {"url": "https://example.com", "usage": "study-only",
                          "usageNote": "Lisans yok", "jsShell": True},
            "analysis": {"fonts": ["Inter", "Georgia"], "palette": ["#000", "#fff"],
                         "libraries": ["react"], "breakpoints": [768, 1024],
                         "ruleConflicts": ["CF-007: Inter başlık"]},
            "content": {"title": "Test", "lang": "tr", "blocks": [
                {"tag": "h1", "text": "Merhaba"}, {"tag": "p", "text": "Deneme"}],
                "links": [{"href": "https://x.com"}]},
            "fontChecks": [{"family": "Inter", "covers": True}],
            "fontStacks": [{"role": "display", "stack": "Georgia, serif"}],
            "nextSteps": ["Token uyarla", "Karşılaştır"],
            "skipped": [],
        }
        md = build_spec_md(spec)
        self.assertIn("# Build Spec", md)
        self.assertIn("study-only", md)
        self.assertIn("JS kabuk", md)
        self.assertIn("Inter", md)
        self.assertIn("Merhaba", md)
        self.assertIn("Sonraki adımlar", md)


if __name__ == "__main__":
    unittest.main()
