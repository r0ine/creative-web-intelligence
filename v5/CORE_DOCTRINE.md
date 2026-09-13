# Creative Web Intelligence v5 — Core Doctrine

## What v5 exists to fix

Earlier versions of this library correctly *listed* the anti-AI patterns but treated them as soft advice. In practice, the outputs kept converging on the same "generated" feel:

- horizontal divider lines slicing every section
- background grid overlays for atmosphere
- bordered cards for every content block
- `opacity 0 → 1; translateY(20-40px) → 0` as the universal entrance
- centered eyebrow + huge grotesk + two-CTA hero
- black surface + faint gray hairlines + one accent glow

None of this is design. It is decoration substituting for decisions.

v5 does not add new effects. It removes permission to reach for them.

## The single question v5 forces at every step

> If the decoration were deleted, would this composition still communicate?

If the answer is no, the composition is broken and no amount of surface polish will save it. Fix the composition. Do not add another line, gradient, glass panel, or reveal animation.

## Five doctrinal shifts from v4

### 1. Decoration is guilty until proven functional

Every line, border, divider, glow, gradient, glass panel, and background pattern must justify its existence in one sentence: **what does it separate, contain, emphasize, or explain?** If the answer is "it makes the section feel finished," delete it.

See `DECORATION_VS_STRUCTURE.md`.

### 2. Section separation has a strict hierarchy — dividers are last

The old `section_separation_recipes.json` lists seven methods as peers. That is wrong. They are not peers. Whitespace, compositional shift, and typography changes are primary separators. A hairline rule is a last resort that must earn its use.

See `DIVIDER_POLICY.md`.

### 3. Motion grammar has hard blockers, not soft penalties

`opacity + translateY` applied to more than one section per page is now a **blocker**, not a fingerprint score of 2. Same for stagger ladders, identical easing across roles, and blur-in. Motion earns its presence per element, not per system.

See `MOTION_GRAMMAR_V2.md`.

### 4. Composition may not default to containment

The default rendering unit is a *region*, not a *card*. A card is what happens when a region needs a functional boundary — an action target, a selection unit, a swappable item, a media container. A card is not what happens because a block of text needed something to sit inside.

See `COMPOSITION_RESTRAINT.md`.

### 5. Typography carries the load

If turning off all borders, gradients, glows, and reveals collapses the hierarchy, the typography system is too weak and no decorative repair will fix it. Typography carries premium. Everything else supports.

See `TYPOGRAPHY_FIRST_PREMIUM.md`.

## What v5 keeps from v4

Everything else. Color intelligence, source-aware asset selection, 3D art direction, scroll director, license/provenance gates, backend intelligence — all intact. v5 only changes how visual decisions are gated.

## Where v5 puts its teeth

Two places:

1. `quality/V5_AUTHENTICITY_GATE.md` — a **blocker gate**, not a score. Any single blocker fails the build. No averaging.
2. `tools/v5/authenticity_check.py` — a static analyzer that reads HTML/CSS and reports the fingerprints it finds. Not a linter — a witness.

## What v5 refuses to do

- Add a "make it feel human" mode with intentional imperfections. That was already banned as `ANT-026` and it is still banned.
- Chase every new visual trend with a matching recipe. The library gets stricter, not larger.
- Publish a scoring rubric that lets weak designs pass by averaging small wins.

## The one-sentence version

**Design quality comes from decisions about hierarchy, typography, composition, and restraint. Decoration is what happens when those decisions were skipped.**
