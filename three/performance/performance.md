# 3D / Performance

Entries: **21**

- **3D-011 Dispose GPU resources** — Clean geometry, materials, textures and render targets when ownership ends. _(tags: performance)_
- **3D-012 Centralize renderer configuration** — DPR, tone mapping, shadows and color management should be deliberate. _(tags: renderer)_
- **3D-013 Cap DPR** — High-DPI screens can multiply pixel cost; expose min/max/adaptive DPR. _(tags: performance)_
- **3D-014 Quality tiers are first-class** — Low/medium/high profiles should alter DPR, particles, shadows, post FX and LOD. _(tags: performance)_
- **3D-015 Measure sustained frame time** — Adaptive quality should respond to sustained performance, not one slow frame. _(tags: performance)_
- **3D-016 Avoid quality oscillation** — Use cooldown/hysteresis before raising/lowering quality repeatedly. _(tags: performance)_
- **3D-017 Use instancing for repetition** — Many identical meshes should use instancing where appropriate. _(tags: performance)_
- **3D-018 LOD for heavy scenes** — Provide distance/screen-size/quality-based level-of-detail options. _(tags: performance)_
- **3D-019 Frustum/offscreen awareness** — Do not update expensive systems when not visible unless continuity requires it. _(tags: performance)_
- **3D-020 Pause hidden tabs** — Browser visibility should reduce render/update workload. _(tags: performance)_
- **3D-021 Avoid React state in frame loops** — R3F animation should mutate refs/external state rather than setState each frame. _(tags: r3f)_
- **3D-022 Do not mount heavy scenes indiscriminately** — Scene lifecycle affects compilation and resource cost. _(tags: r3f)_
- **3D-064 Preload hero assets only** — Lazy-load secondary experiences where possible. _(tags: performance)_
- **3D-069 Mobile is separately art-directed** — Reduce effects and reposition model/camera intentionally. _(tags: responsive)_
- **3D-070 No hover-only mechanics** — Touch input needs equivalent controls. _(tags: responsive)_
- **3D-071 Fallback can be image/video/DOM** — Unsupported or weak WebGL should still communicate core content. _(tags: responsive)_
- **3D-072 Reduced motion can simplify camera** — Use shorter/less parallax/static scene states without hiding content. _(tags: accessibility)_
- **3D-073 Critical text stays DOM** — Do not put SEO/accessibility-critical copy only in Canvas. _(tags: accessibility)_
- **3D-074 3D audio is optional** — Sound should never be required for navigation; user control is necessary. _(tags: accessibility)_
- **3D-075 Loading progress comes from manager** — Use real asset progress and explicit ready state. _(tags: loading)_
- **3D-076 Compile/warm-up can be staged** — Avoid a giant first-frame shader compilation spike where possible. _(tags: performance)_