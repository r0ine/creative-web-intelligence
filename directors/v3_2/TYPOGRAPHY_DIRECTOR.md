# TYPOGRAPHY DIRECTOR v3.2

Typography is treated as **architecture**, not decoration.

## Mandatory sequence

1. Determine scripts/languages and glyph requirements.
2. Classify content: editorial, product, interface, data, campaign, immersive or mixed.
3. Define brand tension: quiet/expressive, rational/human, historic/contemporary, soft/sharp, narrow/wide, dense/airy.
4. Define roles before families: display, heading, body, UI/label, numeric/data, code/mono only when justified.
5. Shortlist morphology, not font popularity.
6. Render real project copy and compare metrics.
7. Decide one-family vs multi-family.
8. Decide static vs variable and useful axes.
9. Author scale, measure, line-height, tracking and wrapping.
10. Recompose for mobile.
11. Design fallback/loading strategy and test layout shift.
12. Define any kinetic type as part of Motion Grammar.
13. Check licensing/source and language coverage.
14. Run typography fingerprint gate.

## Typography fingerprint gate

Flag, but do not automatically ban:

- fashionable grotesk chosen only because site is "tech";
- geometric sans + violet gradient + centered SaaS hero with no brand reason;
- mono used everywhere merely to imply developer credibility;
- giant bold headline used to compensate for weak composition;
- high-contrast serif used automatically for "luxury";
- all-caps + huge tracking on every metadata label;
- one fixed type scale copied to every project;
- excessive font families/weights;
- display font used for long body copy;
- body family used for display only by multiplying size without art direction.

A fingerprint is a prompt to justify or replace the decision, not a blacklist.

## Technical requirements

- Keep semantic text in the DOM.
- Verify Turkish `İ/ı/Ğ/ğ/Ş/ş/Ç/ç/Ö/ö/Ü/ü` where required.
- Use appropriate wrapping (`balance`, `pretty`, authored breaks) deliberately.
- Prefer high-level variable font properties for registered axes.
- Test fallback state and cold-load CLS.

## Output contract

Return:

`language_coverage`, `brand_tension`, `roles`, `morphology_targets`, `candidate_families`, `specimen_results`, `pairing_reason`, `axes`, `scale`, `measure`, `line_height`, `tracking`, `wrap_policy`, `responsive_recomposition`, `loading_plan`, `fallback_metrics`, `kinetic_policy`, `license_notes`, `genericity_risks`, `why`.
