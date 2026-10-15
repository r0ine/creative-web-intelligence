#!/usr/bin/env python3
"""Medya planının beyan edilen maliyetini ve fallback kararlarını denetler."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
METRICS = (
    "initial_payload_kb", "total_page_media_mb", "frame_sequences_kb",
    "glb_kb", "texture_memory_mb", "draw_calls", "concurrent_animations",
)
COUNTS = {"draw_calls", "concurrent_animations"}
STATIC_MEDIA = {"none", "css", "svg", "static-image", "generated-image"}
TIERS = ("lean", "standard", "rich", "cinematic")


def object_fields(record, required, optional, path):
    if not isinstance(record, dict):
        raise ValueError(f"{path}: nesne bekleniyor.")
    if any(not isinstance(field, str) for field in record):
        raise ValueError(f"{path}: alan adları metin olmalı.")
    missing = set(required) - record.keys()
    unknown = record.keys() - set(required) - set(optional)
    if missing:
        raise ValueError(f"{path}: eksik alanlar: {', '.join(sorted(missing))}.")
    if unknown:
        raise ValueError(f"{path}: bilinmeyen alanlar: {', '.join(sorted(unknown))}.")


def nonempty_text(value, path):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path}: boş olmayan metin bekleniyor.")


def choice(value, choices, path):
    if not isinstance(value, str) or value not in choices:
        raise ValueError(f"{path}: geçersiz değer; seçenekler: {', '.join(choices)}.")


def metric_values(metrics, path):
    object_fields(metrics, METRICS, (), path)
    for metric, value in metrics.items():
        if type(value) not in (int, float) or value < 0:
            raise ValueError(f"{path}.{metric}: sıfır veya pozitif sayı bekleniyor.")
        try:
            finite = math.isfinite(value)
        except OverflowError:
            finite = False
        if not finite:
            raise ValueError(f"{path}.{metric}: sonlu bir sayı bekleniyor.")
        if metric in COUNTS and type(value) is not int:
            raise ValueError(f"{path}.{metric}: tam sayı bekleniyor.")


def validate_plan(plan, matrix):
    object_fields(plan, ("version", "project_tier", "mobile_tier", "moments"),
                  ("measurements",), "plan")
    choice(plan["version"], ("6.1",), "version")
    for tier in ("project_tier", "mobile_tier"):
        choice(plan[tier], TIERS, tier)
    if not isinstance(plan["moments"], list) or not plan["moments"]:
        raise ValueError("moments: en az bir görsel karar içeren liste bekleniyor.")

    medium_ids = [medium["id"] for medium in matrix["medium_spectrum"]]
    purposes = matrix["valid_purposes"] + matrix["invalid_purposes"]
    seen_ids = set()
    for index, moment in enumerate(plan["moments"]):
        path = f"moments[{index}]"
        object_fields(moment, (
            "id", "purpose", "purpose_statement", "rationale", "desktop", "mobile",
            "essential_content_in_html", "keyboard_accessible", "reduced_motion",
            "downgrade_chain",
        ), (), path)
        for field in ("id", "purpose_statement", "rationale"):
            nonempty_text(moment[field], f"{path}.{field}")
        if moment["id"] in seen_ids:
            raise ValueError(f"{path}.id: tekrarlanan kimlik: {moment['id']}.")
        seen_ids.add(moment["id"])
        choice(moment["purpose"], purposes, f"{path}.purpose")
        for flag in ("essential_content_in_html", "keyboard_accessible"):
            if type(moment[flag]) is not bool:
                raise ValueError(f"{path}.{flag}: true veya false bekleniyor.")
        for device in ("desktop", "mobile"):
            variant = moment[device]
            object_fields(variant, ("medium", "estimates"), (), f"{path}.{device}")
            choice(variant["medium"], medium_ids, f"{path}.{device}.medium")
            metric_values(variant["estimates"], f"{path}.{device}.estimates")
        fallback = moment["reduced_motion"]
        object_fields(fallback, ("medium", "description"), (), f"{path}.reduced_motion")
        choice(fallback["medium"], medium_ids, f"{path}.reduced_motion.medium")
        nonempty_text(fallback["description"], f"{path}.reduced_motion.description")
        chain = moment["downgrade_chain"]
        if not isinstance(chain, list) or not chain:
            raise ValueError(f"{path}.downgrade_chain: boş olmayan liste bekleniyor.")
        for medium in chain:
            choice(medium, medium_ids, f"{path}.downgrade_chain")

    measurements = plan.get("measurements", {})
    object_fields(measurements, (), ("desktop", "mobile"), "measurements")
    for device, metrics in measurements.items():
        metric_values(metrics, f"measurements.{device}")


def audit_plan(plan, root=ROOT):
    root = Path(root)
    matrix = json.loads((root / "data/v6/media_decision_matrix.json").read_text(encoding="utf-8"))
    profiles = json.loads((root / "data/v6/cinematic_profiles.json").read_text(encoding="utf-8"))
    validate_plan(plan, matrix)
    budgets = {
        "desktop": profiles["performance_budget_tiers"][plan["project_tier"]],
        "mobile": profiles["performance_budget_tiers"][plan["mobile_tier"]],
    }
    estimates = {device: dict.fromkeys(METRICS, 0) for device in budgets}
    findings = []

    def flag(code, path, message):
        findings.append({"code": code, "path": path, "message": message})

    mobile_ceiling = profiles["mobile_tier_mapping"][plan["project_tier"]]
    if TIERS.index(plan["mobile_tier"]) > TIERS.index(mobile_ceiling):
        flag("mobile_tier", "mobile_tier", f"Mobil katman en fazla {mobile_ceiling} olabilir.")

    medium_order = {medium["id"]: index for index, medium in enumerate(matrix["medium_spectrum"])}
    for index, moment in enumerate(plan["moments"]):
        path = f"moments[{index}]"
        if moment["purpose"] in matrix["invalid_purposes"]:
            flag("purpose", f"{path}.purpose", "Görselin amacı içerik veya etkileşimle gerekçelendirilmeli.")
        if not moment["essential_content_in_html"]:
            flag("essential_content", f"{path}.essential_content_in_html", "Esas içerik HTML içinde de bulunmalı.")
        if not moment["keyboard_accessible"]:
            flag("keyboard", f"{path}.keyboard_accessible", "Görselin işlevi klavyeyle de kullanılabilmeli.")
        if moment["reduced_motion"]["medium"] not in STATIC_MEDIA:
            flag("reduced_motion", f"{path}.reduced_motion.medium", "Azaltılmış hareket için statik bir karşılık seç.")
        chain = moment["downgrade_chain"]
        if chain[0] != moment["desktop"]["medium"]:
            flag("downgrade_start", f"{path}.downgrade_chain", "Zincir masaüstünde seçilen medyumla başlamalı.")
        if chain[-1] not in STATIC_MEDIA:
            flag("downgrade_end", f"{path}.downgrade_chain", "Zincir statik bir medyumla bitmeli.")
        if any(medium_order[left] <= medium_order[right] for left, right in zip(chain, chain[1:])):
            flag("downgrade_order", f"{path}.downgrade_chain", "Zincirde her adım daha sade olmalı; tekrar kullanma.")
        if moment["mobile"]["medium"] not in chain:
            flag("mobile_fallback", f"{path}.mobile.medium", "Mobil medyum düşürme zincirinde bulunmalı.")

        for device in budgets:
            variant = moment[device]
            costs = variant["estimates"]
            cost_path = f"{path}.{device}.estimates"
            if costs["initial_payload_kb"] > costs["total_page_media_mb"] * 1000:
                flag("transfer_total", cost_path, "İlk yükleme toplam medya aktarımından büyük olamaz.")
            if costs["frame_sequences_kb"] + costs["glb_kb"] > costs["total_page_media_mb"] * 1000:
                flag("transfer_total", cost_path, "Sekans ve GLB aktarımı toplam medya aktarımını aşıyor.")
            if variant["medium"] in {"realtime-3d", "webgl-webgpu-shader"} and costs["draw_calls"] < 1:
                flag("gpu_estimate", cost_path, "Gerçek zamanlı sahne için draw_calls maliyetini belirt.")
            if variant["medium"] in {"frame-sequence", "prerendered-3d"}:
                if costs["frame_sequences_kb"] <= 0:
                    flag("sequence_estimate", cost_path, "Sekansın aktarım maliyetini belirt.")
                limit = profiles["frame_sequence_profiles"]["transfer_limits"][f"{device}_per_sequence_kb"]
                if costs["frame_sequences_kb"] > limit:
                    flag("sequence_transfer", cost_path, f"Tek sekans {limit} KB sınırını aşıyor.")

    for device in budgets:
        for metric in METRICS:
            costs = [moment[device]["estimates"][metric] for moment in plan["moments"]]
            try:
                estimates[device][metric] = sum(costs) if metric in COUNTS else math.fsum(costs)
            except OverflowError as exc:
                raise ValueError(f"estimates.{device}.{metric}: toplam sayı sınırını aşıyor.") from exc

    measurements = plan.get("measurements", {})
    measured_exceeded = False
    for source, totals in (("estimates", estimates), ("measurements", measurements)):
        for device, metrics in totals.items():
            metric_values(metrics, f"{source}.{device}")
            if source == "measurements":
                total_kb = metrics["total_page_media_mb"] * 1000
                if metrics["initial_payload_kb"] > total_kb:
                    flag("transfer_total", f"{source}.{device}", "İlk yükleme ölçümü toplam medya aktarımını aşıyor.")
                if metrics["frame_sequences_kb"] + metrics["glb_kb"] > total_kb:
                    flag("transfer_total", f"{source}.{device}", "Sekans ve GLB ölçümleri toplam medya aktarımını aşıyor.")
            for metric, value in metrics.items():
                limit = budgets[device][metric]
                if value > limit:
                    flag("budget_exceeded", f"{source}.{device}.{metric}", f"{value:g} değeri {limit:g} bütçesini aşıyor.")
                    measured_exceeded |= source == "measurements"

    measurement_status = "WITHIN" if len(measurements) == 2 else "PARTIAL" if measurements else "NOT_PROVIDED"
    if measured_exceeded:
        measurement_status = "EXCEEDED"
    status = "BLOCKED" if findings else "MEASURED" if measurement_status == "WITHIN" else "PLANNED"
    return {
        "version": "6.1", "status": status, "measurement_status": measurement_status,
        "budgets": budgets, "estimates": estimates, "measurements": measurements,
        "findings": findings,
    }


def reject_constant(value):
    raise ValueError(f"JSON içinde {value} kullanılamaz; sonlu sayı gir.")


def unique_fields(pairs):
    fields = {}
    for key, value in pairs:
        if key in fields:
            raise ValueError(f"JSON alanı tekrarlanıyor: {key}.")
        fields[key] = value
    return fields


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Medya planının bütçe ve fallback kararlarını denetle.")
    parser.add_argument("plan", type=Path, help="Medya planı JSON dosyası")
    parser.add_argument("--format", choices=("json", "text"), default="json", help="Rapor biçimi")
    parser.add_argument("--require-measurements", action="store_true", help="Her iki cihaz için ölçüm iste")
    args = parser.parse_args(argv)
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8-sig"),
                          parse_constant=reject_constant, object_pairs_hook=unique_fields)
        report = audit_plan(plan)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Medya planı okunamadı: {exc}", file=sys.stderr)
        return 2
    if args.require_measurements and report["measurement_status"] in {"NOT_PROVIDED", "PARTIAL"}:
        report["status"] = "BLOCKED"
        report["findings"].append({
            "code": "measurements_required", "path": "measurements",
            "message": "Masaüstü ve mobil için yedi metriğin ölçümünü ekle.",
        })
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    else:
        print(f"Medya planı: {report['status']}")
        print(f"Beyan edilen ölçümler: {report['measurement_status']}")
        for finding in report["findings"]:
            print(f"- {finding['path']}: {finding['message']}")
        if report["status"] == "PLANNED":
            print("Tahminler bütçeye uyuyor; masaüstü ve mobil ölçümleri henüz tamamlanmadı.")
    return 1 if report["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    sys.exit(main())
