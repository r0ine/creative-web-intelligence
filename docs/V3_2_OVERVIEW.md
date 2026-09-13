# V3.2 Overview — Visual Direction Hardening

## Why this version exists

Generative front-end systems often produce technically valid but visually convergent sites. The convergence is visible in recurring combinations: centered oversized grotesk headings, pill labels, violet/blue gradients, glass cards, thin dividers between every section, `opacity + translateY` reveals, identical easing, uniform rounded cards and excessive low-purpose scroll effects.

v3.2 treats these as **systemic fingerprints**, not isolated styling mistakes.

## Sanzo Wada intelligence

The Wada source is used as a relationship reference, not as a magic palette generator. The source dataset model contains 348 combinations of two to four colors and 159 unique named colors. v3.2 preserves source provenance and separates historical/source color data from screen adaptation.

Every palette should be evaluated for:

- color count and area budget
- relative lightness and chroma
- hue/temperature relationships
- strongest and weakest contrast pairs
- likely text/background candidates
- accent scarcity
- decorative-only risk
- dark/light mode adaptation risk
- typography interaction
- image/3D material interaction

A Wada combination may be beautiful and still be unusable for body text. Harmony and legibility are separate gates.

## Typography intelligence

Typography is no longer represented primarily by named font pairs. v3.2 introduces a profile that evaluates morphology and use-role: width, apparent x-height, cap-height impression, stroke contrast, apertures, counters, terminals, rhythm, numeral behavior, variable axes, script coverage, loading and fallback metrics.

The system may choose one family, two families or a system stack. Two fonts are not automatically better than one.

## Motion intelligence

Scroll is a signal, not an entrance-animation factory. v3.2 distinguishes:

- state transition
- masked/cropped reveal
- opacity activation
- scale/settle
- spatial transfer
- media progression
- typographic transform
- pointer response
- route continuity
- intentionally static/rest behavior

A project should normally have one dominant grammar and a small number of supporting motions. Repetition is allowed only when it creates language, not when it exposes a default helper.

## Section separation

Borders are not the default section separator. Prefer whitespace, compositional shift, typography, media, tone/value change, alignment changes or controlled overlap. A divider needs an information-architecture reason.

## Acceptance

A page can fail v3.2 even if every component is polished. If the whole composition still reads as a bundle of common AI motifs, the system must change its decisions rather than increase visual effects.
