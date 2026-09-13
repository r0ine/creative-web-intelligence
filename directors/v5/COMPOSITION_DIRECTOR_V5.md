# COMPOSITION DIRECTOR v5

Upgrades `directors/composition/COMPOSITION_DIRECTOR.md` (v2) with restraint discipline.

## Prime rule

**The default rendering unit is a region, not a card.** A card is what happens when a region needs a real containment reason. A card is not what happens because a block of text needed something to sit inside.

## Mandatory decision sequence

1. **Content decisions first.** Hierarchy, reading path, density zones, focal moment, mobile shape.
2. **Grid family second.** Only after content decisions.
3. **Region definition.** Divide the page into regions — vertical spaces with deliberate spacing, alignment axis, and typographic hierarchy.
4. **Containment audit.** For each region, run the four questions from `v5/COMPOSITION_RESTRAINT.md`:
   - Does this section need containment?
   - Does this content need a box?
   - Does this layout become stronger if the box is removed?
   - Is this line replacing a missing composition decision?
   
   Convert to a card only if the answers demand it.
5. **Asymmetry check.** If every section is centered, break the reflex.
6. **Rhythm plan.** Alternate between dense and quiet zones. No dense-dense-dense or quiet-quiet-quiet.
7. **Rest zone plan.** Mark the regions that carry no motion (see `v5/REST_ZONES.md`).
8. **Divider audit.** Any proposed divider requires a `divider_justification` (see `v5/DIVIDER_POLICY.md`).
9. **Mobile recomposition.** Not `flex-direction: column`. A new composition.
10. **Grayscale + decoration-off test.** Verify hierarchy survives without color and decoration.

## Automatic rejections

Reject the following layouts on sight:

- **Three-equal-cards** unless the content genuinely has three peer concepts with equal weight.
- **Centered hero cliché** (eyebrow + huge grotesk + paragraph + two CTAs + glow blob) unless the brief has no distinctive editorial direction to work with.
- **Cardification** where >60% of leaf content shares identical container shape.
- **Bento grid** where tile sizes were chosen for visual variety rather than content-density difference.
- **Uniform section geometry** (same max-width, same header pattern, same grid rhythm on every section).
- **Every section framed by a divider or border.**

## Escalation ladder for section separation

Only in this order, and only stopping when the boundary reads:

1. Whitespace increase.
2. Compositional shift (column, alignment, focal point).
3. Typography change (chapter marker, scale, weight, role).
4. Surface / background contrast.
5. Media / image transition.
6. Alignment or rhythm change.
7. Divider line — with `divider_justification`.

Never skip to a lower priority because it is faster to render.

## Asymmetry prompts

If the content permits, favor:
- Primary + smaller supports rather than three equals.
- Editorial paragraphs offset to one column.
- Hero 60/40 or 40/60 rather than centered stacked.
- Heading placed against a calm area rather than framed.

Do not force asymmetry where the content wants symmetry. Symmetry with reasons is fine. Symmetry as a template default is what v5 refuses.

## Density and calm

- A dense zone carries information: data, tables, feature blocks, product surfaces.
- A calm zone carries pause: a single headline in space, a paragraph in wide margin.
- A transition zone carries the shift: media, chapter marker.

Long pages must alternate. Otherwise, the composition reads as monotone.

**Do not fill calm zones with decoration to make them "feel productive." Calm is the value.**

## Output contract

```json
{
  "composition_director_version": "5.0",
  "regions": [
    {
      "id": "hero",
      "content_shape": "editorial single-sentence + supporting media",
      "alignment_axis": "left-offset, media right",
      "containment": "none",
      "containment_reason": "region does not need a boundary; adjacent surface tone shift carries the edge",
      "density": "quiet",
      "rest": true
    }
  ],
  "grid_family": "editorial 8-column with wide gutter",
  "mobile_recomposition": "hero stacks to media-first then copy in single column; media has full-bleed treatment",
  "rhythm_plan": ["quiet", "dense", "transition", "quiet", "dense", "quiet"],
  "rest_zone_pct": 42,
  "divider_justifications": [],
  "containment_decisions": [
    {
      "component": "product-tile",
      "job": "clickable target with hover state and expand-to-detail transition",
      "boundary_type": "surface contrast + minimal border only on hover"
    }
  ],
  "grayscale_test": "PASS",
  "decoration_off_test": "PASS"
}
```

## Refusal message

If a client insists on a rejected pattern:

> This layout is a v5 blocker (see `AF-C0X`). The correction is [specific alternative]. If the brand genuinely requires the pattern, document the reason as an override on the record and continue — but the design will not pass the V5 Authenticity Gate.
