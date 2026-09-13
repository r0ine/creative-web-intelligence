# Release Notes — v3.2

v3.2 focuses on visual authorship. It preserves the v3.1 security/full-stack systems and adds a stricter color, typography, motion and composition layer.

## New

- Sanzo Wada source/provenance registry and historical-set aggregate baseline.
- Wada full-set analyzer that reconstructs combination IDs and computes OKLCH/luminance/contrast/role candidates/risk flags from an explicit source snapshot.
- Color Director v3.2 and Wada-to-web adaptation protocol.
- Typography Director v3.2, font archetype taxonomy, context decision matrix, pairing/metric rules, variable-font/loading rules and anti-generic typography fingerprints.
- Motion Director v3.2, ten motion grammar recipes and anti-AI motion fingerprints.
- Section-separation policy and alternatives to universal dividers/cardification.
- Visual Fingerprint Gate with 13 cross-system QA categories.
- New schemas for font profiles and Wada palette analysis.
- Master v3.2 prompt and audit prompt.

## Important behavior change

The library no longer treats a repeated `opacity + translateY` entrance as a neutral default. It is considered a high-salience visual decision and repeated use incurs a fingerprint penalty. Likewise, a divider is no longer the default boundary between sections.

## Compatibility

v3.2 is additive. Existing v1-v3.1 data and directors remain in the archive for compatibility and provenance. New work should enter through `START_HERE_V3_2.md`.
