# Scroll System v3

Scroll is authored as **state choreography**, not scattered `onEnter` animations.

## Required authoring order

1. define section narrative purpose,
2. define scroll states (`S0..Sn`),
3. define normalized progress windows,
4. select one dominant scroll recipe,
5. add at most two supporting recipes per scene,
6. choose implementation technology,
7. author mobile recomposition,
8. author reduced-motion behavior,
9. define cleanup/resizing behavior,
10. run performance and readability gates.

## Technology selection

Prefer the smallest sufficient tool:

- CSS transitions/keyframes: local state changes
- CSS Scroll-Driven Animations: simple browser-native progress mapping when compatibility is acceptable
- IntersectionObserver: enter/leave state changes, not continuous scrubbing
- GSAP + ScrollTrigger: complex pin/scrub/timeline choreography
- native sticky positioning: stable pinned layouts where JS is unnecessary
- requestAnimationFrame: custom rendering loops only when unavoidable
- Three.js/R3F: only when 3D is part of the concept

Smooth-scroll libraries must not become the source of truth for content position. Native scrolling, focus, anchors and accessibility must still work.
