# Divider Policy v5

Lines, hairlines, borders, hairline rules, section dividers, and technical grid overlays are the single most reliable AI fingerprint in the current library outputs. This document replaces the earlier `section_separation_recipes.json` view that treats dividers as an equal peer to whitespace.

## Prime rule

**A line is a last resort. Use it only when every other separation method has been considered and rejected with a reason.**

## Strict hierarchy of section separation

You must consider these in order. Do not skip a step because a lower one is easier to render.

| Priority | Method | Use when |
|:--:|:--|:--|
| 1 | **Whitespace** | The default. Almost always sufficient when the type scale has enough range. |
| 2 | **Compositional shift** | Column count, alignment axis, content mode, or focal-point changes between sections. |
| 3 | **Typography change** | Chapter marker, scale change, weight change, or role change signals a new mode. |
| 4 | **Surface / background contrast** | Two tonally distinct surfaces meet. A real edge, not a decorative one. |
| 5 | **Image / media transition** | Media crop, aspect change, or full-bleed image marks the boundary. |
| 6 | **Alignment or rhythm change** | The grid or vertical rhythm visibly shifts. |
| 7 | **Divider line** | Only after 1–6 have been rejected with a written reason. |

## When a divider is allowed

A divider line is permitted only if **all** of the following are true:

1. **Information boundary is real.** A meaningful semantic boundary exists — not a "this section ended" boundary.
2. **Whitespace has been tried and fails.** Increased spacing was tested and left the hierarchy ambiguous.
3. **The divider is part of the brand's editorial language.** It is a chosen device, not a fallback. Newspaper-style rules, tables of contents, index pages, and editorial navigation are legitimate uses.
4. **It appears rarely.** Two or more dividers in the same vertical flow is a fingerprint.
5. **It has authored weight and length.** Not a `border-top: 1px solid rgba(255,255,255,0.06)` reflex. Weight, color, and length are decisions.

If any of these fail, delete the line.

## Explicitly banned patterns

The following are hard blockers, not fingerprint scores:

### D-01 · Full-width horizontal rule between every section

A hairline stretching across the viewport at the top or bottom of every content block. Almost always used because the composition alone did not communicate the boundary. Delete every instance and rework the whitespace, type scale, or surface.

### D-02 · Global page grid overlay

A subtle background pattern of vertical and horizontal lines "for structure" or "for a technical feel." Grids are compositional decisions, not visual decorations. If you want a grid to be visible, it should be doing work — labeling columns, marking data axes, showing measurements. Otherwise remove it.

### D-03 · Hairline card borders on dark surfaces

`border: 1px solid rgba(255,255,255,0.06)` on every card. A tell of default-dark-UI thinking. Either the card needs a real containment reason (in which case a stronger boundary), or it does not (in which case no border).

### D-04 · Decorative technical lines around empty areas

Bracket marks, corner ticks, register marks, blueprint annotations, and framing lines applied for atmosphere. These read as film-UI clichés. Allowed only when the interface is genuinely about measurement, engineering, or reference — and even then, sparingly.

### D-05 · Repeated `border-bottom` on stacked list items

A hairline under every row of a list. Acceptable in dense tabular data. In editorial or marketing composition, use spacing or alternating surface instead.

### D-06 · Section eyebrow underline

A short horizontal line under every section eyebrow. A sub-fingerprint of the divider habit. Underlines belong to interactive text or links, not decorative labels.

## Justification requirement

If a divider is used, the design spec **must** include a `divider_justification` field with three keys:

```json
{
  "what_it_separates": "editorial chapter from index of related articles",
  "why_whitespace_alone_fails": "index items are dense; extra whitespace read as a gap, not a boundary",
  "comprehension_gain": "reader recognizes the mode change from prose to reference list"
}
```

Missing or vague justifications fail the V5 Authenticity Gate.

## Penalties

- More than one unnecessary divider in a vertical flow → **blocker**.
- Global grid overlay with no structural purpose → **blocker**.
- Hairline separators with no `divider_justification` field → **blocker**.
- Divider used where a heading change would already separate → **blocker** (indicates the type scale is too flat).

## What to do instead when reaching for a line

- Add 1.5× to 2× vertical space and remove any other decoration.
- Introduce a subtle surface value shift (2–4% lightness difference).
- Change alignment axis for the next section (centered → left, or single-column → asymmetric split).
- Introduce a scale or weight shift in the section heading.
- Let the next section's media provide the edge.

## The final test

Turn off every divider in the design. Does section structure survive? If yes, you did not need them. If no, the composition is doing too little and the divider was covering for it. Fix the composition.
