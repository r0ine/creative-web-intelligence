# Technical Baseline — August 2026

- Three.js WebGLRenderer targets WebGL2; WebGL1 is no longer supported in current docs.
- Three.js WebGPURenderer can choose WebGPU and fall back to WebGL2; treat as progressive/optional and test feature compatibility.
- React Three Fiber: do not set React state in frame loops; animate through frame-loop refs and reuse resources.
- GSAP ScrollTrigger supplies trigger/scrub/pin/snap primitives for complex choreography.
- CSS scroll-driven animations can map animation to scroll/view timelines, but use progressive enhancement because support can vary.
- Variable fonts can consolidate multiple style axes; still measure actual file size and load only needed glyph coverage.
- Core Web Vitals good targets: LCP <= 2.5s, INP <= 200ms, CLS <= 0.1.
- WCAG 2.2 minimum normal-text contrast target is 4.5:1; large text 3:1.
