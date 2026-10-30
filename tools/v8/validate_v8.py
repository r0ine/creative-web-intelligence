#!/usr/bin/env python3
"""v8 kaynak kapsamını, kanıt sınırlarını ve eski sürüm doğrulamasını sınar."""

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUIRED = (
    "START_HERE_V8.md", "README_V8.md", "README_V8.en.md",
    "RELEASE_NOTES_V8.md", "RELEASE_NOTES_V8.en.md",
    "source-intelligence/V8_SOURCE_INTELLIGENCE.md",
    "data/v8/source_candidates.json", "data/v8/source_registry.json",
    "data/v8/source_profiles.json", "data/v8/readme_findings.json",
    "tools/v8/source_advisor.py", "tests/test_v8_source_advisor.py",
    "tools/v8/experience_plan.mjs", "runtime/media/experience-plan.mjs",
    "runtime/three/pointer-look.mjs", "v8/OPTIONAL_VIDEO_POINTER_WORKFLOW.md",
    "examples/v8/experience-brief.json", "examples/v8/experience-brief-with-video.json",
    "tests/experience-plan.test.mjs", "tests/pointer-look.test.mjs",
)


def fail(message):
    print(message, file=sys.stderr)
    return 1


def main():
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        return fail("Eksik v8 dosyaları: " + ", ".join(missing))
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("version") not in {"8.0", "9.0"} or not manifest.get("v8"):
        return fail("manifest.json v8 bilgisi eksik.")

    candidates = json.loads((ROOT / "data/v8/source_candidates.json").read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "data/v8/source_registry.json").read_text(encoding="utf-8"))
    profiles = json.loads((ROOT / "data/v8/source_profiles.json").read_text(encoding="utf-8"))["profiles"]
    findings = json.loads((ROOT / "data/v8/readme_findings.json").read_text(encoding="utf-8"))["findings"]
    urls = [url for group in candidates.values() if isinstance(group, list) for url in group]
    sources = registry["sources"]
    ids = [source["id"] for source in sources]
    if len(urls) != 46 or len(urls) != len(set(urls)):
        return fail("Kullanıcının 46 bağlantısı eksik veya yinelenmiş.")
    if len(sources) != len(urls) or {source["url"] for source in sources} != set(urls):
        return fail("Kaynak kayıtları aday listesini karşılamıyor.")
    if len(ids) != len(set(ids)) or set(ids) != set(profiles):
        return fail("Kaynak profilleriyle kayıt kimlikleri uyuşmuyor.")
    if not set(findings).issubset(ids):
        return fail("README bulgusu bilinmeyen bir kaynağa bağlı.")
    if any(source["kind"] == "repository" and source["access"] != "available" and source["codeReuse"] != "blocked" for source in sources):
        return fail("Erişilemeyen depo yeniden kullanıma kapalı olmalı.")
    if any(source["kind"] == "repository" and source["access"] == "available" and not source.get("license") and source["codeReuse"] != "blocked-until-file-license-review" for source in sources):
        return fail("Lisansı bilinmeyen deponun kodu yeniden kullanıma açık görünüyor.")

    commands = (
        [sys.executable, str(ROOT / "tools/v7/validate_v7.py")],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_v8_*.py", "-v"],
        ["node", "--test", str(ROOT / "tests/experience-plan.test.mjs"), str(ROOT / "tests/pointer-look.test.mjs")],
    )
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            return result.returncode
    print("v8 doğrulaması geçti.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
