# Scroll Technology Decision Matrix

| Need | Prefer | Notes |
|---|---|---|
| Simple DOM reveal tied to viewport progress | CSS scroll-driven animation | Progressive enhancement; keep fallback readable. |
| Sticky editorial composition | CSS `position: sticky` | Avoid JS when native layout is enough. |
| Complex pin + scrub + sequencing | GSAP ScrollTrigger | Centralize timelines and cleanup. |
| Persistent WebGL canvas controlled by scroll | R3F/Three.js + normalized progress; optionally ScrollTrigger | Keep continuous values outside React rerender loops. |
| Smooth input signal | Lenis only when justified | Never install just to claim “smooth scrolling”. |
| Video/frame scrubbing | Purpose-built media controller + ScrollTrigger | Preload, test seeking cost, mobile fallback required. |
| Horizontal story from vertical input | ScrollTrigger | Only if information architecture genuinely benefits. |

## Selection principle
Use the **least powerful tool that cleanly expresses the choreography**. Visual quality comes from art direction, timing and hierarchy—not the dependency count.
