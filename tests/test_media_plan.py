import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.v6.audit_media_plan import audit_plan


def estimates(payload=100, media=0.25):
    return {
        "initial_payload_kb": payload,
        "total_page_media_mb": media,
        "frame_sequences_kb": 0,
        "glb_kb": 0,
        "texture_memory_mb": 0,
        "draw_calls": 0,
        "concurrent_animations": 0,
    }


def media_plan():
    return {
        "version": "6.1",
        "project_tier": "standard",
        "mobile_tier": "lean",
        "moments": [{
            "id": "material-detail",
            "purpose": "explanation",
            "purpose_statement": "Malzemenin yüzey dokusunu gösterir.",
            "rationale": "Sabit yakın çekim ürünün dokusunu anlatıyor.",
            "essential_content_in_html": True,
            "keyboard_accessible": True,
            "desktop": {"medium": "static-image", "estimates": estimates()},
            "mobile": {"medium": "static-image", "estimates": estimates(60, 0.1)},
            "reduced_motion": {
                "medium": "static-image",
                "description": "Aynı ürün fotoğrafı hareket olmadan gösterilir.",
            },
            "downgrade_chain": ["static-image"],
        }],
    }


class MediaPlanAuditTests(unittest.TestCase):
    def setUp(self):
        self.plan = media_plan()

    def assert_blocked(self, plan):
        report = audit_plan(plan)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertTrue(report["findings"])
        for finding in report["findings"]:
            for field in ("code", "path", "message"):
                self.assertIsInstance(finding[field], str)
                self.assertTrue(finding[field].strip())
        return report

    def test_unmeasured_plan_does_not_claim_runtime_verification(self):
        report = audit_plan(self.plan)
        self.assertEqual(report["status"], "PLANNED")
        self.assertEqual(report["measurement_status"], "NOT_PROVIDED")
        self.assertEqual(report["findings"], [])

    def test_audit_preserves_input(self):
        original = copy.deepcopy(self.plan)
        audit_plan(self.plan)
        self.assertEqual(self.plan, original)

    def test_complete_measurements_pass(self):
        self.plan["measurements"] = {"desktop": estimates(), "mobile": estimates()}
        report = audit_plan(self.plan)
        self.assertEqual(report["status"], "MEASURED")
        self.assertEqual(report["measurement_status"], "WITHIN")
        self.assertEqual(report["findings"], [])

    def test_partial_measurements_remain_planned(self):
        for device in ("desktop", "mobile"):
            with self.subTest(device=device):
                self.plan["measurements"] = {device: estimates()}
                report = audit_plan(self.plan)
                self.assertEqual(report["status"], "PLANNED")
                self.assertEqual(report["measurement_status"], "PARTIAL")

    def test_partial_measurement_over_budget_is_blocked(self):
        self.plan["measurements"] = {"mobile": estimates(payload=501)}
        report = self.assert_blocked(self.plan)
        self.assertEqual(report["measurement_status"], "EXCEEDED")

    def test_measured_overrun_overrides_estimates(self):
        self.plan["measurements"] = {
            "desktop": estimates(payload=1501),
            "mobile": estimates(),
        }
        report = self.assert_blocked(self.plan)
        self.assertEqual(report["measurement_status"], "EXCEEDED")

    def test_measurements_cannot_erase_governance_findings(self):
        self.plan["moments"][0]["essential_content_in_html"] = False
        self.plan["measurements"] = {"desktop": estimates(), "mobile": estimates()}
        self.assert_blocked(self.plan)

    def test_measurement_totals_must_cover_their_parts(self):
        for measurement in (estimates(payload=300, media=0.2),
                            {**estimates(media=0.2), "frame_sequences_kb": 120, "glb_kb": 120}):
            with self.subTest(measurement=measurement):
                self.plan["project_tier"] = "rich"
                self.plan["measurements"] = {"desktop": measurement, "mobile": estimates()}
                report = self.assert_blocked(self.plan)
                self.assertTrue(any(finding["code"] == "transfer_total"
                                    and finding["path"].startswith("measurements.desktop")
                                    for finding in report["findings"]))
                self.assertNotIn("budget_exceeded", [finding["code"] for finding in report["findings"]])

    def test_declared_budgets_and_aggregates_match_catalog(self):
        report = audit_plan(self.plan)
        self.assertEqual(report["budgets"]["desktop"]["initial_payload_kb"], 1500)
        self.assertEqual(report["budgets"]["mobile"]["initial_payload_kb"], 500)
        self.assertEqual(report["estimates"]["desktop"], estimates())
        self.assertEqual(report["estimates"]["mobile"], estimates(60, 0.1))

    def test_payload_cannot_bypass_page_budget_by_splitting_moments(self):
        for device, payload in (("desktop", 800), ("mobile", 300)):
            with self.subTest(device=device):
                plan = media_plan()
                plan["moments"][0][device]["estimates"] = estimates(payload, 1)
                duplicate = copy.deepcopy(plan["moments"][0])
                duplicate["id"] = "stitch-detail"
                plan["moments"].append(duplicate)
                report = self.assert_blocked(plan)
                self.assertEqual(report["estimates"][device]["initial_payload_kb"], payload * 2)
                self.assertTrue(any(finding["path"] == f"estimates.{device}.initial_payload_kb"
                                    for finding in report["findings"]))

    def test_gpu_and_animation_costs_are_added_across_moments(self):
        for metric, per_moment in (("glb_kb", 1100), ("texture_memory_mb", 20),
                                   ("draw_calls", 20), ("concurrent_animations", 2)):
            with self.subTest(metric=metric):
                plan = media_plan()
                plan["project_tier"] = "rich"
                plan["moments"][0]["desktop"]["estimates"] = estimates(media=2)
                plan["moments"][0]["desktop"]["estimates"][metric] = per_moment
                duplicate = copy.deepcopy(plan["moments"][0])
                duplicate["id"] = "stitch-detail"
                plan["moments"].append(duplicate)
                report = self.assert_blocked(plan)
                self.assertEqual(report["estimates"]["desktop"][metric], per_moment * 2)
                self.assertTrue(any(finding["path"] == f"estimates.desktop.{metric}"
                                    for finding in report["findings"]))

    def test_each_budget_metric_is_enforced(self):
        limits = {
            "initial_payload_kb": 500,
            "total_page_media_mb": 2,
            "frame_sequences_kb": 0,
            "glb_kb": 0,
            "texture_memory_mb": 0,
            "draw_calls": 0,
            "concurrent_animations": 1,
        }
        for metric, limit in limits.items():
            with self.subTest(metric=metric):
                plan = media_plan()
                plan["moments"][0]["mobile"]["estimates"][metric] = limit + 1
                self.assert_blocked(plan)

    def test_exact_budget_limits_are_allowed(self):
        self.plan["moments"][0]["mobile"]["estimates"] = {
            "initial_payload_kb": 500,
            "total_page_media_mb": 2,
            "frame_sequences_kb": 0,
            "glb_kb": 0,
            "texture_memory_mb": 0,
            "draw_calls": 0,
            "concurrent_animations": 1,
        }
        self.assertEqual(audit_plan(self.plan)["status"], "PLANNED")

    def test_decimal_costs_at_budget_limit_do_not_accumulate_rounding_error(self):
        moment = self.plan["moments"][0]
        for device in ("desktop", "mobile"):
            moment[device]["estimates"] = estimates(payload=20, media=0.1)
        self.plan["moments"] = [
            {**copy.deepcopy(moment), "id": f"material-detail-{index}"}
            for index in range(20)
        ]
        report = audit_plan(self.plan)
        self.assertEqual(report["status"], "PLANNED")
        self.assertEqual(report["estimates"]["mobile"]["total_page_media_mb"], 2)
        self.assertEqual(report["findings"], [])

    def test_finite_estimates_cannot_overflow_the_page_total(self):
        self.plan["moments"][0]["desktop"]["estimates"]["total_page_media_mb"] = 1e308
        duplicate = copy.deepcopy(self.plan["moments"][0])
        duplicate["id"] = "stitch-detail"
        self.plan["moments"].append(duplicate)
        with self.assertRaises(ValueError):
            audit_plan(self.plan)

    def test_out_of_range_numbers_are_input_errors(self):
        for value in (float("inf"), 10 ** 400):
            with self.subTest(value=value):
                self.plan["moments"][0]["desktop"]["estimates"]["initial_payload_kb"] = value
                with self.assertRaises(ValueError):
                    audit_plan(self.plan)

    def test_accessibility_requirements_are_independent_blockers(self):
        for field in ("essential_content_in_html", "keyboard_accessible"):
            with self.subTest(field=field):
                plan = media_plan()
                plan["moments"][0][field] = False
                self.assert_blocked(plan)

    def test_disallowed_purpose_is_blocked_even_with_written_rationale(self):
        self.plan["moments"][0]["purpose"] = "looks_impressive"
        self.assert_blocked(self.plan)

    def test_mobile_must_drop_at_least_one_tier(self):
        for desktop, mobile in (("standard", "standard"), ("rich", "rich"), ("lean", "standard")):
            with self.subTest(desktop=desktop, mobile=mobile):
                self.plan["project_tier"] = desktop
                self.plan["mobile_tier"] = mobile
                self.assert_blocked(self.plan)

    def test_lean_desktop_can_keep_lean_mobile(self):
        self.plan["project_tier"] = "lean"
        self.assertEqual(audit_plan(self.plan)["status"], "PLANNED")

    def test_custom_catalog_root_controls_budgets(self):
        with tempfile.TemporaryDirectory() as directory:
            catalog_root = Path(directory)
            catalog_dir = catalog_root / "data" / "v6"
            catalog_dir.mkdir(parents=True)
            for filename in ("media_decision_matrix.json", "cinematic_profiles.json"):
                catalog = json.loads((ROOT / "data" / "v6" / filename).read_text(encoding="utf-8"))
                if filename == "cinematic_profiles.json":
                    catalog["performance_budget_tiers"]["standard"]["initial_payload_kb"] = 99
                (catalog_dir / filename).write_text(json.dumps(catalog), encoding="utf-8")
            report = audit_plan(self.plan, root=catalog_root)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertEqual(report["budgets"]["desktop"]["initial_payload_kb"], 99)

    def test_invalid_top_level_structure(self):
        for plan in (None, [], {}, {**media_plan(), "version": "6.0"}, {**media_plan(), "moments": []}):
            with self.subTest(plan=plan), self.assertRaises(ValueError):
                audit_plan(plan)

    def test_non_string_object_keys_are_input_errors(self):
        self.plan[12] = None
        with self.assertRaises(ValueError):
            audit_plan(self.plan)

    def test_missing_required_fields(self):
        for field in ("project_tier", "mobile_tier", "moments"):
            with self.subTest(field=field):
                plan = media_plan()
                del plan[field]
                with self.assertRaises(ValueError):
                    audit_plan(plan)

    def test_missing_and_unknown_metrics(self):
        for device in ("desktop", "mobile"):
            for metric in estimates():
                with self.subTest(device=device, metric=metric):
                    plan = media_plan()
                    del plan["moments"][0][device]["estimates"][metric]
                    with self.assertRaises(ValueError):
                        audit_plan(plan)
            with self.subTest(device=device, metric="unknown"):
                plan = media_plan()
                plan["moments"][0][device]["estimates"]["payload_kb"] = 12
                with self.assertRaises(ValueError):
                    audit_plan(plan)

    def test_metrics_reject_negative_non_numeric_and_non_finite_values(self):
        for value in (-1, True, False, None, "100", float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                self.plan["moments"][0]["desktop"]["estimates"]["initial_payload_kb"] = value
                with self.assertRaises(ValueError):
                    audit_plan(self.plan)

    def test_count_metrics_reject_fractions(self):
        for metric in ("draw_calls", "concurrent_animations"):
            with self.subTest(metric=metric):
                plan = media_plan()
                plan["moments"][0]["desktop"]["estimates"][metric] = 0.5
                with self.assertRaises(ValueError):
                    audit_plan(plan)

    def test_measurements_use_the_same_metric_validation(self):
        invalid_sets = [estimates(payload=True), estimates(payload=-1), estimates(payload=float("nan"))]
        missing_metric = estimates()
        del missing_metric["draw_calls"]
        invalid_sets.extend((missing_metric, {**estimates(), "payload_kb": 20}))
        for measurement in invalid_sets:
            with self.subTest(measurement=measurement):
                self.plan["measurements"] = {"desktop": measurement}
                with self.assertRaises(ValueError):
                    audit_plan(self.plan)

    def test_duplicate_moment_ids(self):
        self.plan["moments"].append(copy.deepcopy(self.plan["moments"][0]))
        with self.assertRaises(ValueError):
            audit_plan(self.plan)

    def test_moment_fields_reject_wrong_types_or_empty_text(self):
        invalid_fields = {
            "id": ("", " ", 4),
            "purpose": ("unknown-purpose", None),
            "purpose_statement": ("", " ", 4),
            "rationale": ("", " ", None),
            "essential_content_in_html": ("true", 1),
            "keyboard_accessible": ("true", 1),
        }
        for field, values in invalid_fields.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    plan = media_plan()
                    plan["moments"][0][field] = value
                    with self.assertRaises(ValueError):
                        audit_plan(plan)

    def test_unknown_tiers_and_media_are_structure_errors(self):
        for field in ("project_tier", "mobile_tier"):
            with self.subTest(field=field):
                plan = media_plan()
                plan[field] = "premium"
                with self.assertRaises(ValueError):
                    audit_plan(plan)
        self.plan["moments"][0]["desktop"]["medium"] = "hologram"
        with self.assertRaises(ValueError):
            audit_plan(self.plan)

    def test_reduced_motion_requires_valid_medium_and_description(self):
        for fallback in (
            {"medium": "poster", "description": "Ürün fotoğrafı."},
            {"medium": "static-image", "description": " "},
            {"medium": "static-image"},
        ):
            with self.subTest(fallback=fallback):
                self.plan["moments"][0]["reduced_motion"] = fallback
                with self.assertRaises(ValueError):
                    audit_plan(self.plan)

    def test_reduced_motion_cannot_use_animated_media(self):
        self.plan["moments"][0]["reduced_motion"]["medium"] = "video"
        self.assert_blocked(self.plan)

    def test_downgrade_chain_rejects_missing_or_unknown_media(self):
        for chain in ([], ["static-image", "static"]):
            with self.subTest(chain=chain):
                self.plan["moments"][0]["downgrade_chain"] = chain
                with self.assertRaises(ValueError):
                    audit_plan(self.plan)

    def test_downgrade_chain_must_start_at_desktop_and_end_without_motion(self):
        for chain in (["static-image", "static-image"], ["video"], ["video", "static-image"]):
            with self.subTest(chain=chain):
                self.plan["moments"][0]["downgrade_chain"] = chain
                self.assert_blocked(self.plan)

    def test_mobile_medium_must_appear_in_downgrade_chain(self):
        self.plan["moments"][0]["mobile"]["medium"] = "svg"
        self.assert_blocked(self.plan)

    def test_shorter_canonical_downgrade_chain_is_accepted(self):
        self.plan["project_tier"] = "rich"
        moment = self.plan["moments"][0]
        moment["desktop"]["medium"] = "realtime-3d"
        moment["desktop"]["estimates"]["draw_calls"] = 10
        moment["downgrade_chain"] = ["realtime-3d", "static-image"]
        self.assertEqual(audit_plan(self.plan)["status"], "PLANNED")

    def test_realtime_medium_needs_gpu_cost(self):
        for medium in ("realtime-3d", "webgl-webgpu-shader"):
            with self.subTest(medium=medium):
                self.plan["project_tier"] = "rich"
                moment = self.plan["moments"][0]
                moment["desktop"]["medium"] = medium
                moment["downgrade_chain"] = [medium, "static-image"]
                self.assert_blocked(self.plan)

    def test_sequence_requires_transfer_estimate(self):
        for medium in ("frame-sequence", "prerendered-3d"):
            with self.subTest(medium=medium):
                moment = self.plan["moments"][0]
                moment["desktop"]["medium"] = medium
                moment["downgrade_chain"] = [medium, "static-image"]
                self.assert_blocked(self.plan)

    def test_sequence_limit_applies_even_within_page_budget(self):
        for device, transfer in (("desktop", 4001), ("mobile", 1501)):
            with self.subTest(device=device):
                plan = media_plan()
                plan["project_tier"] = "cinematic"
                plan["mobile_tier"] = "rich"
                moment = plan["moments"][0]
                moment["desktop"]["medium"] = "frame-sequence"
                moment["desktop"]["estimates"]["frame_sequences_kb"] = 100
                moment[device]["medium"] = "frame-sequence"
                moment[device]["estimates"] = estimates(media=5)
                moment[device]["estimates"]["frame_sequences_kb"] = transfer
                moment["downgrade_chain"] = ["frame-sequence", "static-image"]
                report = self.assert_blocked(plan)
                self.assertFalse(any(finding["path"].startswith("estimates.") for finding in report["findings"]))

    def test_total_transfer_cannot_be_smaller_than_its_parts(self):
        for costs in (estimates(payload=300, media=0.2),
                      {**estimates(media=0.2), "frame_sequences_kb": 120, "glb_kb": 120}):
            with self.subTest(costs=costs):
                plan = media_plan()
                plan["project_tier"] = "rich"
                plan["moments"][0]["desktop"]["estimates"] = costs
                self.assert_blocked(plan)


class MediaPlanCommandTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.input_path = Path(self.directory.name) / "malzeme planı.json"

    def run_command(self, *arguments):
        return subprocess.run(
            [sys.executable, str(ROOT / "tools" / "v6" / "audit_media_plan.py"), str(self.input_path), *arguments],
            cwd=self.directory.name,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
            timeout=15,
        )

    def write_plan(self, plan):
        self.input_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")

    def test_default_json_output_works_outside_repository(self):
        self.write_plan(media_plan())
        completed = self.run_command()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "PLANNED")
        self.assertEqual(completed.stderr, "")

    def test_text_output(self):
        self.write_plan(media_plan())
        completed = self.run_command("--format", "text")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("PLANNED", completed.stdout)
        self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_governance_blocker_exits_one(self):
        plan = media_plan()
        plan["moments"][0]["purpose"] = "looks_impressive"
        self.write_plan(plan)
        completed = self.run_command()
        self.assertEqual(completed.returncode, 1, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "BLOCKED")

    def test_require_measurements_rejects_absent_and_partial_measurements(self):
        for measurement in (None, {"desktop": estimates()}):
            with self.subTest(measurement=measurement):
                plan = media_plan()
                if measurement is not None:
                    plan["measurements"] = measurement
                self.write_plan(plan)
                completed = self.run_command("--require-measurements")
                self.assertEqual(completed.returncode, 1, completed.stderr)
                report = json.loads(completed.stdout)
                self.assertEqual(report["status"], "BLOCKED")
                self.assertIn("measurements_required", [finding["code"] for finding in report["findings"]])

    def test_require_measurements_accepts_complete_measurements(self):
        plan = media_plan()
        plan["measurements"] = {"desktop": estimates(), "mobile": estimates()}
        self.write_plan(plan)
        completed = self.run_command("--require-measurements")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "MEASURED")

    def test_bad_input_exits_two_without_traceback(self):
        for content in ("{", "[]", "null", '{"version": "6.1"}'):
            with self.subTest(content=content):
                self.input_path.write_text(content, encoding="utf-8")
                completed = self.run_command()
                self.assertEqual(completed.returncode, 2)
                self.assertNotIn("Traceback", completed.stdout + completed.stderr)
                self.assertTrue((completed.stdout + completed.stderr).strip())

    def test_non_finite_json_constants_are_rejected(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                plan = media_plan()
                plan["moments"][0]["desktop"]["estimates"]["initial_payload_kb"] = value
                self.write_plan(plan)
                completed = self.run_command()
                self.assertEqual(completed.returncode, 2)
                self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_duplicate_json_fields_are_rejected(self):
        self.input_path.write_text('{"version": "6.1", "version": "6.0"}', encoding="utf-8")
        completed = self.run_command()
        self.assertEqual(completed.returncode, 2)
        self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_invalid_unicode_in_error_context_does_not_break_output(self):
        plan = media_plan()
        plan["moments"][0]["id"] = "\ud800"
        plan["moments"].append(copy.deepcopy(plan["moments"][0]))
        self.input_path.write_text(json.dumps(plan), encoding="utf-8")
        completed = self.run_command()
        self.assertEqual(completed.returncode, 2)
        self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_invalid_metric_types_are_reported_without_traceback(self):
        for value in (-1, True, "100"):
            with self.subTest(value=value):
                plan = media_plan()
                plan["moments"][0]["desktop"]["estimates"]["initial_payload_kb"] = value
                self.write_plan(plan)
                completed = self.run_command()
                self.assertEqual(completed.returncode, 2)
                self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_missing_file_exits_two_without_traceback(self):
        completed = self.run_command()
        self.assertEqual(completed.returncode, 2)
        self.assertNotIn("Traceback", completed.stdout + completed.stderr)
        self.assertTrue((completed.stdout + completed.stderr).strip())

    def test_published_examples_have_expected_exit_codes(self):
        for filename, exit_code in (("media_plan.json", 0), ("over_budget_media_plan.json", 1)):
            with self.subTest(filename=filename):
                self.input_path = ROOT / "examples" / "v6" / filename
                completed = self.run_command()
                self.assertEqual(completed.returncode, exit_code, completed.stderr)
                self.assertEqual(json.loads(completed.stdout)["status"], "PLANNED" if exit_code == 0 else "BLOCKED")


if __name__ == "__main__":
    unittest.main()
