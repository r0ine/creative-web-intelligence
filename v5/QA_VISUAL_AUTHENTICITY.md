# QA Visual Authenticity v5

This gate replaces `anti-ai/v3_2/VISUAL_FINGERPRINT_GATE.md` (the 0–3 score model) with a **blocker gate**.

## Why the score model was wrong

The 0–3 fingerprint score allowed weak designs to pass by averaging. A page could accumulate 2/3 on divider repetition, 2/3 on cardification, and 2/3 on motion repetition — a total that "reads as passing" under most rubrics — and still be maximally AI-looking.

The score also implied that "less of the pattern" was the fix. It is not. The fix is a compositional decision that removes the pattern entirely.

## The gate

Any single **blocker** is a fail. No averaging. No exceptions for other strengths.

## Blocker categories

### Category A — Line and border

- **[A-01]** More than one hairline divider between top-level sections
- **[A-02]** Global background grid overlay for atmosphere
- **[A-03]** Repeated identical `border` on non-interactive containers
- **[A-04]** Register / corner marks placed for atmosphere

### Category B — Motion

- **[B-01]** Universal fade-up entrance across multiple sections
- **[B-02]** Repeated stagger ladder (`index * 0.1s`)
- **[B-03]** Same easing/duration across UI, editorial, and object motion
- **[B-04]** Every section entering with the same grammar
- **[B-05]** Zero rest zones on a page longer than two viewports

### Category C — Composition

- **[C-01]** Cardification: > 60% of leaf content blocks share identical container shape
- **[C-02]** Repeated centered-hero cliché (eyebrow + huge grotesk + two CTAs + glow)
- **[C-03]** Bento layout with no content-density justification
- **[C-04]** Every section using identical geometry (max-width, header pattern, grid rhythm)

### Category D — Color

- **[D-01]** Default dark surface + hairlines + single accent glow with no chosen surface strategy
- **[D-02]** Unmotivated blue-purple gradient identity
- **[D-03]** Gradient text fill on hero headline
- **[D-04]** Three or more high-chroma colors competing at similar area weight

### Category E — Typography

- **[E-01]** Hierarchy expressed only through size (no weight/width/case/tracking/family axis)
- **[E-02]** Monospace used for body copy (developer costume)
- **[E-03]** All-caps eyebrows on every section

### Category F — Decoration

- **[F-01]** Emoji feature icons where a chosen icon system was skipped
- **[F-02]** Fake dashboards / terminals / charts as decoration
- **[F-03]** Metadata pills with no filtering, linking, or state semantics
- **[F-04]** Glass panels without a scene behind them

## Gate operation

For each blocker present in the design, produce:

```
[BLOCKER-ID] · location · one-sentence reason it is present · required correction
```

Example:

```
[B-01] · sections#features, #testimonials, #pricing · all three use the same fade-up-30 helper
        · delete the helper; choose one section for a distinct entrance; leave the others static
```

**A build with any blocker cannot ship.** Corrections are not "reduce the pattern." They are the specific reworks in `ANTI_AI_VISUAL_FINGERPRINTS.md` and the policy documents.

## The three summary tests

After the blocker gate passes, run three summary tests. These are pass/fail interpretive tests — not scores.

### Test 1 — The decoration-off test

Turn off every border, divider, glow, gradient, background pattern, and shadow. Does the composition still communicate?

- **Yes** — decoration was doing honest supporting work. Pass.
- **No** — decoration was carrying the composition. Rework.

### Test 2 — The motion-off test

Turn off every animation, scroll effect, and hover response. Does the composition still communicate?

- **Yes** — motion was doing honest supporting work. Pass.
- **No** — motion was carrying the composition. Rework.

### Test 3 — The identity test

If the logo and copy were replaced with a competitor's, would this page still be identifiably *this* brand?

- **Yes** — the design has identity. Pass.
- **No** — the design is generic. Rework.

## The final gate output

The V5 Authenticity Gate produces one of three states:

- **PASS** — no blockers, all three summary tests pass.
- **PASS WITH NOTES** — no blockers, one or more medium/low fingerprints logged for a follow-up.
- **FAIL** — one or more blockers, or one or more summary tests failed.

There is no numeric score. The design either meets the doctrine or it does not.
