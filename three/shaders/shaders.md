# 3D / Shaders

Entries: **12**

- **3D-041 Use shaders only when standard materials are insufficient** — GLSL complexity requires a visual reason. _(tags: shaders)_
- **3D-042 Standardize common uniforms** — Time/progress/pointer/resolution/velocity can be optional shared interfaces. _(tags: shaders)_
- **3D-043 Shader effects should be composable** — Noise, fresnel, dissolve, distortion and masks should be primitives. _(tags: shaders)_
- **3D-044 Avoid shader soup** — Do not combine chromatic distortion, noise, fresnel, scanlines and dissolve by default. _(tags: shaders)_
- **3D-045 GPGPU particles need quality fallback** — Particle count/compute complexity should scale down. _(tags: shaders)_
- **3D-046 Use particles with meaning** — Atmosphere, data, formation or trails are stronger than random stars. _(tags: particles)_
- **3D-047 Particle systems need interaction budgets** — Pointer and scroll forces should not require CPU updates for every particle. _(tags: particles)_
- **3D-048 Post-processing is opt-in** — Bloom, DOF, SSAO, vignette, noise and chromatic aberration should not all be enabled. _(tags: postfx)_
- **3D-049 Selective bloom beats whole-scene glow** — Apply bloom to intended emissive elements where feasible. _(tags: postfx)_
- **3D-050 DOF must preserve information** — Do not blur essential product details or text. _(tags: postfx)_
- **3D-051 Chromatic aberration should be subtle** — Heavy aberration quickly reads as effect-first design. _(tags: postfx)_
- **3D-052 Color grading connects DOM and WebGL** — Scene tone should match surrounding interface palette. _(tags: postfx)_