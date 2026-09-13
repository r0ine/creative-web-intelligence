# Typography System v3.1

A site’s font work is evaluated as a system.

## Roles

Define explicit roles: display, heading, body, UI/label, numeric/data, code/mono (only when needed).

## Metrics

Measure/test:
- apparent x-height
- width/condensation
- cap height impression
- stroke contrast
- line gap
- character spacing
- punctuation/numeric behavior
- wrapping at target container widths

## Hierarchy

Use size, weight, width, contrast, case, tracking and whitespace deliberately. Do not make every hierarchy level bold + larger.

## Responsive

Use clamp/fluid scales only when they improve continuity. Define minimum/maximum sizes, line-height transitions, wrap policies and breakpoint-specific changes. Recompose headings on mobile rather than accepting accidental 5–7 line wraps.

## Fallbacks

Choose fallback stacks with similar metrics when possible. Use CSS font metric overrides where appropriate to reduce layout shift. Test the actual fallback state by blocking web fonts.

## Variable fonts

Use axes (weight, width, optical size, slant etc.) only when the chosen font supports them and the product gains something. Avoid animating axes simply because it is possible.

## Language coverage

Check every required script, diacritics, punctuation, currency symbols and numerals. A beautiful Latin-only display font is not acceptable if the site must render Turkish or another required language correctly.
