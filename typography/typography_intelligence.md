# Typography Intelligence

Total rules: **45**

These are reusable design/engineering rules synthesized from verified standards, indexed creator material, current award galleries, studios, and creative-development sources. They are not laws; project context wins.

## TYP-001 — Separate display and reading roles

**Rule:** Treat display type and body/UI type as separate jobs unless one family demonstrably handles both.

**Why:** Expressive headings and long-form readability have different constraints.

**Tags:** pairing, hierarchy  
**Confidence:** `SYNTHESIZED`

## TYP-002 — Contrast pairings by role

**Rule:** When pairing fonts, create meaningful contrast in voice, proportions or texture instead of selecting two nearly identical sans serifs.

**Why:** A strong role contrast makes the hierarchy legible and avoids accidental-looking pairings.

**Tags:** pairing  
**Confidence:** `SYNTHESIZED`

## TYP-003 — Limit active families

**Rule:** Default to one or two families; add a third only when it represents a distinct content role.

**Why:** Too many families weaken visual coherence and increase loading cost.

**Tags:** system, performance  
**Confidence:** `SYNTHESIZED`

## TYP-004 — Use variable fonts deliberately

**Rule:** Prefer variable fonts when a project genuinely uses multiple weights/widths/axes.

**Why:** They can reduce the cost of loading many separate font files and allow finer art direction.

**Tags:** variable-font, performance  
**Confidence:** `VERIFIED+SYNTHESIZED`

## TYP-005 — Do not use display fonts for dense copy

**Rule:** Keep highly stylized faces away from long paragraphs, dense tables and controls.

**Why:** Distinctive letterforms can reduce reading speed and UI clarity.

**Tags:** readability  
**Confidence:** `SYNTHESIZED`

## TYP-006 — Define a type scale

**Rule:** Create named tokens for display, h1-h6, body, small, label and caption instead of ad-hoc sizes.

**Why:** A type scale gives hierarchy consistency across pages and responsive states.

**Tags:** tokens, hierarchy  
**Confidence:** `SYNTHESIZED`

## TYP-007 — Fluid type needs accessible bounds

**Rule:** Use clamp/min/max strategies that preserve zoom/user font preferences rather than pure viewport units.

**Why:** Fluid type should respond to viewport without overriding user control.

**Tags:** responsive, accessibility  
**Confidence:** `VERIFIED+SYNTHESIZED`

## TYP-008 — Control measure

**Rule:** Set comfortable line lengths for body copy rather than letting paragraphs span arbitrary wide containers.

**Why:** Line length is a composition variable, not an afterthought.

**Tags:** readability, layout  
**Confidence:** `SYNTHESIZED`

## TYP-009 — Tune line-height by role

**Rule:** Display headings can be tight; paragraph text and UI labels need different line-height systems.

**Why:** One global line-height produces weak rhythm.

**Tags:** rhythm  
**Confidence:** `SYNTHESIZED`

## TYP-010 — Tune tracking by size

**Rule:** Large display type often tolerates tighter tracking; all-caps labels usually need more tracking.

**Why:** Optical spacing changes with size and casing.

**Tags:** tracking  
**Confidence:** `SYNTHESIZED`

## TYP-011 — Avoid fake font weights

**Rule:** Do not rely on browser-synthesized bold/italic when real faces/axes exist.

**Why:** Synthetic styles can distort intended design.

**Tags:** quality  
**Confidence:** `SYNTHESIZED`

## TYP-012 — Use optical size where available

**Rule:** If a variable font has opsz, test it for text and display roles rather than freezing one setting.

**Why:** Optical-size axes can improve shapes for different point sizes.

**Tags:** variable-font  
**Confidence:** `SYNTHESIZED`

## TYP-013 — Respect script/language coverage

**Rule:** Verify required glyphs, Turkish characters and punctuation before choosing a display font.

**Why:** Missing glyphs or fallback mixing destroys visual consistency.

**Tags:** localization  
**Confidence:** `SYNTHESIZED`

## TYP-014 — Fallback metrics matter

**Rule:** Define compatible fallbacks and consider size-adjust/metric overrides for large web fonts.

**Why:** Reducing metric mismatch can reduce layout shift.

**Tags:** performance, CLS  
**Confidence:** `VERIFIED+SYNTHESIZED`

## TYP-015 — Preload only critical fonts

**Rule:** Preload only font files needed above the fold; avoid preloading every weight.

**Why:** Over-preloading competes with more important resources.

**Tags:** performance  
**Confidence:** `VERIFIED+SYNTHESIZED`

## TYP-016 — Create font-loading states

**Rule:** Ensure layout remains usable before custom fonts load.

**Why:** The experience should not depend on a blank-font phase.

**Tags:** performance, resilience  
**Confidence:** `SYNTHESIZED`

## TYP-017 — Numbers are a distinct typographic role

**Rule:** Check tabular/proportional numerals for dashboards, prices and counters.

**Why:** Numeric content can require alignment behavior different from prose.

**Tags:** data-ui  
**Confidence:** `SYNTHESIZED`

## TYP-018 — Use hierarchy before decoration

**Rule:** Use size, weight, spacing and contrast before adding gradients, outlines or glow to text.

**Why:** Decoration cannot repair weak hierarchy.

**Tags:** anti-slop  
**Confidence:** `SYNTHESIZED`

## TYP-019 — Avoid center-aligning long copy

**Rule:** Reserve centered alignment for short statements or intentional compositions.

**Why:** Long centered text is harder to scan and often signals generic landing-page layout.

**Tags:** readability, anti-slop  
**Confidence:** `SYNTHESIZED`

## TYP-020 — Create editorial contrast

**Rule:** Combine scale changes, width changes, italics, serif/sans contrast or density shifts intentionally.

**Why:** Editorial rhythm can make pages distinctive without extra cards/effects.

**Tags:** art-direction  
**Confidence:** `SYNTHESIZED`

## TYP-021 — Use text width as composition

**Rule:** A heading can be narrow, wide, stacked or offset; do not force every headline into the same max-width.

**Why:** Text block shape is part of visual composition.

**Tags:** composition  
**Confidence:** `SYNTHESIZED`

## TYP-022 — Define casing rules

**Rule:** Specify where uppercase, title case and sentence case belong.

**Why:** Random casing makes interfaces feel assembled rather than art-directed.

**Tags:** system  
**Confidence:** `SYNTHESIZED`

## TYP-023 — Define punctuation style

**Rule:** Decide how dashes, quotes, slashes and numbered labels appear in art-directed layouts.

**Why:** Micro-typography adds consistency.

**Tags:** microtype  
**Confidence:** `SYNTHESIZED`

## TYP-024 — Use display fonts sparingly

**Rule:** A distinctive typeface is more memorable when concentrated in high-value moments.

**Why:** Overuse turns character into noise.

**Tags:** art-direction  
**Confidence:** `SYNTHESIZED`

## TYP-025 — Body contrast must pass accessibility

**Rule:** Keep paragraph and control text at sufficient contrast against its background.

**Why:** Readability is a non-negotiable quality gate.

**Tags:** accessibility  
**Confidence:** `VERIFIED`

## TYP-026 — Build responsive line breaks

**Rule:** Do not hardcode desktop <br> line breaks that become awkward on mobile; use responsive variants or natural wrapping.

**Why:** Editorial line breaks are viewport-specific.

**Tags:** responsive  
**Confidence:** `SYNTHESIZED`

## TYP-027 — Keep labels compact

**Rule:** Navigation, chips and controls should use concise language and stable metrics.

**Why:** UI typography should optimize recognition, not display drama.

**Tags:** ui  
**Confidence:** `SYNTHESIZED`

## TYP-028 — Animate text by semantic unit

**Rule:** Choose character, word, line or block animation based on reading intent.

**Why:** Animating every character independently can reduce comprehension.

**Tags:** motion  
**Confidence:** `SYNTHESIZED`

## TYP-029 — Split-text must be reversible

**Rule:** Any split-text implementation should restore on resize/unmount and preserve accessibility.

**Why:** Responsive text reflow can invalidate line wrappers.

**Tags:** motion, engineering  
**Confidence:** `SYNTHESIZED`

## TYP-030 — Do not scramble critical copy

**Rule:** Scramble/glitch effects belong to short decorative moments, not essential instructions.

**Why:** Legibility must win over spectacle.

**Tags:** motion, accessibility  
**Confidence:** `SYNTHESIZED`

## TYP-031 — Use hierarchy tokens in 3D scenes

**Rule:** DOM annotations, 3D labels and normal page text should share a coherent type system.

**Why:** 3D overlays should not look like a separate product.

**Tags:** 3d, system  
**Confidence:** `SYNTHESIZED`

## TYP-032 — Support reduced motion in kinetic type

**Rule:** Provide static or simpler reveals when reduced motion is requested.

**Why:** Text remains content even when animation is removed.

**Tags:** accessibility, motion  
**Confidence:** `SYNTHESIZED`

## TYP-033 — Avoid default Inter-everywhere behavior

**Rule:** System/Inter-like sans can be valid, but require a reason and supporting art direction.

**Why:** The problem is defaulting, not the font itself.

**Tags:** anti-slop  
**Confidence:** `SYNTHESIZED`

## TYP-034 — Use content to choose font mood

**Rule:** Map font characteristics to brand voice: technical, editorial, playful, institutional, luxurious, raw, etc.

**Why:** Type choice should be project-specific.

**Tags:** branding  
**Confidence:** `SYNTHESIZED`

## TYP-035 — Pair width with layout density

**Rule:** Condensed display faces can support narrow columns; wide faces need room.

**Why:** Typeface proportions influence grid decisions.

**Tags:** layout  
**Confidence:** `SYNTHESIZED`

## TYP-036 — Test real content extremes

**Rule:** Test long names, Turkish diacritics, 4-digit numbers, error messages and multiline buttons.

**Why:** Type systems should survive production content.

**Tags:** testing  
**Confidence:** `SYNTHESIZED`

## TYP-037 — Do not rely on font alone for hierarchy

**Rule:** Combine spacing, grouping and color with typography.

**Why:** Hierarchy is multimodal.

**Tags:** hierarchy  
**Confidence:** `SYNTHESIZED`

## TYP-038 — Use italic as a role, not decoration

**Rule:** Define whether italic means emphasis, voice, quote or editorial contrast.

**Why:** Consistent semantics strengthen design.

**Tags:** system  
**Confidence:** `SYNTHESIZED`

## TYP-039 — Create font licenses/availability metadata

**Rule:** Every font recipe should record license/source/hosting constraints.

**Why:** A library cannot recommend fonts that cannot legally or practically ship.

**Tags:** library, metadata  
**Confidence:** `SYNTHESIZED`

## TYP-040 — Track performance cost

**Rule:** Font catalog entries should include file count, variable/static mode and estimated loading impact.

**Why:** Premium typography should not quietly destroy performance.

**Tags:** library, performance  
**Confidence:** `SYNTHESIZED`

## TYP-041 — Catalog pairing archetypes

**Rule:** Store pairings as archetypes (neutral+expressive, grotesk+serif, mono+humanist, etc.), not only font names.

**Why:** Archetypes transfer to new projects even when fonts change.

**Tags:** library, pairing  
**Confidence:** `SYNTHESIZED`

## TYP-042 — Near-black text can create softer dark themes

**Rule:** Tinted near-black can reduce the harshness of pure black when the art direction calls for it.

**Why:** Shinobi indexed posts repeatedly showcase near-black alternatives; treat this as an option, not a universal rule.

**Tags:** color, shinobi  
**Confidence:** `INDEXED+SYNTHESIZED`

## TYP-043 — Do not encode Shinobi examples as laws

**Rule:** Font lists from a creator should become references, not mandatory defaults.

**Why:** A library should preserve principles while preventing stylistic cloning.

**Tags:** research-method  
**Confidence:** `SYNTHESIZED`

## TYP-044 — Typography needs visual QA

**Rule:** Screenshot the same type system at mobile, tablet and wide desktop.

**Why:** Metrics that look good in code may fail visually.

**Tags:** testing  
**Confidence:** `SYNTHESIZED`

## TYP-045 — Store text-motion compatibility

**Rule:** Each text effect should declare which type sizes and content lengths it supports.

**Why:** Effects that work on a one-line hero may break a paragraph.

**Tags:** library, motion  
**Confidence:** `SYNTHESIZED`
