# Typography — Font Loading & Performance

Entries: **7**

## TYP-003 — Limit active families

Default to one or two families; add a third only when it represents a distinct content role.

**Why:** Too many families weaken visual coherence and increase loading cost.

**Tags:** system, performance

## TYP-004 — Use variable fonts deliberately

Prefer variable fonts when a project genuinely uses multiple weights/widths/axes.

**Why:** They can reduce the cost of loading many separate font files and allow finer art direction.

**Tags:** variable-font, performance

## TYP-012 — Use optical size where available

If a variable font has opsz, test it for text and display roles rather than freezing one setting.

**Why:** Optical-size axes can improve shapes for different point sizes.

**Tags:** variable-font

## TYP-014 — Fallback metrics matter

Define compatible fallbacks and consider size-adjust/metric overrides for large web fonts.

**Why:** Reducing metric mismatch can reduce layout shift.

**Tags:** performance, CLS

## TYP-015 — Preload only critical fonts

Preload only font files needed above the fold; avoid preloading every weight.

**Why:** Over-preloading competes with more important resources.

**Tags:** performance

## TYP-016 — Create font-loading states

Ensure layout remains usable before custom fonts load.

**Why:** The experience should not depend on a blank-font phase.

**Tags:** performance, resilience

## TYP-040 — Track performance cost

Font catalog entries should include file count, variable/static mode and estimated loading impact.

**Why:** Premium typography should not quietly destroy performance.

**Tags:** library, performance
