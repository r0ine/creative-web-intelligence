#!/usr/bin/env python3
"""v8 kaynaklarını referans, uygulama ve çakışma kararlarına dönüştürür."""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/v8"
LENSES = {
    "design": "Hero, tipografi, grid, boşluk, renk ve mobil kırılımları ölç; ekran görüntüsü olmadan görsel hüküm verme.",
    "motion": "Tetik, süre, easing, çıkış durumu ve reduced-motion karşılığını kaydet.",
    "architecture": "Bileşen sınırları, tema tokenları, veri akışı ve sürüm bağımlılıklarını ayır.",
    "antiGeneric": "Kaynağın hangi kararını öğrenip hangi hazır görünümünü bilinçli değiştireceğini yaz.",
    "performance": "Mobil yük, animasyon bütçesi, giriş gecikmesi ve statik fallback'ı ölç.",
}


def load_catalog():
    registry = json.loads((DATA / "source_registry.json").read_text(encoding="utf-8"))
    profiles = json.loads((DATA / "source_profiles.json").read_text(encoding="utf-8"))["profiles"]
    findings = json.loads((DATA / "readme_findings.json").read_text(encoding="utf-8"))["findings"]
    sources = {item["id"]: {**item, **profiles[item["id"]]} for item in registry["sources"]}
    return sources, findings


def stack_fit(source, framework):
    stack = source["stack"]
    if "agnostic" in stack:
        return 1
    if framework in stack:
        return 4
    if framework == "next" and "react" in stack:
        return 2
    if framework == "astro" and "html" in stack:
        return 1
    if "unknown" in stack:
        return -1
    return -4


def review_score(source, framework, findings):
    if source["access"] != "available":
        return -100
    return stack_fit(source, framework) + (2 if source["id"] in findings else 0)


def source_brief(source, findings):
    license_name = source.get("license")
    return {
        "id": source["id"],
        "url": source.get("canonicalUrl", source["url"]),
        "requestedUrl": source["url"],
        "access": source["access"],
        "role": source["role"],
        "stackHint": source["stack"],
        "license": license_name or source.get("licenseNote") or "unverified",
        "licenseEvidenceUrl": source.get("licenseEvidenceUrl") or source.get("licenseUrl"),
        "reuse": "review-required" if license_name or source.get("licenseNote") else "blocked-until-license-verified",
        "evidence": "README-reviewed" if source["id"] in findings else "metadata-only",
        "evidenceUrl": source.get("canonicalUrl", source["url"]) + "#readme" if source["id"] in findings else source.get("metadataUrl", source["url"]),
        "readmeFindings": findings.get(source["id"], {}),
        "studyFocus": source["focus"],
        "inspectionLenses": LENSES,
    }


def conflicts(selected, framework):
    issues = []
    roles = {role: [s["id"] for s in selected if s["role"] == role] for role in {
        "site-template", "dashboard-template", "app-starter", "ui-foundation", "motion-engine",
        "3d-helper", "3d-renderer", "scroll-enhancer",
    }}
    shells = roles["site-template"] + roles["dashboard-template"] + roles["app-starter"]
    if len(shells) > 1:
        issues.append({"severity": "block", "code": "multiple-shells", "message": "Birden çok site kabuğunu birleştirme; yalnız birini uygulama temeli seç."})
    if len(roles["ui-foundation"]) > 1:
        issues.append({"severity": "block", "code": "multiple-ui-foundations", "message": "Birden çok stilli UI temelinin token ve davranışları çakışır."})
    if len(roles["motion-engine"]) > 1:
        issues.append({"severity": "block", "code": "multiple-motion-owners", "message": "Aynı öğe için tek animasyon sahibi seç; Motion ve GSAP zaman çizelgelerini üst üste koyma."})
    if roles["3d-helper"] and not roles["3d-renderer"]:
        issues.append({"severity": "block", "code": "missing-3d-renderer", "message": "Drei, React Three Fiber olmadan 3D renderer değildir."})
    if roles["scroll-enhancer"]:
        issues.append({"severity": "review", "code": "scroll-coordination", "message": "Lenis yerel scroll, anchor, sticky ve scroll tetikleyicileriyle hedef cihazda birlikte sınanmalı."})
    for source in selected:
        if source["access"] != "available":
            issues.append({"severity": "block", "code": "unavailable", "source": source["id"], "message": "Kaynağa erişim doğrulanamadı."})
        if stack_fit(source, framework) < 0 and source["role"] != "discovery":
            issues.append({"severity": "review", "code": "stack-mismatch", "source": source["id"], "message": "Kaynak bu framework için doğrudan uygulama adayı değil; yalnız referans olarak incele."})
        if source.get("licenseNote"):
            issues.append({"severity": "review", "code": "custom-license-review", "source": source["id"], "message": "Özel lisansın güncel koşullarını hedef kullanım için ayrıca değerlendir."})
        elif source["kind"] == "repository" and not source.get("license"):
            issues.append({"severity": "block", "code": "license-unverified", "source": source["id"], "message": "Kod kopyalama/entegrasyon için lisans dosyası doğrulanmalı; fikir incelemesi yapılabilir."})
        elif source.get("license", "").startswith("GPL"):
            issues.append({"severity": "review", "code": "copyleft-review", "source": source["id"], "message": "GPL koşulları hedef projenin dağıtımına göre ayrıca değerlendirilmeli."})
    return issues


def recommend(sources, findings, surface, framework, motion):
    group = {"portfolio": "portfolio", "landing": "saas_landing", "dashboard": "dashboard"}[surface]
    candidate_roles = {"site-template", "site-reference", "dashboard-template", "3d-reference"}
    candidates = [s for s in sources.values() if s["category"] == group and s["role"] in candidate_roles]
    candidates.sort(key=lambda s: (-review_score(s, framework, findings), s["id"]))
    reference = candidates[0] if candidates and review_score(candidates[0], framework, findings) >= 0 else None
    support = []
    if motion == "3d":
        if framework in {"react", "next"}:
            support.extend([sources["pmndrs/react-three-fiber"], sources["pmndrs/drei"]])
    elif motion == "scroll":
        support.append(sources["framer/motion"] if framework in {"react", "next", "vue"} else sources["greensock/gsap"])
    elif motion == "subtle" and framework in {"react", "next", "vue"}:
        support.append(sources["framer/motion"])

    selected = ([reference] if reference else []) + support
    workflow = [
        "Önce tek ekranlık kısa görsel prototip ve beş mercekli inceleme notu üret.",
        "Seçilen kaynağın masaüstü, mobil ve etkileşim durumlarını gerçek ekranda doğrula.",
        "Lisans ve framework uyumu geçmeden kod kopyalama veya bağımlılık ekleme.",
        "Uygulamayı aynı viewport'ta kaynakla karşılaştır; yük ve reduced-motion davranışını ölç.",
    ]
    if motion == "3d" and framework not in {"react", "next"}:
        workflow.append("Bu framework için R3F/Drei önerilmedi; mevcut runtime/three yaklaşımını veya statik fallback'ı değerlendir.")
    return {
        "input": {"surface": surface, "framework": framework, "motion": motion},
        "firstReference": source_brief(reference, findings) if reference else None,
        "supportingStudies": [source_brief(s, findings) for s in support],
        "conflicts": conflicts(selected, framework),
        "workflow": workflow,
    }


def render_text(result):
    if "firstReference" not in result:
        source = result
        lines = [f"Kaynak: {source['id']}", f"Adres: {source['url']}",
                 f"Durum: {source['access']} · {source['evidence']}",
                 f"Lisans: {source['license']} · yeniden kullanım: {source['reuse']}",
                 f"İnceleme odağı: {source['studyFocus']}"]
        for key, note in source["readmeFindings"].items():
            lines.append(f"{key}: {note}")
        for key, prompt in LENSES.items():
            lines.append(f"{key} sorusu: {prompt}")
        return "\n".join(lines)
    lines = ["İlk referans: " + (result["firstReference"]["id"] if result["firstReference"] else "uygun kaynak bulunamadı")]
    if result["firstReference"]:
        lines.append("İnceleme odağı: " + result["firstReference"]["studyFocus"])
    lines.extend("Destek kaynağı: " + source["id"] for source in result["supportingStudies"])
    lines.extend(f"{issue['severity']}: {issue['message']}" for issue in result["conflicts"])
    lines.extend(result["workflow"])
    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="v8 kaynak seçimi ve çakışma denetimi")
    parser.add_argument("--surface", choices=["portfolio", "landing", "dashboard"], default="portfolio")
    parser.add_argument("--framework", choices=["next", "react", "astro", "vue", "vanilla"], default="react")
    parser.add_argument("--motion", choices=["none", "subtle", "scroll", "3d"], default="none")
    parser.add_argument("--source", help="Tek kaynağın kanıt ve inceleme fişi")
    parser.add_argument("--check", nargs="+", help="Kaynak kimlikleri için çakışma denetimi")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()
    sources, findings = load_catalog()
    if args.source:
        if args.source.lower() not in sources:
            parser.error(f"Bilinmeyen kaynak: {args.source}")
        result = source_brief(sources[args.source.lower()], findings)
    elif args.check:
        unknown = [sid for sid in args.check if sid.lower() not in sources]
        if unknown:
            parser.error("Bilinmeyen kaynak: " + ", ".join(unknown))
        result = {"sources": args.check, "conflicts": conflicts([sources[sid.lower()] for sid in args.check], args.framework)}
    else:
        result = recommend(sources, findings, args.surface, args.framework, args.motion)
    if args.format == "json" or args.check:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
