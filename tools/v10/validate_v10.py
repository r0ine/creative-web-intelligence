#!/usr/bin/env python3
"""v10 referans laboratuvarının dosyalarını ve diğer katmanlarla tutarlılığını; ardından v9 zincirini doğrular."""

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUIRED = (
    "START_HERE_V10.md", "RELEASE_NOTES_V10.md", "RELEASE_NOTES_V10.en.md", "reference-engine/REFERENCE_LAB.md",
    "tools/v10/mirror_reference.py", "tools/v10/capture_reference.mjs", "tools/v10/analyze_reference.py",
    "tools/v10/compare_reference.mjs", "tools/v10/template_catalog.py", "tools/v10/extract_content.py", "tools/v10/font_coverage.py", "tools/v10/validate_v10.py",
    "data/v10/font_stacks.json",
    "runtime/reference/style-metrics.mjs", "runtime/reference/pixel-compare.mjs",
    "tests/test_v10_reference_lab.py", "tests/style-metrics.test.mjs", "tests/fixtures/reference-site/index.html",
)


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def check_consistency(root=ROOT):
    errors = []
    analyzer = module("analyze_reference", "tools/v10/analyze_reference.py")
    catalog = module("template_catalog", "tools/v10/template_catalog.py")
    ranking = json.loads((root / "data/v9/visibility_ranking.json").read_text(encoding="utf-8"))
    surfaces = {surface["id"] for surface in ranking["surfaces"]}
    if set(analyzer.SURFACE_RULES) != surfaces:
        missing = sorted(surfaces - set(analyzer.SURFACE_RULES))
        extra = sorted(set(analyzer.SURFACE_RULES) - surfaces)
        errors.append(f"Düzenleme haritası v9 yüzeyleriyle uyuşmuyor; eksik: {missing}, fazla: {extra}")

    register = json.loads((root / "data/v9/rule_precedence.json").read_text(encoding="utf-8"))
    known = {conflict["id"] for conflict in register["conflicts"]}
    source = (root / "tools/v10/analyze_reference.py").read_text(encoding="utf-8")
    for cited in sorted(set(re.findall(r'"conflict": "(CF-\d{3})"', source))):
        if cited not in known:
            errors.append(f"analyze_reference.py bilinmeyen çakışmaya bağlanıyor: {cited}")

    _, entries = catalog.load(root)
    if not entries:
        errors.append("Şablon kataloğu boş; v8 kaynak kaydı okunamadı.")
    if catalog.PERMISSIVE & catalog.COPYLEFT:
        errors.append("Bir lisans hem izin verici hem copyleft sayılıyor.")

    font_data = json.loads((root / "data/v10/font_stacks.json").read_text(encoding="utf-8"))
    languages = set(font_data["languages"])
    for stack in font_data["stacks"]:
        if stack["role"] not in {"display", "body", "mono"}:
            errors.append(f"font_stacks: bilinmeyen rol {stack['role']} ({stack['id']})")
        for lang in stack["lang"]:
            if lang not in languages:
                errors.append(f"font_stacks: {stack['id']} bilinmeyen dile bağlı: {lang}")
    gitignore = (root / ".gitignore").read_text(encoding="utf-8").split()
    if "reference-workspace/" not in gitignore:
        errors.append(".gitignore indirilen siteleri (reference-workspace/) dışarıda bırakmıyor.")
    return errors


def main():
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        print("Eksik v10 dosyaları: " + ", ".join(missing), file=sys.stderr)
        return 1
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    errors = [] if manifest.get("version") == "10.0" and manifest.get("v10") else ["manifest.json v10 bilgisi eksik."]
    errors += check_consistency()
    for error in errors:
        print("- " + error, file=sys.stderr)
    print(f"v10 hata sayısı: {len(errors)}")
    if errors:
        return 1
    commands = (
        [sys.executable, str(ROOT / "tools/v9/validate_v9.py")],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_v10_*.py"],
        ["node", "--test", str(ROOT / "tests/style-metrics.test.mjs")],
    )
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            return result.returncode
    print("v10 doğrulaması geçti.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
