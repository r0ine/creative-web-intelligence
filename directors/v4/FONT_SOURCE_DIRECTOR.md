# FONT SOURCE DIRECTOR v4

Font Director chooses the typographic voice. Font Source Director verifies that the chosen voice can actually be sourced, licensed, loaded and rendered for the required languages.

## Use Fontsource metadata for
- family discovery after typographic criteria are already defined;
- subset checks (including Latin Extended when Turkish coverage matters);
- supported weights/styles;
- variable-font availability and axes;
- Unicode ranges and file variants;
- version information.

## Do not
- sort a font API by popularity and call the first result art direction;
- assume `latin` includes every required Turkish glyph;
- confuse availability with suitability;
- request dozens of font files because the API exposes them.

## Required output
`candidateFamily`, `sourceId`, `subsets`, `weights`, `styles`, `variable`, `axes`, `languageCoverage`, `licenseReview`, `loadingPlan`, `fallbackMetrics`, `rejectReason`.
