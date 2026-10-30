#!/usr/bin/env python3
"""v9 geri bildirim sözlüğünü, kural önceliğini ve çakışma kaydını; ardından v8 zincirini doğrular."""

import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUIRED = (
    "START_HERE_V9.md", "RELEASE_NOTES_V9.md", "RELEASE_NOTES_V9.en.md",
    "reference-engine/REVISION_FEEDBACK.md", "v9/RULE_PRECEDENCE.md",
    "data/v9/feedback_lexicon.json", "data/v9/visibility_ranking.json", "data/v9/rule_precedence.json",
    "tools/v9/feedback_triage.py", "tools/v9/precedence.py", "tools/v9/validate_v9.py",
    "tests/test_v9_feedback_triage.py", "tests/test_v9_precedence.py",
)
DIRECTOR_GLOBS = ("directors/**/*.md", "v[0-9]*/**/*DIRECTOR*.md")
ENTRY_KINDS = {"vague", "direction", "revert"}
MARKER_KEYS = ("global", "positive", "negateAfter", "negateBefore", "contrast")
NOTE = "Öncelik (v9)"


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


TRIAGE = module("feedback_triage", "tools/v9/feedback_triage.py")
PRECEDENCE = module("precedence", "tools/v9/precedence.py")


def read_json(root, relative, errors):
    try:
        return json.loads((root / relative).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{relative}: okunamadı ({error})")
        return None


def missing_files(root, paths, owner, errors):
    for path in paths:
        if not (root / path).is_file():
            errors.append(f"{owner}: dosya yok: {path}")


def check_feedback(root=ROOT):
    errors = []
    lexicon = read_json(root, "data/v9/feedback_lexicon.json", errors)
    ranking = read_json(root, "data/v9/visibility_ranking.json", errors)
    if lexicon is None or ranking is None:
        return errors
    for name, data in (("feedback_lexicon", lexicon), ("visibility_ranking", ranking)):
        if data.get("version") != "9.0":
            errors.append(f"{name}: version 9.0 olmalı")

    surfaces = ranking.get("surfaces", [])
    ids = [s.get("id") for s in surfaces]
    for rid, count in Counter(ids).items():
        if count > 1:
            errors.append(f"visibility_ranking: yinelenen yüzey {rid}")
    if sorted(s.get("rank") for s in surfaces) != list(range(1, len(surfaces) + 1)):
        errors.append("visibility_ranking: sıra 1'den başlayıp boşluksuz artmalı")
    for surface in surfaces:
        for key in ("label", "why", "phrases", "changes", "cssHints", "references"):
            if not surface.get(key):
                errors.append(f"{surface.get('id')}: {key} boş")
        missing_files(root, surface.get("references", []), surface.get("id"), errors)

    entries = lexicon.get("entries", [])
    for rid, count in Counter(e.get("id") for e in entries).items():
        if count > 1:
            errors.append(f"feedback_lexicon: yinelenen kimlik {rid}")
    for entry in entries:
        rid = entry.get("id", "?")
        if not re.fullmatch(r"FB-\d{2}", rid):
            errors.append(f"{rid}: kimlik FB-00 biçiminde olmalı")
        if entry.get("kind") not in ENTRY_KINDS:
            errors.append(f"{rid}: bilinmeyen tür {entry.get('kind')}")
        required = ("label", "phrases", "likelySurfaces", "causes", "firstMoves", "avoid", "references") \
            if entry.get("kind") == "direction" else ("label", "phrases", "meaning")
        for key in required:
            if not entry.get(key):
                errors.append(f"{rid}: {key} boş")
        for surface in entry.get("likelySurfaces", []):
            if surface not in ids:
                errors.append(f"{rid}: bilinmeyen yüzey {surface}")
        missing_files(root, entry.get("references", []), rid, errors)

    markers = lexicon.get("markers", {})
    for key in MARKER_KEYS:
        if not markers.get(key):
            errors.append(f"markers.{key} boş")
    contrast = {token for value in markers.get("contrast", []) for token in TRIAGE.words(value)}

    owners = {}
    phrases = [(f"yüzey {s['id']}", p) for s in surfaces for p in s.get("phrases", [])]
    phrases += [(f"giriş {e['id']}", p) for e in entries for p in e.get("phrases", [])]
    phrases += [(f"işaret {k}", p) for k in ("global", "positive") for p in markers.get(k, [])]
    for owner, phrase in phrases:
        key = TRIAGE.pattern(phrase)
        if not key[0]:
            errors.append(f"{owner}: boş ifade '{phrase}'")
            continue
        if contrast & set(key[0]):
            errors.append(f"{owner}: '{phrase}' bağlaç içeriyor; cümle bölünürken kaybolur")
        if key in owners and owners[key] != owner:
            errors.append(f"'{phrase}' iki anlama bağlı: {owners[key]} ve {owner}")
        owners.setdefault(key, owner)
    return errors


def director_files(root):
    found = set()
    for pattern in DIRECTOR_GLOBS:
        found |= {p.relative_to(root).as_posix() for p in root.glob(pattern) if p.is_file()}
    return sorted(found)


def check_matcher(root, matcher, owner, errors):
    if not (root / matcher.get("file", "")).is_file():
        errors.append(f"{owner}: dosya yok: {matcher.get('file')}")
        return None
    kinds = [key for key in ("contains", "ids", "pattern") if key in matcher]
    if len(kinds) != 1 or (kinds == ["pattern"] and not matcher.get("fields")):
        errors.append(f"{owner}: eşleştirici contains, ids veya pattern+fields'tan yalnız birini içermeli")
        return None
    if "pattern" in matcher:
        try:
            re.compile(matcher["pattern"])
        except re.error as error:
            errors.append(f"{owner}: geçersiz desen ({error})")
            return None
    return PRECEDENCE.matched(matcher, root)


def check_precedence(root=ROOT):
    errors = []
    register = read_json(root, PRECEDENCE.REGISTER, errors)
    if register is None:
        return errors
    if register.get("version") != "9.0":
        errors.append("rule_precedence: version 9.0 olmalı")

    levels = [item.get("level") for item in register.get("order", [])]
    if levels != list(range(1, len(levels) + 1)):
        errors.append("order: düzeyler 1'den başlayıp boşluksuz artmalı")
    for item in register.get("order", []):
        for path in item.get("paths", []):
            if not (root / path).exists():
                errors.append(f"order {item.get('level')}: yol yok: {path}")

    domains = register.get("domains", [])
    for name, count in Counter(d.get("domain") for d in domains).items():
        if count > 1:
            errors.append(f"yinelenen alan {name}")
    registered = Counter()
    for domain in domains:
        files = [domain.get("winner"), *domain.get("alongside", []), *domain.get("superseded", [])]
        registered.update(files)
        missing_files(root, files, f"alan {domain.get('domain')}", errors)
        for path in [*domain.get("alongside", []), *domain.get("superseded", [])]:
            if (root / path).is_file():
                head = (root / path).read_text(encoding="utf-8")[:800]
                if NOTE not in head or domain["winner"] not in head:
                    errors.append(f"{path}: başında geçerli dosyayı ({domain['winner']}) gösteren '{NOTE}' notu yok")
    for path in director_files(root):
        if registered[path] == 0:
            errors.append(f"{path}: director öncelik kaydında hiçbir alana bağlı değil")
    for path, count in registered.items():
        if count > 1:
            errors.append(f"{path}: birden fazla alanda kayıtlı")

    conflicts = register.get("conflicts", [])
    for rid, count in Counter(c.get("id") for c in conflicts).items():
        if count > 1:
            errors.append(f"yinelenen çakışma {rid}")
    for conflict in conflicts:
        rid = conflict.get("id", "?")
        if not re.fullmatch(r"CF-\d{3}", rid):
            errors.append(f"{rid}: kimlik CF-000 biçiminde olmalı")
        if conflict.get("status") not in {"open", "resolved"}:
            errors.append(f"{rid}: durum open veya resolved olmalı")
        for key in ("topic", "resolution", "older", "newer"):
            if not conflict.get(key):
                errors.append(f"{rid}: {key} boş")
        for matcher in conflict.get("older", []):
            hits = check_matcher(root, matcher, f"{rid} eski", errors)
            if hits is None:
                continue
            if conflict.get("status") == "open" and not hits:
                errors.append(f"{rid}: eski taraf artık {matcher['file']} içinde eşleşmiyor; düzeltildiyse status: resolved yap")
            if conflict.get("status") == "resolved" and hits:
                errors.append(f"{rid}: çözüldü denmiş ama {matcher['file']} içinde hâlâ {len(hits)} kayıt eşleşiyor")
        for matcher in conflict.get("newer", []):
            hits = check_matcher(root, matcher, f"{rid} yeni", errors)
            expected = len(matcher.get("ids", [])) or 1
            if hits is not None and len(hits) < expected:
                errors.append(f"{rid}: yeni taraftaki kanıt {matcher['file']} içinde bulunamadı")

    listed = {item.get("id"): sorted(item.get("files", [])) for item in register.get("idCollisions", [])}
    for item in register.get("idCollisions", []):
        if not item.get("reason"):
            errors.append(f"idCollisions {item.get('id')}: gerekçe yok")
    actual = PRECEDENCE.id_collisions(root)
    for rid, files in actual.items():
        if rid not in listed:
            errors.append(f"kimlik çakışması: '{rid}' birden fazla dosyada: {', '.join(files)}")
        elif listed[rid] != files:
            errors.append(f"kimlik çakışması '{rid}' kayıtlı dosyalardan farklı: {', '.join(files)}")
    for rid in listed:
        if rid not in actual:
            errors.append(f"idCollisions '{rid}': artık çakışmıyor; listeden çıkar")
    return errors


def main():
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        print("Eksik v9 dosyaları: " + ", ".join(missing), file=sys.stderr)
        return 1
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    errors = [] if float(manifest.get("version", 0)) >= 9 and manifest.get("v9") else ["manifest.json v9 bilgisi eksik."]
    errors += check_feedback() + check_precedence()
    for error in errors:
        print("- " + error, file=sys.stderr)
    print(f"v9 hata sayısı: {len(errors)}")
    if errors:
        return 1

    commands = (
        [sys.executable, str(ROOT / "tools/v8/validate_v8.py")],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_v9_*.py"],
    )
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            return result.returncode
    print("v9 doğrulaması geçti.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
