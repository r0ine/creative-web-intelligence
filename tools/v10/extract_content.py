#!/usr/bin/env python3
"""İndirilen sitenin içeriğini (başlık, metin, bağlantı, görsel) sayfa sırasıyla çıkarır; kendi siteni yeni tasarıma taşımak içindir."""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


BLOCK = {"h1", "h2", "h3", "h4", "p", "li", "blockquote", "figcaption", "dt", "dd", "td", "th", "button", "summary"}
SKIP = {"script", "style", "noscript", "template", "svg"}
REGIONS = {"header", "nav", "main", "footer", "aside"}
SOCIAL = {
    "github.com": "GitHub", "gitlab.com": "GitLab", "discord.gg": "Discord", "discord.com": "Discord",
    "twitter.com": "X", "x.com": "X", "instagram.com": "Instagram", "linkedin.com": "LinkedIn",
    "youtube.com": "YouTube", "twitch.tv": "Twitch", "t.me": "Telegram", "builtbybit.com": "BuiltByBit",
    "spigotmc.org": "SpigotMC", "modrinth.com": "Modrinth", "polymart.org": "Polymart", "behance.net": "Behance",
    "dribbble.com": "Dribbble", "codepen.io": "CodePen",
}


class ContentProbe(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks, self.links, self.images = [], [], []
        self.title, self.meta, self.lang = "", {}, None
        self._skip = 0
        self._regions = []
        self._block = None
        self._link = None
        self._in_title = False

    def region(self):
        return self._regions[-1] if self._regions else "body"

    def handle_starttag(self, tag, attrs):
        attrs = {k: (v or "") for k, v in attrs}
        if tag in SKIP:
            self._skip += 1
            return
        if self._skip:
            return
        if tag == "html":
            self.lang = attrs.get("lang") or None
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and (attrs.get("name") or attrs.get("property")):
            self.meta[(attrs.get("name") or attrs.get("property")).lower()] = attrs.get("content", "")
        elif tag in REGIONS:
            self._regions.append(tag)
        elif tag == "img":
            self.images.append({"src": attrs.get("src", ""), "alt": attrs.get("alt", ""), "region": self.region()})
        elif tag == "a":
            self._link = {"href": attrs.get("href", ""), "text": [], "label": attrs.get("aria-label") or attrs.get("title", ""),
                          "region": self.region()}
        if tag in BLOCK:
            self._flush()
            self._block = {"tag": tag, "text": [], "region": self.region()}

    def handle_endtag(self, tag):
        if tag in SKIP:
            self._skip = max(0, self._skip - 1)
            return
        if self._skip:
            return
        if tag == "title":
            self._in_title = False
        elif tag in REGIONS and self._regions and self._regions[-1] == tag:
            self._flush()
            self._regions.pop()
        elif tag == "a" and self._link is not None:
            text = " ".join("".join(self._link["text"]).split()) or self._link["label"]
            self.links.append({"text": text, "href": self._link["href"], "region": self._link["region"]})
            self._link = None
        if tag in BLOCK and self._block and self._block["tag"] == tag:
            self._flush()

    def handle_data(self, data):
        if self._skip:
            return
        if self._in_title:
            self.title += data
        if self._link is not None:
            self._link["text"].append(data)
        if self._block is not None:
            self._block["text"].append(data)

    def _flush(self):
        if self._block:
            text = " ".join("".join(self._block["text"]).split())
            if text:
                self.blocks.append({"tag": self._block["tag"], "text": text, "region": self._block["region"]})
        self._block = None


def classify(href):
    if href.startswith("mailto:"):
        return "email", "E-posta"
    if href.startswith("tel:"):
        return "phone", "Telefon"
    host = (urlparse(href).hostname or "").removeprefix("www.")
    for domain, name in SOCIAL.items():
        if host == domain or host.endswith("." + domain):
            return "social", name
    if host:
        return "external", host
    return "internal", ""


def extract_page(path, site):
    probe = ContentProbe()
    probe.feed(path.read_text(encoding="utf-8", errors="replace"))
    probe._flush()
    links = []
    seen = set()
    for link in probe.links:
        key = (link["href"], link["text"])
        if not link["href"] or link["href"].startswith("#") or key in seen:
            continue
        seen.add(key)
        kind, name = classify(link["href"])
        links.append({**link, "kind": kind, "service": name})
    return {
        "page": path.relative_to(site).as_posix(),
        "title": " ".join(probe.title.split()),
        "lang": probe.lang,
        "description": probe.meta.get("description") or probe.meta.get("og:description", ""),
        "blocks": probe.blocks,
        "links": links,
        "images": probe.images,
    }


def extract(target):
    target = Path(target)
    site = target / "site" if (target / "site").is_dir() else target
    pages = sorted(p for p in site.rglob("*") if p.suffix.lower() in {".html", ".htm"})
    result = {"version": "10.0", "site": str(site), "pages": [extract_page(p, site) for p in pages[:200]]}
    capture = target / "capture.json"
    if capture.is_file():
        data = json.loads(capture.read_text(encoding="utf-8"))
        result["source"] = {"url": data.get("url"), "usage": data.get("usage")}
    contacts = {}
    for page in result["pages"]:
        for link in page["links"]:
            if link["kind"] in {"social", "email", "phone"}:
                contacts.setdefault(link["service"], link["href"])
    result["contacts"] = contacts
    return result


def report(result):
    lines = ["# Site içeriği", ""]
    source = result.get("source")
    if source:
        lines += [f"Kaynak: {source['url']} · kullanım: {source['usage']}", ""]
        if source["usage"] == "study-only":
            lines += ["> Bu içerik başka bir siteye ait; yalnız yapıyı incelemek için kullan, metni kopyalama.", ""]
    if result["contacts"]:
        lines += ["## İletişim ve profiller", ""] + [f"- {name}: {href}" for name, href in result["contacts"].items()] + [""]
    for page in result["pages"]:
        lines += [f"## {page['page']} — {page['title'] or 'başlıksız'}", ""]
        if page["description"]:
            lines += [f"> {page['description']}", ""]
        for block in page["blocks"]:
            tag = block["tag"]
            # Sayfa adı ## olduğu için sayfa içindeki h1 ### olarak yazılır.
            prefix = "#" * (int(tag[1]) + 2) + " " if re.fullmatch(r"h[1-4]", tag) else "- " if tag == "li" else ""
            lines.append(prefix + block["text"])
        external = [l for l in page["links"] if l["kind"] != "internal"]
        if external:
            lines += ["", "Bağlantılar:"] + [f"- [{l['text'] or l['href']}]({l['href']}) · {l['service'] or l['kind']}" for l in external]
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Sitenin metin, başlık, bağlantı ve görsellerini sayfa sırasıyla çıkarır.")
    parser.add_argument("target", help="mirror_reference.py çalışma alanı veya HTML klasörü")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    target = Path(args.target)
    if not target.exists():
        parser.error(f"Bulunamadı: {target}")
    result = extract(target)
    if not result["pages"]:
        parser.error("HTML sayfası bulunamadı.")
    if not args.no_write and target.is_dir():
        (target / "content.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        (target / "content.md").write_text(report(result), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else report(result))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
