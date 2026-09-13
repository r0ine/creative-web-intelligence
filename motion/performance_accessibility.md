# Motion — Performance & Accessibility

Entries: **13**

## MOT-006 — Use frame-rate-independent damping

Interactive follow motion should use delta-aware damping/springs.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** engineering

## MOT-007 — Centralize frame loops

Avoid unmanaged requestAnimationFrame loops per module.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** performance

## MOT-008 — Pause inactive work

Use visibility/offscreen signals to reduce animation work.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** performance

## MOT-009 — Prefer transforms for DOM motion

Use transform/opacity for common motion where possible.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** performance

## MOT-013 — Timelines should be inspectable

Use named timelines and labels for complex sequences.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** engineering

## MOT-016 — Hover must not be required

Touch and keyboard users need equivalent interaction paths.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** accessibility

## MOT-020 — Scramble effects are decorative

Do not scramble essential information or forms.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** accessibility

## MOT-022 — Reduced motion is centralized

All modules should subscribe to one motion-preference signal.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** accessibility

## MOT-031 — Do not stagger huge lists

Large repeated items need batching/virtualization, not theatrical delay.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** performance

## MOT-032 — Animate state, not CSS soup

Prefer named states/timelines over scattered property mutations.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** engineering

## MOT-033 — Measure animation performance

Track frame time and dropped frames on representative devices.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** performance

## MOT-040 — Animation cleanup is mandatory

Kill timelines/listeners/observers on unmount or route change.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** engineering

## MOT-041 — Resize should refresh timelines

Scroll ranges and text splits may change after resize/fonts load.

**Why:** Motion should be coherent, performant, accessible and tied to interaction or story.

**Tags:** engineering
