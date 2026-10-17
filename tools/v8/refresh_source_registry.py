#!/usr/bin/env python3
"""Kullanıcının kaynak listesini GitHub depo meta verisiyle günceller."""

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
CANDIDATES = ROOT / "data/v8/source_candidates.json"
OUTPUT = ROOT / "data/v8/source_registry.json"


def inspect_source(item):
    category, url = item
    path = urlparse(url).path.strip("/")
    if path.startswith("topics/"):
        return {
            "id": path.lower(), "category": category, "kind": "topic-index",
            "url": url, "access": "index", "license": None,
            "licenseEvidence": "not-applicable", "designEvidence": "not-reviewed",
            "codeReuse": "not-applicable",
        }
    if "/" not in path:
        return {
            "id": f"org/{path.lower()}", "category": category, "kind": "organization-index",
            "url": url, "access": "index", "license": None,
            "licenseEvidence": "not-applicable", "designEvidence": "not-reviewed",
            "codeReuse": "not-applicable",
        }

    result = subprocess.run(
        ["gh", "api", f"repos/{path}"], capture_output=True, text=True,
        encoding="utf-8", check=False,
    )
    if result.returncode:
        return {
            "id": path.lower(), "category": category, "kind": "repository",
            "url": url, "access": "unverified", "license": None,
            "licenseEvidence": "unverified", "designEvidence": "not-reviewed",
            "codeReuse": "blocked", "reviewNote": result.stderr.strip()[:240],
        }

    repo = json.loads(result.stdout)
    license_info = repo.get("license") or {}
    spdx = license_info.get("spdx_id")
    if spdx == "NOASSERTION":
        spdx = None
    return {
        "id": path.lower(), "category": category, "kind": "repository",
        "url": url, "canonicalUrl": repo["html_url"],
        "access": "available", "archived": repo["archived"],
        "description": repo.get("description"),
        "language": repo.get("language"),
        "topics": repo.get("topics", []),
        "defaultBranch": repo["default_branch"],
        "lastPushed": repo.get("pushed_at"),
        "license": spdx, "licenseEvidence": "github-api" if spdx else "manual-review-needed",
        "licenseUrl": f"https://api.github.com/repos/{repo['full_name']}/license" if spdx else None,
        "metadataUrl": repo["url"],
        "designEvidence": "not-reviewed", "codeReuse": "blocked-until-file-license-review",
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not shutil_gh_available():
        print("gh CLI bulunamadı. Kayıt yenileme için gh auth login gerekir.", file=sys.stderr)
        return 2
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    items = [(category, url) for category, urls in candidates.items()
             if isinstance(urls, list) for url in urls]
    with ThreadPoolExecutor(max_workers=4) as pool:
        sources = list(pool.map(inspect_source, items))
    registry = {
        "version": "8.0", "checkedAt": date.today().isoformat(),
        "scope": "GitHub metadata only; no rendered design or source-code review implied",
        "sources": sources,
    }
    OUTPUT.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    unavailable = [source["id"] for source in sources if source["access"] == "unverified"]
    unknown = [source["id"] for source in sources if source["kind"] == "repository" and not source["license"]]
    print(f"{len(sources)} kaynak kaydedildi; {len(unavailable)} erişim, {len(unknown)} lisans yeniden inceleme istiyor.")
    if unavailable:
        print("Erişim doğrulanamadı: " + ", ".join(unavailable))
    if unknown:
        print("Lisans meta verisi yok: " + ", ".join(unknown))
    return 0


def shutil_gh_available():
    from shutil import which
    return which("gh") is not None


if __name__ == "__main__":
    raise SystemExit(main())
