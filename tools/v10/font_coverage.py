#!/usr/bin/env python3
"""Bir font ailesinin dil (ör. Türkçe) glif kapsamını kontrol eder ve çevrimdışı sistem-font yığınları önerir.

Veri `data/v10/font_stacks.json`'dan gelir ve her ortamda çalışır. fontconfig (fc-list) kuruluysa
istenen kod noktaları canlı olarak da denetlenir; böylece veri tablosunda olmayan fontlar da ölçülür.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/v10/font_stacks.json"


def load(path=DATA):
    return json.loads(path.read_text(encoding="utf-8"))


def families_in_stack(stack):
    """Bir CSS font yığınındaki aile adlarını, genel aileleri atlayarak döndürür."""
    generic = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
               "ui-serif", "ui-sans-serif", "ui-monospace", "ui-rounded"}
    names = [part.strip().strip("\"'") for part in stack.split(",")]
    return [name for name in names if name and name.lower() not in generic]


def fc_available():
    return shutil.which("fc-list") is not None


def fc_query(pattern):
    """fc-list çıktısı (satırlar) veya fc-list yoksa/çağrı başarısızsa None."""
    if not fc_available():
        return None
    try:
        result = subprocess.run(["fc-list", pattern, "family"],
                                capture_output=True, encoding="utf-8", errors="replace", timeout=10, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip()


def fc_family_present(family):
    """Aile sistemde gerçekten kurulu mu? (Kurulu değilse glif denetimi yanıltıcı olur.)"""
    output = fc_query(f":family={family}")
    if output is None:
        return None
    return any(family.lower() in line.lower() for line in output.splitlines())


def fc_covers(family, codepoint):
    """fontconfig'e göre aile bu kod noktasını içeriyor mu?"""
    output = fc_query(f":family={family}:charset={codepoint.lower()}")
    return None if output is None else bool(output)


def check_family(family, language, data):
    lang = data["languages"][language]
    record = data["fonts"].get(family)
    known = record["covers"].get(language) if record else None
    present = fc_family_present(family)  # True/False/None
    live_missing, live_checked = [], False
    if present:
        for codepoint in lang["required"]:
            covered = fc_covers(family, codepoint)
            if covered is None:
                break
            live_checked = True
            if not covered:
                live_missing.append(codepoint)
    live = (not live_missing) if live_checked else None
    covers = live if live is not None else known
    return {
        "family": family,
        "language": language,
        "covers": covers,
        "known": known,
        "live": live,
        "installed": present,
        "missing": [chr(int(cp, 16)) for cp in live_missing],
        "note": (record or {}).get("note", ""),
    }


def stacks_for(language, data, role=None):
    return [stack for stack in data["stacks"]
            if language in stack["lang"] and (role is None or stack["role"] == role)]


def report(result=None, stacks=None, language="tr", data=None):
    lines = []
    if result:
        lang_name = data["languages"][language]["name"]
        status = {True: "kapsıyor", False: "KAPSAMIYOR", None: "bilinmiyor"}[result["covers"]]
        lines.append(f"{result['family']} · {lang_name}: {status}")
        if result["missing"]:
            lines.append("  Eksik glifler: " + " ".join(result["missing"]))
        if result["live"] is not None:
            lines.append("  (fontconfig ile canlı denetlendi)")
        elif result["known"] is not None:
            reason = "sistemde kurulu değil" if result["installed"] is False else "fontconfig yok"
            lines.append(f"  (veri tablosundan; {reason})")
        else:
            lines.append("  Bu aile veri tablosunda yok ve canlı doğrulanamadı; kapsam bilinmiyor.")
        if result["note"]:
            lines.append(f"  Not: {result['note']}")
        if result["covers"] is False:
            lines.append("  Öneri: aşağıdaki çevrimdışı yığınlardan birini kullan.")
    if stacks is not None:
        lang_name = data["languages"][language]["name"]
        lines.append(f"{lang_name} kapsayan çevrimdışı yığınlar:" if not result else "")
        for stack in stacks:
            lines.append(f"- [{stack['role']}] {stack['stack']}")
            lines.append(f"    {stack['note']}")
    return "\n".join(line for line in lines if line is not None)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Font dil kapsamını denetler ve çevrimdışı sistem-font yığınları önerir.")
    parser.add_argument("family", nargs="?", help="Denetlenecek aile adı, ör. \"Bitstream Charter\". Verilmezse yığınlar listelenir.")
    parser.add_argument("--lang", default="tr", help="Dil kodu (varsayılan tr)")
    parser.add_argument("--role", choices=("display", "body", "mono"), help="Önerilerde rol filtresi")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    data = load()
    if args.lang not in data["languages"]:
        parser.error("Bilinmeyen dil: " + args.lang + ". Diller: " + ", ".join(data["languages"]))
    result = check_family(args.family, args.lang, data) if args.family else None
    stacks = stacks_for(args.lang, data, args.role) if (not args.family or (result and result["covers"] is False)) else None
    if args.format == "json":
        print(json.dumps({"check": result, "stacks": stacks}, ensure_ascii=False, indent=2))
    else:
        print(report(result, stacks, args.lang, data))
    return 1 if result and result["covers"] is False else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
