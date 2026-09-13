# V5 Overview — Authenticity Correction

## The problem v5 addresses

The library's outputs at v4 were still fingerprinting as generated. Everywhere the outputs converged on the same patterns:

- horizontal divider lines slicing every section
- background grid overlays for "technical feel"
- bordered cards as the default rendering unit
- `opacity + translateY` as the universal scroll entrance
- centered eyebrow + huge grotesk + two CTAs + accent glow
- near-black surfaces with hairline strokes and one gradient blob

Every one of these was already named as an anti-pattern in the v4 library. The rules existed. They were not enforced.

## The change v5 makes

**Rules are no longer advice.** They are gate blockers. A design with any single v5 blocker cannot ship, regardless of how strong its other dimensions are.

The tools:

1. A stricter fingerprint catalog (`v5/ANTI_AI_VISUAL_FINGERPRINTS.md`) with per-pattern reasoning.
2. A blocker gate (`quality/V5_AUTHENTICITY_GATE.md`) that replaces the 0–3 score.
3. Six policy documents that make the doctrine explicit:
   - `DIVIDER_POLICY.md`
   - `MOTION_GRAMMAR_V2.md`
   - `COMPOSITION_RESTRAINT.md`
   - `TYPOGRAPHY_FIRST_PREMIUM.md`
   - `DECORATION_VS_STRUCTURE.md`
   - `REST_ZONES.md`
   - `COLOR_RESTRAINT.md`
4. A new Authenticity Director with veto power over other directors.
5. Updated composition, motion, and QA directors that enforce the doctrine.
6. A working static analyzer that flags the top 15+ patterns in real HTML/CSS/JS.

## The doctrine in one paragraph

Design quality is a property of hierarchy, typography, composition, and restraint. Decoration is what happens when those decisions were not made. If turning off every border, divider, glow, gradient, and animation collapses the design, the design was hiding behind decoration and no additional decoration will fix it. The fix is always: rework the composition and typography until they carry the meaning alone, then let decoration honestly support them.

## Compatibility

v5 is additive. v4 remains fully in force for color, typography, source intelligence, 3D, scroll, backend, and reference recreation. v5 changes how visual decisions are *gated*, not what they cover.

## Acceptance

A v5-compliant output:
- has no v5 blockers.
- has at most one high-severity fingerprint.
- passes the three summary tests (decoration off, motion off, identity).
- carries the `authenticity_gate_result: PASS` field in its spec.

A v5-compliant page reads as *less* decorated than a v4-style page — and reads as more considered. That is the intended result.
