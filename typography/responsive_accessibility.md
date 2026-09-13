# Typography — Responsive & Accessibility

Entries: **6**

## TYP-007 — Fluid type needs accessible bounds

Use clamp/min/max strategies that preserve zoom/user font preferences rather than pure viewport units.

**Why:** Fluid type should respond to viewport without overriding user control.

**Tags:** responsive, accessibility

## TYP-013 — Respect script/language coverage

Verify required glyphs, Turkish characters and punctuation before choosing a display font.

**Why:** Missing glyphs or fallback mixing destroys visual consistency.

**Tags:** localization

## TYP-025 — Body contrast must pass accessibility

Keep paragraph and control text at sufficient contrast against its background.

**Why:** Readability is a non-negotiable quality gate.

**Tags:** accessibility

## TYP-026 — Build responsive line breaks

Do not hardcode desktop <br> line breaks that become awkward on mobile; use responsive variants or natural wrapping.

**Why:** Editorial line breaks are viewport-specific.

**Tags:** responsive

## TYP-030 — Do not scramble critical copy

Scramble/glitch effects belong to short decorative moments, not essential instructions.

**Why:** Legibility must win over spectacle.

**Tags:** motion, accessibility

## TYP-032 — Support reduced motion in kinetic type

Provide static or simpler reveals when reduced motion is requested.

**Why:** Text remains content even when animation is removed.

**Tags:** accessibility, motion
