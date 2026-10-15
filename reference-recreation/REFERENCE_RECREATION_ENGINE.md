# Reference Recreation Engine v3

Purpose: turn user-provided screenshots, images, screen recordings or videos into a **measurable implementation specification**. Start with [one compact visual reference](../reference-engine/BRIEF_TO_REFERENCE.md) before expanding to the full site.

## Modes

- `inspired`: preserve design principles, not geometry.
- `structure-close`: match hierarchy, layout and responsive behavior.
- `pixel-close`: match visible geometry, spacing, typography metrics, colors and media framing at target viewports.
- `behavior-close`: match visible interaction/scroll timing and state transitions from video.

## Pipeline

1. **Intake** — record viewport/aspect ratio, source type, known breakpoints and target stack.
2. **Segment** — split page/video into hero, sections, transitions and interaction scenes.
3. **Geometry pass** — measure bounding relationships, alignment axes, gutters, max widths, section heights and media crops.
4. **Type pass** — infer role, weight, casing, tracking, line-height and approximate scale. Do not assume a proprietary font is reusable.
5. **Color/material pass** — roles first, raw hex second; include opacity/blend/backdrop behavior.
6. **Motion pass** — create a timeline with triggers, states, progress windows, easing class and dependency order.
7. **Asset map** — identify user-provided/owned assets vs placeholders needed.
8. **Small preview** — one viewport-sized composition and one signature interaction, with a short note. The preview is a direction check, not a finished 1:1 claim.
9. **Implementation spec** — independent code; no source-code copying.
10. **Capture** — render exact target viewport screenshots/video.
11. **Compare** — geometry/color/type/motion/fidelity report.
12. **Iterate** — fix largest structural error first, not micro pixels first.

## Fidelity hierarchy

1. composition and section geometry
2. typography metrics
3. media framing
4. color/material hierarchy
5. motion state timing
6. micro spacing and decorative details

A recreation should not be declared “1:1” merely because it feels similar.
