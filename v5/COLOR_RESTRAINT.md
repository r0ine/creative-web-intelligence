# Color Restraint v5

The library's color intelligence in v3.2 taught relationship-based color thinking — that part is intact. What v5 adds is a **restraint layer** targeting the specific dark-UI cliché that has been recurring in outputs.

## The pattern being corrected

Near-black background. Faint hairline borders in white at 6–10% alpha. One saturated brand-color glow behind the hero. Body text in a mid-gray. Repeated across sections.

This is not a color decision. It is a color *default*. It signals that no one chose the surface, only that the surface should be dark.

## The rule

Color decisions must be traceable to:

- **Brand** — a defined identity system, with reasons for its choices.
- **Material or subject** — the product's actual material, the image content, the photograph's tonal range.
- **A named source strategy** — Wada-derived, image-derived, editorial reference, deliberate neutral system.
- **A calm intention** — a chosen quiet palette because the content deserves quiet.

Not traceable to:
- "Dark UI looks premium."
- "Purple-blue looks like AI."
- "Black-and-gold looks luxury."
- "One accent glow adds finish."

## Anti-cliché blockers

### CR-01 · Default dark + hairlines + accent glow

**Signal:** background near `#0A0A0B`, strokes at rgba(255,255,255, < 0.15), single radial gradient in a saturated hue behind the primary content.

**Correction.** Pick a real surface. If dark, commit to it with imagery, materials, or texture, not with hairlines. Kill the accent glow — put the color scarcity somewhere else on the page in one point of restraint.

### CR-02 · Blue-purple gradient identity

**Signal:** primary brand gradient in the 210°–290° hue range with high chroma.

**Correction.** Color must come from brand or material. If the product genuinely needs one signal color, pick a single flat color with a reason.

### CR-03 · Gradient text as identity

**Signal:** `background-clip: text` on H1 or hero headline.

**Correction.** Fix the typography first. If a single-color headline does not carry identity, the type system is wrong.

### CR-04 · Multiple accents competing

**Signal:** three or more high-chroma colors used at similar area weight, each on a CTA or highlight.

**Correction.** Accent scarcity is a color decision. One color is scarce. Two is a system. Three is noise.

## Calm surfaces as a positive strategy

The alternative to the default-dark cliché is not "make it lighter." It is:

- **Calm off-neutrals** — warm off-whites, cool paper tones, muted blue-grays. Surfaces that feel considered rather than defaulted.
- **Real material color** — cameras, paper, metal, fabric, wood if the product touches those materials.
- **Two-surface systems** — a primary calm surface with a single deeper anchor for chapters that need weight.
- **One point of scarcity** — a single small chroma point (a numeral, a caption color, a link state) rather than a dominant accent.

## Temperature discipline

Warm and cool are compositional choices. Randomly mixing them reads as unedited. Choose:

- **Predominantly warm** — off-whites with amber-beige-terracotta anchors.
- **Predominantly cool** — off-whites with slate-glass-steel anchors.
- **Cool-warm tension** — a chosen tension, e.g., cool surface with one warm anchor. Stated on purpose.

Never: three cool colors, two warm colors, one green because "green means growth." That is not a temperature decision.

## The one-accent test

How many colors on the page are competing for the user's attention?

- **Zero accents** — the design is calm. Legitimate.
- **One accent** — scarce, meaningful. Legitimate.
- **Two accents in separate roles** — e.g., a primary CTA color and an error/warning color. Legitimate.
- **Three or more accents** — the palette is not disciplined. Rebuild.

## The dark-UI license

You may build a dark UI when:

- The product is genuinely used in a dark context (media viewing, coding at night, cinematography).
- The imagery being displayed benefits from a dark surround.
- The brand identity is genuinely dark with reasons for it.

You may not build a dark UI because:

- "Dark looks premium."
- "It hides missing composition better."
- The system defaulted to dark and no one questioned it.

## Contrast is not optional

Whatever the palette chooses, body text must meet WCAG contrast on every surface it appears on. Beautiful low-contrast palettes are decorative until they are readable. This is unchanged from v3.2 and reinforced here.

## The final color test

Turn the page grayscale. Is the hierarchy still legible? Is one moment still the moment? Does the composition still communicate?

If yes, the color is doing supporting work honestly.
If no, the color was carrying compositional load — put the load back on composition and typography and re-derive the color.
