# V5 Authenticity Gate

Release status: PASS / PASS-WITH-NOTES / FAIL.

Supersedes `quality/V3_2_VISUAL_DIRECTION_GATE.md` for visual authenticity release decisions. v3.2 gate remains available for retrospective analysis but v5 gate is authoritative going forward.

## Blocker categories

A build fails if any single item in these categories is present.

### Line, border, and grid
- **A-01** More than one hairline divider between top-level sections.
- **A-02** Global background grid overlay for atmosphere.
- **A-03** Repeated identical `border` on non-interactive containers.
- **A-04** Register / corner marks placed for atmosphere.

### Motion
- **B-01** Universal fade-up entrance across multiple sections.
- **B-02** Repeated stagger ladder (`index * 0.1s`).
- **B-03** Same easing / duration across UI, editorial, and object motion.
- **B-04** Every section entering with the same grammar.
- **B-05** Zero rest zones on a page longer than two viewports.

### Composition
- **C-01** Cardification: > 60% of leaf content shares identical container shape.
- **C-02** Centered-hero cliché (eyebrow + huge grotesk + two CTAs + glow).
- **C-03** Bento layout with no content-density justification.
- **C-04** Every section using identical geometry.

### Color
- **D-01** Default dark + hairlines + accent glow with no chosen surface strategy.
- **D-02** Unmotivated blue-purple gradient identity.
- **D-03** Gradient text fill on hero headline.
- **D-04** Three or more high-chroma colors competing at similar area weight.

### Typography
- **E-01** Hierarchy expressed only through size.
- **E-02** Monospace used for body copy (developer costume).
- **E-03** All-caps eyebrows on every section.

### Decoration
- **F-01** Emoji feature icons where an icon system was skipped.
- **F-02** Fake dashboards / terminals / charts as decoration.
- **F-03** Metadata pills with no filtering, linking, or state semantics.
- **F-04** Glass panels without a scene behind them.

## Summary tests (all three must pass)

- **Decoration off** — hierarchy holds when borders, dividers, glows, gradients, and shadows are removed.
- **Motion off** — composition still communicates without any animation.
- **Identity** — page is identifiably *this* brand when logo and copy are swapped for a competitor's.

## Preserved v3.2 gates (still enforced)

- Palette source/provenance is accurate.
- Body text meets WCAG contrast.
- Type composition survives target viewports.
- Motion has a reduced-motion variant.
- Font fallback does not cause destructive CLS.

## Preserved v4 gates (still enforced)

- External asset provenance and license.
- Icon families chosen by brand voice, not category.
- No restricted marketplace scraping.

## Gate operation

For each blocker present, produce:

```
[BLOCKER-ID] · location · one-sentence reason · required correction
```

Corrections come from the fingerprint catalog and the doctrine documents. They are not "reduce the pattern" — they are specific compositional or structural changes.

## The final rule

> A design that meets every director's individual optimum can still fail the gate. Authenticity is the constraint the other directors optimize under, not a dimension they compete with.
