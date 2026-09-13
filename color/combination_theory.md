# Color Combination Theory — Teaching Module

This module teaches an agent **how to choose and explain color combinations**, not merely how to output attractive hex values.

## 1. Start from a job, not a color wheel
Before choosing colors, classify the page:

- **content density:** sparse / editorial / application-dense
- **mood:** calm / energetic / premium / playful / technical / organic / dramatic
- **mode:** light / dark / adaptive
- **visual driver:** typography / photography / illustration / 3D / data
- **brand constraint:** existing brand hue / no fixed hue / product-derived palette
- **interaction risk:** many states / simple marketing page

Then select a palette strategy.

## 2. The five practical harmony families

### Monochromatic
One hue family, varied mainly by lightness/chroma.

**Use when:** premium, editorial, product-focused, dense UI, strong imagery or 3D already carries visual complexity.

**Strength:** coherence and restraint.

**Risk:** hierarchy can collapse if lightness differences are too small.

### Analogous
Neighboring hues on the color wheel.

**Use when:** organic, atmospheric, editorial, fashion, environmental, soft storytelling.

**Strength:** naturally cohesive.

**Risk:** all colors may compete at the same saturation; establish one dominant hue.

### Complementary
Opposing hue families.

**Use when:** a strong focal action needs to pop against a dominant world.

**Strength:** high visual separation.

**Risk:** can become childish or sports-like when both sides are equally saturated. Usually mute one side.

### Split-complementary
A base hue plus two colors near its opposite.

**Use when:** you want more range than a simple complementary pair without the chaos of a triad.

**Strength:** flexible hierarchy.

**Risk:** too many accents. Keep one primary accent and let the others support illustration/data.

### Triadic
Three roughly spaced hue families.

**Use when:** playful systems, illustration-heavy brands, educational products, expressive identities.

**Strength:** variety.

**Risk:** easiest harmony to misuse in UI. Do not give all three equal area and saturation.

## 3. Harmony is not enough
A mathematically harmonious palette can still be bad UI.

Every palette must additionally define:

1. **background**
2. **surface**
3. **primary text**
4. **secondary/muted text**
5. **primary accent**
6. **optional secondary accent**
7. **border/divider**
8. **focus**
9. **success/warning/danger/info**, when applicable

This role-based model follows the same practical idea used by modern design systems: colors should be assigned according to what they do, not only how they look.

## 4. Area is as important as hue
Never evaluate a palette as five equal swatches only.

A useful starting distribution for a marketing page is roughly:

- 70–90% neutral/background family
- 8–25% surfaces/supporting tones
- 2–10% accent

This is **not a law**. It is a composition check. If a strong accent covers 50% of the viewport, it stops being an accent.

## 5. Saturation is hierarchy
Reserve the highest chroma for one of:

- primary CTA
- focused 3D detail
- active navigation
- key data state
- brand signature moment

Muted content should generally be lower chroma, not merely lower opacity.

## 6. Lightness is the fastest hierarchy tool
When combinations feel noisy, first reduce the number of competing lightness levels.

In dark mode, build layers such as:

- background: very dark
- surface-1: slightly lighter
- surface-2: another small step lighter
- border: visible but quiet
- text: high enough contrast

Do not use glow as a substitute for surface hierarchy.

## 7. Warm vs cool neutrals
Neutral does not mean hue-less.

- warm black/cream can support craft, editorial, food, hospitality, analog, luxury
- cool graphite/off-white can support technical, architecture, spatial, industrial
- green-tinted charcoal can support organic or environmental themes
- red/brown-tinted charcoal can feel cinematic or material-driven

Tint neutrals subtly. If the tint is obvious before the content is noticed, it may be too strong.

## 8. Brand hue does not need to be the background
A bright brand color can work better as:

- accent
- focus ring
- small navigation marker
- highlighted word
- selected product material
- lighting accent in a 3D scene

rather than filling the entire page.

## 9. A practical combination workflow

1. Choose dominant neutral family.
2. Choose primary text pair and validate contrast.
3. Choose one accent from brand/content intent.
4. Decide harmony family for any secondary color.
5. Lower chroma on supporting colors.
6. Assign semantic roles.
7. Test real component states, not swatches only.
8. Test light/dark if both exist.
9. Test 3D/photography integration if present.
10. Run accessibility checks.
11. Remove any color that has no job.

## 10. Combination explanation format
When an AI proposes a palette, it should explain it like this:

- **Base:** why this background family fits the mood
- **Primary text:** why its temperature and contrast fit
- **Accent:** why this hue is selected and where it should appear
- **Secondary:** harmony relationship and why it remains subordinate
- **Area strategy:** which color dominates and which stays scarce
- **States:** success/warning/danger separation if relevant
- **3D note:** how lighting/materials should interact with the DOM palette
- **Accessibility:** which pairs are validated and which are decorative-only

A palette without this explanation is incomplete for this library.
