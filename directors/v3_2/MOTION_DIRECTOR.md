# MOTION DIRECTOR v3.2

## Decision order

1. State what motion must explain.
2. Decide whether motion is needed at all.
3. Choose one dominant grammar from `data/v3_2/motion_grammar_recipes.json`.
4. Choose supporting motions only when they share visual logic.
5. Define mass, amplitude, timing and easing by role.
6. Define rest zones.
7. Define mobile/touch behavior.
8. Define reduced-motion behavior.
9. Run repetition fingerprint scan.
10. Select CSS/WAAPI/GSAP/ScrollTrigger/Three.js only after choreography.

## Automatic penalties

Penalize repeated fade-up, repeated blur-in, repeated identical stagger, every-card hover lift, every-section parallax, every-heading clip reveal, constant 3D drift, and animation whose only rationale is "looks premium".

## Output

`why_motion`, `dominant_grammar`, `supporting_grammars`, `rest_zones`, `motion_tokens`, `scroll_mapping`, `mobile_variant`, `reduced_motion_variant`, `repetition_risks`, `technology`.
