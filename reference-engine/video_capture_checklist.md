# Video / Reel Capture Checklist

For frame-level analysis, capture or upload the video/screen recording. Then record:

- viewport/aspect ratio
- first-frame composition
- font role changes
- palette/background transitions
- section boundaries
- scroll or gesture trigger
- camera path / target changes
- model transforms / exploded states
- DOM↔3D overlaps
- lighting changes
- shader/postFX evidence
- loader/intro behavior
- hover/cursor/drag behavior
- final CTA/exit state

Do not invent exact CSS/GSAP/Three.js implementation from pixels alone; map observed behavior to multiple plausible engine choices and choose the simplest production approach.
