#!/usr/bin/env python3
"""İndirilen referans siteden tasarım ölçüleri, yapı, kütüphane, erişilebilirlik ve düzenleme haritası çıkarır."""

import argparse
import colorsys
import json
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAX_FILES = 400
MAX_BYTES = 3_000_000
NAMED = {"white": "#ffffff", "black": "#000000"}
COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)|\b(?:white|black)\b")
LENGTH = re.compile(r"(-?\d*\.?\d+)(px|rem|em)\b")
BEZIER = re.compile(r"cubic-bezier\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)")
DURATION = re.compile(r"(?<![\w.-])(\d*\.?\d+)(ms|s)\b")
MEDIA = re.compile(r"\((?:min|max)-width\s*:\s*(\d*\.?\d+)(px|em|rem)\)")
LIBRARIES = {
    "gsap": r"gsap(\.min)?\.js|GreenSock|gsap\.registerPlugin", "scrolltrigger": r"ScrollTrigger",
    "three": r"three(\.module|\.core)?(\.min)?\.m?js|THREE\.REVISION|WebGLRenderer", "lenis": r"lenis",
    "locomotive-scroll": r"locomotive-scroll", "swiper": r"swiper", "splide": r"splide",
    "framer-motion": r"framer-motion", "react": r"react-dom|__REACT_DEVTOOLS|reactroot", "next": r"/_next/|__NEXT_DATA__",
    "nuxt": r"/_nuxt/|__NUXT__", "vue": r"vue(\.runtime)?(\.global)?(\.min)?\.js|data-v-[0-9a-f]{6}", "svelte": r"svelte-[a-z0-9]{6}",
    "alpine": r"alpinejs|x-data=", "jquery": r"jquery(\.min)?\.js|jQuery v\d", "bootstrap": r"bootstrap(\.bundle)?(\.min)?\.(css|js)",
    "tailwind": r"tailwindcss|--tw-", "webflow": r"webflow\.js|data-wf-page", "wordpress": r"wp-content|wp-includes",
    "shopify": r"cdn\.shopify\.com", "lottie": r"lottie", "rive": r"@rive-app|rive\.wasm", "barba": r"barba(\.min)?\.js|data-barba",
    "particles": r"particles(\.min)?\.js|tsparticles", "anime": r"anime(\.min)?\.js", "aos": r"aos(\.min)?\.(js|css)|data-aos=",
}
SURFACE_RULES = {
    "background": (r"^(html|body|:root|main)$|section|wrapper|page", r"^background(-color|-image)?$"),
    "hero": (r"hero|banner|masthead|intro|jumbotron|splash", r"."),
    "palette": (r"^:root$|^html$", r"^--.*(color|colour|accent|brand|primary|secondary|bg|fg|ink|paper)"),
    "display-type": (r"(^|[\s,>])h[12]\b|title|headline|display|heading", r"^(font(-family|-size|-weight)?|letter-spacing|line-height)$"),
    "imagery": (r"\b(img|picture|video|canvas|figure)\b|image|media|photo", r"."),
    "spacing": (r"section|container|wrapper|^body$|grid|stack", r"^(padding|margin|gap|row-gap|column-gap|max-width)(-|$)"),
    "surfaces": (r"card|btn|button|tile|panel|box", r"^(border(-radius)?|box-shadow|background(-color)?)$"),
    "navigation": (r"\b(nav|header|footer|menu)\b|navbar|topbar", r"."),
    "body-type": (r"^(body|p|article|li)$|\bp\b|text|copy|prose", r"^(font(-family|-size)?|line-height|max-width|color)$"),
    "motion": (r".", r"^(transition|animation)(-|$)"),
    "details": (r"icon|svg|badge|tag|chip", r"."),
}


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


# --- CSS -----------------------------------------------------------------

def parse_css(text, source="inline", line_offset=0):
    """Basit ama satır numaralı CSS okuyucu: @media iç içeliğini izler, yorumları atlar."""
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    declarations, stack, buffer, line = [], [], "", 1 + line_offset
    buffer_line = line
    for char in text:
        if char == "\n":
            line += 1
        if char == "{":
            stack.append((" ".join(buffer.split()), buffer_line))
            buffer, buffer_line = "", line
        elif char == "}":
            if buffer.strip() and stack:
                declarations += split_declarations(buffer, stack, source, buffer_line)
            if stack:
                stack.pop()
            buffer, buffer_line = "", line
        elif char == ";" and stack and not stack[-1][0].startswith("@"):
            declarations += split_declarations(buffer, stack, source, buffer_line)
            buffer, buffer_line = "", line
        else:
            if not buffer.strip():
                buffer_line = line
            buffer += char
    return declarations


def split_declarations(chunk, stack, source, line):
    if ":" not in chunk:
        return []
    prop, value = chunk.split(":", 1)
    prop = prop.strip().lower()
    if not re.fullmatch(r"-{0,2}[a-z][a-z0-9-]*", prop):
        return []
    selector = stack[-1][0]
    media = " ".join(s for s, _ in stack[:-1] if s.startswith("@"))
    return [{"selector": selector, "property": prop, "value": " ".join(value.split()).removesuffix("!important").strip(),
             "media": media, "file": source, "line": line}]


def at_rules(text, name):
    return re.findall(rf"@{name}\s+([^{{\s]+)", text)


def hex_color(value):
    value = value.strip().lower()
    if value in NAMED:
        return NAMED[value]
    if value.startswith("#"):
        digits = value[1:]
        if len(digits) in (3, 4):
            digits = "".join(c * 2 for c in digits[:3])
        return "#" + digits[:6] if len(digits) >= 6 else None
    numbers = [float(n) for n in re.findall(r"-?\d*\.?\d+", value)]
    percent = "%" in value
    if value.startswith("rgb") and len(numbers) >= 3:
        rgb = numbers[:3]
        if percent and value.split("(")[1].split(",")[0].strip().endswith("%"):
            rgb = [n * 2.55 for n in rgb]
        return "#" + "".join(f"{max(0, min(255, round(n))):02x}" for n in rgb)
    if value.startswith("hsl") and len(numbers) >= 3:
        r, g, b = colorsys.hls_to_rgb((numbers[0] % 360) / 360, numbers[2] / 100, numbers[1] / 100)
        return "#" + "".join(f"{round(c * 255):02x}" for c in (r, g, b))
    return None


def colors_in(value, variables):
    found = [hex_color(m.group(0)) for m in COLOR.finditer(value)]
    for name in re.findall(r"var\(\s*(--[\w-]+)", value):
        found += variables.get(name, [])
    return [c for c in found if c]


GENERIC_FAMILIES = {"sans-serif", "serif", "monospace", "system-ui", "ui-sans-serif", "ui-serif", "ui-monospace",
                    "inherit", "initial", "unset", "revert", "cursive", "fantasy", "-apple-system", "blinkmacsystemfont",
                    "emoji", "math", "fangsong"}
FONT_STYLE_WORDS = {"normal", "italic", "oblique", "bold", "bolder", "lighter", "small-caps", "condensed", "expanded",
                    *(str(w) for w in range(100, 1000, 100))}
SIZE_TOKEN = re.compile(r"^[\d.]+(px|rem|em|ex|ch|%|pt|pc|vw|vh|vmin|vmax)?$")


def first_family(value):
    """font-family veya font kısayolundan ilk gerçek aile adını alır; boyut, ağırlık, var() ve genel aileler atlanır."""
    for part in value.split(","):
        kept = []
        for word in part.replace("/", " ").split():
            token = word.strip("\"'")
            if SIZE_TOKEN.match(token) or token.lower() in FONT_STYLE_WORDS:
                continue
            kept.append(token)
        name = " ".join(kept).strip()
        if not name or name.startswith("var(") or name.lower() in GENERIC_FAMILIES:
            continue
        return name
    return None


def families_in(value, font_vars):
    """font-family değerindeki aileleri, var(--font-*) değişkenlerini çözerek döndürür."""
    names = []
    for name in re.findall(r"var\(\s*(--[\w-]+)", value):
        names += font_vars.get(name, [])
    direct = first_family(re.sub(r"var\([^)]*\)", "", value))
    if direct:
        names.append(direct)
    return names


def luminance(hex_value):
    channels = [int(hex_value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a, b):
    light, dark = sorted((luminance(a), luminance(b)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def chroma(hex_value):
    channels = [int(hex_value[i:i + 2], 16) for i in (1, 3, 5)]
    return max(channels) - min(channels)


def to_px(number, unit):
    return float(number) * (16 if unit in {"rem", "em"} else 1)


def seconds(number, unit):
    return float(number) / (1000 if unit == "ms" else 1)


# --- HTML ----------------------------------------------------------------

class PageProbe(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.title = ""
        self.meta = {}
        self.headings = []
        self.images = []
        self.links = []
        self.buttons = []
        self.inputs = []
        self.labels = set()
        self.scripts = []
        self.stylesheets = []
        self.styles = []
        self.inline_styles = []
        self.counts = Counter()
        self.classes = Counter()
        self.attributes = set()
        self._open = []
        self._style_line = None

    def handle_starttag(self, tag, attrs):
        attrs = {k: (v or "") for k, v in attrs}
        self.counts[tag] += 1
        self.attributes |= {k for k in attrs if k.startswith(("data-", "x-"))}
        self.classes.update(attrs.get("class", "").split())
        if attrs.get("style"):
            self.inline_styles.append((attrs["style"], self.getpos()[0]))
        if tag == "html":
            self.lang = attrs.get("lang") or None
        elif tag == "meta" and (attrs.get("name") or attrs.get("property")):
            self.meta[(attrs.get("name") or attrs.get("property")).lower()] = attrs.get("content", "")
        elif tag == "img":
            self.images.append({"src": attrs.get("src", ""), "alt": attrs.get("alt"), "line": self.getpos()[0]})
        elif tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])
        elif tag == "link" and "stylesheet" in attrs.get("rel", "").lower():
            self.stylesheets.append(attrs.get("href", ""))
        elif tag == "label" and attrs.get("for"):
            self.labels.add(attrs["for"])
        elif tag in {"input", "select", "textarea"} and attrs.get("type") not in {"hidden", "submit", "button"}:
            self.inputs.append({"id": attrs.get("id"), "label": attrs.get("aria-label") or attrs.get("aria-labelledby"),
                                "line": self.getpos()[0]})
        elif tag == "style":
            self._style_line = self.getpos()[0]
        if tag in {"a", "button", "title"} or re.fullmatch(r"h[1-6]", tag):
            self._open.append({"tag": tag, "attrs": attrs, "text": [], "line": self.getpos()[0]})

    def handle_endtag(self, tag):
        if self._open and self._open[-1]["tag"] == tag:
            node = self._open.pop()
            text = " ".join(" ".join(node["text"]).split())
            label = text or node["attrs"].get("aria-label") or node["attrs"].get("title") or ""
            if tag == "title":
                self.title = text
            elif tag == "a":
                self.links.append({"label": label, "href": node["attrs"].get("href", ""), "line": node["line"]})
            elif tag == "button":
                self.buttons.append({"label": label, "line": node["line"]})
            else:
                self.headings.append({"level": int(tag[1]), "text": text[:90], "line": node["line"]})
            if self._open:
                self._open[-1]["text"].append(text)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if self._style_line is not None:
            self.styles.append((data, self._style_line))
            self._style_line = None
        elif self._open:
            self._open[-1]["text"].append(data)


def accessibility(page, relative):
    issues = []
    def add(code, message, line=None):
        issues.append({"code": code, "page": relative, "line": line, "message": message})
    if not page.lang:
        add("missing-lang", "html etiketinde lang yok; ekran okuyucu dili tahmin eder.")
    if not page.title:
        add("missing-title", "Sayfa başlığı (title) yok.")
    viewport = page.meta.get("viewport", "")
    if not viewport:
        add("missing-viewport", "viewport meta etiketi yok; mobilde küçük görünür.")
    elif re.search(r"user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b", viewport):
        add("zoom-blocked", "Yakınlaştırma kapatılmış (user-scalable/maximum-scale).")
    for image in page.images:
        if image["alt"] is None:
            add("img-alt", f"Görselde alt metni yok: {image['src'][:60]}", image["line"])
    levels = [h["level"] for h in page.headings]
    if levels.count(1) == 0 and levels:
        add("no-h1", "Sayfada h1 yok.")
    if levels.count(1) > 1:
        add("multiple-h1", f"{levels.count(1)} adet h1 var.")
    for previous, current in zip(levels, levels[1:]):
        if current > previous + 1:
            add("heading-skip", f"Başlık seviyesi h{previous} → h{current} atlıyor.")
            break
    for link in page.links:
        if not link["label"]:
            add("empty-link", f"Metni olmayan bağlantı: {link['href'][:60]}", link["line"])
    for button in page.buttons:
        if not button["label"]:
            add("empty-button", "Metni veya aria-label'ı olmayan buton.", button["line"])
    for field in page.inputs:
        if not field["label"] and field["id"] not in page.labels:
            add("input-label", "Etiketi olmayan form alanı.", field["line"])
    return issues


# --- analysis ------------------------------------------------------------

def collect_files(target):
    target = Path(target)
    site = target / "site" if (target / "site").is_dir() else target
    if site.is_file():
        return site.parent, [site]
    files = sorted(p for p in site.rglob("*") if p.is_file() and p.suffix.lower() in {".html", ".htm", ".css", ".js", ".mjs"})
    return site, files[:MAX_FILES]


def analyse(target):
    site, files = collect_files(target)
    declarations, pages, issues, scripts_text = [], [], [], []
    keyframes, font_faces, media_values = [], [], []
    for path in files:
        if path.stat().st_size > MAX_BYTES:
            continue
        relative = path.relative_to(site).as_posix()
        text = read_text(path)
        suffix = path.suffix.lower()
        if suffix == ".css":
            declarations += parse_css(text, relative)
            keyframes += at_rules(text, "keyframes")
            media_values += MEDIA.findall(text)
        elif suffix in {".js", ".mjs"}:
            scripts_text.append(text[:200_000])
        else:
            probe = PageProbe()
            probe.feed(text)
            for css, line in probe.styles:
                declarations += parse_css(css, relative, line - 1)
                keyframes += at_rules(css, "keyframes")
                media_values += MEDIA.findall(css)
            for style, line in probe.inline_styles:
                declarations += split_declarations_inline(style, relative, line)
            pages.append((relative, probe, text))
            issues += accessibility(probe, relative)
    font_faces = [d for d in declarations if d["selector"].startswith("@font-face") and d["property"] == "font-family"]

    variables = defaultdict(list)
    font_vars = defaultdict(list)
    for d in declarations:
        if d["property"].startswith("--"):
            variables[d["property"]] += [c for c in (hex_color(m.group(0)) for m in COLOR.finditer(d["value"])) if c]
            family = first_family(d["value"])
            if family and not COLOR.search(d["value"]):
                font_vars[d["property"]].append(family)

    roles = {"background": Counter(), "text": Counter(), "border": Counter(), "other": Counter()}
    for d in declarations:
        if d["property"].startswith("--"):
            continue
        role = ("background" if d["property"].startswith("background") else "text" if d["property"] == "color"
                else "border" if d["property"].startswith(("border", "outline")) else "other")
        roles[role].update(colors_in(d["value"], variables))
    palette = Counter()
    for counter in roles.values():
        palette.update(counter)

    families = Counter()
    for d in declarations:
        if d["property"] in {"font-family", "font"} and not d["selector"].startswith("@font-face"):
            for family in families_in(d["value"], font_vars):
                families[family] += 1
    google = [re.findall(r"family=([^&:\"']+)", src) for _, probe, _ in pages for src in probe.stylesheets]
    google_families = sorted({name.replace("+", " ") for group in google for name in group})

    sizes, spacing, radii, durations, easings = Counter(), Counter(), Counter(), Counter(), Counter()
    shadows = transition_all = 0
    for d in declarations:
        prop, value = d["property"], d["value"]
        if prop == "font-size":
            sizes.update(round(to_px(n, u)) for n, u in LENGTH.findall(value))
            if "clamp(" in value:
                sizes[value] += 1
        elif re.match(r"(padding|margin|gap|row-gap|column-gap)(-|$)", prop):
            spacing.update(round(to_px(n, u)) for n, u in LENGTH.findall(value) if float(n) > 0)
        elif prop.endswith("radius"):
            radii[value] += 1
        elif prop in {"box-shadow", "text-shadow"} and value != "none":
            shadows += 1
        if prop.startswith(("transition", "animation")):
            durations.update(round(seconds(n, u), 3) for n, u in DURATION.findall(value))
            easings.update(re.findall(r"cubic-bezier\([^)]*\)|\b(?:ease-in-out|ease-in|ease-out|ease|linear|steps\([^)]*\))", value))
            if re.search(r"(^|[\s,])all\b", value) and prop in {"transition", "transition-property"}:
                transition_all += 1

    live = load_live(Path(target))
    live_scripts = [url for view in (live or {}).get("viewports", {}).values() for url in view["network"]["scripts"]]
    blob = "\n".join([*scripts_text, *(text for _, _, text in pages), *(s for _, p, _ in pages for s in p.scripts), *live_scripts])
    libraries = sorted(name for name, pattern in LIBRARIES.items() if re.search(pattern, blob, re.I))
    tailwind_like = sum(c for name, c in Counter(cls for _, p, _ in pages for cls in p.classes.elements()).items()
                        if re.match(r"(sm|md|lg|xl):|^(px|py|mx|my|pt|pb|gap|text|bg)-\d", name))
    if tailwind_like > 20 and "tailwind" not in libraries:
        libraries.append("tailwind")

    background = root_color(declarations, variables, roles["background"], {"background", "background-color"})
    text_color = root_color(declarations, variables, roles["text"], {"color"})
    accent = next((c for c, _ in palette.most_common() if chroma(c) >= 60), None)
    contrast_issues = static_contrast(declarations, variables)
    issues += contrast_issues

    tokens = {
        "palette": [{"color": c, "count": n} for c, n in palette.most_common(12)],
        "roles": {"background": background, "text": text_color, "accent": accent},
        "customProperties": {name: values[0] for name, values in variables.items() if values},
        "fonts": [{"family": f, "count": n} for f, n in families.most_common(6)],
        "fontFaces": sorted({d["value"].strip("\"' ") for d in font_faces}),
        "googleFonts": google_families,
        "typeScale": sorted(s for s in sizes if isinstance(s, int))[:16],
        "fluidSizes": sorted(s for s in sizes if isinstance(s, str))[:6],
        "spacingScale": [v for v, _ in spacing.most_common(10)],
        "radii": [{"value": v, "count": n} for v, n in radii.most_common(6)],
        "durations": [{"seconds": v, "count": n} for v, n in durations.most_common(6)],
        "easings": [{"value": v, "count": n} for v, n in easings.most_common(6)],
        "breakpoints": sorted({round(to_px(n, u)) for n, u in media_values}),
    }
    structure = [{
        "page": relative, "title": probe.title, "lang": probe.lang, "description": probe.meta.get("description", ""),
        "outline": probe.headings[:12], "sections": probe.counts["section"], "nav": probe.counts["nav"],
        "images": len(probe.images), "videos": probe.counts["video"], "canvas": probe.counts["canvas"], "iframes": probe.counts["iframe"],
    } for relative, probe, _ in pages[:20]]
    return {
        "version": "10.0",
        "site": str(site),
        "capture": load_capture(Path(target)),
        "live": live_summary(live),
        "counts": {"pages": len(pages), "cssDeclarations": len(declarations), "keyframes": len(set(keyframes)),
                   "shadows": shadows, "transitionAll": transition_all},
        "tokens": tokens,
        "libraries": libraries,
        "structure": structure,
        "accessibility": issues,
        "weight": weight(site),
        "surfaceMap": surface_map(declarations),
        "ruleNotes": rule_notes(tokens, libraries, declarations, transition_all, background),
    }


def split_declarations_inline(style, source, line):
    return [d for chunk in style.split(";") for d in split_declarations(chunk, [("[style]", line)], source, line)]


def root_color(declarations, variables, counter, properties):
    """Sayfanın kök rengi body/html tanımından gelir; yoksa en sık kullanılan değer seçilir."""
    for d in declarations:
        if d["property"] in properties and re.fullmatch(r"(html|body|:root)", d["selector"].strip()):
            found = colors_in(d["value"], variables)
            if found:
                return found[0]
    return (counter.most_common(1) or [(None, 0)])[0][0]


def static_contrast(declarations, variables):
    by_rule = defaultdict(dict)
    for d in declarations:
        key = (d["file"], d["selector"], d["media"])
        if d["property"] == "color":
            by_rule[key]["fg"] = (colors_in(d["value"], variables) or [None])[0], d["line"]
        elif d["property"] in {"background", "background-color"}:
            by_rule[key]["bg"] = (colors_in(d["value"], variables) or [None])[0], d["line"]
    issues = []
    for (file, selector, _), pair in by_rule.items():
        if "fg" in pair and "bg" in pair and pair["fg"][0] and pair["bg"][0]:
            ratio = contrast(pair["fg"][0], pair["bg"][0])
            if ratio < 4.5:
                issues.append({"code": "low-contrast", "page": file, "line": pair["fg"][1],
                               "message": f"{selector}: {pair['fg'][0]} / {pair['bg'][0]} kontrastı {ratio:.2f}:1 (metin için en az 4.5:1)."})
    return issues


def surface_map(declarations, per_surface=8):
    mapped = {}
    for surface, (selector_pattern, property_pattern) in SURFACE_RULES.items():
        hits = [d for d in declarations
                if re.search(selector_pattern, d["selector"], re.I) and re.search(property_pattern, d["property"], re.I)
                and not d["selector"].startswith("@")]
        mapped[surface] = [{k: d[k] for k in ("file", "line", "selector", "property", "value")} for d in hits[:per_surface]]
    return mapped


def rule_notes(tokens, libraries, declarations, transition_all, background):
    notes = []
    heading_fonts = {f["family"].lower() for f in tokens["fonts"][:2]} | {f.lower() for f in tokens["googleFonts"]}
    if heading_fonts & {"inter", "space grotesk"}:
        notes.append({"conflict": "CF-007", "message": "Inter veya Space Grotesk kullanılıyor; kendi projende varsayılan başlık fontu olarak seçme."})
    body_mono = [d for d in declarations if d["property"] == "font-family" and re.search(r"mono", d["value"], re.I)
                 and re.fullmatch(r"(body|p|html)", d["selector"].strip())]
    if body_mono:
        notes.append({"conflict": "CF-007", "message": "Gövde metninde mono font kullanılıyor; uzun okumada kaçın."})
    if "particles" in libraries:
        notes.append({"conflict": "CF-001", "message": "Parçacık kütüphanesi var; yalnız veri veya sayılan varlık gösteriyorsa kullan."})
    for value in {m.group(0) for d in declarations for m in BEZIER.finditer(d["value"])}:
        _, y1, _, y2 = (float(n) for n in BEZIER.search(value).groups())
        if y1 > 1 or y2 > 1 or y1 < 0 or y2 < 0:
            notes.append({"conflict": "CF-008", "message": f"Aşmalı eğri {value}; ağırlıklı nesne hareketinde varsayılan yapma."})
            break
    if background and luminance(background) < 0.03:
        notes.append({"conflict": "CF-003", "message": f"Koyu zemin ({background}); kendi projende koyu arayüzün içerik gerekçesini yaz."})
    if transition_all:
        notes.append({"conflict": "v7", "message": f"{transition_all} yerde 'transition: all' var; v7 kalibrasyonu özellik bazlı geçiş ister."})
    if "aos" in libraries:
        notes.append({"conflict": "v7", "message": "AOS (scroll'da fade-up) kullanılıyor; her bölümde aynı giriş hareketi v7'de yasak."})
    return notes


def weight(site):
    files = [p for p in site.rglob("*") if p.is_file()]
    largest = sorted(files, key=lambda p: p.stat().st_size, reverse=True)[:5]
    images = [p for p in files if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg"}]
    legacy = [p for p in images if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}]
    fonts = [p for p in files if p.suffix.lower() in {".woff", ".woff2", ".ttf", ".otf"}]
    return {
        "bytes": sum(p.stat().st_size for p in files),
        "largest": [{"file": p.relative_to(site).as_posix(), "bytes": p.stat().st_size} for p in largest],
        "images": len(images), "legacyImageFormats": len(legacy), "fontFiles": len(fonts),
    }


def load_live(target):
    path = target / "live" / "live.json"
    return json.loads(read_text(path)) if path.is_file() else None


def live_summary(live):
    if not live:
        return None
    return {name: {"palette": view["palette"], "fonts": sorted({f["family"] for f in view["fonts"]})[:6],
                   "animations": len(view["animations"]), "contrastFindings": len(view["contrast"]),
                   "axeViolations": [v["id"] for v in view["accessibility"] or []]}
            for name, view in live["viewports"].items()}


def load_capture(target):
    path = target / "capture.json"
    if not path.is_file():
        return None
    capture = json.loads(read_text(path))
    return {key: capture.get(key) for key in ("url", "capturedAt", "usage", "usageNote", "jsShell", "entry")}


def tokens_css(tokens):
    lines = ["/* Referanstan ölçülen başlangıç değerleri. Kendi tasarım kararlarınla değiştir. */", ":root {"]
    for role, value in tokens["roles"].items():
        if value:
            lines.append(f"  --ref-{role}: {value};")
    for index, font in enumerate(tokens["fonts"][:2]):
        lines.append(f"  --ref-font-{'display' if index == 0 else 'body'}: \"{font['family']}\";")
    for index, size in enumerate(tokens["typeScale"][:8]):
        lines.append(f"  --ref-size-{index + 1}: {size}px;")
    for index, space in enumerate(sorted(tokens["spacingScale"])[:8]):
        lines.append(f"  --ref-space-{index + 1}: {space}px;")
    if tokens["radii"]:
        lines.append(f"  --ref-radius: {tokens['radii'][0]['value']};")
    if tokens["durations"]:
        lines.append(f"  --ref-duration: {tokens['durations'][0]['seconds']}s;")
    lines.append("}")
    return "\n".join(lines) + "\n"


def report(result):
    t = result["tokens"]
    capture = result["capture"] or {}
    lines = ["# Referans incelemesi", ""]
    if capture:
        lines += [f"Kaynak: {capture.get('url')} · {capture.get('capturedAt')}", f"Kullanım: **{capture.get('usage')}** — {capture.get('usageNote')}", ""]
    lines += ["## Tasarım ölçüleri", "",
              f"- Zemin / metin / vurgu: {t['roles']['background']} / {t['roles']['text']} / {t['roles']['accent']}",
              "- Palet: " + ", ".join(f"{p['color']} ({p['count']})" for p in t["palette"][:8]),
              "- Fontlar: " + (", ".join(f["family"] for f in t["fonts"]) or "bulunamadı") + (f" · Google Fonts: {', '.join(t['googleFonts'])}" if t["googleFonts"] else ""),
              "- Tip ölçeği (px): " + ", ".join(map(str, t["typeScale"])) + (f" · akışkan: {', '.join(t['fluidSizes'])}" if t["fluidSizes"] else ""),
              "- Boşluk (px): " + ", ".join(map(str, sorted(t["spacingScale"]))),
              "- Köşe: " + ", ".join(r["value"] for r in t["radii"]),
              "- Hareket: " + ", ".join(f"{d['seconds']}s" for d in t["durations"]) + " · " + ", ".join(e["value"] for e in t["easings"]),
              "- Kırılımlar (px): " + ", ".join(map(str, t["breakpoints"])),
              f"- Kütüphaneler: {', '.join(result['libraries']) or 'tespit edilmedi'}", ""]
    for name, view in (result.get("live") or {}).items():
        plan = view["palette"]["plan"]
        lines += [f"## Canlı ölçüm · {name}", "",
                  "- Ekranda kaplanan alan: " + ", ".join(f"{c['hex']} %{round(c['share'] * 100)}" for c in view["palette"]["colors"][:5]),
                  f"- Alan planı: nötr %{round(plan['neutral'] * 100)} · destek %{round(plan['support'] * 100)} · vurgu %{round(plan['accent'] * 100)}",
                  f"- Fontlar: {', '.join(view['fonts'])} · animasyon: {view['animations']} · kontrast bulgusu: {view['contrastFindings']}"
                  + (f" · axe: {', '.join(view['axeViolations'])}" if view["axeViolations"] else ""), ""]
    lines += ["## Sayfalar", ""]
    for page in result["structure"]:
        outline = " › ".join(f"h{h['level']} {h['text']}" for h in page["outline"][:5])
        lines.append(f"- `{page['page']}` — {page['title'] or 'başlıksız'} · {page['sections']} bölüm, {page['images']} görsel · {outline}")
    lines += ["", "## Düzenleme haritası", "", "Kullanıcı bir yüzeyi beğenmezse önce bu satırlara bak:", ""]
    for surface, hits in result["surfaceMap"].items():
        if hits:
            lines.append(f"- **{surface}**: " + "; ".join(f"`{h['file']}:{h['line']}` {h['selector']} {{{h['property']}: {h['value'][:40]}}}" for h in hits[:3]))
    if result["ruleNotes"]:
        lines += ["", "## Kütüphane kurallarıyla çakışanlar", ""]
        lines += [f"- {n['conflict']}: {n['message']}" for n in result["ruleNotes"]]
    a11y = result["accessibility"]
    lines += ["", f"## Erişilebilirlik ({len(a11y)} bulgu)", ""]
    for code, count in Counter(i["code"] for i in a11y).most_common():
        example = next(i for i in a11y if i["code"] == code)
        lines.append(f"- {code} × {count}: {example['message']} (`{example['page']}`)")
    w = result["weight"]
    lines += ["", "## Ağırlık", "", f"- Toplam {w['bytes'] / 1024:.0f} KB · {w['images']} görsel ({w['legacyImageFormats']} eski biçim) · {w['fontFiles']} font dosyası"]
    lines += [f"- {item['file']}: {item['bytes'] / 1024:.0f} KB" for item in w["largest"][:3]]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="İndirilen referans siteyi inceler; ölçüleri, haritayı ve raporu yazar.")
    parser.add_argument("target", help="mirror_reference.py çalışma alanı, site klasörü veya tek HTML dosyası")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--no-write", action="store_true", help="analysis/tokens dosyalarını yazma")
    args = parser.parse_args(argv)
    target = Path(args.target)
    if not target.exists():
        parser.error(f"Bulunamadı: {target}")
    result = analyse(target)
    if result["counts"]["pages"] == 0 and result["counts"]["cssDeclarations"] == 0:
        parser.error("HTML veya CSS bulunamadı.")
    if not args.no_write:
        out = target if target.is_dir() else target.parent
        (out / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        (out / "analysis.md").write_text(report(result), encoding="utf-8")
        (out / "tokens.css").write_text(tokens_css(result["tokens"]), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else report(result))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
