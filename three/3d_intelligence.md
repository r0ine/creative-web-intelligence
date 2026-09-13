# 3D Intelligence

Total rules: **92**

These are reusable design/engineering rules synthesized from verified standards, indexed creator material, current award galleries, studios, and creative-development sources. They are not laws; project context wins.

## 3D-001 — 3D must have a role

**Rule:** Classify 3D as product, navigation, narrative, atmosphere, explanation or interaction before building.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** purpose  
**Confidence:** `SYNTHESIZED`

## 3D-002 — Do not bolt model onto template

**Rule:** If removing the model leaves the same experience, integration is weak.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** anti-slop  
**Confidence:** `SYNTHESIZED`

## 3D-003 — Use one dominant 3D concept

**Rule:** Assembly, world exploration, camera journey or configurator should lead; secondary tricks support it.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** concept  
**Confidence:** `SYNTHESIZED`

## 3D-004 — Scene graph must be organized

**Rule:** Separate environment, hero object, interactive objects, effects, lights and controllers.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** architecture  
**Confidence:** `SYNTHESIZED`

## 3D-005 — Keep logic outside giant components

**Rule:** Use dedicated camera, asset, scene-state, interaction and effect modules.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** architecture  
**Confidence:** `SYNTHESIZED`

## 3D-006 — Prefer glTF/GLB for web models

**Rule:** Use GLTFLoader and standard compression paths for production assets.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-007 — Support Draco when assets use it

**Rule:** Loader pipeline should accept DRACO compressed geometry.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-008 — Support KTX2 compressed textures

**Rule:** Use KTX2 paths where projects ship compressed GPU textures.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-009 — Support Meshopt

**Rule:** Asset pipeline should accept meshopt-decoded glTF when used.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-010 — Cache loaded assets

**Rule:** Avoid duplicate model/texture loads across scenes/routes.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-011 — Dispose GPU resources

**Rule:** Clean geometry, materials, textures and render targets when ownership ends.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## 3D-012 — Centralize renderer configuration

**Rule:** DPR, tone mapping, shadows and color management should be deliberate.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** renderer  
**Confidence:** `SYNTHESIZED`

## 3D-013 — Cap DPR

**Rule:** High-DPI screens can multiply pixel cost; expose min/max/adaptive DPR.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## 3D-014 — Quality tiers are first-class

**Rule:** Low/medium/high profiles should alter DPR, particles, shadows, post FX and LOD.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## 3D-015 — Measure sustained frame time

**Rule:** Adaptive quality should respond to sustained performance, not one slow frame.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## 3D-016 — Avoid quality oscillation

**Rule:** Use cooldown/hysteresis before raising/lowering quality repeatedly.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## 3D-017 — Use instancing for repetition

**Rule:** Many identical meshes should use instancing where appropriate.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## 3D-018 — LOD for heavy scenes

**Rule:** Provide distance/screen-size/quality-based level-of-detail options.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## 3D-019 — Frustum/offscreen awareness

**Rule:** Do not update expensive systems when not visible unless continuity requires it.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## 3D-020 — Pause hidden tabs

**Rule:** Browser visibility should reduce render/update workload.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## 3D-021 — Avoid React state in frame loops

**Rule:** R3F animation should mutate refs/external state rather than setState each frame.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** r3f  
**Confidence:** `SYNTHESIZED`

## 3D-022 — Do not mount heavy scenes indiscriminately

**Rule:** Scene lifecycle affects compilation and resource cost.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** r3f  
**Confidence:** `SYNTHESIZED`

## 3D-023 — Camera is part of composition

**Rule:** Treat focal length, distance, target and framing as design variables.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** camera  
**Confidence:** `SYNTHESIZED`

## 3D-024 — Use camera states

**Rule:** Define named hero/detail/feature/outro camera states.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** camera  
**Confidence:** `SYNTHESIZED`

## 3D-025 — Interpolate camera target

**Rule:** Position and look-at target should transition together.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** camera  
**Confidence:** `SYNTHESIZED`

## 3D-026 — Separate pointer influence from authored path

**Rule:** Cursor response should be a small offset layered on top of the main camera state.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** camera  
**Confidence:** `SYNTHESIZED`

## 3D-027 — Camera paths need orientation strategy

**Rule:** Path travel can follow tangent, look at target or interpolate authored rotation.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** camera  
**Confidence:** `SYNTHESIZED`

## 3D-028 — Responsive camera states

**Rule:** Mobile may need different FOV/distance/target, not a scaled desktop camera.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** camera  
**Confidence:** `SYNTHESIZED`

## 3D-029 — Avoid random orbiting

**Rule:** Camera movement should reveal content or maintain composition.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** camera  
**Confidence:** `SYNTHESIZED`

## 3D-030 — Use damping for camera follow

**Rule:** Smooth follow generally feels more physical than direct mapping.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** camera  
**Confidence:** `SYNTHESIZED`

## 3D-031 — Preserve safe UI zones

**Rule:** Camera framing should keep key model details clear of persistent DOM overlays.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** camera  
**Confidence:** `SYNTHESIZED`

## 3D-032 — Lighting is hierarchy

**Rule:** Key/fill/rim/environment roles should direct attention.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** lighting  
**Confidence:** `SYNTHESIZED`

## 3D-033 — Limit random point lights

**Rule:** More lights do not equal better lighting.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** lighting  
**Confidence:** `SYNTHESIZED`

## 3D-034 — Transition lights with scene state

**Rule:** Feature focus can be communicated by light changes.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** lighting  
**Confidence:** `SYNTHESIZED`

## 3D-035 — Environment maps need budget

**Rule:** HDR environment resolution should match reflection importance.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** lighting  
**Confidence:** `SYNTHESIZED`

## 3D-036 — Shadows need selective quality

**Rule:** Use only where they improve form/depth; shadow maps are expensive.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** lighting  
**Confidence:** `SYNTHESIZED`

## 3D-037 — Material language should be coherent

**Rule:** Metal, plastic, glass, ceramic etc. need a shared art direction.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** materials  
**Confidence:** `SYNTHESIZED`

## 3D-038 — Do not max all PBR properties

**Rule:** Roughness, metalness, clearcoat, transmission should follow plausible/material intent.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** materials  
**Confidence:** `SYNTHESIZED`

## 3D-039 — Shared materials need ownership rules

**Rule:** Animating one instance can affect multiple meshes if materials are shared.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** materials  
**Confidence:** `SYNTHESIZED`

## 3D-040 — Emissive is not bloom

**Rule:** Emissive values and post-processing should be tuned separately.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** materials  
**Confidence:** `SYNTHESIZED`

## 3D-041 — Use shaders only when standard materials are insufficient

**Rule:** GLSL complexity requires a visual reason.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** shaders  
**Confidence:** `SYNTHESIZED`

## 3D-042 — Standardize common uniforms

**Rule:** Time/progress/pointer/resolution/velocity can be optional shared interfaces.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** shaders  
**Confidence:** `SYNTHESIZED`

## 3D-043 — Shader effects should be composable

**Rule:** Noise, fresnel, dissolve, distortion and masks should be primitives.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** shaders  
**Confidence:** `SYNTHESIZED`

## 3D-044 — Avoid shader soup

**Rule:** Do not combine chromatic distortion, noise, fresnel, scanlines and dissolve by default.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** shaders  
**Confidence:** `SYNTHESIZED`

## 3D-045 — GPGPU particles need quality fallback

**Rule:** Particle count/compute complexity should scale down.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** shaders  
**Confidence:** `SYNTHESIZED`

## 3D-046 — Use particles with meaning

**Rule:** Atmosphere, data, formation or trails are stronger than random stars.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** particles  
**Confidence:** `SYNTHESIZED`

## 3D-047 — Particle systems need interaction budgets

**Rule:** Pointer and scroll forces should not require CPU updates for every particle.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** particles  
**Confidence:** `SYNTHESIZED`

## 3D-048 — Post-processing is opt-in

**Rule:** Bloom, DOF, SSAO, vignette, noise and chromatic aberration should not all be enabled.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** postfx  
**Confidence:** `SYNTHESIZED`

## 3D-049 — Selective bloom beats whole-scene glow

**Rule:** Apply bloom to intended emissive elements where feasible.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** postfx  
**Confidence:** `SYNTHESIZED`

## 3D-050 — DOF must preserve information

**Rule:** Do not blur essential product details or text.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** postfx  
**Confidence:** `SYNTHESIZED`

## 3D-051 — Chromatic aberration should be subtle

**Rule:** Heavy aberration quickly reads as effect-first design.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** postfx  
**Confidence:** `SYNTHESIZED`

## 3D-052 — Color grading connects DOM and WebGL

**Rule:** Scene tone should match surrounding interface palette.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** postfx  
**Confidence:** `SYNTHESIZED`

## 3D-053 — DOM anchor projection is a core primitive

**Rule:** Project 3D points to viewport coordinates for labels/hotspots.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** dom-bridge  
**Confidence:** `SYNTHESIZED`

## 3D-054 — World labels need visibility rules

**Rule:** Hide labels behind camera/offscreen and handle overlap.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** dom-bridge  
**Confidence:** `SYNTHESIZED`

## 3D-055 — Hotspots need focus states

**Rule:** Hover/click/focus/touch should lead to clear scene/UI feedback.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** interaction  
**Confidence:** `SYNTHESIZED`

## 3D-056 — Exploded view needs authored transforms

**Rule:** Parts should separate along meaningful axes or explicit target transforms.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-057 — Exploded view should reassemble

**Rule:** Store origin transforms so the model can return precisely.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-058 — Part metadata matters

**Rule:** Name model parts and attach semantic IDs for features/hotspots.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-059 — Model transitions need normalized progress

**Rule:** Assembly/disassembly should expose 0..1 for scroll/timeline binding.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-060 — Morph targets need safe ranges

**Rule:** Validate model-specific morph target indexes and limits.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-061 — Animation clips need state control

**Rule:** Do not autoplay all clips; map clips to scene/story states.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-062 — Model bounds utilities are essential

**Rule:** Center/fit/framing helpers reduce repeated setup work.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-063 — Asset manager needs errors

**Rule:** Missing model/texture should produce clear fallback, not blank canvas.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** models  
**Confidence:** `SYNTHESIZED`

## 3D-064 — Preload hero assets only

**Rule:** Lazy-load secondary experiences where possible.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## 3D-065 — Canvas can persist across routes

**Rule:** Persistent renderer can reduce reinitialization for immersive multi-page experiences.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** architecture  
**Confidence:** `SYNTHESIZED`

## 3D-066 — Persistent scenes need explicit teardown/state swap

**Rule:** Retained GPU resources need lifecycle ownership.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** architecture  
**Confidence:** `SYNTHESIZED`

## 3D-067 — Scene states should be serializable where practical

**Rule:** Config-driven camera/object/light states help agent authoring and devtools.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** architecture  
**Confidence:** `SYNTHESIZED`

## 3D-068 — Allow escape hatches

**Rule:** Advanced projects need direct Three.js object/material/uniform access.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** architecture  
**Confidence:** `SYNTHESIZED`

## 3D-069 — Mobile is separately art-directed

**Rule:** Reduce effects and reposition model/camera intentionally.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** responsive  
**Confidence:** `SYNTHESIZED`

## 3D-070 — No hover-only mechanics

**Rule:** Touch input needs equivalent controls.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** responsive  
**Confidence:** `SYNTHESIZED`

## 3D-071 — Fallback can be image/video/DOM

**Rule:** Unsupported or weak WebGL should still communicate core content.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** responsive  
**Confidence:** `SYNTHESIZED`

## 3D-072 — Reduced motion can simplify camera

**Rule:** Use shorter/less parallax/static scene states without hiding content.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** accessibility  
**Confidence:** `SYNTHESIZED`

## 3D-073 — Critical text stays DOM

**Rule:** Do not put SEO/accessibility-critical copy only in Canvas.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** accessibility  
**Confidence:** `SYNTHESIZED`

## 3D-074 — 3D audio is optional

**Rule:** Sound should never be required for navigation; user control is necessary.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** accessibility  
**Confidence:** `SYNTHESIZED`

## 3D-075 — Loading progress comes from manager

**Rule:** Use real asset progress and explicit ready state.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** loading  
**Confidence:** `SYNTHESIZED`

## 3D-076 — Compile/warm-up can be staged

**Rule:** Avoid a giant first-frame shader compilation spike where possible.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## 3D-077 — Renderer stats belong in devtools

**Rule:** Expose draw calls, triangles, textures and frame time during development.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** devtools  
**Confidence:** `SYNTHESIZED`

## 3D-078 — Camera recorder speeds authoring

**Rule:** Allow capturing position/target/FOV into named states.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** devtools  
**Confidence:** `SYNTHESIZED`

## 3D-079 — Timeline scrubber helps polish

**Rule:** Manual scroll/progress scrub reveals transition problems.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** devtools  
**Confidence:** `SYNTHESIZED`

## 3D-080 — Shader inspector helps debugging

**Rule:** Expose uniform values and quality mode.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** devtools  
**Confidence:** `SYNTHESIZED`

## 3D-081 — WebGPU should remain optional

**Rule:** Do not make emerging renderer paths mandatory if WebGL is the broad fallback.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** future  
**Confidence:** `SYNTHESIZED`

## 3D-082 — Procedural worlds need deterministic seeds when reproducibility matters

**Rule:** Agent demos/tests should be repeatable.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** procedural  
**Confidence:** `SYNTHESIZED`

## 3D-083 — 3D configurator needs state schema

**Rule:** Variant, material, camera and selected-part states should be serializable.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** configurator  
**Confidence:** `SYNTHESIZED`

## 3D-084 — Configurator changes should not reload the world

**Rule:** Swap material/mesh variants efficiently.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** configurator  
**Confidence:** `SYNTHESIZED`

## 3D-085 — Annotated product story needs section mapping

**Rule:** Each content chapter should map to a model/camera/light state.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** storytelling  
**Confidence:** `SYNTHESIZED`

## 3D-086 — World exploration needs navigation aids

**Rule:** Free camera experiences need orientation, reset or chapter landmarks.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** navigation  
**Confidence:** `SYNTHESIZED`

## 3D-087 — Game-like portfolio needs input onboarding

**Rule:** Keyboard/mouse/touch controls must be discoverable without long instructions.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** navigation  
**Confidence:** `SYNTHESIZED`

## 3D-088 — Use 3D space as information architecture only when justified

**Rule:** Spatial navigation can be memorable but may slow simple tasks.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** ux  
**Confidence:** `SYNTHESIZED`

## 3D-089 — Do not recreate random chrome-sphere trend

**Rule:** Generic shiny primitives are a visual anti-pattern unless conceptually justified.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** anti-slop  
**Confidence:** `SYNTHESIZED`

## 3D-090 — Do not default to black void

**Rule:** Choose environment based on product/brand/story.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** anti-slop  
**Confidence:** `SYNTHESIZED`

## 3D-091 — Do not add starfield automatically

**Rule:** Particles need a narrative/atmospheric reason.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** anti-slop  
**Confidence:** `SYNTHESIZED`

## 3D-092 — Do not make every product spin forever

**Rule:** Idle animation should be subtle or state-driven.

**Why:** 3D web quality depends on purpose, composition, rendering discipline and integration with content.

**Tags:** anti-slop  
**Confidence:** `SYNTHESIZED`
