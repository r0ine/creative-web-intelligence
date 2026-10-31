#!/usr/bin/env python3
"""Referans tabanlı site oluşturma pipeline'ını tek komutla çalıştırır.

Adımlar:
  1. Referans siteyi indir (mirror_reference)
  2. Tasarım ölçülerini çıkar (analyze_reference)
  3. Varsa içerik kaynağını indir ve içeriği çıkar (extract_content)
  4. Tipografi kapsamını denetle (font_coverage)
  5. Her şeyi bir build spec (JSON + MD) dosyasına yaz

Çıktı çalışma alanına ``build-spec.json`` ve ``build-spec.md`` olarak yazılır.
Ajan veya geliştirici bu spec'i okuyarak siteyi kurabilir.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "reference-workspace"
TOOLS = ROOT / "tools" / "v10"


def run_tool(label, args, capture=True):
    """Python aracını çalıştır, hata varsa not olarak kaydet."""
    print(f"  [{label}] çalışıyor...")
    try:
        result = subprocess.run(
            [sys.executable, "-I"] + args,
            capture_output=capture, encoding="utf-8", errors="replace", timeout=300, check=False)
        if result.returncode == 0:
            print(f"  [{label}] tamam")
            return result, None
        msg = f"{label}: çıkış kodu {result.returncode}"
        if capture and result.stderr:
            msg += f" — {result.stderr.strip()[:200]}"
        print(f"  [{label}] uyarı — {msg}")
        return result, msg
    except Exception as exc:
        msg = f"{label}: {exc}"
        print(f"  [{label}] atlandı — {exc}")
        return None, msg


def check_fonts(families, lang="tr"):
    """Font listesindeki ailelerin dil kapsamını denetle."""
    results = []
    for family in families:
        r, _ = run_tool(f"font:{family}",
                        [str(TOOLS / "font_coverage.py"), family, "--lang", lang, "--format", "json"],
                        capture=True)
        if r and r.stdout.strip():
            try:
                data = json.loads(r.stdout)
                if data.get("check"):
                    results.append(data["check"])
            except json.JSONDecodeError:
                pass
    return results


def build_spec_md(spec):
    """Build spec'i okunabilir Markdown'a çevir."""
    lines = ["# Build Spec", ""]

    lines.append("## Referans")
    ref = spec.get("reference", {})
    lines.append(f"- Kaynak: {ref.get('url', 'yok')}")
    lines.append(f"- Kullanım: **{ref.get('usage', '?')}** — {ref.get('usageNote', '')}")
    if ref.get("jsShell"):
        lines.append("- JS kabuk: evet (canlı yakalama gerekli)")
    lines.append("")

    if spec.get("analysis"):
        lines.append("## Tasarım ölçüleri")
        a = spec["analysis"]
        if a.get("palette"):
            lines.append(f"- Palet: {', '.join(c['color'] if isinstance(c, dict) else str(c) for c in a['palette'][:8])}")
        if a.get("fonts"):
            lines.append(f"- Fontlar: {', '.join(a['fonts'][:6])}")
        if a.get("breakpoints"):
            lines.append(f"- Kırılımlar: {', '.join(str(b) for b in a['breakpoints'][:4])}")
        if a.get("libraries"):
            lines.append(f"- Kütüphaneler: {', '.join(a['libraries'][:6])}")
        if a.get("ruleConflicts"):
            lines.append(f"- Kural çakışmaları: {len(a['ruleConflicts'])}")
            for c in a["ruleConflicts"][:5]:
                lines.append(f"  - {c.get('message', c) if isinstance(c, dict) else c}")
        lines.append("")

    if spec.get("content"):
        lines.append("## İçerik")
        c = spec["content"]
        lines.append(f"- Başlık: {c.get('title', '?')}")
        lines.append(f"- Dil: {c.get('lang', '?')}")
        if c.get("blocks"):
            headings = [b for b in c["blocks"] if b.get("tag", "").startswith("h")]
            lines.append(f"- Başlıklar: {len(headings)}")
            for h in headings[:10]:
                lines.append(f"  - <{h['tag']}> {(h.get('text') or '')[:60]}")
        if c.get("links"):
            lines.append(f"- Bağlantılar: {len(c['links'])}")
        lines.append("")

    if spec.get("fontChecks"):
        lines.append("## Font kapsamı")
        for fc in spec["fontChecks"]:
            status = {True: "kapsıyor", False: "KAPSAMIYOR", None: "bilinmiyor"}.get(fc.get("covers"), "?")
            lines.append(f"- {fc['family']}: {status}")
        lines.append("")
        if spec.get("fontStacks"):
            lines.append("### Önerilen yığınlar")
            for st in spec["fontStacks"]:
                lines.append(f"- [{st['role']}] `{st['stack']}`")
            lines.append("")

    if spec.get("nextSteps"):
        lines.append("## Sonraki adımlar")
        for i, step in enumerate(spec["nextSteps"], 1):
            lines.append(f"{i}. {step}")
        lines.append("")

    if spec.get("skipped"):
        lines.append("## Atlanan adımlar")
        for s in spec["skipped"]:
            lines.append(f"- {s}")
        lines.append("")

    lines.append("---")
    lines.append("*build_from_reference.py tarafından oluşturuldu.*")
    return "\n".join(lines)


def pipeline(reference_url, content_url=None, out=None, level=2, quota_mb=200,
             wait=1.0, own=False, lang="tr", allow_domains=()):
    """Tüm pipeline'ı çalıştır, build spec döndür."""
    skipped = []
    workspace_root = out or str(WORKSPACE)

    # 1. Mirror reference
    print("1/5 Referans indiriliyor...")
    mirror_args = [str(TOOLS / "mirror_reference.py"), reference_url, "--out", workspace_root,
                   "--level", str(level), "--quota-mb", str(quota_mb), "--wait", str(wait)]
    if own:
        mirror_args.append("--own")
    for domain in allow_domains:
        mirror_args += ["--allow-domain", domain]
    r, err = run_tool("mirror", mirror_args, capture=False)
    if err:
        skipped.append(err)

    # Find workspace
    from mirror_reference import validate_url as _validate
    import re
    host = _validate(reference_url)
    ws_parent = Path(workspace_root) / re.sub(r"[^a-z0-9.-]", "_", host.lower())
    if ws_parent.is_dir():
        candidates = sorted(ws_parent.iterdir(), reverse=True)
        workspace = candidates[0] if candidates else ws_parent
    else:
        print("Hata: çalışma alanı bulunamadı.")
        return {"skipped": ["mirror: çalışma alanı oluşturulamadı"]}

    capture_path = workspace / "capture.json"
    capture = json.loads(capture_path.read_text(encoding="utf-8")) if capture_path.is_file() else {}

    ref_info = {
        "url": reference_url,
        "workspace": str(workspace),
        "usage": capture.get("usage", "study-only"),
        "usageNote": capture.get("usageNote", ""),
        "jsShell": capture.get("jsShell", False),
        "entry": capture.get("entry"),
        "files": capture.get("files", 0),
    }

    # 2. Analyze reference
    print("\n2/5 Tasarım analizi...")
    analysis_data = None
    if capture.get("entry"):
        run_tool("analiz", [str(TOOLS / "analyze_reference.py"), str(workspace)], capture=False)
        analysis_json = workspace / "analysis.json"
        if analysis_json.is_file():
            analysis_data = json.loads(analysis_json.read_text(encoding="utf-8"))
            print(f"  Fontlar: {analysis_data.get('fonts', [])}")
            print(f"  Kütüphaneler: {analysis_data.get('libraries', [])}")
    else:
        skipped.append("analiz: giriş sayfası yok")

    # 3. Content extraction
    print("\n3/5 İçerik çıkarma...")
    content_data = None
    content_workspace = None
    if content_url:
        print(f"  İçerik kaynağı indiriliyor: {content_url}")
        content_mirror_args = [str(TOOLS / "mirror_reference.py"), content_url, "--out", workspace_root, "--own"]
        run_tool("içerik-indir", content_mirror_args, capture=False)

        content_host = _validate(content_url)
        cws_parent = Path(workspace_root) / re.sub(r"[^a-z0-9.-]", "_", content_host.lower())
        if cws_parent.is_dir():
            candidates = sorted(cws_parent.iterdir(), reverse=True)
            content_workspace = candidates[0] if candidates else None

        if content_workspace:
            run_tool("içerik-çıkar", [str(TOOLS / "extract_content.py"), str(content_workspace)], capture=False)
            content_json = content_workspace / "content.json"
            if content_json.is_file():
                content_data = json.loads(content_json.read_text(encoding="utf-8"))
    else:
        print("  İçerik kaynağı verilmedi, atlanıyor.")

    # 4. Font coverage
    print("\n4/5 Font kapsamı denetleniyor...")
    fonts_to_check = set()
    if analysis_data and analysis_data.get("fonts"):
        fonts_to_check.update(analysis_data["fonts"])
    font_checks = []
    if fonts_to_check:
        font_checks = check_fonts(list(fonts_to_check), lang)
    else:
        print("  Font bulunamadı, atlanıyor.")

    # Font stacks
    font_stacks = []
    r, _ = run_tool("yığınlar", [str(TOOLS / "font_coverage.py"), "--lang", lang, "--format", "json"], capture=True)
    if r and r.stdout.strip():
        try:
            stacks_data = json.loads(r.stdout)
            font_stacks = stacks_data.get("stacks") or []
        except json.JSONDecodeError:
            pass

    # 5. Build spec
    print("\n5/5 Build spec oluşturuluyor...")
    next_steps = []
    if capture.get("jsShell"):
        next_steps.append(f"Canlı yakalama: `node tools/v10/capture_reference.mjs --workspace {workspace}`")
    if capture.get("usage") == "study-only":
        next_steps.append("Referans study-only: kod/görsel/font kopyalanmaz, düzen yeni kodla kurulur.")
    next_steps.append(f"Tasarım tokenlarını kendi projenize uyarlayın: `{workspace}/tokens.css`")
    if any(fc.get("covers") is False for fc in font_checks):
        next_steps.append("Kapsamı yetersiz fontları önerilen yığınlarla değiştirin.")
    next_steps.append("Siteyi kurun ve karşılaştırın: `node tools/v10/compare_reference.mjs <ref.png> http://localhost:3000`")
    next_steps.append("Son denetim: `python tools/v10/check_site.py <site-klasörü>`")

    spec = {
        "version": "10.0",
        "reference": ref_info,
        "analysis": analysis_data,
        "content": content_data,
        "contentWorkspace": str(content_workspace) if content_workspace else None,
        "fontChecks": [{"family": fc.get("family", "?"), "covers": fc.get("covers"),
                        "installed": fc.get("installed"), "missing": fc.get("missing", []),
                        "note": fc.get("note", "")} for fc in font_checks],
        "fontStacks": [{"role": s.get("role", "?"), "stack": s.get("stack", ""),
                        "note": s.get("note", "")} for s in font_stacks],
        "lang": lang,
        "nextSteps": next_steps,
        "skipped": skipped,
    }

    spec_path = workspace / "build-spec.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path = workspace / "build-spec.md"
    md_path.write_text(build_spec_md(spec), encoding="utf-8")
    print(f"\nBuild spec: {spec_path}")
    print(f"Build spec (MD): {md_path}")
    return spec


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Referans tabanlı site oluşturma: indir → analiz → içerik çıkar → font denetle → build spec.",
        epilog="Örnek: python tools/v10/build_from_reference.py https://www.orneksite.com --content https://kendi-sitem.com")
    parser.add_argument("reference", help="Referans site adresi")
    parser.add_argument("--content", help="İçerik kaynağı site adresi (kendi siten)")
    parser.add_argument("--out", help="Çalışma alanı kökü")
    parser.add_argument("--level", type=int, default=2, help="wget bağlantı derinliği")
    parser.add_argument("--quota-mb", type=int, default=200, help="wget indirme sınırı (MB)")
    parser.add_argument("--wait", type=float, default=1.0, help="wget istekler arası bekleme (sn)")
    parser.add_argument("--own", action="store_true", help="Referans site sana ait")
    parser.add_argument("--lang", default="tr", help="Font kapsamı dili (varsayılan: tr)")
    parser.add_argument("--allow-domain", action="append", default=[], help="Ek CDN alan adı")
    parser.add_argument("--dry-run", action="store_true", help="Yalnız planı göster")
    args = parser.parse_args(argv)

    if args.dry_run:
        print("Pipeline adımları:")
        print(f"  1. wget {args.reference}")
        print(f"  2. analyze_reference → tokens.css, analysis.json")
        if args.content:
            print(f"  3. wget {args.content} → extract_content → content.json")
        else:
            print(f"  3. (içerik kaynağı yok, atlanıyor)")
        print(f"  4. font_coverage --lang {args.lang}")
        print(f"  5. build-spec.json + build-spec.md")
        return 0

    spec = pipeline(args.reference, args.content, args.out, args.level, args.quota_mb,
                    args.wait, args.own, args.lang, args.allow_domain)
    has_analysis = spec.get("analysis") is not None
    return 0 if has_analysis else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
