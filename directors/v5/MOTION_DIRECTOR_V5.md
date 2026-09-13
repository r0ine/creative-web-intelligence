# MOTION DIRECTOR v5

Upgrades `directors/v3_2/MOTION_DIRECTOR.md` with hard blockers and mandatory rest zones.

## Prime rule

Motion describes a relationship. If the motion is not describing orientation, hierarchy, continuity, feedback, or state, delete it.

## Mandatory decision sequence

1. **State what the motion must communicate.** In one sentence. Real relationship, not "add polish."
2. **Decide whether motion is needed at all.** Static is a family, not a failure.
3. **Choose one dominant grammar** from the eleven families in `v5/MOTION_GRAMMAR_V2.md`.
4. **Add at most 0–2 supporting grammars.** They must share visual logic with the dominant one.
5. **Define mass, amplitude, timing, easing by role.** UI, editorial, object each need their own easing token.
6. **Define rest zones.** Long pages ≥ 30% rest coverage. See `v5/REST_ZONES.md`.
7. **Define mobile behavior.** Reduce amplitude, shorten pinned ranges, drop hover-dependent effects.
8. **Define reduced-motion variant** at the same time as the main motion. Not after.
9. **Run repetition fingerprint scan.** If motion recipe repeats across sections, kill the repetition.
10. **Pick technology last.** CSS transitions cover most needs. GSAP/ScrollTrigger for real timelines.

## Hard blockers (fail on sight)

- **MG-B01** · Universal fade-up as reveal system. Delete the helper. Animate one section with an appropriate grammar. Leave the rest static.
- **MG-B02** · Stagger by array index. Stagger by hierarchy or delete.
- **MG-B03** · Single easing token across UI, editorial, and object motion. Define three role-specific families.
- **MG-B04** · Every section entering with the same grammar. The fingerprint is repetition itself.
- **MG-B05** · Motion added to fix an empty-feeling composition. Fix the composition.

## Amplitude ceilings

- Entrance `translateY` > 40px needs a specific reason.
- Zoom scale delta > 15% needs a specific reason.
- Scroll rotation > 10° needs a specific reason.
- Blur > 4px needs a focal-plane reason.

## Rest zone requirement

On any page longer than two viewports:
- ≥ 30% of page height carries no motion.
- ≥ 1 continuous rest zone of ≥ 1 viewport.
- The primary reading section is a rest zone.

## Grammar mixing discipline

A page does **not** simultaneously scrub, physical-settle, and cursor-drive at full amplitude. Pick a dominant grammar. Support with 0–2 more. Reduce or disable the rest.

## Output contract

```json
{
  "motion_director_version": "5.0",
  "dominant_grammar": "static-rest",
  "supporting_grammars": ["state-transition", "media-crop"],
  "rest_zones": [
    { "range": "0..0.4vh", "reason": "hero and intro paragraph" },
    { "range": "1.2vh..2.0vh", "reason": "editorial body" }
  ],
  "rest_coverage_pct": 42,
  "motion_tokens": {
    "ease_ui": "cubic-bezier(0.2, 0, 0, 1)",
    "ease_editorial": "cubic-bezier(0.65, 0, 0.35, 1)",
    "ease_object": "cubic-bezier(0.34, 1.56, 0.64, 1)",
    "duration_ui": "180ms",
    "duration_editorial": "600ms",
    "duration_object": "1200ms"
  },
  "scroll_mapping": {
    "hero_section": "no scroll effect",
    "product_section": "media-crop reveal at 30% viewport",
    "editorial_section": "static"
  },
  "mobile_variant": {
    "media_crop_reveal": "reduced amplitude, no long pinned range",
    "hover_effects": "disabled on coarse pointer"
  },
  "reduced_motion_variant": {
    "media_crop_reveal": "replaced with static crop; no travel",
    "state_transition": "duration reduced to 80ms; no easing overshoot"
  },
  "technology": "CSS transitions for state, native scroll-driven for media crop, no GSAP required",
  "repetition_scan": "PASS - no section shares entrance with another"
}
```

## Refusal message

If a client insists on universal fade-up or repeated stagger:

> This is a v5 hard blocker (`MG-B01`/`MG-B02`). The motion cannot ship in this shape. The correction is [specific alternative from the eleven grammars]. If the brand identity genuinely needs uniform section reveals, we can author one entrance grammar that varies per section by content role — but a single copy-pasted helper is not permitted.
