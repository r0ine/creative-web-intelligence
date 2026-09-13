# Sanzo Wada Color Intelligence v3.2

## Principle

Do not convert Wada into a folder of "pretty hex palettes". The useful part is the relationship between colors: value distance, chroma tension, temperature, area potential and the way a small set works as a whole.

## Dataset model

The canonical open dataset model contains 348 historical combinations built from 159 named colors. Combinations contain two, three or four colors. Preserve the source combination ID and original color names.

The library recognizes that digital reproductions can differ because of conversion choices. Store source CMYK/Lab/RGB/HEX where available and label the conversion. A screen value is a working representation, not the printed pigment itself.

## What to measure for every combination

### Structural

- palette size
- repeated/frequent source colors
- warm/cool membership
- neutral anchors
- number of competing accents

### Perceptual

- OKLCH lightness/chroma/hue per color
- lightness range and standard deviation
- chroma range and average
- circular hue distance
- warm/cool balance
- strongest light/dark anchor candidates

### Interface safety

- pairwise WCAG contrast matrix
- strongest contrast ratio
- number of AA and AAA-capable pairs
- likely text/background roles
- decorative-only warning
- focus/interactive-state visibility warning

### Composition

- dominant color suitability
- surface suitability
- accent suitability
- recommended area ranges, not fixed 60/30/10
- whether the palette needs an external neutral for web use

## Historical-set observations used as priors, not laws

The 348-combination archive is dominated by small palettes and mid-toned relationships. Independent aggregate analysis reports 120 two-color, 120 three-color and 108 four-color combinations. It also shows many combinations do not contain a modern body-text-safe pair. Therefore the Color Director must not equate historical harmony with UI accessibility.

Use these observations only as priors. The analyzer must compute the actual selected palette before assignment.

## No textbook-harmony forcing

Do not force every Wada combination into "analogous", "complementary" or "triadic" labels. These labels may describe some palettes but they are too coarse for the whole archive. Prefer measured hue distances and explicit visual tension.

## Source vs web adaptation

A selected source combination goes through:

`source -> provenance -> screen conversion -> OKLCH analysis -> role assignment -> contrast gate -> area plan -> typography/media integration -> light/dark adaptation`

Never change the source record in-place. Create an adaptation record so the historical combination remains traceable.

## Accent scarcity

A 4-color Wada combination does not mean four equal UI accents. One or two colors may become small decorative/material accents while neutralized or external tones carry text and surfaces.

## Dark-mode rule

Do not invert Wada colors mechanically. Rebuild roles by lightness/chroma and verify contrast. Some mid-tone palettes need external neutral anchors to survive dark UI.

## Typography integration

Color and typography are co-dependent. High-contrast thin display type may require quieter backgrounds. Small body text needs stronger contrast than large editorial type. Never choose palette roles before knowing the text roles.
