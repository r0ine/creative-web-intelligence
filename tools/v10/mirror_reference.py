#!/usr/bin/env python3
"""Referans siteyi wget ile yerel çalışma alanına indirir ve ne indiğini kaydeder."""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "reference-workspace"
TYPES = {
    "html": {".html", ".htm"}, "css": {".css"}, "js": {".js", ".mjs"},
    "image": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg", ".ico"},
    "font": {".woff", ".woff2", ".ttf", ".otf", ".eot"}, "video": {".mp4", ".webm", ".mov", ".m4v"},
    "model": {".glb", ".gltf", ".obj", ".fbx", ".usdz", ".hdr", ".ktx2"},
}
LICENSE_FILE = re.compile(r"^(licen[cs]e|copying)(\.[a-z]+)?$", re.I)
LICENSE_TEXT = re.compile(r"SPDX-License-Identifier:\s*([\w.+-]+)|@license\s+([\w.+-]+)|\b(MIT License|Apache License|GNU General Public License|Creative Commons)\b")
PERMISSIVE = re.compile(r"\b(MIT|Apache|BSD|ISC|CC0|Unlicense)\b", re.I)
# wget çıkış kodu 8: bazı dosyalar 404/403 döndü; indirilen kısım yine kullanılabilir.
USABLE_EXIT = {0, 8}
DIAGNOSES = (
    (r"Proxy tunneling failed|ERROR 407", "Ağ veya proxy bağlantıyı reddetti; bu ortamda dış sitelere erişim kapalı olabilir."),
    (r"unable to resolve host|Name or service not known|Temporary failure in name resolution", "Alan adı çözülemedi; adresi ve internet bağlantısını kontrol et."),
    (r"certificate", "Sertifika doğrulanamadı; güvenli bağlantı kurulamadı."),
    (r"ERROR 403", "Sunucu erişimi reddetti (403); site otomatik indirmeye kapalı olabilir."),
    (r"ERROR 404", "Bazı adresler bulunamadı (404)."),
    (r"ERROR 429", "Sunucu çok fazla istek dedi (429); --wait değerini artır."),
    (r"quota", "Kota doldu; indirme yarıda kaldı. Gerekirse --quota-mb değerini artır."),
)


def diagnose(log_text):
    return [message for pattern, message in DIAGNOSES if re.search(pattern, log_text, re.I)]


def build_command(url, destination, level=2, quota_mb=200, wait=1.0, allow_domains=(), wget="wget"):
    host = urlparse(url).hostname
    command = [
        wget, "--mirror", "--convert-links", "--adjust-extension", "--page-requisites", "--no-parent",
        f"--level={level}", f"--quota={quota_mb}m", f"--wait={wait:g}", "--random-wait",
        "--timeout=20", "--tries=2", "--restrict-file-names=windows",
        f"--directory-prefix={destination}", f"--output-file={Path(destination).parent / 'wget.log'}",
    ]
    if allow_domains:
        command += ["--span-hosts", "--domains=" + ",".join([host, *allow_domains])]
    return command + [url]


def validate_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Adres http:// veya https:// ile başlayan tam bir site adresi olmalı.")
    return parsed.hostname


def file_type(path):
    suffix = path.suffix.lower()
    return next((name for name, suffixes in TYPES.items() if suffix in suffixes), "other")


class TextProbe(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.text = []
        self.scripts = 0
        self.license_links = []
        self.app_root = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style", "noscript", "template"}:
            self.skip += 1
            self.scripts += tag == "script" and bool(attrs.get("src"))
        if tag == "link" and "license" in (attrs.get("rel") or "").lower().split():
            self.license_links.append(attrs.get("href", ""))
        if tag == "div" and attrs.get("id") in {"root", "__next", "app", "__nuxt", "svelte"}:
            self.app_root = True

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "template"} and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


def probe_html(path):
    probe = TextProbe()
    probe.feed(path.read_text(encoding="utf-8", errors="replace"))
    text = " ".join(" ".join(probe.text).split())
    return probe, text


def find_entry(site_dir, host):
    candidates = [site_dir / host / "index.html", *sorted(site_dir.rglob("index.html")), *sorted(site_dir.rglob("*.html"))]
    return next((path for path in candidates if path.is_file()), None)


def license_evidence(site_dir, files):
    root_licenses, library_licenses = [], []
    for path in files:
        relative = path.relative_to(site_dir).as_posix()
        if LICENSE_FILE.match(path.name):
            head = path.read_text(encoding="utf-8", errors="replace")[:400]
            root_licenses.append({"file": relative, "match": " ".join(head.split())[:120]})
        elif file_type(path) in {"css", "js"} and path.stat().st_size < 5_000_000:
            match = LICENSE_TEXT.search(path.read_text(encoding="utf-8", errors="replace")[:20000])
            if match:
                library_licenses.append({"file": relative, "match": next(g for g in match.groups() if g)})
    return root_licenses, library_licenses


def usage_decision(owned, root_licenses, license_links):
    if owned:
        return "owned", "Kullanıcı bu sitenin kendisine ait olduğunu belirtti; indirilen kopya düzenlenebilir."
    declared = [item["match"] for item in root_licenses] + license_links
    if declared and any(PERMISSIVE.search(item) for item in declared):
        return "license-review", ("Sitede izin verici bir lisans bulundu. Koşullarını (atıf, lisans metnini koruma) okuduktan sonra "
                                  "kod düzenlenebilir; görsel, metin ve fontların lisansı ayrıca kontrol edilir.")
    if declared:
        return "license-review", "Sitede bir lisans beyanı var ama izin verici olduğu doğrulanamadı; metni okumadan kod kullanma."
    return "study-only", ("Lisans bulunamadı: kopya yalnız yerel inceleme ve ölçüm içindir. Yayınlanacak sitede kod, görsel, metin ve "
                          "font kopyalanmaz; düzen ve davranış yeni kodla yeniden kurulur.")


def summarize(site_dir, url, host, command, exit_code, owned=False):
    files = sorted(p for p in site_dir.rglob("*") if p.is_file())
    by_type = {}
    for path in files:
        bucket = by_type.setdefault(file_type(path), {"count": 0, "bytes": 0})
        bucket["count"] += 1
        bucket["bytes"] += path.stat().st_size
    entry = find_entry(site_dir, host)
    notes, js_shell, license_links = [], False, []
    if entry is None:
        notes.append("HTML sayfası inmedi; adres, robots.txt kısıtı veya erişim engeli olabilir.")
    else:
        probe, text = probe_html(entry)
        license_links = probe.license_links
        # Boş uygulama kabuğu: görünür metin neredeyse yok ve içerik betikten geliyor.
        js_shell = (len(text) < 40 and probe.scripts > 0) or (probe.app_root and len(text) < 200)
        if js_shell:
            notes.append("Sayfa içeriği JavaScript ile oluşturuluyor; wget görünen tasarımı yakalayamaz. "
                         "Canlı görünüm için tools/v10/capture_reference.mjs kullan.")
    log = site_dir.parent / "wget.log"
    if log.is_file():
        notes += diagnose(log.read_text(encoding="utf-8", errors="replace")[-20000:])
    if exit_code not in USABLE_EXIT:
        notes.append(f"wget {exit_code} koduyla bitti; ayrıntı wget.log içinde.")
    elif exit_code == 8:
        notes.append("Bazı dosyalar sunucudan alınamadı (404/403); eksikler wget.log içinde.")
    root_licenses, library_licenses = license_evidence(site_dir, files)
    usage, usage_note = usage_decision(owned, root_licenses, license_links)
    return {
        "version": "10.0",
        "url": url,
        "host": host,
        "capturedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "command": command,
        "wgetExit": exit_code,
        "entry": entry.relative_to(site_dir).as_posix() if entry else None,
        "files": len(files),
        "bytes": sum(item["bytes"] for item in by_type.values()),
        "byType": dict(sorted(by_type.items())),
        "jsShell": js_shell,
        "license": {"site": root_licenses, "links": license_links, "libraries": library_licenses},
        "usage": usage,
        "usageNote": usage_note,
        "notes": notes,
    }


def mirror(url, out=WORKSPACE, level=2, quota_mb=200, wait=1.0, allow_domains=(), owned=False, wget=None):
    host = validate_url(url)
    binary = wget or shutil.which("wget")
    if not binary:
        raise FileNotFoundError("wget bulunamadı. Kur (Linux: apt install wget, macOS: brew install wget) veya --wget ile yolunu ver.")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    workspace = Path(out) / re.sub(r"[^a-z0-9.-]", "_", host.lower()) / stamp
    site_dir = workspace / "site"
    site_dir.mkdir(parents=True, exist_ok=True)
    command = build_command(url, site_dir, level, quota_mb, wait, allow_domains, binary)
    exit_code = subprocess.run(command, check=False).returncode
    capture = summarize(site_dir, url, host, command, exit_code, owned)
    (workspace / "capture.json").write_text(json.dumps(capture, ensure_ascii=False, indent=2), encoding="utf-8")
    return workspace, capture


def render(workspace, capture):
    size = capture["bytes"] / 1024 / 1024
    lines = [f"Çalışma alanı: {workspace}", f"Giriş sayfası: {capture['entry'] or 'yok'}",
             f"{capture['files']} dosya, {size:.1f} MB · wget çıkış kodu {capture['wgetExit']}"]
    lines += [f"  {kind}: {item['count']} dosya" for kind, item in capture["byType"].items()]
    lines.append(f"Kullanım: {capture['usage']} — {capture['usageNote']}")
    lines += [f"Not: {note}" for note in capture["notes"]]
    lines.append(f"Sonraki adım: python tools/v10/analyze_reference.py {workspace}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Referans siteyi wget ile indirir (robots.txt'e uyar, boyut ve derinlik sınırlıdır).")
    parser.add_argument("url")
    parser.add_argument("--out", default=str(WORKSPACE), help="Çalışma alanı kökü (git'e girmez)")
    parser.add_argument("--level", type=int, default=2, help="Bağlantı derinliği; 0 sınırsızdır")
    parser.add_argument("--quota-mb", type=int, default=200, help="Toplam indirme sınırı (MB)")
    parser.add_argument("--wait", type=float, default=1.0, help="İstekler arası bekleme (sn)")
    parser.add_argument("--allow-domain", action="append", default=[], help="Görsel/font CDN alan adı (tekrarlanabilir)")
    parser.add_argument("--own", action="store_true", help="Site sana ait; kopya düzenlenebilir olarak işaretlenir")
    parser.add_argument("--wget", help="wget dosyasının yolu")
    parser.add_argument("--dry-run", action="store_true", help="Yalnız çalıştırılacak komutu göster")
    args = parser.parse_args(argv)
    if args.level < 0 or args.quota_mb < 1 or args.wait < 0:
        parser.error("Derinlik ve bekleme negatif olamaz; kota en az 1 MB olmalı.")
    try:
        validate_url(args.url)
        if args.dry_run:
            print(" ".join(build_command(args.url, Path(args.out) / "<host>/<zaman>/site", args.level, args.quota_mb,
                                         args.wait, args.allow_domain, args.wget or "wget")))
            return 0
        workspace, capture = mirror(args.url, args.out, args.level, args.quota_mb, args.wait, args.allow_domain, args.own, args.wget)
    except (ValueError, FileNotFoundError) as error:
        parser.error(str(error))
    print(render(workspace, capture))
    return 0 if capture["wgetExit"] in USABLE_EXIT and capture["entry"] else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
