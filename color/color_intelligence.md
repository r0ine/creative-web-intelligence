# Color Intelligence

Total rules: **102**

Reusable design/engineering rules. Source-observed examples, standards and synthesized guidance must remain clearly distinguished.

## COL-001 — Use semantic color roles

**Rule:** Define background, surface, text, muted, accent, success, warning, danger and focus roles rather than scattering hex values.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** tokens
**Confidence:** `SYNTHESIZED`

## COL-002 — Pure black is optional, not mandatory

**Rule:** Test tinted near-black values for dark interfaces when softer contrast or brand tone is desired.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** dark-theme
**Confidence:** `SYNTHESIZED`

## COL-003 — Do not ban pure black globally

**Rule:** Pure black can be correct for a specific identity, OLED-focused art direction or sharp editorial contrast.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** anti-dogma
**Confidence:** `SYNTHESIZED`

## COL-004 — Build palettes from relationships

**Rule:** Store hue, lightness and contrast relationships instead of only fixed swatches.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** palette
**Confidence:** `SYNTHESIZED`

## COL-005 — One accent can be enough

**Rule:** Use a single strong accent when the composition already has rich imagery or 3D.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** restraint
**Confidence:** `SYNTHESIZED`

## COL-006 — Separate brand accent from status colors

**Rule:** Do not reuse the brand color for destructive/success states if meaning becomes ambiguous.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** semantics
**Confidence:** `SYNTHESIZED`

## COL-007 — Text contrast is a gate

**Rule:** Normal text should meet WCAG minimum contrast against its actual background.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** accessibility
**Confidence:** `SYNTHESIZED`

## COL-008 — Large text still needs contrast

**Rule:** Large display text has a lower minimum ratio than body text but should still be validated.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** accessibility
**Confidence:** `SYNTHESIZED`

## COL-009 — Do not communicate state by color alone

**Rule:** Pair color with icon, label, shape or text where state matters.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** accessibility
**Confidence:** `SYNTHESIZED`

## COL-010 — Dark mode needs luminance layers

**Rule:** Create multiple dark surface levels rather than black background + glowing cards.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** dark-theme
**Confidence:** `SYNTHESIZED`

## COL-011 — Light mode needs surface hierarchy

**Rule:** Use subtle tonal differences and borders where needed; not every section needs a grey card.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** light-theme
**Confidence:** `SYNTHESIZED`

## COL-012 — Avoid default AI purple-blue

**Rule:** Purple/blue gradients require a brand or content reason, not an AI/tech stereotype.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** anti-slop
**Confidence:** `SYNTHESIZED`

## COL-013 — Gradient has a job

**Rule:** Use gradients for depth, material, state, atmosphere or brand—not filler.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** gradient
**Confidence:** `SYNTHESIZED`

## COL-014 — Keep gradient count low

**Rule:** Multiple unrelated gradients quickly destroy palette coherence.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** restraint
**Confidence:** `SYNTHESIZED`

## COL-015 — Use color temperature intentionally

**Rule:** Warm/cool shifts can separate foreground/background or emotional states.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** art-direction
**Confidence:** `SYNTHESIZED`

## COL-016 — Use saturation as hierarchy

**Rule:** Not every object should be fully saturated; reserve saturation for focus.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** hierarchy
**Confidence:** `SYNTHESIZED`

## COL-017 — Image palette should influence UI

**Rule:** When a hero image/3D model dominates, derive surrounding neutrals/accents from it where appropriate.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** integration
**Confidence:** `SYNTHESIZED`

## COL-018 — 3D lighting and DOM palette must agree

**Rule:** WebGL scene and HTML should appear in the same color world.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** 3d
**Confidence:** `SYNTHESIZED`

## COL-019 — Emissive colors need headroom

**Rule:** Do not set every bright material to maximum intensity; selective emission makes bloom meaningful.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** 3d
**Confidence:** `SYNTHESIZED`

## COL-020 — Color recipes need contrast metadata

**Rule:** Palette catalog records should store text-on-bg pass/fail pairs.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** library
**Confidence:** `SYNTHESIZED`

## COL-021 — Catalog dark alternatives

**Rule:** Store several near-black families: neutral, warm, cool, green-tinted, red-tinted.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** library
**Confidence:** `SYNTHESIZED`

## COL-022 — Catalog off-whites

**Rule:** Store warm/cool/neutral off-white families for softer editorial themes.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** library
**Confidence:** `SYNTHESIZED`

## COL-023 — Use black/white extremes intentionally

**Rule:** Extremes can create brutalist/editorial impact when hierarchy is clear.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** art-direction
**Confidence:** `SYNTHESIZED`

## COL-024 — Avoid low-contrast grey-on-grey UI

**Rule:** Muted does not mean unreadable.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** accessibility
**Confidence:** `SYNTHESIZED`

## COL-025 — Focus indicators are part of palette

**Rule:** Define focus colors and contrast as first-class tokens.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** accessibility
**Confidence:** `SYNTHESIZED`

## COL-026 — Hover color should preserve meaning

**Rule:** Hover should not make text or controls fail contrast.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** interaction
**Confidence:** `SYNTHESIZED`

## COL-027 — Selected state needs more than tiny hue shift

**Rule:** Use border, fill, scale, icon or type changes if hue difference is too subtle.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** interaction
**Confidence:** `SYNTHESIZED`

## COL-028 — Color transitions should be synchronized

**Rule:** When scene background changes, text/surface colors should transition as a coordinated state.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** motion
**Confidence:** `SYNTHESIZED`

## COL-029 — Use color chaptering selectively

**Rule:** Long narratives can assign distinct controlled palettes to chapters.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** storytelling
**Confidence:** `SYNTHESIZED`

## COL-030 — Do not auto-generate rainbow palettes

**Rule:** Large color sets should have semantic or narrative logic.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** anti-slop
**Confidence:** `SYNTHESIZED`

## COL-031 — Record palette mood as metadata

**Rule:** Catalog palettes with descriptors such as industrial, editorial, playful, luxury, organic.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** library
**Confidence:** `SYNTHESIZED`

## COL-032 — Record display context

**Rule:** A palette proven on dark hero art may fail in dense dashboard tables.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** library
**Confidence:** `SYNTHESIZED`

## COL-033 — Shinobi palette examples are references

**Rule:** Indexed combinations like Deep Sea/Sea Foam and high-contrast pairings should inspire palette archetypes, not be mandatory.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** shinobi
**Confidence:** `SYNTHESIZED`

## COL-034 — Tinted black library should include source examples

**Rule:** Preserve indexed near-black examples as reference swatches with source labels.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** shinobi
**Confidence:** `SYNTHESIZED`

## COL-035 — Test with screenshots and browser rendering

**Rule:** Color changes in 3D post-processing and display profiles can alter perceived results.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** testing
**Confidence:** `SYNTHESIZED`

## COL-036 — Never invent exact colors from inaccessible reels

**Rule:** Mark unviewed reel palettes NEEDS_CAPTURE until visual evidence is supplied.

**Why:** Color should support hierarchy, meaning, accessibility and art direction.

**Tags:** research-method
**Confidence:** `SYNTHESIZED`

## COL-037 — Teach the relationship, not only the swatches

**Rule:** When proposing a palette, explain dominance, harmony, role assignment, area and contrast.

**Why:** A reusable design intelligence library should make future agents understand why a combination works.

**Tags:** education
**Confidence:** `SYNTHESIZED`

## COL-038 — Start from role architecture

**Rule:** Choose background/surface/text/accent/status roles before decorative colors.

**Why:** Role-first palettes transfer better across components and themes.

**Tags:** tokens, semantics
**Confidence:** `SYNTHESIZED`

## COL-039 — Classify visual driver first

**Rule:** Decide whether typography, imagery, 3D, data or illustration is the primary visual driver before choosing palette complexity.

**Why:** Rich visual drivers often need simpler UI color systems.

**Tags:** workflow
**Confidence:** `SYNTHESIZED`

## COL-040 — Use monochromatic systems for restraint

**Rule:** Prefer monochromatic families when imagery, typography or 3D already provides enough visual complexity.

**Why:** A single hue family can preserve coherence without visual boredom when lightness and material vary.

**Tags:** harmony
**Confidence:** `SYNTHESIZED`

## COL-041 — Use analogous systems for atmosphere

**Rule:** Use neighboring hue families when the design needs a cohesive atmospheric transition.

**Why:** Analogous hues create softer separation than complementary pairs.

**Tags:** harmony
**Confidence:** `SYNTHESIZED`

## COL-042 — Use complementary color as a focal tool

**Rule:** Use the opposite hue family primarily to create focal contrast, not as an equal-area second background.

**Why:** Equal strong complements can create visual conflict.

**Tags:** harmony
**Confidence:** `SYNTHESIZED`

## COL-043 — Split complements need hierarchy

**Rule:** Promote only one split-complement color to primary accent; keep the other supportive.

**Why:** Three strong accent families quickly destroy hierarchy.

**Tags:** harmony
**Confidence:** `SYNTHESIZED`

## COL-044 — Triads need unequal weight

**Rule:** In triadic systems, make one hue dominant, one secondary and one sparse.

**Why:** Equal-area triads often look childish or noisy in UI.

**Tags:** harmony
**Confidence:** `SYNTHESIZED`

## COL-045 — Area is part of palette design

**Rule:** Evaluate colors in approximate screen area, not only as equal swatches.

**Why:** A small strong accent can work even if the same hue overwhelms at large area.

**Tags:** composition
**Confidence:** `SYNTHESIZED`

## COL-046 — Accent scarcity increases value

**Rule:** Keep the strongest chroma scarce unless brand art direction explicitly requires a large color field.

**Why:** Scarcity makes action and signature details easier to notice.

**Tags:** hierarchy
**Confidence:** `SYNTHESIZED`

## COL-047 — Saturation can encode hierarchy

**Rule:** Reduce chroma for support colors before reaching for opacity everywhere.

**Why:** Chroma differences preserve cleaner, more predictable states.

**Tags:** hierarchy
**Confidence:** `SYNTHESIZED`

## COL-048 — Lightness creates structure

**Rule:** Use lightness steps to separate surfaces and content levels.

**Why:** A strong luminance structure reduces dependence on borders, shadows and glow.

**Tags:** hierarchy
**Confidence:** `SYNTHESIZED`

## COL-049 — Temperature can separate depth

**Rule:** Use warm/cool relationships to distinguish foreground, background or narrative states when justified.

**Why:** Temperature creates depth without requiring high saturation.

**Tags:** art-direction
**Confidence:** `SYNTHESIZED`

## COL-050 — Tint neutrals subtly

**Rule:** Warm, cool or colored neutrals should support atmosphere without announcing themselves before content.

**Why:** Over-tinted neutrals become extra accent colors.

**Tags:** neutral
**Confidence:** `SYNTHESIZED`

## COL-051 — Do not force brand hue into every component

**Rule:** Use strong brand colors where they create recognition or hierarchy rather than as universal fill.

**Why:** Overuse weakens both brand signal and component semantics.

**Tags:** brand
**Confidence:** `SYNTHESIZED`

## COL-052 — Derive from dominant imagery when useful

**Rule:** If a hero image or model dominates, sample or conceptually derive nearby neutrals and accents from it.

**Why:** This helps DOM and media feel art-directed as one world.

**Tags:** imagery
**Confidence:** `SYNTHESIZED`

## COL-053 — Image-derived does not mean exact sampling

**Rule:** Adjust sampled hues for contrast, hierarchy and screen use instead of blindly copying pixel colors.

**Why:** Photography colors often need normalization for UI.

**Tags:** imagery
**Confidence:** `SYNTHESIZED`

## COL-054 — Separate decorative and functional colors

**Rule:** Mark colors that are decorative-only versus colors safe for text, controls or status.

**Why:** A beautiful swatch may be unusable for readable text.

**Tags:** semantics, accessibility
**Confidence:** `SYNTHESIZED`

## COL-055 — Store safe text-on-accent pair

**Rule:** Every primary accent should declare whether black, white or another foreground is the readable text color.

**Why:** CTA readability should not be guessed per component.

**Tags:** accessibility
**Confidence:** `SYNTHESIZED`

## COL-056 — Validate muted text explicitly

**Rule:** Muted text must be tested on every surface where it appears.

**Why:** Lower visual priority is not permission for unreadability.

**Tags:** accessibility
**Confidence:** `SYNTHESIZED`

## COL-057 — Validate non-text UI contrast

**Rule:** Borders, controls and focus indicators need sufficient contrast where accessibility rules require it.

**Why:** Interfaces communicate through more than text.

**Tags:** accessibility
**Confidence:** `SYNTHESIZED`

## COL-058 — Never use color alone for critical state

**Rule:** Add iconography, label, shape or other cues for success, warning, error and selection when meaning matters.

**Why:** Users may not perceive hue differences reliably.

**Tags:** accessibility
**Confidence:** `SYNTHESIZED`

## COL-059 — Focus color is a core token

**Rule:** Define focus-ring treatment at palette design time.

**Why:** Keyboard interaction should not be patched after styling.

**Tags:** accessibility
**Confidence:** `SYNTHESIZED`

## COL-060 — Do not create light mode by inversion

**Rule:** Recompose surfaces, borders, accent intensity and imagery for light mode rather than mathematically inverting dark colors.

**Why:** Optical balance differs between modes.

**Tags:** theme
**Confidence:** `SYNTHESIZED`

## COL-061 — Do not create dark mode by blackening everything

**Rule:** Use intentional luminance layers and adjust accent chroma for dark surroundings.

**Why:** Dark themes need structure, not an empty black field.

**Tags:** theme
**Confidence:** `SYNTHESIZED`

## COL-062 — Dark accent may need lower chroma

**Rule:** An accent that works on white may become painfully intense on near-black.

**Why:** Perceived intensity depends on context.

**Tags:** theme
**Confidence:** `SYNTHESIZED`

## COL-063 — Light accent may need greater depth

**Rule:** Very light accents may disappear on off-white surfaces.

**Why:** Light themes often need darker accent tones for controls and text.

**Tags:** theme
**Confidence:** `SYNTHESIZED`

## COL-064 — Pair warm near-black with warm off-white carefully

**Rule:** Warm dark/light themes should share temperature without making every surface beige or brown.

**Why:** Temperature coherence is useful; monotony is not.

**Tags:** theme
**Confidence:** `SYNTHESIZED`

## COL-065 — Use OKLCH for controlled ramps when practical

**Rule:** For generated systems, use perceptual lightness/chroma controls when browser/tooling constraints allow.

**Why:** More predictable ramps make programmatic palettes easier to reason about.

**Tags:** oklch
**Confidence:** `SYNTHESIZED`

## COL-066 — Do not equate OKLCH values with accessibility

**Rule:** Always run actual contrast checks after generating colors.

**Why:** Perceptual uniformity and WCAG contrast are different concerns.

**Tags:** oklch, accessibility
**Confidence:** `SYNTHESIZED`

## COL-067 — Generate hover states from role logic

**Rule:** Derive hover/active states through controlled lightness/chroma shifts or structural feedback.

**Why:** Random hex changes create inconsistent interaction.

**Tags:** interaction
**Confidence:** `SYNTHESIZED`

## COL-068 — Hover should not disappear in dark mode

**Rule:** Check that interaction deltas remain visible on dark surfaces.

**Why:** Small color changes can vanish at low luminance.

**Tags:** interaction
**Confidence:** `SYNTHESIZED`

## COL-069 — Selection requires persistent difference

**Rule:** Selected state should remain visually distinct after hover ends.

**Why:** Interaction state and hover state solve different problems.

**Tags:** interaction
**Confidence:** `SYNTHESIZED`

## COL-070 — 3D environment affects perceived material color

**Rule:** Judge reflective materials with their environment and lights enabled.

**Why:** Metal/glass appearance is inseparable from lighting context.

**Tags:** 3d
**Confidence:** `SYNTHESIZED`

## COL-071 — Coordinate DOM accent with scene accent

**Rule:** Use related accent families across UI and WebGL unless deliberate contrast is part of the concept.

**Why:** Independent palettes make the model look pasted behind the page.

**Tags:** 3d
**Confidence:** `SYNTHESIZED`

## COL-072 — Keep emissive color scarce

**Rule:** Reserve emissive materials and bloom-driving colors for high-value details.

**Why:** Too much emission destroys depth and hierarchy.

**Tags:** 3d
**Confidence:** `SYNTHESIZED`

## COL-073 — Use light temperature as narrative state

**Rule:** Lighting temperature can shift across chapters if DOM tokens transition with it.

**Why:** Synchronized changes create coherent scene storytelling.

**Tags:** 3d, motion
**Confidence:** `SYNTHESIZED`

## COL-074 — Do not use cyan-magenta by default in 3D

**Rule:** Choose 3D light colors from the project palette rather than the generic cyberpunk preset.

**Why:** Creative-web clichés can be as repetitive as SaaS clichés.

**Tags:** 3d, anti-slop
**Confidence:** `SYNTHESIZED`

## COL-075 — Material albedo is not final perceived color

**Rule:** Account for roughness, metalness, environment, tone mapping and post-processing.

**Why:** Rendered color is contextual.

**Tags:** 3d
**Confidence:** `SYNTHESIZED`

## COL-076 — Tone mapping belongs in palette QA

**Rule:** Evaluate the final render after tone mapping and post effects before locking DOM accents.

**Why:** Rendering transforms can shift perceived values.

**Tags:** 3d
**Confidence:** `SYNTHESIZED`

## COL-077 — Bloom changes area perception

**Rule:** A glowing accent visually occupies more area than its geometry.

**Why:** Area guidance should include halo/bloom footprint.

**Tags:** 3d
**Confidence:** `SYNTHESIZED`

## COL-078 — Gradient endpoints need a relationship

**Rule:** Choose gradient endpoints through material, harmony or narrative logic.

**Why:** Two fashionable colors are not automatically a coherent gradient.

**Tags:** gradient
**Confidence:** `SYNTHESIZED`

## COL-079 — Gradient direction should support composition

**Rule:** Align gradient direction with depth, lighting, movement or layout.

**Why:** Arbitrary diagonal gradients often feel decorative and generic.

**Tags:** gradient
**Confidence:** `SYNTHESIZED`

## COL-080 — Use fewer gradient stops by default

**Rule:** Begin with two meaningful endpoints and add stops only when needed.

**Why:** Excess stops often introduce muddy intermediate colors.

**Tags:** gradient
**Confidence:** `SYNTHESIZED`

## COL-081 — Gradient text is a special effect

**Rule:** Use gradient typography only when the text itself is a signature visual object.

**Why:** Using it on every marketing headline destroys typographic clarity.

**Tags:** gradient, anti-slop
**Confidence:** `SYNTHESIZED`

## COL-082 — Status colors should remain semantically stable

**Rule:** Success/warning/danger families should not change meaning across pages.

**Why:** Semantic consistency matters more than section-level aesthetics.

**Tags:** semantics
**Confidence:** `SYNTHESIZED`

## COL-083 — Data colors need separability

**Rule:** Categorical colors should be distinguishable in context and not merely aesthetically harmonious.

**Why:** Data communication has different requirements from decorative branding.

**Tags:** data
**Confidence:** `SYNTHESIZED`

## COL-084 — Sequential data needs ordered lightness

**Rule:** Use an ordered perceptual progression for low→high values.

**Why:** Users should see magnitude order without memorizing labels.

**Tags:** data
**Confidence:** `SYNTHESIZED`

## COL-085 — Diverging data needs a meaningful midpoint

**Rule:** Use two directional families only when the middle value is semantically meaningful.

**Why:** Diverging color without a real midpoint can mislead.

**Tags:** data
**Confidence:** `SYNTHESIZED`

## COL-086 — Do not use brand accent for every chart series

**Rule:** Create data-specific scales when multiple categories must be compared.

**Why:** Brand color alone is not a data visualization system.

**Tags:** data
**Confidence:** `SYNTHESIZED`

## COL-087 — Palette names should describe intent

**Rule:** Catalog recipes by mood/use/harmony/mode instead of vague names like cool-1.

**Why:** Descriptive metadata improves agent retrieval.

**Tags:** library
**Confidence:** `SYNTHESIZED`

## COL-088 — Store harmony metadata

**Rule:** Every catalog palette should declare monochromatic/analogous/complementary/etc.

**Why:** Agents can then learn and retrieve by relationship rather than hex similarity.

**Tags:** library
**Confidence:** `SYNTHESIZED`

## COL-089 — Store role metadata

**Rule:** Machine-readable recipes should label every swatch by UI role.

**Why:** Roles make palettes composable.

**Tags:** library
**Confidence:** `SYNTHESIZED`

## COL-090 — Store contrast measurements

**Rule:** Record verified contrast ratios for primary text pairs in recipe data.

**Why:** This prevents agents from assuming readability.

**Tags:** library, accessibility
**Confidence:** `SYNTHESIZED`

## COL-091 — Store area guidance

**Rule:** Recipe metadata should suggest dominant/support/accent usage.

**Why:** Area relationships are central to whether a palette works.

**Tags:** library
**Confidence:** `SYNTHESIZED`

## COL-092 — Store 3D notes

**Rule:** Palettes intended for immersive sites should declare lighting/material guidance.

**Why:** The same hex values behave differently in DOM and rendered scenes.

**Tags:** library, 3d
**Confidence:** `SYNTHESIZED`

## COL-093 — Store avoid-with metadata

**Rule:** Document combinations that usually conflict, such as high-chroma dual accents plus heavy bloom.

**Why:** Compatibility guidance reduces effect stacking.

**Tags:** library
**Confidence:** `SYNTHESIZED`

## COL-094 — Explain palette confidence

**Rule:** Mark whether a recipe is source-observed, verified standard-based or synthesized.

**Why:** Research integrity prevents false attribution.

**Tags:** research
**Confidence:** `SYNTHESIZED`

## COL-095 — Do not attribute generated recipes to creators

**Rule:** Creator examples may inspire rules, but synthesized palettes must remain clearly labeled.

**Why:** Avoid fabricated claims about what a designer recommends.

**Tags:** research
**Confidence:** `SYNTHESIZED`

## COL-096 — Use references as evidence, not authority

**Rule:** A palette from an award-winning site still has to fit the new project.

**Why:** Context-specific choices should not become universal laws.

**Tags:** research
**Confidence:** `SYNTHESIZED`

## COL-097 — Critique equal swatch previews

**Rule:** Always preview a palette on a realistic UI composition in addition to equal color chips.

**Why:** Screen-area relationships can reverse the impression of a swatch set.

**Tags:** evaluation
**Confidence:** `SYNTHESIZED`

## COL-098 — Test grayscale hierarchy

**Rule:** Temporarily remove chroma to see whether hierarchy survives on lightness/structure.

**Why:** If the layout collapses without hue, colors may be doing too much structural work.

**Tags:** evaluation
**Confidence:** `SYNTHESIZED`

## COL-099 — Test accent removal

**Rule:** Remove the accent temporarily; content hierarchy should still mostly work.

**Why:** Accent should enhance hierarchy rather than rescue a weak layout.

**Tags:** evaluation
**Confidence:** `SYNTHESIZED`

## COL-100 — Test reduced color modes

**Rule:** Consider forced-colors/high-contrast environments for functional content.

**Why:** Robust interfaces should not depend on exact authored colors.

**Tags:** accessibility
**Confidence:** `SYNTHESIZED`

## COL-101 — Teach with counterexamples

**Rule:** When explaining a combination, mention one plausible misuse and why it fails.

**Why:** Contrastive examples build reusable design judgment.

**Tags:** education
**Confidence:** `SYNTHESIZED`

## COL-102 — Offer alternatives by mood, not random colors

**Rule:** If presenting multiple palettes, vary strategic direction such as restrained/energetic/editorial instead of random hue swaps.

**Why:** Options should represent real art-direction choices.

**Tags:** education
**Confidence:** `SYNTHESIZED`
