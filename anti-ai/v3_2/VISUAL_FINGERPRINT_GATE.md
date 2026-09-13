# Visual Fingerprint Gate v3.2

This gate looks for **repeated generated-design habits**, not individual CSS properties.

## Score categories

Each category is scored 0–3:

- color cliché
- typography cliché
- hero cliché
- cardification
- divider repetition
- motion repetition
- easing/timing sameness
- decorative glow/gradient dependency
- bento-without-information-need
- fake technical metadata / pills
- excessive glassmorphism
- identical section geometry
- lack of rest/static ranges

## Interpretation

- 0–5: low fingerprint risk
- 6–10: inspect repeated motifs
- 11–18: recompose at least one major system
- 19+: fail; decoration is substituting for art direction

Do not game the score by randomly changing effects. Repetition is solved through a clearer concept, stronger typography/composition and fewer unnecessary devices.

## High-confidence fingerprints

- every section: fade + upward translation
- every section: top border + same vertical padding
- every content unit: rounded card + thin border + low-opacity fill
- AI/tech product: blue/purple gradient selected with no brand rationale
- centered hero: eyebrow pill + huge grotesk + paragraph + two CTAs + glow blobs
- developer site: mono everywhere + fake terminal metadata + green dots without product meaning
- luxury: Didone + black/gold chosen only from category stereotype
- all hover interactions: `translateY(-4px) scale(1.02)`

## Review question

If all animations and decorative effects are disabled, does the page still have a distinct identity? If not, return to typography, content hierarchy and composition.
