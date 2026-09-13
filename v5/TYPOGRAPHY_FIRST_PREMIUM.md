# Typography-First Premium v5

The library's outputs have been leaning on borders, dividers, glows, and gradients to signal quality. When those decorations are removed, the pages feel flat. That means the typography system is not doing its job.

This document sets the rule: **premium is a property of the type system. Everything else is support.**

## The test

If turning off every border, divider, glow, gradient, background pattern, and reveal animation makes the hierarchy collapse, the typography is too weak. No amount of decorative repair will fix it. Rebuild the type system.

## Six axes of typographic hierarchy

Hierarchy is not scale alone. Scale is one axis of six.

1. **Size** — the most obvious, but the weakest signal when used alone.
2. **Weight** — regular vs semibold vs black. Weight contrast makes even a single family read as multi-role.
3. **Width** — condensed vs regular vs expanded. Available in variable fonts. A widely under-used axis.
4. **Casing** — sentence case, all caps, small caps. Case shift creates immediate role distinction.
5. **Tracking** — tight negative tracking on large display, generous positive tracking on small caps. Not one global letter-spacing.
6. **Family shift** — a second family used *for role*, not for variety.

**Rule:** every hierarchy level in the type system must differ on **at least two of these six axes** from adjacent levels. A hierarchy that changes only size is broken.

## The role list, not the size list

Do not start typography by defining `h1 = 72px, h2 = 48px, h3 = 32px…`. Start by listing the roles the design has:

- Display (hero moments)
- Editorial heading (chapter markers)
- Section heading
- Sub-heading
- Body (reading)
- Body (UI)
- Numeric / data
- Caption / metadata
- Label / eyebrow (if the design has any — not automatic)
- Code / mono (if the product needs it)

Assign each role to a family, weight, width, size, case, tracking, and measure. Now you have a system, not a scale.

## Measure and line-height as premium signals

The tells of amateur type systems:

- Body paragraphs 800px wide.
- Line-height 1.5 applied to everything including display.
- Display type with the same line-height as body.
- All labels sharing the same size and tracking.

The tells of considered type systems:

- Body measure between 45 and 75 characters per line.
- Display line-height 1.0–1.1 at large sizes, 1.5–1.7 for body.
- Tracking that opens up as size decreases and case shifts to caps.
- Paragraph spacing derived from body line-height, not an arbitrary margin.

## Type carries voice

A page has a voice: quiet, expressive, precise, editorial, industrial, human, technical. Voice is carried by:

- **The display family and its state** (weight, width, tracking).
- **The tension between display and body.** Contrast in structure, not just size.
- **The pace of the copy.** Short headline, long body vs long headline, short body. This is a typographic decision.

If the voice does not survive when color and decoration are turned off, voice was being carried by decoration.

## What "premium" actually looks like

Premium is not high-contrast serif on black. Premium is not glass panels. Premium is:

- A single family used with discipline — a variable grotesk with three weights and two widths deployed to real roles.
- A display face with a distinctive character choice (aperture, terminal, x-height) that reads at a glance.
- Body copy with real measure, real line-height, real tracking.
- Headlines that land on chosen line breaks, not random ones.
- Small text that is small but not tiny, and tracked out enough to breathe.
- No display face used for long copy. No body face inflated for display use without art direction.

Any single one of these does more for perceived quality than every gradient, glow, and divider combined.

## The one-family test

Can the page work with a single well-chosen family across every role?

If yes, prefer it. A one-family system with disciplined weight/width/size/case use reads as *decided* — the mark of considered work. Two families should exist because two families are doing different jobs, not because "two families is more designed."

## Signals that typography is compensating for weak composition

- Repeated `text-align: center` on every heading. Centered type is a strong statement; it stops being one when it is the default.
- Huge display type used to force a section to feel important. If the section is important, its position and surrounding space should already say so.
- Gradient fills on headlines. See `ANTI_AI_VISUAL_FINGERPRINTS.md` § AF-D03.
- All-caps eyebrows on every section as a substitute for section design. See § AF-E03.

## Language and script

Typography includes language coverage. Turkish `İ/ı/Ğ/ğ/Ş/ş/Ç/ç/Ö/ö/Ü/ü`, extended Latin, non-Latin scripts — verified in the actual fonts, not assumed. Fallback strategy authored *before* implementation. Layout shift measured during cold load.

## The final typography test

Render the page with:
- One color for text (default surface color for body, one darker or lighter for display)
- No borders, glows, gradients, or backgrounds
- No animation

Does the hierarchy still read at every viewport? Does the voice still come through?

If yes, type is doing its job.
If no, no amount of decoration will hide the gap.
