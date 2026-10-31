#!/usr/bin/env python3
"""Bir siteyi kütüphanenin üç denetim aracıyla tek seferde denetler ve birleşik rapor üretir.

Çalıştırılan araçlar:
  1. analyze_reference.py — tasarım ölçüleri, kural çakışmaları, erişilebilirlik
  2. audit_visual_defaults.mjs — v7 görsel kalıp denetimi
  3. authenticity_check.py — v5 özgünlük kapısı

Her aracın kapsamı ve sınırları raporda ayrı ayrı belirtilir.
Hiçbiri tek başına yeterli kanıt değildir; birleşik rapor üç bakış açısını bir araya getirir.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from shutil import which

ROOT = Path(__file__).resolve().parents[2]
TOOLS_V10 = ROOT / "tools" / "v10"
TOOLS_V7 = ROOT / "tools" / "v7"
TOOLS_V5 = ROOT / "tools" / "v5"


def run_python(label, script, args, timeout=120):
    """Python aracını çalıştır."""
    cmd = [sys.executable, "-I", str(script)] + args
    try:
        r = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace",
                           timeout=timeout, check=False)
        return {"tool": label, "exit": r.returncode, "stdout": r.stdout, "stderr": r.stderr}
    except Exception as exc:
        return {"tool": label, "exit": -1, "stdout": "", "stderr": str(exc)}


def run_node(label, script, args, timeout=120):
    """Node aracını çalıştır."""
    node = which("node")
    if not node:
        return {"tool": label, "exit": -1, "stdout": "", "stderr": "node bulunamadı"}
    cmd = [node, str(script)] + args
    try:
        r = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace",
                           timeout=timeout, check=False)
        return {"tool": label, "exit": r.returncode, "stdout": r.stdout, "stderr": r.stderr}
    except Exception as exc:
        return {"tool": label, "exit": -1, "stdout": "", "stderr": str(exc)}


def parse_analysis(result):
    """analyze_reference çıktısından bulgu sayılarını çıkar."""
    findings = {"ruleConflicts": 0, "accessibility": 0, "fonts": [], "libraries": []}
    text = result["stdout"]
    for line in text.splitlines():
        if "çakışma" in line.lower() or "conflict" in line.lower():
            try:
                findings["ruleConflicts"] = int("".join(c for c in line.split(":")[0] if c.isdigit()) or 0)
            except ValueError:
                pass
    # Try JSON from file
    return findings


def format_report(target, results, analysis_json_path=None):
    """Birleşik raporu Markdown olarak oluştur."""
    lines = [f"# Site denetim raporu: {target}", ""]

    for r in results:
        status = "tamam" if r["exit"] == 0 else f"çıkış kodu {r['exit']}"
        lines.append(f"## {r['tool']} ({status})")
        if r["exit"] == -1:
            lines.append(f"Çalıştırılamadı: {r['stderr']}")
        else:
            output = r["stdout"].strip()
            if output:
                lines.append("```")
                lines.append(output[:3000])
                lines.append("```")
            if r["stderr"].strip():
                lines.append(f"Uyarı: {r['stderr'].strip()[:500]}")
        lines.append("")

    # Summary
    lines.append("## Özet")
    total_issues = 0
    for r in results:
        if r["exit"] != 0 and r["exit"] != -1:
            total_issues += 1
    lines.append(f"- Çalıştırılan araç: {len(results)}")
    lines.append(f"- Sorunlu çıkış: {total_issues}")

    # Analysis details from JSON
    if analysis_json_path and analysis_json_path.is_file():
        try:
            data = json.loads(analysis_json_path.read_text(encoding="utf-8"))
            conflicts = data.get("ruleConflicts", [])
            a11y = data.get("accessibility", [])
            lines.append(f"- Kural çakışması: {len(conflicts)}")
            lines.append(f"- Erişilebilirlik bulgusu: {len(a11y)}")
        except (json.JSONDecodeError, KeyError):
            pass

    lines.append("")
    lines.append("## Kapsam ve sınırlar")
    lines.append("- **analyze_reference**: CSS ölçüleri, renk, font, kontrast (sınırlı çift), kural çakışmaları. "
                 "Bakmaz: odak göstergesi, dokunma hedefi, form etiketi, skip link.")
    lines.append("- **audit_visual_defaults**: v7 görsel kalıplar (transition-all, infinite-motion, "
                 "büyük gölge, çakışan z-index). Bakmaz: aşmalı eğri (CF-008), kontrast, erişilebilirlik.")
    lines.append("- **authenticity_check**: v5 özgünlük kapısı (dekorasyon/yapı oranı, tema benzersizliği). "
                 "Bakmaz: CF-007/CF-008, .mjs dosyaları, kural çakışmaları.")
    lines.append("")
    lines.append("Hiçbir aracın tek başına temiz çıktısı yeterli kanıt değildir. Canlı görsel denetim (Playwright) ayrıca gereklidir.")
    lines.append("")
    lines.append("---")
    lines.append("*check_site.py tarafından oluşturuldu.*")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Siteyi üç denetim aracıyla (analiz + v7 audit + v5 authenticity) tek seferde denetle.",
        epilog="Örnek: python tools/v10/check_site.py examples/v10/test-site/")
    parser.add_argument("target", help="Site klasörü veya HTML dosyası")
    parser.add_argument("--no-write", action="store_true", help="Analiz dosyalarını yazma")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    target = Path(args.target)
    if not target.exists():
        parser.error(f"Bulunamadı: {target}")

    results = []

    # 1. analyze_reference
    analyze_args = [str(target)]
    if args.no_write:
        analyze_args.append("--no-write")
    results.append(run_python("analyze_reference", TOOLS_V10 / "analyze_reference.py", analyze_args))

    # 2. audit_visual_defaults (Node)
    results.append(run_node("audit_visual_defaults", TOOLS_V7 / "audit_visual_defaults.mjs", [str(target)]))

    # 3. authenticity_check
    results.append(run_python("authenticity_check", TOOLS_V5 / "authenticity_check.py", [str(target)]))

    # Analysis JSON
    analysis_json = target / "analysis.json" if target.is_dir() else target.parent / "analysis.json"

    if args.format == "json":
        output = {
            "target": str(target),
            "results": [{"tool": r["tool"], "exit": r["exit"],
                          "output": r["stdout"][:2000], "error": r["stderr"][:500]}
                         for r in results],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        report = format_report(target, results, analysis_json if not args.no_write else None)
        print(report)

        # Write report
        if not args.no_write:
            out = target if target.is_dir() else target.parent
            report_path = out / "check-report.md"
            report_path.write_text(report, encoding="utf-8")
            print(f"\nRapor: {report_path}")

    return 1 if any(r["exit"] != 0 and r["exit"] != -1 for r in results) else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
