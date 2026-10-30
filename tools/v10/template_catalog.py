#!/usr/bin/env python3
"""Açık kaynak şablon ve bileşen kaynaklarını lisansa göre listeler; veriyi v8 kaynak kaydından okur."""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PERMISSIVE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "0BSD", "Unlicense", "CC0-1.0"}
COPYLEFT = {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.1", "LGPL-3.0", "MPL-2.0"}
TEMPLATE_ROLES = {"site-template", "app-starter", "dashboard-template", "site-reference"}
COMPONENT_ROLES = {"ui-foundation", "component-accent", "motion-component", "headless-primitives"}
RIGHTS = {
    "permissive": "Kodu indirip düzenleyebilirsin; LICENSE dosyasını ve telif satırını koru. Görsel ve fontların lisansını ayrıca kontrol et.",
    "copyleft": "Düzenleyebilirsin ama dağıttığın türev çalışma da aynı lisansla açık olmalı.",
    "unknown": "Depo lisansı doğrulanmadı; LICENSE dosyasını okumadan kod kopyalama, yalnız incele.",
}


def license_class(license_id):
    if license_id in PERMISSIVE:
        return "permissive"
    if license_id in COPYLEFT:
        return "copyleft"
    return "unknown"


def load(root=ROOT):
    registry = json.loads((root / "data/v8/source_registry.json").read_text(encoding="utf-8"))
    profiles = json.loads((root / "data/v8/source_profiles.json").read_text(encoding="utf-8"))["profiles"]
    entries = []
    for source in registry["sources"]:
        profile = profiles.get(source["id"], {})
        if source.get("kind") != "repository" or source.get("access") != "available":
            continue
        role = profile.get("role")
        if role not in TEMPLATE_ROLES | COMPONENT_ROLES:
            continue
        rights = license_class(source.get("license"))
        note = RIGHTS[rights]
        if role == "site-reference":
            note += " Kişisel sitedir; yazı ve fotoğraflar kodla aynı lisansta olmayabilir."
        entries.append({
            "id": source["id"], "url": source["url"], "license": source.get("license") or "doğrulanmadı",
            "rights": rights, "rightsNote": note, "kind": "template" if role in TEMPLATE_ROLES else "component",
            "role": role, "stack": profile.get("stack", []), "focus": profile.get("focus", ""),
            "get": f"git clone --depth 1 {source['url']}.git",
        })
    return registry.get("checkedAt"), sorted(entries, key=lambda e: (e["rights"] != "permissive", e["kind"], e["id"]))


def select(entries, kind=None, stack=None, rights=None):
    return [e for e in entries if (not kind or e["kind"] == kind) and (not stack or stack in e["stack"])
            and (not rights or e["rights"] == rights)]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Lisansı bilinen açık kaynak şablon ve bileşenleri listeler.")
    parser.add_argument("--kind", choices=("template", "component"))
    parser.add_argument("--stack", help="örn. next, react, astro, tailwind, html")
    parser.add_argument("--rights", choices=tuple(RIGHTS), help="permissive: düzenlenebilir, copyleft: aynı lisansla, unknown: yalnız incele")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    checked_at, entries = load()
    chosen = select(entries, args.kind, args.stack, args.rights)
    if args.format == "json":
        print(json.dumps({"checkedAt": checked_at, "entries": chosen}, ensure_ascii=False, indent=2))
        return 0
    print(f"Lisans bilgisi depo düzeyinde, {checked_at} tarihli. Kullanmadan önce indirilen kopyadaki LICENSE dosyasını oku.")
    for entry in chosen:
        print(f"- {entry['id']} [{entry['license']} · {entry['kind']} · {', '.join(entry['stack'])}]")
        print(f"  {entry['rightsNote']}")
        print(f"  {entry['get']}")
    if not chosen:
        print("Eşleşen kaynak yok; filtreleri gevşet.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
