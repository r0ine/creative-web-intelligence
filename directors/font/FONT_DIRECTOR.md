# FONT DIRECTOR v2

## Goal
Choose and explain a typographic system instead of defaulting to a fashionable font.

## Decision pipeline
1. Classify content: editorial / interface / data / campaign / product / immersive.
2. Choose voice level: neutral, characteristic, expressive, extreme.
3. Choose display role separately from body/UI role.
4. Check language/glyph coverage and licensing.
5. Decide static vs variable font. Variable fonts can expose weight/width/optical-size axes and may reduce multiple font-file requests when used well.
6. Build responsive type scale using optical size, line length, leading and tracking—not font-size alone.
7. Test hierarchy without color; if hierarchy collapses, type system is weak.
8. Load fonts without causing layout instability; prefer WOFF2 and preload only critical faces.

## Pairing heuristics
- Contrast roles, not just classifications: expressive heading + calm body is often safer than expressive+expressive.
- Similar x-height can improve visual rhythm; too-similar families can look accidental.
- Serif/sans is not automatically good; compare stroke contrast, width, counters, terminals and rhythm.
- Mono is an accent/interface voice, not a universal 'developer' aesthetic.
- One family with variable width/weight can be stronger than unnecessary multi-family pairing.

## Anti-defaults
Never choose Inter, Space Grotesk, Helvetica-like grotesks, or a high-contrast serif merely because the project category suggests it. First justify the voice.

## Output contract
Return: `font_roles`, `pairing_reason`, `scale`, `measure`, `line_height`, `tracking`, `responsive_behavior`, `loading_plan`, `fallback_stack`, `licensing_check`, `anti_patterns`.
