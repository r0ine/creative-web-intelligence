#!/usr/bin/env python3
"""Sürümler arası kural önceliğini ve bilinen çakışmaları sorgular."""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = "data/v9/rule_precedence.json"


def load(root=ROOT):
    return json.loads((root / REGISTER).read_text(encoding="utf-8"))


def records(data):
    """JSON içindeki kimlikli bütün kayıtları gezer; v2 listeleri ve v5 iç içe bölümleri aynı biçimde okunur."""
    if isinstance(data, dict):
        if isinstance(data.get("id"), str):
            yield data
        for value in data.values():
            yield from records(value)
    elif isinstance(data, list):
        for value in data:
            yield from records(value)


def matched(matcher, root=ROOT):
    """Eşleşen kayıt kimliklerini döndürür; Markdown kanıtında eşleşme dosya yolunun kendisidir."""
    path = root / matcher["file"]
    if "contains" in matcher:
        return [matcher["file"]] if matcher["contains"] in path.read_text(encoding="utf-8") else []
    data = json.loads(path.read_text(encoding="utf-8"))
    if "ids" in matcher:
        present = {record["id"] for record in records(data)}
        return [rid for rid in matcher["ids"] if rid in present]
    pattern = re.compile(matcher["pattern"])
    hits = []
    for record in records(data):
        for field in matcher["fields"]:
            value = record.get(field)
            values = value if isinstance(value, list) else [value]
            if any(isinstance(v, str) and pattern.search(v) for v in values):
                hits.append(record["id"])
                break
    return hits


def affected(conflict, root=ROOT):
    return sorted({rid for matcher in conflict["older"] for rid in matched(matcher, root)})


def domain_of(path, register):
    for domain in register["domains"]:
        for role in ("winner", "alongside", "superseded"):
            entries = domain[role] if isinstance(domain[role], list) else [domain[role]]
            if path in entries:
                return domain, role
    return None, None


def id_collisions(root=ROOT):
    where = defaultdict(set)
    for path in sorted((root / "data").rglob("*.json")):
        if path == root / REGISTER:
            continue
        for record in records(json.loads(path.read_text(encoding="utf-8"))):
            where[record["id"]].add(path.relative_to(root).as_posix())
    return {rid: sorted(files) for rid, files in where.items() if len(files) > 1}


ROLE_TEXT = {"winner": "geçerli", "alongside": "birlikte kullanılır; çakışmada geçerli dosya", "superseded": "yerini aldı"}


def describe_file(path, register, root=ROOT):
    domain, role = domain_of(path, register)
    lines = []
    if domain is None:
        lines.append(f"{path}: öncelik kaydında yok.")
    elif role == "winner":
        lines.append(f"{path}: '{domain['domain']}' alanında geçerli director.")
    else:
        lines.append(f"{path}: '{domain['domain']}' alanında {ROLE_TEXT[role]} → {domain['winner']}")
    for conflict in register["conflicts"]:
        sides = [side for side in ("older", "newer") if any(m["file"] == path for m in conflict[side])]
        if sides:
            lines.append(f"  {conflict['id']} ({'eski' if 'older' in sides else 'yeni'} taraf): {conflict['topic']}")
    return lines


def describe_record(record_id, register, root=ROOT):
    lines = []
    for conflict in register["conflicts"]:
        if conflict["status"] == "open" and record_id in affected(conflict, root):
            lines.append(f"{conflict['id']} · {conflict['topic']}")
            lines.append(f"  Çözüm: {conflict['resolution']}")
    return lines or [f"{record_id}: bilinen bir çakışmada yok."]


def summary(register, root=ROOT):
    lines = ["Öncelik sırası:"]
    lines += [f"  {item['level']}. {item['label']}" for item in register["order"]]
    lines.append("Açık çakışmalar:")
    for conflict in register["conflicts"]:
        if conflict["status"] == "open":
            lines.append(f"  {conflict['id']} · {conflict['topic']} ({len(affected(conflict, root))} kayıt)")
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description="Hangi kuralın geçerli olduğunu ve bilinen çakışmaları gösterir.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--domain", help="Alan adı, örn. motion, typography, scroll")
    group.add_argument("--file", help="Depo köküne göre dosya yolu")
    group.add_argument("--id", help="Katalog kayıt kimliği, örn. font-029")
    group.add_argument("--conflict", help="Çakışma kimliği, örn. CF-004")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    register = load()

    if args.domain:
        domain = next((d for d in register["domains"] if d["domain"] == args.domain), None)
        if domain is None:
            parser.error("Bilinmeyen alan: " + args.domain + ". Alanlar: " + ", ".join(d["domain"] for d in register["domains"]))
        payload = domain
        lines = [f"{domain['domain']}: geçerli {domain['winner']}"]
        lines += [f"  birlikte: {path}" for path in domain["alongside"]]
        lines += [f"  yerini aldı: {path}" for path in domain["superseded"]]
    elif args.file:
        path = Path(args.file).as_posix().removeprefix("./")
        payload = {"file": path, "lines": describe_file(path, register)}
        lines = payload["lines"]
    elif args.id:
        payload = {"id": args.id, "lines": describe_record(args.id, register)}
        lines = payload["lines"]
    elif args.conflict:
        conflict = next((c for c in register["conflicts"] if c["id"] == args.conflict), None)
        if conflict is None:
            parser.error("Bilinmeyen çakışma: " + args.conflict)
        payload = {**conflict, "affected": affected(conflict)}
        lines = [f"{conflict['id']} · {conflict['topic']} [{conflict['status']}]", f"Çözüm: {conflict['resolution']}",
                 "Etkilenen kayıtlar: " + (", ".join(payload["affected"]) or "yok")]
    else:
        payload = {"order": register["order"], "conflicts": [c["id"] for c in register["conflicts"] if c["status"] == "open"]}
        lines = summary(register)

    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else "\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
