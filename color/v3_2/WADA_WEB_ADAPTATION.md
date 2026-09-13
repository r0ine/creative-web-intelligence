# Wada -> Web Adaptation Protocol

## Input

A source combination plus project Design DNA.

## Stage A — preserve the source

Keep `combination_id`, source color names, source conversion values and provenance. Do not silently edit a source color to make the website work.

## Stage B — compute perceptual geometry

Convert sRGB to OKLab/OKLCH for analysis. Compute luminance/contrast separately using the WCAG relative-luminance method. OKLCH is for perceptual art direction; WCAG contrast is for text/UI safety.

## Stage C — classify roles

Candidate roles:

- page background
- elevated surface
- display-text color
- body-text color
- muted text
- primary accent
- secondary/decorative accent
- focus/selection state
- media/material tint

A source color can be rejected for a role even if it remains in decorative use.

## Stage D — contrast repair

If no source pair is safe for required text, choose one of these in order:

1. add a quiet external neutral while preserving Wada colors as accents/materials;
2. derive a controlled lightness-adjusted companion in OKLCH and record it as an adaptation, never source data;
3. restrict the original palette to large/decorative roles;
4. choose another Wada combination.

Do not "fix" low contrast with text-shadow, glow or boldness alone.

## Stage E — area plan

Assign ranges instead of one universal ratio. Examples:

- quiet editorial: 78–92% neutral/base, 6–18% support, 2–8% accent
- expressive campaign: 55–75% dominant, 15–30% support, 5–15% accent
- product UI: 80–94% neutral/surface system, 3–12% brand accent, semantic colors separate

These are composition ranges, not templates.

## Stage F — run real components

Test the palette on hero type, long body copy, buttons, form states, cards only if cards are actually needed, media captions, focus indicators and disabled states. Swatches alone cannot approve the system.
