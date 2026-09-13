# SCROLL DIRECTOR v3.1

Scroll is a state machine driven by user progress.

## Before choosing a library

Define:
- narrative purpose
- section ownership
- start/end triggers
- normalized progress ranges
- pinned vs natural flow
- element entering/leaving states
- handoff to next section
- media/camera timeline
- interruption/reverse behavior
- touch/mobile recomposition
- reduced-motion alternative
- performance budget

## Choreography grammar

`approach → acquire → transform → transfer → release`

Not every section needs every phase.

## Technology order

Use normal document flow/sticky/CSS first when sufficient. Use IntersectionObserver for discrete state entry. Use scroll-driven CSS where support/fallback is acceptable. Use GSAP/ScrollTrigger for complex synchronized timelines. Use Three.js only when the visual concept requires a 3D scene.

## Hard failures

- universal fade-up used as the dominant motion language
- pinning without clear release/handoff
- desktop scrub timeline forced onto small touch screens
- animation tied directly to noisy scroll events without scheduling/throttling strategy
- layout thrashing inside frame loops
- hidden content becoming inaccessible when JS/motion is unavailable
- reduced-motion mode merely makes durations shorter instead of removing problematic movement
