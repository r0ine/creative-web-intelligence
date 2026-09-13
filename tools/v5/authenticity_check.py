#!/usr/bin/env python3
"""CWI v5 authenticity check.

Static analyzer that reads HTML/CSS/JS files and reports the v5 fingerprints it
finds. Python stdlib only; regex-level detection. Not a linter, a witness.

Honest limitations:
- Regex cannot resolve computed styles, only source values. A fingerprint defined
  by a CSS variable applied conditionally may be missed.
- Detection is best-effort. Absence of a report is not proof of absence of the
  pattern. Human review of the summary tests (decoration-off, motion-off,
  identity) is still required.
- Coverage-based checks (rest zones, cardification ratio) require the analyzer
  to see the whole page bundle; individual component files can only report
  local evidence.

Usage:
  python tools/v5/authenticity_check.py path/to/build --json > report.json
  python tools/v5/authenticity_check.py path/to/build --format text
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / 'data/v5/authenticity_fingerprints.json'


def load_catalog():
    return json.loads(CATALOG.read_text(encoding='utf-8'))


def collect_files(root: Path):
    exts = {'.html', '.htm', '.css', '.scss', '.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte', '.astro'}
    files = []
    for p in root.rglob('*'):
        if p.is_file() and p.suffix.lower() in exts and 'node_modules' not in p.parts and '.git' not in p.parts:
            try:
                files.append((p, p.read_text(encoding='utf-8', errors='ignore')))
            except Exception:
                continue
    return files


def is_style_file(p: Path) -> bool:
    return p.suffix.lower() in {'.css', '.scss'}


def is_script_file(p: Path) -> bool:
    return p.suffix.lower() in {'.js', '.jsx', '.ts', '.tsx'}


def is_markup_file(p: Path) -> bool:
    return p.suffix.lower() in {'.html', '.htm', '.vue', '.svelte', '.astro', '.jsx', '.tsx'}


HAIRLINE_RE = re.compile(
    r'border(?:-top|-bottom|-left|-right)?\s*:\s*(?:0\.5px|1px|1\.5px|2px)\s+(?:solid|dashed)\s+(?:rgba?\([^)]*(?:0?\.0?\d|0?\.1[0-4])[^)]*\)|hsla?\([^)]*(?:0?\.0?\d|0?\.1[0-4])\)|#[0-9a-fA-F]{6,8}(?:[0-9a-fA-F]{2})?)',
    re.IGNORECASE
)

HR_RE = re.compile(r'<hr\b|class\s*=\s*["\'][^"\']*(?:divider|separator|section-line|hairline)[^"\']*["\']', re.IGNORECASE)

GRID_OVERLAY_RE = re.compile(
    r'background(?:-image)?\s*:\s*(?:repeating-)?linear-gradient\([^)]*(?:transparent|rgba?\([^)]*0?\.0[0-8][^)]*\))[^)]*\)\s*,?\s*(?:repeating-)?linear-gradient\(',
    re.IGNORECASE
)

FADE_UP_CSS_RE = re.compile(
    r'(?:transform\s*:\s*translateY\(\s*(?:1[5-9]|[2-4]\d)px\s*\)[^;}]*;\s*[^{}]*opacity\s*:\s*0)|(?:opacity\s*:\s*0[^;}]*;\s*[^{}]*transform\s*:\s*translateY\(\s*(?:1[5-9]|[2-4]\d)px)',
    re.IGNORECASE | re.DOTALL
)

GSAP_FADE_UP_RE = re.compile(
    r'gsap\s*\.\s*(?:from|fromTo)\s*\([^)]*\{\s*[^}]*opacity\s*:\s*0[^}]*(?:,\s*y\s*:\s*(?:1[5-9]|[2-4]\d)|,\s*translateY\s*:\s*(?:1[5-9]|[2-4]\d))',
    re.IGNORECASE | re.DOTALL
)

STAGGER_LADDER_RE = re.compile(
    r'(?:delay\s*:\s*(?:i|index|idx)\s*\*\s*0?\.\d)|(?:stagger\s*:\s*0?\.[01]\d?)|(?:transitionDelay\s*:\s*`?\$?\{?\s*(?:i|index|idx)\s*\*\s*(?:100|150|200)\s*\}?ms)',
    re.IGNORECASE
)

BLUR_IN_RE = re.compile(
    r'filter\s*:\s*blur\(\s*(?:[4-9]|1\d|2\d)px\s*\)[^;}]*;[^{}]*filter\s*:\s*blur\(\s*0?px?\s*\)|blur\(\s*(?:[4-9]|1\d)px\s*\)\s*,\s*blur\(\s*0',
    re.IGNORECASE | re.DOTALL
)

CENTERED_HERO_RE = re.compile(
    r'(?:class\s*=\s*["\'][^"\']*hero[^"\']*["\'][^>]*>[\s\S]{0,800}text-align\s*:\s*center)|(?:hero[^{]{0,120}\{[^}]*text-align\s*:\s*center[^}]*\})',
    re.IGNORECASE
)

RADIAL_GLOW_RE = re.compile(
    r'radial-gradient\(\s*(?:circle|ellipse)?[^)]*(?:rgba?\([^)]*0?\.[2-9][^)]*\)|hsla?\([^)]*0?\.[2-9][^)]*\))[^)]*\)',
    re.IGNORECASE
)

DARK_SURFACE_RE = re.compile(
    r'background(?:-color)?\s*:\s*(?:#0[0-9a-fA-F]{5}|#0[0-9a-fA-F]{2}|rgb\(\s*(?:[0-9]|1\d|2\d)\s*,\s*(?:[0-9]|1\d|2\d)\s*,\s*(?:[0-9]|1\d|2\d)\s*\))',
    re.IGNORECASE
)

BLUE_PURPLE_GRADIENT_RE = re.compile(
    r'linear-gradient\([^)]*(?:#[0-9a-fA-F]{6}|rgb\([^)]+\))\s*,?\s*(?:#[0-9a-fA-F]{6}|rgb\([^)]+\))',
    re.IGNORECASE
)

GRADIENT_TEXT_RE = re.compile(
    r'(?:-webkit-)?background-clip\s*:\s*text|(?:-webkit-)?text-fill-color\s*:\s*transparent',
    re.IGNORECASE
)

MONO_BODY_RE = re.compile(
    r'body[^{]{0,60}\{[^}]*font-family\s*:[^;}]*(?:mono|courier|consolas|menlo|monaco|"?JetBrains Mono"?|"?Fira Code"?)',
    re.IGNORECASE | re.DOTALL
)

BACKDROP_BLUR_RE = re.compile(r'backdrop-filter\s*:\s*blur\(', re.IGNORECASE)

EMOJI_FEATURE_RE = re.compile(
    r'(?:class\s*=\s*["\'][^"\']*(?:feature|card|item)[^"\']*["\'][^>]*>\s*(?:[\U0001F300-\U0001FAFF]|[\u2600-\u27BF]))',
)

HOVER_LIFT_RE = re.compile(
    r':hover\s*\{[^}]*transform\s*:\s*translateY\(\s*-\s*(?:[2-9]|1\d)px[^}]*\}',
    re.IGNORECASE | re.DOTALL
)

CURSOR_MOUSEMOVE_RE = re.compile(r'addEventListener\(\s*["\']mousemove', re.IGNORECASE)

REPEAT_3_COLUMNS_RE = re.compile(r'grid-template-columns\s*:\s*repeat\(\s*3\s*,', re.IGNORECASE)

BAD_ALL_CAPS_RE = re.compile(r'text-transform\s*:\s*uppercase', re.IGNORECASE)

BACKGROUND_CLIP_TEXT_RE = re.compile(r'background-clip\s*:\s*text', re.IGNORECASE)

CENTERED_H1_RE = re.compile(
    r'h1[^{]{0,40}\{[^}]*text-align\s*:\s*center[^}]*font-size\s*:\s*(?:[6-9]|1\d)v?w?',
    re.IGNORECASE | re.DOTALL
)


def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) >= 6:
        try:
            return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        except ValueError:
            return None
    return None


def rgb_to_hsv(r, g, b):
    r_, g_, b_ = r / 255, g / 255, b / 255
    mx, mn = max(r_, g_, b_), min(r_, g_, b_)
    v = mx
    d = mx - mn
    s = 0 if mx == 0 else d / mx
    if d == 0:
        h = 0
    elif mx == r_:
        h = ((g_ - b_) / d) % 6
    elif mx == g_:
        h = (b_ - r_) / d + 2
    else:
        h = (r_ - g_) / d + 4
    return int(h * 60) % 360, s, v


def is_blue_purple(rgb):
    if not rgb:
        return False
    h, s, v = rgb_to_hsv(*rgb)
    return 210 <= h <= 290 and s > 0.35 and v > 0.3


def scan(root: Path):
    files = collect_files(root)
    findings = defaultdict(list)

    hairline_hits = 0
    hr_hits = 0
    fade_up_hits = 0
    gsap_fade_up_hits = 0
    stagger_hits = 0
    blur_in_hits = 0
    centered_hero_hits = 0
    radial_glow_hits = 0
    dark_surface_hits = 0
    backdrop_blur_hits = 0
    hover_lift_hits = 0
    mousemove_hits = 0
    three_col_hits = 0
    grad_text_hits = 0
    mono_body_hits = 0
    grid_overlay_hits = 0
    emoji_feature_hits = 0
    centered_h1_hits = 0
    all_caps_hits = 0

    for p, text in files:
        rel = str(p.relative_to(root))

        if is_style_file(p) or is_markup_file(p):
            for m in HAIRLINE_RE.finditer(text):
                hairline_hits += 1
                findings['AF-A03_hairline'].append({'file': rel, 'snippet': m.group(0)[:120]})

            for m in HR_RE.finditer(text):
                hr_hits += 1
                findings['AF-A01_divider'].append({'file': rel, 'snippet': m.group(0)[:120]})

            for m in GRID_OVERLAY_RE.finditer(text):
                grid_overlay_hits += 1
                findings['AF-A02_grid_overlay'].append({'file': rel, 'snippet': m.group(0)[:200]})

            for m in FADE_UP_CSS_RE.finditer(text):
                fade_up_hits += 1
                findings['AF-B01_fade_up'].append({'file': rel, 'source': 'css', 'snippet': m.group(0)[:200]})

            for m in BLUR_IN_RE.finditer(text):
                blur_in_hits += 1
                findings['AF-B04_blur_in'].append({'file': rel, 'snippet': m.group(0)[:200]})

            for m in CENTERED_HERO_RE.finditer(text):
                centered_hero_hits += 1
                findings['AF-C01_centered_hero'].append({'file': rel, 'snippet': m.group(0)[:200]})

            for m in RADIAL_GLOW_RE.finditer(text):
                radial_glow_hits += 1

            for m in DARK_SURFACE_RE.finditer(text):
                dark_surface_hits += 1

            for m in BACKDROP_BLUR_RE.finditer(text):
                backdrop_blur_hits += 1

            for m in HOVER_LIFT_RE.finditer(text):
                hover_lift_hits += 1
                findings['AF-F01_hover_lift'].append({'file': rel, 'snippet': m.group(0)[:200]})

            for m in REPEAT_3_COLUMNS_RE.finditer(text):
                three_col_hits += 1
                findings['AF-C03_three_columns'].append({'file': rel, 'snippet': m.group(0)[:120]})

            for m in GRADIENT_TEXT_RE.finditer(text):
                grad_text_hits += 1
                findings['AF-D03_gradient_text'].append({'file': rel, 'snippet': m.group(0)[:120]})

            for m in MONO_BODY_RE.finditer(text):
                mono_body_hits += 1
                findings['AF-E02_mono_body'].append({'file': rel, 'snippet': m.group(0)[:200]})

            for m in CENTERED_H1_RE.finditer(text):
                centered_h1_hits += 1
                findings['AF-E01_centered_h1'].append({'file': rel, 'snippet': m.group(0)[:200]})

            for m in BAD_ALL_CAPS_RE.finditer(text):
                all_caps_hits += 1

            for grad in BLUE_PURPLE_GRADIENT_RE.finditer(text):
                snippet = grad.group(0)
                hexes = re.findall(r'#[0-9a-fA-F]{6}', snippet)
                if any(is_blue_purple(hex_to_rgb(h)) for h in hexes):
                    findings['AF-D02_blue_purple_gradient'].append({'file': rel, 'snippet': snippet[:200]})

        if is_script_file(p):
            for m in GSAP_FADE_UP_RE.finditer(text):
                gsap_fade_up_hits += 1
                findings['AF-B01_fade_up'].append({'file': rel, 'source': 'gsap', 'snippet': m.group(0)[:200]})

            for m in STAGGER_LADDER_RE.finditer(text):
                stagger_hits += 1
                findings['AF-B02_stagger_ladder'].append({'file': rel, 'snippet': m.group(0)[:120]})

            for m in CURSOR_MOUSEMOVE_RE.finditer(text):
                mousemove_hits += 1

        if is_markup_file(p):
            for m in EMOJI_FEATURE_RE.finditer(text):
                emoji_feature_hits += 1
                findings['AF-F03_emoji_feature'].append({'file': rel, 'snippet': m.group(0)[:120]})

    total_fade_up = fade_up_hits + gsap_fade_up_hits

    verdicts = []

    if hr_hits >= 2 or hairline_hits >= 3:
        verdicts.append(('AF-A01', 'blocker', f'{hr_hits} <hr>/divider + {hairline_hits} hairline borders across files'))
    elif hairline_hits >= 1:
        verdicts.append(('AF-A03', 'high', f'{hairline_hits} hairline border(s) found'))

    if grid_overlay_hits >= 1:
        verdicts.append(('AF-A02', 'blocker', f'{grid_overlay_hits} likely grid overlay pattern(s)'))

    if total_fade_up >= 2:
        verdicts.append(('AF-B01', 'blocker', f'{total_fade_up} fade-up entrances (css={fade_up_hits}, gsap={gsap_fade_up_hits})'))
    elif total_fade_up == 1:
        verdicts.append(('AF-B01', 'high', f'1 fade-up entrance - watch for repetition'))

    if stagger_hits >= 1:
        verdicts.append(('AF-B02', 'high', f'{stagger_hits} stagger ladder pattern(s)'))

    if blur_in_hits >= 1:
        verdicts.append(('AF-B04', 'medium', f'{blur_in_hits} blur-in entrance(s)'))

    if centered_hero_hits >= 1 and radial_glow_hits >= 1:
        verdicts.append(('AF-C01', 'high', 'centered hero + radial glow present'))

    if three_col_hits >= 1:
        verdicts.append(('AF-C03', 'high', f'{three_col_hits} three-equal-column grid(s) present'))

    if dark_surface_hits >= 1 and hairline_hits >= 2 and radial_glow_hits >= 1:
        verdicts.append(('AF-D01', 'high', 'dark surface + hairlines + radial glow default pattern'))

    if grad_text_hits >= 1:
        verdicts.append(('AF-D03', 'high', f'{grad_text_hits} gradient text fill(s) on text'))

    if 'AF-D02_blue_purple_gradient' in findings:
        verdicts.append(('AF-D02', 'high', f'{len(findings["AF-D02_blue_purple_gradient"])} blue-purple gradient(s)'))

    if backdrop_blur_hits >= 3:
        verdicts.append(('AF-D04_glass', 'high', f'{backdrop_blur_hits} glass panels'))

    if mono_body_hits >= 1:
        verdicts.append(('AF-E02', 'high', 'monospace applied to body'))

    if centered_h1_hits >= 1:
        verdicts.append(('AF-E01', 'medium', 'oversized centered H1'))

    if hover_lift_hits >= 3:
        verdicts.append(('AF-F01', 'medium', f'{hover_lift_hits} hover-lift hover states'))

    if emoji_feature_hits >= 2:
        verdicts.append(('AF-F03', 'medium', f'{emoji_feature_hits} emoji-as-feature-icon uses'))

    if mousemove_hits >= 3:
        verdicts.append(('AF-F02', 'high', f'{mousemove_hits} mousemove listeners - cursor may drive multiple effects'))

    return {
        'files_scanned': len(files),
        'verdicts': verdicts,
        'raw_findings': dict(findings),
        'counts': {
            'hairline': hairline_hits,
            'hr_or_divider': hr_hits,
            'grid_overlay': grid_overlay_hits,
            'fade_up_css': fade_up_hits,
            'fade_up_gsap': gsap_fade_up_hits,
            'stagger': stagger_hits,
            'blur_in': blur_in_hits,
            'centered_hero': centered_hero_hits,
            'radial_glow': radial_glow_hits,
            'dark_surface': dark_surface_hits,
            'backdrop_blur': backdrop_blur_hits,
            'hover_lift': hover_lift_hits,
            'mousemove_listener': mousemove_hits,
            'three_column_grid': three_col_hits,
            'gradient_text': grad_text_hits,
            'mono_body': mono_body_hits,
            'emoji_feature': emoji_feature_hits,
            'centered_h1': centered_h1_hits,
            'all_caps_uppercase': all_caps_hits,
        }
    }


def summarize_gate(result):
    blockers = [v for v in result['verdicts'] if v[1] == 'blocker']
    highs = [v for v in result['verdicts'] if v[1] == 'high']
    mediums = [v for v in result['verdicts'] if v[1] == 'medium']
    lows = [v for v in result['verdicts'] if v[1] == 'low']

    if blockers:
        gate = 'FAIL'
    elif len(highs) >= 2:
        gate = 'FAIL'
    elif highs or mediums:
        gate = 'PASS-WITH-NOTES'
    else:
        gate = 'PASS'

    return {
        'gate_result': gate,
        'blockers': blockers,
        'high_severity': highs,
        'medium_severity': mediums,
        'low_severity': lows,
        'summary_tests_reminder': 'Static analysis cannot judge the three summary tests (decoration-off, motion-off, identity). Human review of those is still required before the gate can PASS.',
    }


def format_text(result, gate):
    lines = []
    lines.append(f"CWI v5 Authenticity Check")
    lines.append(f"Files scanned: {result['files_scanned']}")
    lines.append('')
    lines.append(f"GATE: {gate['gate_result']}")
    lines.append('')
    if gate['blockers']:
        lines.append(f"Blockers ({len(gate['blockers'])}):")
        for id_, sev, msg in gate['blockers']:
            lines.append(f"  [{id_}] {msg}")
        lines.append('')
    if gate['high_severity']:
        lines.append(f"High severity ({len(gate['high_severity'])}):")
        for id_, sev, msg in gate['high_severity']:
            lines.append(f"  [{id_}] {msg}")
        lines.append('')
    if gate['medium_severity']:
        lines.append(f"Medium severity ({len(gate['medium_severity'])}):")
        for id_, sev, msg in gate['medium_severity']:
            lines.append(f"  [{id_}] {msg}")
        lines.append('')
    lines.append("Note: " + gate['summary_tests_reminder'])
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='CWI v5 authenticity check (regex-level static analyzer, stdlib only)')
    parser.add_argument('path', help='path to a build directory or a single file')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--include-raw', action='store_true', help='include raw findings in JSON output')
    args = parser.parse_args()

    target = Path(args.path).resolve()
    if not target.exists():
        print(f'not found: {target}', file=sys.stderr)
        sys.exit(2)

    if target.is_file():
        original_rglob = Path.rglob
        parent = target.parent
        Path.rglob = lambda self, pat, _t=target: [_t] if self == parent else []
        result = scan(parent)
        Path.rglob = original_rglob
    else:
        result = scan(target)

    gate = summarize_gate(result)

    if args.format == 'json':
        output = {
            'files_scanned': result['files_scanned'],
            'gate': gate,
            'counts': result['counts'],
        }
        if args.include_raw:
            output['raw_findings'] = result['raw_findings']
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(format_text(result, gate))

    sys.exit(1 if gate['gate_result'] == 'FAIL' else 0)


if __name__ == '__main__':
    main()
