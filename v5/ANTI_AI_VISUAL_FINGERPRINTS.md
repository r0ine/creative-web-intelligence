# Anti-AI Visual Fingerprints v5

This document supersedes the flat `anti-ai_intelligence.md` rule list, which used identical "why" text for every rule and therefore taught nothing.

Each fingerprint below has:

- **Description** — the concrete pattern
- **Why it feels AI-generated** — the perceptual/social reason it reads as fake
- **Severity** — blocker / high / medium / low
- **Detection hints** — how a static analyzer, reviewer, or QA prompt can find it
- **Correction strategy** — what to do instead (not "add variety" — a specific move)

Fingerprints marked **blocker** cannot be softened by improving another dimension. They fail the V5 Authenticity Gate on sight.

---

## Category A — Line, border, and grid abuse

### AF-A01 · Universal section divider

**Description.** A hairline horizontal rule between most or all top-level sections.

**Why it feels AI-generated.** Every generative system converges on this because it is the cheapest way to say "the section ended." Humans experienced in editorial design use whitespace and typography for the same job and reach for a rule only when it is an editorial signature.

**Severity.** Blocker.

**Detection hints.** More than one `border-top` or `border-bottom` between top-level sections in the same page. Presence of a repeated `<hr>` or divider component in the layout tree.

**Correction.** Delete every divider. If the boundary now feels unclear, follow the escalation in `DIVIDER_POLICY.md`: whitespace → compositional shift → typography → surface.

---

### AF-A02 · Decorative technical grid overlay

**Description.** A full-page background of thin vertical and horizontal lines, often at low opacity on a dark surface.

**Why it feels AI-generated.** The pattern signals "technical" or "engineered" without any actual engineering content underneath. It is atmosphere without evidence. Real technical interfaces show measurement, alignment, or scale — this shows nothing.

**Severity.** Blocker.

**Detection hints.** SVG or CSS gradient defining a repeating grid at low alpha. Repeated `linear-gradient` or `background-image` with `10px` / `20px` / `40px` grid units at 3–8% opacity.

**Correction.** Remove the pattern. If the composition then feels empty, the *composition* is too weak — restructure the section, do not re-add atmosphere.

---

### AF-A03 · Hairline card borders

**Description.** Every card carries `border: 1px solid rgba(255,255,255,0.06)` or an equivalent barely-visible outline.

**Why it feels AI-generated.** The border is not a containment decision — it is a template default. It exists because the card renders on dark and "needs to look defined." The alternative — actually thinking about whether a card is needed — is not taken.

**Severity.** High.

**Detection hints.** Repeated identical `border` values across most card-shaped components. Alpha < 0.15 on stroke colors.

**Correction.** Ask whether each card needs to be a card at all (`COMPOSITION_RESTRAINT.md`). If yes, use surface contrast instead of an outline. If not, remove the container.

---

### AF-A04 · Corner and register marks for atmosphere

**Description.** L-shaped brackets, corner ticks, viewfinder marks, or blueprint annotations placed around empty areas or headings.

**Why it feels AI-generated.** These read as film UI or engineering-mimicry with no engineering intent. When present without measurement content underneath, they are pure costume.

**Severity.** High.

**Detection hints.** Small SVG paths in corners of container elements with no data association. Repeated bracket glyphs in text.

**Correction.** Remove. If the composition needs framing energy, get it from typography scale or media edge, not from ornamental brackets.

---

## Category B — Motion defaults

### AF-B01 · Universal fade-up entrance

**Description.** `opacity: 0; transform: translateY(20–40px)` applied as a scroll-triggered reveal to most or all elements on the page.

**Why it feels AI-generated.** The animation is the tell that the page was assembled, not composed. A human designer would either not animate most content, or would animate different content in different ways for reasons.

**Severity.** Blocker when applied to more than one section. High when applied selectively but still without variation.

**Detection hints.** Repeated identical `translateY` keyframe values across sections. IntersectionObserver + a single reveal helper function used everywhere. GSAP `from` calls with the same `{ opacity: 0, y: 30 }` shape across many selectors.

**Correction.** Pick one section that genuinely benefits from an entrance and animate only that. Everything else stays static. If two sections need entrance motion, they should use different grammars (see `MOTION_GRAMMAR_V2.md`), not different durations of the same one.

---

### AF-B02 · Stagger ladder

**Description.** Children of a list animate in with delays `0.1s`, `0.2s`, `0.3s`, `0.4s`, `0.5s`.

**Why it feels AI-generated.** The ladder is a code pattern (`index * 0.1`), not a design decision. Real staggers reflect reading order, spatial cause and effect, or emphasis — not array position.

**Severity.** High.

**Detection hints.** `delay: index * 0.1` or equivalent. Repeated 100ms increments in animation configs.

**Correction.** If the stagger is decorative, remove it. If the order matters, stagger by hierarchy (e.g., the primary card enters first, the two supporting cards enter together after a beat), not by array index.

---

### AF-B03 · Identical easing across roles

**Description.** UI microfeedback, editorial reveals, camera moves, and 3D object motion share the same easing token (usually a generic `ease-out` or `cubic-bezier(0.16, 1, 0.3, 1)`).

**Why it feels AI-generated.** Perceived mass and function should shape easing. A button click, a hero reveal, and a camera dolly should not feel the same. When they do, the system is defaulting.

**Severity.** High.

**Detection hints.** Fewer than 3 distinct easing values in the entire codebase across UI, media, and 3D. Single `--ease` token used everywhere.

**Correction.** Define at least three easing families: `ui`, `editorial`, `object`. Assign by role. See `MOTION_GRAMMAR_V2.md`.

---

### AF-B04 · Blur-in on entrance

**Description.** `filter: blur(8px) → blur(0)` on entrance, often paired with fade-up.

**Why it feels AI-generated.** Blur has no communicative purpose here — it does not describe focus, depth of field, or state. It exists to "make the entrance feel premium."

**Severity.** Medium.

**Detection hints.** `filter: blur(…)` in keyframes or `from`/`to` states without any associated focal-plane logic.

**Correction.** Remove. If the motion needs more perceived weight, use a settle grammar (small scale/rotation resolve), not blur.

---

### AF-B05 · Motion without rest zones

**Description.** Every viewport range on the page has some element in motion (parallax, scrub, drift, entrance, hover response).

**Why it feels AI-generated.** Continuous stimulation flattens hierarchy — if everything moves, nothing feels important. Real editorial pacing includes long static ranges where the reader reads.

**Severity.** Blocker on long pages.

**Detection hints.** No section on a multi-viewport page has zero animated elements. `IntersectionObserver` or scroll listeners attached to more than 70% of top-level sections.

**Correction.** Designate at least two rest zones per long page. See `REST_ZONES.md`.

---

## Category C — Composition clichés

### AF-C01 · Centered hero with eyebrow + huge headline + paragraph + two CTAs + glow

**Description.** The single most-generated page opening in existence: small centered label, oversized centered grotesk headline, one-line supporting paragraph, primary + secondary CTA, radial gradient blob behind.

**Why it feels AI-generated.** Every generative system reaches for this because it is the safest layout that "looks like a hero." That is the problem — it announces the system, not the product.

**Severity.** High. Blocker if the brief indicated any distinctive editorial direction.

**Detection hints.** Hero root element uses `text-align: center` combined with a max-width text block and a 2-button flex row. Radial gradient at `top: 50%` behind the copy.

**Correction.** Move the copy off-center. Or make the hero asymmetric with content and media in unequal columns. Or lead with a full-bleed image and let type overlap it. Or write a hero that is a single sentence at editorial scale with no CTA. The problem is the reflex, not the specific elements.

---

### AF-C02 · Cardification of everything

**Description.** Nearly every content unit sits inside a bordered, rounded, padded container regardless of whether it is a selection target, an interactive object, or plain informational text.

**Why it feels AI-generated.** Cards are a rendering habit, not a design decision. A human designer would ask "does this content need containment?" and mostly answer no.

**Severity.** Blocker.

**Detection hints.** More than 60% of leaf content blocks share the same border-radius + border + padding tuple. Ratio of `.card` components to unique content shapes is very high.

**Correction.** See `COMPOSITION_RESTRAINT.md`. Delete containers whose contents don't need a boundary. Use spacing and typography.

---

### AF-C03 · Three-equal-cards feature grid

**Description.** A section titled "Features" (or equivalent) with exactly three cards of equal size, each with an icon, a short heading, and one line of body.

**Why it feels AI-generated.** Content rarely has three peer concepts. Real product features have priorities and relationships. Rendering three equals says the system defaulted to a shape.

**Severity.** High.

**Detection hints.** `grid-template-columns: repeat(3, 1fr)` under a features section. Three-item array in a features config.

**Correction.** If the content actually has three peer concepts, use them but vary size or emphasis. If it has a primary and two supports, render one large card with two smaller supports. If there is one central feature, use one large panel and delete the others.

---

### AF-C04 · Bento grid as default layout

**Description.** A mixed-size tile grid where tile sizes were chosen for visual variety, not because different content needs different footprints.

**Why it feels AI-generated.** Bento is a technique that solves a specific problem — mixed-density peer information. When applied to content that does not have that shape, the tile sizes read as arbitrary.

**Severity.** High.

**Detection hints.** Grid with mixed span values applied to content units that do not measurably differ in density or importance.

**Correction.** Justify each tile size by content density. If they do not differ, use a uniform grid or drop the grid entirely.

---

### AF-C05 · Decorative metadata pills

**Description.** Small pill-shaped labels ("NEW", "AI-POWERED", "v2.0", tag chips) that do not link to filtering, categorization, or state.

**Why it feels AI-generated.** Real metadata does something — filters a list, categorizes an item, indicates state. Decorative metadata is costume.

**Severity.** Medium.

**Detection hints.** Pill component used more than three times on a marketing page without associated filter, link, or state logic.

**Correction.** Delete pills that do not act. If the label carries information ("New in v5"), use a typographic treatment, not a pill.

---

## Category D — Color and surface clichés

### AF-D01 · Dark surface + faint hairlines + single accent glow

**Description.** Near-black background, hairline borders at 6–10% white alpha, one radial gradient behind the headline in a saturated brand color.

**Why it feels AI-generated.** The combination is the standard "premium tech" fallback because it looks polished with almost no compositional effort. It signals the effort was skipped.

**Severity.** High.

**Detection hints.** Body background near `#0A0A0B`, strokes at rgba(255,255,255, < 0.15), one large `radial-gradient` behind hero content.

**Correction.** Either commit to darkness as a chosen surface (with real depth from imagery, materials, or type) or move to a lighter, calmer surface. Kill the accent glow — one point of color scarcity somewhere else.

---

### AF-D02 · Unmotivated blue-purple gradient

**Description.** Gradient from blue to purple (or purple to pink) used as brand identity for anything "tech" or "AI."

**Why it feels AI-generated.** This gradient has been the AI/SaaS default for a decade. Choosing it says the color decision was skipped.

**Severity.** High.

**Detection hints.** Gradient stops in the 210°–290° hue range with high chroma. Applied to headlines, CTAs, background auras, or the whole surface.

**Correction.** Color must come from brand, material, image, or a chosen source (Wada, editorial reference). If the product genuinely needs a signal color, choose one flat color, not a gradient.

---

### AF-D03 · Gradient headline as identity

**Description.** The primary headline uses `background-clip: text` with a gradient fill because the brand identity does not exist without it.

**Why it feels AI-generated.** Removing the gradient reveals that the type has no character. The gradient is compensating.

**Severity.** High.

**Detection hints.** `background-clip: text` or `-webkit-background-clip: text` on H1 or hero headline.

**Correction.** Fix the type first (weight, size, tracking, family). If a single-color headline does not carry the identity, the type system is wrong and gradient will not save it.

---

### AF-D04 · Glassmorphism spam

**Description.** Multiple translucent frosted-glass panels stacked on the page as a general "premium" signal, without any spatial reason (there is no environment behind them worth suggesting).

**Why it feels AI-generated.** Glass is a spatial device. Used without a spatial world, it is a texture applied to hide the flatness beneath.

**Severity.** High.

**Detection hints.** More than two `backdrop-filter: blur(…)` elements on one screen without underlying imagery/scene.

**Correction.** If there is a scene behind, one glass panel is fine. If there is not, glass is not the right device.

---

## Category E — Typography clichés

### AF-E01 · Oversized centered grotesk headline

**Description.** A very large sans-serif headline, centered, typically the only "big" typographic moment on the page.

**Why it feels AI-generated.** The move is the safest possible display decision. It signals "we made the headline big" without doing anything editorial.

**Severity.** Medium. High if paired with a fashionable grotesk chosen for category (Inter, Geist, General Sans, etc.) with no morphology rationale.

**Detection hints.** H1 with `text-align: center` and font-size ≥ 6vw. Font family among the current top-10 "startup grotesks."

**Correction.** Break the reflex. Use asymmetry, mixed weight or width, or a different typographic voice entirely. See `TYPOGRAPHY_FIRST_PREMIUM.md`.

---

### AF-E02 · Mono everywhere developer costume

**Description.** Monospace face used for body, headings, and nav to signal "developer product," accompanied by fake terminal metadata and green status dots.

**Why it feels AI-generated.** Mono is a role, not a costume. When used outside its role (code, data, metadata) it reads as an attempt to look technical.

**Severity.** High.

**Detection hints.** Mono family applied to body copy or primary navigation. Presence of terminal prompt characters (`$`, `>`) as decoration.

**Correction.** Reserve mono for actual code and precise data. Use a real body face for reading.

---

### AF-E03 · All-caps eyebrow spam

**Description.** Every section leads with a small, all-caps, wide-tracked label (`—— FEATURES`, `—— HOW IT WORKS`).

**Why it feels AI-generated.** Repetition reveals it as a template slot rather than an editorial device. When every eyebrow is present because the template has one, none of them signal what an eyebrow should — a chapter marker.

**Severity.** Medium.

**Detection hints.** Repeated small-caps or `text-transform: uppercase` label at the top of every section.

**Correction.** Delete most of them. Keep one or two where the chapter marker is genuinely useful.

---

### AF-E04 · Scale-only hierarchy

**Description.** Hierarchy is expressed only by font-size differences. Weight, width, casing, tracking, and family stay the same across levels.

**Why it feels AI-generated.** It is the laziest possible use of type. Real hierarchy uses multiple axes.

**Severity.** High.

**Detection hints.** Type scale where every heading uses the same weight and family, differentiated only by size.

**Correction.** Introduce a second axis of contrast. See `TYPOGRAPHY_FIRST_PREMIUM.md`.

---

## Category F — Interaction and micro-detail clichés

### AF-F01 · Universal hover-lift + shadow

**Description.** Every card responds to hover with `translateY(-4px)` and increased shadow.

**Why it feels AI-generated.** The move is the same across the entire page and across the entire generative-web output style. It is default hover polish.

**Severity.** Medium.

**Detection hints.** Multiple selectors sharing identical `:hover` transform + shadow rules.

**Correction.** Reserve hover feedback for elements that respond to click or drag. Cards that are just information should not physically move on hover.

---

### AF-F02 · Cursor-follows-everything

**Description.** A custom cursor drives multiple simultaneous effects across the page — camera tilt, model rotation, magnetic buttons, blob-follows-mouse, image warp.

**Why it feels AI-generated.** One gesture cannot mean five things at full amplitude. When it does, no single response feels intentional.

**Severity.** High.

**Detection hints.** Multiple mousemove-based transforms on one screen at full amplitude.

**Correction.** Pick one dominant pointer response per scene. Others are muted or off. See `MOTION_GRAMMAR_V2.md`.

---

### AF-F03 · Emoji as feature icons

**Description.** 🚀 🧠 ⚡ 🛡️ used as feature icons because a coherent icon system was not chosen.

**Why it feels AI-generated.** Emojis are the fastest visual shorthand and betray the fastest visual decision.

**Severity.** Medium.

**Detection hints.** Emoji characters appearing as leading glyphs for feature blocks.

**Correction.** Either commit to an icon family with brand rationale (see v4 Icon Director) or use no icons and let typography carry the block.

---

### AF-F04 · Decorative fake dashboard / terminal

**Description.** A screenshot-style block showing a fake dashboard, fake terminal output, fake code, or fake chart placed to signal "product" without showing a real product surface.

**Why it feels AI-generated.** Real product surfaces look inconvenient — real data, real edge cases. Faked ones look clean because they were designed to look clean.

**Severity.** High.

**Detection hints.** Chart, terminal, or table with no live data and no link to the real product.

**Correction.** Show a real product screenshot with real data, or do not show a product surface at all. Do not fabricate.

---

## Scoring

There is no score.

- Any **blocker** = the design fails the V5 Authenticity Gate.
- Two or more **high** severity fingerprints = the design fails the V5 Authenticity Gate.
- **Medium** fingerprints are logged and must be addressed before ship.
- **Low** fingerprints are noted.

The old 0–3 scoring in `data/v3_2/visual_fingerprint_checks.json` remains available as a *retrospective* tool, not as a passing metric.
