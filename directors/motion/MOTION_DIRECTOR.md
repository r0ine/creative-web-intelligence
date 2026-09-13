# MOTION DIRECTOR v2

## Motion hierarchy
Every scene gets one dominant motion idea. Secondary motion must support it.

## Decide
- trigger: time / scroll / hover / drag / route / state
- mapping: triggered vs scrubbed
- mass: light / medium / heavy
- continuity: persistent / entering / exiting
- emphasis level: 0-3
- reduced-motion alternative

## Technology decision
Use native CSS transitions/animations for simple compositor-friendly states. Consider CSS scroll-driven animations for progressive-enhancement cases; use GSAP/ScrollTrigger when choreography, pinning, complex scrubbed timelines or broad control is required.

## Anti-patterns
No universal fade-up. No constant motion. No identical easing for camera, UI and tiny microinteractions. No hover-only critical actions.
