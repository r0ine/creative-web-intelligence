# Motion Intelligence

Total rules: **52**

These are reusable design/engineering rules synthesized from verified standards, indexed creator material, current award galleries, studios, and creative-development sources. They are not laws; project context wins.

## MOT-001 — Create one motion language

**Rule:** Define shared easing/duration/weight principles for UI, text, camera and objects.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** system  
**Confidence:** `SYNTHESIZED`

## MOT-002 — Motion needs purpose

**Rule:** Animation should communicate state, hierarchy, causality, spatial change or narrative progression.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** principle  
**Confidence:** `SYNTHESIZED`

## MOT-003 — Avoid universal fade-up

**Rule:** Do not attach opacity+translateY to every element.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** anti-slop  
**Confidence:** `SYNTHESIZED`

## MOT-004 — Use stillness

**Rule:** Not everything should move continuously; rest makes motion meaningful.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** restraint  
**Confidence:** `SYNTHESIZED`

## MOT-005 — Different masses move differently

**Rule:** Large 3D objects, UI labels and camera should not share identical timing.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** weight  
**Confidence:** `SYNTHESIZED`

## MOT-006 — Use frame-rate-independent damping

**Rule:** Interactive follow motion should use delta-aware damping/springs.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** engineering  
**Confidence:** `SYNTHESIZED`

## MOT-007 — Centralize frame loops

**Rule:** Avoid unmanaged requestAnimationFrame loops per module.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## MOT-008 — Pause inactive work

**Rule:** Use visibility/offscreen signals to reduce animation work.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## MOT-009 — Prefer transforms for DOM motion

**Rule:** Use transform/opacity for common motion where possible.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## MOT-010 — Scroll is a normalized signal

**Rule:** Expose 0..1 progress that can drive DOM, WebGL and shaders.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** scroll  
**Confidence:** `SYNTHESIZED`

## MOT-011 — Velocity is secondary

**Rule:** Scroll velocity can add inertia but should not overpower content.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** scroll  
**Confidence:** `SYNTHESIZED`

## MOT-012 — Pinned scenes need chapters

**Rule:** Map ranges of scroll to explicit states rather than dozens of unrelated tweens.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** scroll  
**Confidence:** `SYNTHESIZED`

## MOT-013 — Timelines should be inspectable

**Rule:** Use named timelines and labels for complex sequences.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** engineering  
**Confidence:** `SYNTHESIZED`

## MOT-014 — Transitions should preserve context

**Rule:** Persistent objects/camera continuity can make section changes feel spatial.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** storytelling  
**Confidence:** `SYNTHESIZED`

## MOT-015 — Route transitions should be brief

**Rule:** Do not hide navigation speed behind long cinematic transitions.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** ux  
**Confidence:** `SYNTHESIZED`

## MOT-016 — Hover must not be required

**Rule:** Touch and keyboard users need equivalent interaction paths.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** accessibility  
**Confidence:** `SYNTHESIZED`

## MOT-017 — Magnetic motion must be small

**Rule:** Never make the user chase a button.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** interaction  
**Confidence:** `SYNTHESIZED`

## MOT-018 — Cursor effects are optional

**Rule:** Disable or simplify custom cursor logic on touch/coarse pointers.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** interaction  
**Confidence:** `SYNTHESIZED`

## MOT-019 — Text reveal unit must match content

**Rule:** Animate by line/word/character based on reading goal.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** typography  
**Confidence:** `SYNTHESIZED`

## MOT-020 — Scramble effects are decorative

**Rule:** Do not scramble essential information or forms.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** accessibility  
**Confidence:** `SYNTHESIZED`

## MOT-021 — Clip/mask reveals need fallback

**Rule:** Content must remain visible without animation.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** resilience  
**Confidence:** `SYNTHESIZED`

## MOT-022 — Reduced motion is centralized

**Rule:** All modules should subscribe to one motion-preference signal.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** accessibility  
**Confidence:** `SYNTHESIZED`

## MOT-023 — Camera follows slower than pointer

**Rule:** Subtle lag makes camera response weighted; direct 1:1 mapping often feels cheap.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** 3d  
**Confidence:** `SYNTHESIZED`

## MOT-024 — Avoid motion on every pointer move

**Rule:** Only selected scene elements should react.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** anti-slop  
**Confidence:** `SYNTHESIZED`

## MOT-025 — Scroll-scrub video should have poster fallback

**Rule:** Heavy video timelines need resilience.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** video  
**Confidence:** `SYNTHESIZED`

## MOT-026 — Do not smooth-scroll by default

**Rule:** Native scroll can be best; opt into smooth scrolling when it benefits the experience.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** scroll  
**Confidence:** `SYNTHESIZED`

## MOT-027 — One gesture should have one dominant response

**Rule:** Avoid cursor simultaneously rotating model, moving camera, warping shader and moving typography at full strength.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** restraint  
**Confidence:** `SYNTHESIZED`

## MOT-028 — Use easing families

**Rule:** Create UI, object and camera easing tokens instead of random cubic-bezier values.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** tokens  
**Confidence:** `SYNTHESIZED`

## MOT-029 — Keep durations contextual

**Rule:** Micro feedback fast; scene changes slower; loading intro short.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** tokens  
**Confidence:** `SYNTHESIZED`

## MOT-030 — Stagger by hierarchy

**Rule:** Stagger order should reflect reading/visual order.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** hierarchy  
**Confidence:** `SYNTHESIZED`

## MOT-031 — Do not stagger huge lists

**Rule:** Large repeated items need batching/virtualization, not theatrical delay.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## MOT-032 — Animate state, not CSS soup

**Rule:** Prefer named states/timelines over scattered property mutations.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** engineering  
**Confidence:** `SYNTHESIZED`

## MOT-033 — Measure animation performance

**Rule:** Track frame time and dropped frames on representative devices.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** performance  
**Confidence:** `SYNTHESIZED`

## MOT-034 — Post-processing can animate too

**Rule:** Bloom/DOF/color grade may transition between scene states, but subtly.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** 3d  
**Confidence:** `SYNTHESIZED`

## MOT-035 — Lighting transitions can replace UI effects

**Rule:** A light shift can reveal a feature more elegantly than adding overlays.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** 3d  
**Confidence:** `SYNTHESIZED`

## MOT-036 — Use motion to explain 3D construction

**Rule:** Assembly/exploded views should reveal relationships, not random movement.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** 3d  
**Confidence:** `SYNTHESIZED`

## MOT-037 — 3D motion should preserve orientation cues

**Rule:** Do not spin products so aggressively that users lose spatial understanding.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** 3d  
**Confidence:** `SYNTHESIZED`

## MOT-038 — Camera cuts are rare on web

**Rule:** Prefer interpolated moves unless a deliberate hard cut serves the concept.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** 3d  
**Confidence:** `SYNTHESIZED`

## MOT-039 — Pointer inertia should decay

**Rule:** Velocity-driven effects need a clear return to rest.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** interaction  
**Confidence:** `SYNTHESIZED`

## MOT-040 — Animation cleanup is mandatory

**Rule:** Kill timelines/listeners/observers on unmount or route change.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** engineering  
**Confidence:** `SYNTHESIZED`

## MOT-041 — Resize should refresh timelines

**Rule:** Scroll ranges and text splits may change after resize/fonts load.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** engineering  
**Confidence:** `SYNTHESIZED`

## MOT-042 — Loading exit belongs to timeline

**Rule:** Preloader, first scene and first headline should transition as one sequence.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** loading  
**Confidence:** `SYNTHESIZED`

## MOT-043 — Do not fake loading progress

**Rule:** Bind loaders to actual asset progress where possible.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** loading  
**Confidence:** `SYNTHESIZED`

## MOT-044 — Motion recipes need performance cost

**Rule:** Catalog low/medium/high motion/effect cost.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** library  
**Confidence:** `SYNTHESIZED`

## MOT-045 — Motion recipes need compatibility

**Rule:** Declare whether an effect works with smooth-scroll, R3F, mobile, reduced-motion.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** library  
**Confidence:** `SYNTHESIZED`

## MOT-046 — Motion recipes need parameters

**Rule:** Expose amplitude, damping, duration, easing, trigger and range.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** library  
**Confidence:** `SYNTHESIZED`

## MOT-047 — Reference analysis should capture timing relationships

**Rule:** Note which event triggers what and relative pace, not imagined exact milliseconds.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** research-method  
**Confidence:** `SYNTHESIZED`

## MOT-048 — Do not infer frame-perfect easing from inaccessible video

**Rule:** Mark it NEEDS_CAPTURE.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** research-method  
**Confidence:** `SYNTHESIZED`

## MOT-049 — Avoid perpetual decorative loops

**Rule:** Continuous idle loops need strong brand/ambient purpose.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** anti-slop  
**Confidence:** `SYNTHESIZED`

## MOT-050 — Use animation as transition between layouts

**Rule:** FLIP-like transformations can maintain object continuity when geometry changes.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** layout  
**Confidence:** `SYNTHESIZED`

## MOT-051 — 3D hover highlight should coordinate with DOM

**Rule:** Hovered model part and its label/card should share state.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** 3d  
**Confidence:** `SYNTHESIZED`

## MOT-052 — Interaction feedback should begin quickly

**Rule:** Even cinematic sites need prompt acknowledgment of input.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** ux  
**Confidence:** `SYNTHESIZED`
