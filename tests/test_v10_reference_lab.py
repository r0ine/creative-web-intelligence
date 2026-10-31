import functools
import importlib.util
import json
import shutil
import tempfile
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/reference-site"


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MIRROR = load("mirror_reference", "tools/v10/mirror_reference.py")
ANALYZE = load("analyze_reference", "tools/v10/analyze_reference.py")
CATALOG = load("template_catalog", "tools/v10/template_catalog.py")
CONTENT = load("extract_content", "tools/v10/extract_content.py")


class MirrorCommandTests(unittest.TestCase):
    def test_command_keeps_user_flags_and_adds_limits(self):
        command = MIRROR.build_command("https://www.orneksite.com", Path("ws/site"), level=3, quota_mb=50, wait=0.5)
        for flag in ("--mirror", "--convert-links", "--adjust-extension", "--page-requisites", "--no-parent",
                     "--level=3", "--quota=50m", "--wait=0.5", "--random-wait"):
            self.assertIn(flag, command)
        self.assertEqual(command[-1], "https://www.orneksite.com")
        self.assertFalse(any("robots=off" in part for part in command), "robots.txt kuralına uyulmalı")
        self.assertNotIn("--span-hosts", command)

    def test_extra_asset_domains_are_explicit(self):
        command = MIRROR.build_command("https://site.com", Path("ws/site"), allow_domains=["cdn.site.com"])
        self.assertIn("--span-hosts", command)
        self.assertIn("--domains=site.com,cdn.site.com", command)

    def test_wget_log_failures_are_explained(self):
        self.assertEqual(len(MIRROR.diagnose("Proxy tunneling failed: Forbidden")), 1)
        self.assertIn("429", MIRROR.diagnose("ERROR 429: Too Many Requests.")[0])
        self.assertIn("Kota", MIRROR.diagnose("Download quota of 200M EXCEEDED!")[0])
        self.assertEqual(MIRROR.diagnose("Saving to: 'index.html'"), [])

    def test_only_http_urls_are_accepted(self):
        self.assertEqual(MIRROR.validate_url("https://www.orneksite.com/a"), "www.orneksite.com")
        for bad in ("ftp://site.com", "site.com", "file:///etc/passwd", ""):
            with self.subTest(url=bad), self.assertRaises(ValueError):
                MIRROR.validate_url(bad)


class CaptureSummaryTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.site = Path(self.scratch.name) / "site"
        shutil.copytree(FIXTURE, self.site)

    def tearDown(self):
        self.scratch.cleanup()

    def summary(self, owned=False):
        return MIRROR.summarize(self.site, "https://example.com/", "example.com", ["wget"], 0, owned)

    def test_unlicensed_site_is_study_only_and_library_licenses_are_listed(self):
        capture = self.summary()
        self.assertEqual(capture["usage"], "study-only")
        self.assertEqual(capture["entry"], "index.html")
        self.assertFalse(capture["jsShell"])
        self.assertEqual(capture["byType"]["html"]["count"], 2)
        self.assertEqual([item["file"] for item in capture["license"]["libraries"]], ["js/gsap.min.js"])

    def test_permissive_license_file_allows_review_and_owned_sites_are_editable(self):
        (self.site / "LICENSE").write_text("MIT License\n\nCopyright (c) 2026 Örnek", encoding="utf-8")
        self.assertEqual(self.summary()["usage"], "license-review")
        self.assertEqual(self.summary(owned=True)["usage"], "owned")

    def test_empty_app_shell_is_flagged_for_live_capture(self):
        (self.site / "index.html").write_text(
            '<!doctype html><html><body><div id="root"></div><noscript>JS gerekli</noscript>'
            '<script src="app.js"></script></body></html>', encoding="utf-8")
        capture = self.summary()
        self.assertTrue(capture["jsShell"])
        self.assertTrue(any("capture_reference.mjs" in note for note in capture["notes"]))


@unittest.skipUnless(shutil.which("wget"), "wget kurulu değil")
class WgetIntegrationTests(unittest.TestCase):
    def test_mirror_downloads_local_site(self):
        handler = functools.partial(QuietHandler, directory=str(FIXTURE))
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as out:
                workspace, capture = MIRROR.mirror(f"http://127.0.0.1:{server.server_port}/", out, wait=0)
                self.assertEqual(capture["wgetExit"], 0)
                self.assertEqual(capture["files"], 5)
                self.assertTrue((workspace / "capture.json").is_file())
                result = ANALYZE.analyse(workspace)
                self.assertEqual(result["capture"]["usage"], "study-only")
                self.assertEqual(result["tokens"]["roles"]["background"], "#f4f1ea")
        finally:
            server.shutdown()
            server.server_close()


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class AnalyzerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = ANALYZE.analyse(FIXTURE)

    def test_design_tokens(self):
        tokens = self.result["tokens"]
        self.assertEqual(tokens["roles"], {"background": "#f4f1ea", "text": "#1d1b18", "accent": "#c2410c"})
        self.assertEqual([f["family"] for f in tokens["fonts"]], ["Inter", "Fraunces"])
        self.assertEqual(tokens["googleFonts"], ["Fraunces", "Inter"])
        self.assertEqual(tokens["typeScale"], [14, 16, 48, 112])
        self.assertEqual(tokens["breakpoints"], [480, 768])
        self.assertEqual(tokens["customProperties"]["--color-accent"], "#c2410c")
        self.assertIn(0.2, [d["seconds"] for d in tokens["durations"]])

    def test_libraries_and_structure(self):
        self.assertEqual(self.result["libraries"], ["gsap"])
        index = next(page for page in self.result["structure"] if page["page"] == "index.html")
        self.assertEqual([h["level"] for h in index["outline"]], [1, 3])
        self.assertEqual(index["sections"], 2)

    def test_accessibility_findings(self):
        codes = {issue["code"] for issue in self.result["accessibility"]}
        self.assertEqual(codes, {"img-alt", "heading-skip", "empty-link", "empty-button", "missing-lang",
                                 "zoom-blocked", "input-label", "low-contrast"})
        self.assertEqual(sum(issue["code"] == "low-contrast" for issue in self.result["accessibility"]), 2)

    def test_surface_map_points_to_editable_lines(self):
        surface_map = self.result["surfaceMap"]
        visibility = json.loads((ROOT / "data/v9/visibility_ranking.json").read_text(encoding="utf-8"))
        self.assertEqual(set(surface_map), {s["id"] for s in visibility["surfaces"]})
        background = surface_map["background"][0]
        self.assertEqual((background["file"], background["line"], background["property"]), ("css/style.css", 10, "background-color"))
        lines = (FIXTURE / "css/style.css").read_text(encoding="utf-8").splitlines()
        for surface, hits in surface_map.items():
            for hit in hits:
                if hit["file"] == "css/style.css":
                    with self.subTest(surface=surface, line=hit["line"]):
                        self.assertIn(hit["property"], lines[hit["line"] - 1])

    def test_library_rule_conflicts_are_reported(self):
        conflicts = {note["conflict"] for note in self.result["ruleNotes"]}
        self.assertEqual(conflicts, {"CF-007", "CF-008", "v7"})
        register = json.loads((ROOT / "data/v9/rule_precedence.json").read_text(encoding="utf-8"))
        known = {c["id"] for c in register["conflicts"]} | {"v7"}
        self.assertTrue(conflicts <= known)

    def test_fonts_set_through_custom_properties_are_resolved(self):
        # Kütüphanenin önerdiği var(--font-*) kalıbı CF-007 denetimini atlamamalı.
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, "index.html").write_text('<html lang="tr"><head><title>t</title>'
                '<link rel="stylesheet" href="style.css"></head><body><h1>x</h1></body></html>', encoding="utf-8")
            Path(folder, "style.css").write_text(
                ':root { --font-display: Inter; --font-body: Georgia; }\n'
                'h1 { font-family: var(--font-display); }\nbody { font-family: var(--font-body), serif; }\n', encoding="utf-8")
            result = ANALYZE.analyse(folder)
        families = [f["family"] for f in result["tokens"]["fonts"]]
        self.assertIn("Inter", families)
        self.assertIn("Georgia", families)
        self.assertIn("CF-007", {note["conflict"] for note in result["ruleNotes"]})

    def test_generic_family_keywords_are_not_counted_as_fonts(self):
        self.assertEqual(ANALYZE.first_family("var(--x), sans-serif"), None)
        self.assertEqual(ANALYZE.first_family('"Fraunces", Georgia, serif'), "Fraunces")
        self.assertEqual(ANALYZE.first_family("700 1rem/1.4 Inter, sans-serif"), "Inter")

    def test_tokens_css_and_report(self):
        css = ANALYZE.tokens_css(self.result["tokens"])
        self.assertIn("--ref-background: #f4f1ea;", css)
        self.assertIn('--ref-font-display: "Inter";', css)
        report = ANALYZE.report(self.result)
        self.assertIn("## Düzenleme haritası", report)
        self.assertIn("`css/style.css:10`", report)

    def test_css_parser_tracks_lines_media_and_comments(self):
        css = "/* a\n b */\n.a { color: red; }\n@media (min-width: 600px) {\n  .b {\n    padding: 8px;\n  }\n}\n"
        declarations = ANALYZE.parse_css(css, "x.css")
        self.assertEqual([(d["selector"], d["line"], d["media"]) for d in declarations],
                         [(".a", 3, ""), (".b", 6, "@media (min-width: 600px)")])

    def test_color_normalisation(self):
        self.assertEqual(ANALYZE.hex_color("#abc"), "#aabbcc")
        self.assertEqual(ANALYZE.hex_color("rgba(29, 27, 24, 0.12)"), "#1d1b18")
        self.assertEqual(ANALYZE.hex_color("hsl(0, 100%, 50%)"), "#ff0000")
        self.assertEqual(ANALYZE.hex_color("white"), "#ffffff")
        self.assertIsNone(ANALYZE.hex_color("oklch(0.7 0.1 40)"))


class ContentExtractionTests(unittest.TestCase):
    def test_own_site_content_keeps_order_regions_and_profiles(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, "index.html").write_text(
                '<html lang="tr"><head><title>r0ine</title><meta name="description" content="Geliştirici"></head><body>'
                '<header><nav><a href="/">Ana sayfa</a></nav></header><main><h1>Merhaba</h1>'
                '<p>Minecraft için <b>eklenti</b> yazıyorum.</p><ul><li>Java</li><li>Kotlin</li></ul>'
                '<a href="https://github.com/r0ine">GitHub</a><a href="https://discord.gg/x" aria-label="Discord"><svg><title>i</title></svg></a>'
                '<a href="mailto:a@b.c">Yaz</a><script>var p = "<p>gizli</p>";</script></main>'
                '<footer><p>© 2026</p></footer></body></html>', encoding="utf-8")
            result = CONTENT.extract(folder)
        page = result["pages"][0]
        self.assertEqual((page["title"], page["lang"], page["description"]), ("r0ine", "tr", "Geliştirici"))
        self.assertEqual([(b["tag"], b["text"], b["region"]) for b in page["blocks"]], [
            ("h1", "Merhaba", "main"), ("p", "Minecraft için eklenti yazıyorum.", "main"),
            ("li", "Java", "main"), ("li", "Kotlin", "main"), ("p", "© 2026", "footer")])
        self.assertEqual(result["contacts"], {"GitHub": "https://github.com/r0ine", "Discord": "https://discord.gg/x",
                                              "E-posta": "mailto:a@b.c"})
        self.assertEqual(next(l for l in page["links"] if l["service"] == "Discord")["text"], "Discord")

    def test_link_classification(self):
        self.assertEqual(CONTENT.classify("https://builtbybit.com/resources/ultimate-ui.105345/"), ("social", "BuiltByBit"))
        self.assertEqual(CONTENT.classify("https://majesteleri.net"), ("external", "majesteleri.net"))
        self.assertEqual(CONTENT.classify("about.html"), ("internal", ""))


class TemplateCatalogTests(unittest.TestCase):
    def test_catalog_reads_v8_registry_and_classifies_rights(self):
        _, entries = CATALOG.load()
        self.assertTrue(entries)
        by_id = {e["id"]: e for e in entries}
        self.assertEqual(by_id["dillionverma/portfolio"]["rights"], "permissive")
        self.assertEqual(by_id["surjithctly/astroship"]["rights"], "copyleft")
        self.assertEqual(by_id["vercel/nextjs-portfolio-starter"]["rights"], "unknown")
        self.assertNotIn("pmndrs/react-three-fiber", by_id, "kütüphaneler şablon kataloğunda yer almaz")
        self.assertTrue(all(e["get"].startswith("git clone --depth 1 https://") for e in entries))

    def test_filters(self):
        _, entries = CATALOG.load()
        chosen = CATALOG.select(entries, kind="template", stack="next", rights="permissive")
        self.assertTrue(chosen)
        self.assertTrue(all(e["kind"] == "template" and "next" in e["stack"] and e["rights"] == "permissive" for e in chosen))


if __name__ == "__main__":
    unittest.main()
