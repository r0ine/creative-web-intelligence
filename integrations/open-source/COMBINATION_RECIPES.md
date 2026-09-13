# Curated Integration Stacks

These are **capability stacks**, not visual templates.

## Cinematic React 3D product
`three` + `@react-three/fiber` + `@react-three/drei` + optional `@react-three/postprocessing` + one scroll adapter + Motion for DOM.

Use when a persistent model/camera story is central. Keep post-processing optional and mobile quality adaptive.

## Shader-first minimal experience
`ogl` or direct Three.js + local shader modules + Tweakpane in development.

Use when custom shader control matters more than a large helper ecosystem. Do not add R3F merely for branding.

## High-performance 2D interactive page
`pixi.js` + Motion for surrounding DOM + Floating UI/Radix for accessible overlays.

Use for sprite/particle/canvas-heavy 2D scenes.

## Accessible art-directed marketing UI
Radix Primitives + Floating UI + selectively ingested shadcn/Origin UI behavior + local Design DNA + Motion.

Use accessibility primitives but overwrite visual defaults.

## Creative component prototype
One or two components from Motion Primitives / Magic UI / UI Layouts / Kokonut UI, normalized into internal recipe schema.

Never combine all of them in one project.

## Authored 3D sequence
Three/R3F + Theatre.js core; Theatre Studio only in development. Export/ship only the runtime needed.

## Server-rendered creative transitions
Swup **or** Barba + Motion/GSAP-like project animator. Choose one route owner. Prefer native View Transitions when they fully satisfy requirements and browser support policy.

## Interaction-heavy 3D
R3F + use-gesture + React Spring or Motion + optional Rapier when actual physical simulation is required.

Scripted easing should remain scripted; do not turn every interaction into physics.
