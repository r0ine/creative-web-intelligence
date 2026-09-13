# Before / After — a landing page under v5

A worked example of what the v5 doctrine changes about the same brief.

## The brief

Homepage for a small SaaS analytics product. Target audience: engineering leads. Brand voice: precise, calm, no-hype.

## What v4 tended to produce

Reconstructed from the fingerprint patterns present in the library's own examples.

- Hero: centered eyebrow "ANALYTICS FOR ENGINEERS", giant grotesk headline "See What's Really Happening", one-line paragraph, "Get Started" + "Book a Demo" buttons, purple-blue radial gradient behind.
- Below hero: three equal cards. "Real-time", "Actionable", "Secure". Each with an icon, one heading, one line.
- Section divider: hairline at rgba(255,255,255,0.08) between every section.
- Background: `#0A0A0B` with a subtle grid overlay at 4% opacity.
- Bento grid mid-page with 4 tiles of varying size showing fake dashboard screenshots.
- Every section reveals with `opacity 0 → 1; translateY(30px) → 0` at scroll.
- Every card has `border: 1px solid rgba(255,255,255,0.06)` and `border-radius: 12px`.
- Every card lifts `-4px` on hover with a shadow bloom.
- Section eyebrows: all-caps small labels, wide tracking, present on every section.
- Body font: Inter. Headings: Inter. Hero H1: Inter with `background-clip: text` gradient fill.

### Authenticity check on the v4-style build

```
[AF-A01] blocker   universal section dividers (hairlines between all sections)
[AF-A02] blocker   background grid overlay
[AF-B01] blocker   universal fade-up entrance across sections
[AF-B04] blocker   every section entering with the same grammar
[AF-C01] high      centered hero cliché + radial glow
[AF-C02] blocker   >60% of content cardified
[AF-C03] high      three-equal-cards feature grid
[AF-D01] high      dark surface + hairlines + accent glow default
[AF-D02] high      unmotivated blue-purple gradient
[AF-D03] high      gradient text on H1
[AF-E01] medium    oversized centered grotesk H1
[AF-E03] medium    all-caps eyebrow on every section
[AF-E04] high      scale-only hierarchy (Inter one weight, only size varies)
[AF-F01] medium    universal hover-lift + shadow
[AF-F04] high      fake dashboard screenshots
```

Gate: **FAIL**. Six blockers, seven high, three medium. Cannot ship under v5.

---

## What v5 does with the same brief

### Design DNA (rederived under v5)

- **Voice**: precise, calm, no-hype. Words are the interface. The product is engineering evidence.
- **Signature idea**: the page reads like a well-designed technical memo. One dense information-first opening, then an editorial rhythm.
- **Typography**: one variable grotesk (`Söhne` or `GT America Mono` paired with `GT America`) for headline + body. Real weight range used: 300 for body, 400 for editorial captions, 620 for headlines, 380 for large calm display. Numeric data uses tabular figures.
- **Color**: warm off-white surface (`#F5F1EA`), one deeper anchor (`#1A1A1A` for chapter contrast), one small chroma point (`#B85431` used only in status numerals and one link state). No accent glow. No gradient.
- **Composition**: editorial 8-column grid on desktop, single column with wide margin on mobile. Content decides symmetry per section.
- **Motion grammar**: dominant is `static-rest`. One supporting grammar is `media-crop` for a single product screenshot mid-page. That is it. No reveals.

### Hero

**Not** centered eyebrow + huge headline + two CTAs + glow.

Instead: a single sentence at editorial scale, offset to the left column of the 8-column grid, wrapping to three lines the designer chose. Below it, one line of body copy at real reading measure. One call to action, not two. The right two columns hold a small block of live product data — a real number, not a fake dashboard.

No gradient. No glow. No underline on the eyebrow (there is no eyebrow).

### Section 2 — What we do

Not a three-card grid. A two-column editorial layout: the left column is a 60-character paragraph explaining what the product measures; the right column is a small annotated diagram of the data flow. The diagram is not decorative — it labels three named parts of the product. A single, real, structural information graphic.

### Section 3 — Product surface

A real screenshot of the real product, cropped tight. Above it, one caption in editorial voice. This is the only place motion appears: as the media enters the viewport, its crop opens from a tight framing to full width. That is the entire motion budget for the page.

### Section 4 — Editorial rest zone

A long paragraph in a comfortable measure. Real writing. This is the primary rest zone. No animation, no borders, no cards. Just typography and space.

### Section 5 — Pricing

Three tiers, but not as three equal cards. As a table with type hierarchy. The primary tier is emphasized by weight and a subtle background tint, not by a lifted card. Table rows use spacing, not hairlines.

### Section 6 — Contact

Left column: three lines of address / support hours / email. Right column: the same single CTA from the hero, matched. No fake testimonials. No press logos.

### Divider audit

Zero dividers on the page. Section boundaries carry themselves through:
- Whitespace (default separator).
- Alignment axis shift between sections 1, 2, and 3.
- Surface tint shift between the editorial rest zone (section 4) and the surrounding sections.
- Media edge at section 3.
- Typography change (weight and role) between the editorial rest zone and the pricing table.

The `divider_justifications` array in the spec is empty.

### Motion audit

- Dominant grammar: `static-rest`.
- Supporting: `media-crop` (used once).
- Rest zones: sections 1, 2, 4, 5, 6 — 5 of 6 sections. Rest coverage ≈ 75%.
- Easing tokens: three distinct — `--ease-ui`, `--ease-editorial`, `--ease-object`. Only `--ease-editorial` is currently used (for the single crop reveal).
- Reduced-motion variant: crop reveal replaced with static crop; no travel.

### Authenticity check on the v5 build

```
[AF-A03] not present — no hairline card borders
[AF-B01] not present — no fade-up
[AF-B02] not present — no stagger
[AF-C01] not present — hero is left-offset, single CTA, no glow
[AF-C02] not present — cards limited to pricing tier emphasis; content is regions elsewhere
[AF-C03] not present — no three-equal-cards
[AF-D01] not present — warm off-white surface, no accent glow
[AF-D02] not present — no gradient
[AF-D03] not present — no gradient text
[AF-E01] not present — headline is left-offset, chosen weight/size combination
[AF-E03] not present — no all-caps eyebrows
[AF-F01] not present — no hover-lift on non-interactive elements
[AF-F04] not present — real product screenshot, real data
```

Summary tests:
- Decoration off: PASS — hierarchy is carried by type, spacing, and alignment.
- Motion off: PASS — only one motion device on the page.
- Identity: PASS — the page is recognizably calm-technical, not generic SaaS.

Gate: **PASS**.

---

## What the comparison reveals

The v5 page is **less** decorated than the v4 page. It has fewer effects, fewer devices, fewer moments of visual noise. And it reads as more considered — because every element on it is doing work.

That is the whole point of the refactor. **Restraint is the premium.**

The v4 page could be any startup. The v5 page is a specific product for a specific reader. The difference did not come from adding art direction. It came from removing the substitutes for art direction.

## Notes on the process

- The v5 pass took *less* time to specify than the v4 pass would have. Fewer decisions were needed because most decisions were "delete."
- The composition director spent nearly all its work on the four questions of `COMPOSITION_RESTRAINT.md`, not on grid families.
- The motion director's output was three sentences: "dominant is static, supporting is one media-crop, three easing tokens defined by role."
- The typography director spent most of its output on real measure, real line-height, real weight range — not on picking a font.
- The authenticity director rejected two rounds of drafts before the composition director stopped reaching for containment.

This is the intended shape of v5 work: harder decisions, fewer devices, a shorter spec, a more legible result.
