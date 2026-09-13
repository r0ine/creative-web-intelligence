# Typography — Kinetic Type

Entries: **5**

## TYP-028 — Animate text by semantic unit

Choose character, word, line or block animation based on reading intent.

**Why:** Animating every character independently can reduce comprehension.

**Tags:** motion

## TYP-029 — Split-text must be reversible

Any split-text implementation should restore on resize/unmount and preserve accessibility.

**Why:** Responsive text reflow can invalidate line wrappers.

**Tags:** motion, engineering

## TYP-030 — Do not scramble critical copy

Scramble/glitch effects belong to short decorative moments, not essential instructions.

**Why:** Legibility must win over spectacle.

**Tags:** motion, accessibility

## TYP-032 — Support reduced motion in kinetic type

Provide static or simpler reveals when reduced motion is requested.

**Why:** Text remains content even when animation is removed.

**Tags:** accessibility, motion

## TYP-045 — Store text-motion compatibility

Each text effect should declare which type sizes and content lengths it supports.

**Why:** Effects that work on a one-line hero may break a paragraph.

**Tags:** library, motion
