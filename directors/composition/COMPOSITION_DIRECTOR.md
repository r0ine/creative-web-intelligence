# COMPOSITION DIRECTOR v2

> **Öncelik (v9):** Bu dosyanın yerini [`directors/v5/COMPOSITION_DIRECTOR_V5.md`](../v5/COMPOSITION_DIRECTOR_V5.md) aldı. Çakışmada o dosya geçerlidir; bu dosya yalnız arka plan bilgisi içindir. Ayrıntı: [kural önceliği](../../v9/RULE_PRECEDENCE.md).

A composition is a reading path, not a collection of containers.

## Inputs
content density, primary object, primary action, brand tension, desired rhythm, media ratio, 3D role, mobile priority.

## Process
- Establish focal point and reading order.
- Choose grid family only after content hierarchy.
- Assign negative-space zones deliberately.
- Decide where composition should BREAK its own rhythm once or twice for emphasis.
- Test layout in grayscale and without border/shadow decoration.
- Recompose mobile rather than shrinking desktop.

## AI-slop gate
Reject repeated `eyebrow -> centered h2 -> paragraph -> 3 equal cards` sections unless the content genuinely has three peer concepts.

## Output
`layout_family`, `grid`, `focal_axis`, `reading_path`, `section_rhythm`, `negative_space`, `breakpoints`, `mobile_recomposition`, `avoid_patterns`.
