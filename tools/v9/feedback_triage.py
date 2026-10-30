#!/usr/bin/env python3
"""Belirsiz revizyon geri bildirimini konum, yön ve sorulacak tek soruya çevirir."""

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/v9"
FOLD = str.maketrans("çğıöşüâîû", "cgiosuaiu")
CLAUSE_BREAK = re.compile(r"[,.;:!?\n]+")
MAX_QUESTIONS = 3
GLOBAL_OPTION = "Genel olarak (en çok görünen yerlerden başlarım)"
# "arka plan rengi", "başlık rengi": renk sözcüğü önündeki yüzeyin niteliğidir, ayrı hedef değildir.
MODIFIER_SURFACES = {"palette"}


def tr_lower(text):
    # str.lower() "İ" harfini "i̇" yapar ve "I" harfini "ı" yerine "i" yapar.
    return text.replace("I", "ı").replace("İ", "i").lower()


def fold(text):
    return tr_lower(text).translate(FOLD)


def words(text):
    return re.findall(r"[a-z0-9]+", fold(text))


def pattern(phrase):
    return tuple(words(phrase.rstrip("*"))), phrase.endswith("*")


def load_data(root=ROOT):
    lexicon = json.loads((root / "data/v9/feedback_lexicon.json").read_text(encoding="utf-8"))
    surfaces = json.loads((root / "data/v9/visibility_ranking.json").read_text(encoding="utf-8"))["surfaces"]
    return lexicon, sorted(surfaces, key=lambda surface: surface["rank"])


def build_patterns(lexicon, surfaces):
    patterns = []
    for surface in surfaces:
        patterns += [(*pattern(p), "surface", surface["id"]) for p in surface["phrases"]]
    for entry in lexicon["entries"]:
        patterns += [(*pattern(p), "entry", entry["id"]) for p in entry["phrases"]]
    for kind in ("global", "positive"):
        patterns += [(*pattern(p), kind, p) for p in lexicon["markers"][kind]]
    return sorted(patterns, key=lambda item: -len(item[0]))


def matches(tokens, start, sequence, prefix):
    if start + len(sequence) > len(tokens):
        return False
    for offset, expected in enumerate(sequence):
        token = tokens[start + offset]
        last = offset == len(sequence) - 1
        if token != expected and not (prefix and last and token.startswith(expected)):
            return False
    return True


def scan(tokens, patterns):
    """Soldan sağa en uzun eşleşme: "her yerde var" bir kez okunur, "her yer" ayrıca sayılmaz."""
    hits, index = [], 0
    while index < len(tokens):
        for sequence, prefix, category, ref in patterns:
            if matches(tokens, index, sequence, prefix):
                hits.append({"start": index, "end": index + len(sequence), "category": category, "ref": ref})
                index += len(sequence)
                break
        else:
            index += 1
    return hits


def clauses(text, contrast):
    for part in CLAUSE_BREAK.split(fold(text)):
        current = []
        for token in words(part):
            if token in contrast:
                if current:
                    yield current
                current = []
            else:
                current.append(token)
        if current:
            yield current


def negated(hit, hits, tokens, markers, kinds):
    after = tokens[hit["end"]] if hit["end"] < len(tokens) else None
    before = tokens[hit["start"] - 1] if hit["start"] else None
    following = next((h for h in hits if h["start"] == hit["end"]), None)
    return (after in markers["negateAfter"] or before in markers["negateBefore"]
            or (following is not None and following["category"] == "entry" and kinds[following["ref"]] != "revert"))


def analyse(text, answer=None, lexicon=None, surfaces=None, top=3):
    if lexicon is None or surfaces is None:
        lexicon, surfaces = load_data()
    markers = {key: {" ".join(words(value)) for value in values} for key, values in lexicon["markers"].items()}
    entries = {entry["id"]: entry for entry in lexicon["entries"]}
    kinds = {key: entry["kind"] for key, entry in entries.items()}
    by_id = {surface["id"]: surface for surface in surfaces}
    patterns = build_patterns(lexicon, surfaces)

    focus, preserve, matched, is_global, approved = [], [], [], False, False
    full = text if not answer else f"{text}.\n{answer}"
    for tokens in clauses(full, markers["contrast"]):
        hits = scan(tokens, patterns)
        found_entries = [h["ref"] for h in hits if h["category"] == "entry"]
        found_surfaces = [h["ref"] for h, prev in zip(hits, [None, *hits]) if h["category"] == "surface"
                          and not (h["ref"] in MODIFIER_SURFACES and prev and prev["category"] == "surface"
                                   and prev["end"] == h["start"])]
        liked = [h for h in hits if h["category"] == "positive" and not negated(h, hits, tokens, markers, kinds)]
        matched += [ref for ref in found_entries if ref not in matched]
        if liked and not found_entries:
            preserve += [ref for ref in found_surfaces if ref not in preserve]
            approved = True
            continue
        focus += [ref for ref in found_surfaces if ref not in focus]
        is_global = is_global or any(h["category"] == "global" for h in hits)

    focus = [ref for ref in focus if ref not in preserve]
    directions = [entries[ref] for ref in matched if kinds[ref] == "direction"]
    ranked = [s["id"] for s in surfaces if s["id"] not in preserve]
    leaning = [s for s in ranked if any(s in d["likelySurfaces"] for d in directions)]

    if any(kinds[ref] == "revert" for ref in matched):
        mode = "revert"
    elif focus:
        mode = "located"
    elif is_global:
        mode = "global"
    elif directions:
        mode = "direction"
    elif any(kinds[ref] == "vague" for ref in matched):
        mode = "ask-location"
    elif approved:
        mode = "approved"
    else:
        mode = "unclear"

    if mode == "located":
        targets = sorted(focus, key=lambda ref: by_id[ref]["rank"])
    elif mode == "global":
        targets = (leaning or ranked)[:top]
    elif mode == "direction":
        targets = leaning[:top]
    else:
        targets = []

    result = {
        "mode": mode,
        "targets": [surface_summary(by_id[ref]) for ref in targets],
        "preserve": [{"id": ref, "label": by_id[ref]["label"]} for ref in preserve],
        "matched": [{"id": ref, "kind": kinds[ref], "label": entries[ref]["label"]} for ref in matched],
        "directions": [direction_summary(d) for d in directions],
        "questions": questions(mode, ranked, leaning, preserve, by_id),
        "plan": plan(mode, targets, preserve, by_id),
    }
    assert len(result["questions"]) <= MAX_QUESTIONS
    return result


def surface_summary(surface):
    return {key: surface[key] for key in ("id", "rank", "label", "why", "changes", "cssHints", "references")}


def direction_summary(entry):
    return {key: entry[key] for key in ("id", "label", "causes", "firstMoves", "avoid", "references")}


def option_labels(refs, by_id, limit):
    return [by_id[ref]["label"] for ref in refs[:limit]] + [GLOBAL_OPTION]


def questions(mode, ranked, leaning, preserve, by_id):
    keep = [] if preserve else [{"text": "Beğendiğin ve aynen kalmasını istediğin bir yer var mı?", "options": []}]
    if mode == "ask-location":
        return [{"text": "Neresi içine sinmedi?", "options": option_labels(ranked, by_id, 4)}] + keep
    if mode == "direction":
        return [{"text": "Bu his en çok nerede?", "options": option_labels(leaning or ranked, by_id, 3)}] + keep
    if mode == "unclear":
        return [{"text": "Neyi değiştirmemi istersin?", "options": option_labels(ranked, by_id, 4)}]
    if mode == "revert":
        return [{"text": "Hangi değişikliği geri alayım?",
                 "options": ["Son değişikliğin tamamını", "Yalnız belirttiğin yeri", "Bir önceki onaylı hali"]}]
    return []


def plan(mode, targets, preserve, by_id):
    labels = ", ".join(tr_lower(by_id[ref]["label"]) for ref in targets)
    kept = ", ".join(tr_lower(by_id[ref]["label"]) for ref in preserve)
    steps = {
        "ask-location": ["Henüz hiçbir şeyi değiştirme; tek soruyu seçeneklerle sor.",
                         "Cevap 'genel' olursa en çok görünen yüzeylerden başla."],
        "unclear": ["İsteği tahmin ederek değiştirme; kısa bir soru sor."],
        "approved": ["Değişiklik isteği yok; mevcut hali koru ve beğenilen kararları revizyon notuna yaz."],
        "direction": ["Konumu sorarken olası nedenleri incelemeye başla.",
                      "Cevap gelmezse veya 'genel' ise listelenen yüzeylerden başla."],
        "revert": ["Revizyon notundaki son değişiklikleri listele; yeni yön üretme.",
                   "Geri alınacak kısmı netleştirip yalnız onu geri al."],
        "located": [f"Yalnız şu yüzeylere dokun: {labels}.",
                    "Soru yerine 2-3 alternatifi yan yana göster; geri kalan kararları koru."],
        "global": [f"En çok görünen yüzeylerden başla: {labels}.",
                   "Bu yüzeyleri birlikte değiştiren 2-3 yön hazırla ve ilk ekranda göster; mikro detaylara dokunma."],
    }[mode]
    if kept:
        steps.append(f"Kullanıcının beğendiği yerleri koru: {kept}.")
    steps.append("Değişen kararları ve dosya yollarını revizyon notuna yaz; kullanıcıya hangi dosyaların değiştiğini söyle.")
    return steps


def render_text(result):
    lines = [f"Mod: {result['mode']}"]
    if result["matched"]:
        lines.append("Algılanan: " + ", ".join(f"{m['label']} ({m['id']})" for m in result["matched"]))
    if result["preserve"]:
        lines.append("Korunacak: " + ", ".join(p["label"] for p in result["preserve"]))
    for question in result["questions"]:
        lines.append(f"Soru: {question['text']}")
        lines += [f"  - {option}" for option in question["options"]]
    for target in result["targets"]:
        lines.append(f"Yüzey {target['rank']}: {target['label']} — {target['why']}")
        lines.append("  Değiştirilebilecekler: " + "; ".join(target["changes"]))
        lines.append("  Nerede: " + "; ".join(target["cssHints"]))
    for direction in result["directions"]:
        lines.append(f"Yön: {direction['label']}")
        lines.append("  İlk hamle: " + "; ".join(direction["firstMoves"]))
        lines.append("  Kaçın: " + "; ".join(direction["avoid"]))
    lines += [f"Adım: {step}" for step in result["plan"]]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Revizyon geri bildirimini yorumlar; konum yoksa sorulacak soruyu üretir.")
    parser.add_argument("feedback", nargs="+", help="Kullanıcının yazdığı geri bildirim")
    parser.add_argument("--answer", help="Kullanıcının 'neresi?' sorusuna cevabı")
    parser.add_argument("--top", type=int, default=3, help="Genel geri bildirimde ele alınacak yüzey sayısı")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    result = analyse(" ".join(args.feedback), args.answer, top=max(1, args.top))
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else render_text(result))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
