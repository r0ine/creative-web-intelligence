# v10 release notes

**Language:** [Türkçe](RELEASE_NOTES_V10.md) · English

## Reference lab

The [reference lab](reference-engine/REFERENCE_LAB.md) (Turkish) downloads a reference site, measures it, locates what to edit, and compares new work against it. Downloads stay in `reference-workspace/`, which git ignores.

- `tools/v10/mirror_reference.py`: runs `wget --mirror --convert-links --adjust-extension --page-requisites --no-parent` with depth, quota and wait limits. It respects robots.txt and writes `capture.json` with file types, size, entry page and detected licenses. The result is one usage decision: `owned`, `license-review` or `study-only`. Pages that JavaScript renders into an empty shell are flagged.
- `tools/v10/capture_reference.mjs`: opens the site in Playwright at desktop and mobile sizes. It records screenshots, a reduced-motion screenshot, an area-weighted palette with neutral/support/accent shares, fonts, animations, script URLs and WCAG contrast findings. If axe-core is installed, it adds axe violations.
- `tools/v10/analyze_reference.py` extracts from the downloaded copy:
  - **design measurements:** color roles, palette, fonts, type scale, spacing, radii, durations/easings, breakpoints, CSS variables;
  - **site information:** libraries, page structure, static accessibility issues and page weight.

  It also produces an **edit map** that points each v9 surface to the CSS file and line where it is defined, and lists where the reference conflicts with library rules. Outputs are `analysis.md`, `analysis.json` and `tokens.css`.
- `tools/v10/compare_reference.mjs`: compares reference and new work at the same viewport. It produces a diff image, the mismatch percentage and the most different screen region, using the v7 pixel-compare module.
- `tools/v10/template_catalog.py`: groups open-source templates and components from the v8 registry by license: editable, share-alike, or study only.
- `runtime/reference/style-metrics.mjs`: tested pure helpers for color parsing, WCAG contrast, area palette and diff regions.

## Found during trials

- On the sample site, static analysis and axe-core reported the same five issues: empty button, contrast, heading order, image alt and empty link.
- Small static pages were mistaken for JavaScript shells; fixed.

## Dogfooding fixes

Gaps found while building a real test site (`examples/v10/test-site/`) with the library were fixed:

- `analyze_reference.py` now resolves fonts set through `font-family: var(--font-*)` (CF-007 was being bypassed) and checks text contrast against the inherited page background.
- The three audit tools (`analyze_reference.py`, `audit_visual_defaults.mjs`, `authenticity_check.py`) now state their coverage and limits; "0 findings / PASS" is not proof on its own.
- `tools/v10/font_coverage.py` + `data/v10/font_stacks.json`: check a font's Turkish (İ ı Ğ ğ Ş ş) glyph coverage (live via fontconfig when present) and suggest an offline system-font stack.
- `BRIEF_TO_REFERENCE.md` covers a fully-specified brief and an unreachable (network-blocked) source; `START_HERE_V10.md` includes the browser install command and a minimal reading path for a small site.

## Pipeline and site checker commands

- `tools/v10/build_from_reference.py`: runs the full reference-based site building pipeline in one command. Download → analyze → extract content → check fonts → build spec (JSON + MD). `--content` also extracts content from your own site; `--dry-run` shows only the steps.
- `tools/v10/check_site.py`: runs three audit tools (analyze + v7 audit + v5 authenticity) in one command, producing a merged `check-report.md`. Each tool's coverage and limits are stated in the report.

## Maintenance

- The v7, v8 and v9 validators now compare the manifest version numerically, so new releases no longer require editing them.
- `validate_v10.py` checks two consistency rules: the edit map must match the v9 surfaces, and every conflict cited by the analyzer must exist in the v9 register. `validate_all.py` runs the v10 chain.
