# Media Decision Engine v6

The central routing system for all visual medium decisions. Every visual moment on a page passes through this engine before a medium is selected.

## Prime rule

**Choose the simplest medium capable of delivering the intended experience.** Not the most technically impressive. Not the one that "feels more premium." The simplest one that works.

## The medium spectrum

Ordered from simplest to most complex. Prefer earlier entries unless a later one is genuinely required.

| Medium | Cost | Use when |
|:--|:--|:--|
| **No visual** | Zero | The content communicates without imagery. Typography and space carry it. |
| **CSS-only** | Minimal | Color, gradient, shape, simple transition. No external asset needed. |
| **SVG** | Low | Vector graphics, icons, simple illustration, authored line work. |
| **Static image** | Low | Photography, editorial art, product shots where no interaction is needed. |
| **Generated image** | Low–Med | Original artwork, illustration, or visualization where no stock/existing asset fits, and the image serves a real content purpose. |
| **CSS motion** | Low | Simple state transitions, hover responses, micro-interactions. |
| **SVG animation** | Low–Med | Authored vector animation with editorial control. |
| **Lottie / dotLottie** | Medium | Complex authored animation with precise frame control, exported from After Effects or similar. Lightweight playback. |
| **Rive** | Medium | Interactive state-machine animation. When animation responds to user state, not just time. |
| **Video** | Medium | Cinematic content with sound or complex motion where scroll control is not needed. |
| **Scroll-controlled video** | Med–High | Video whose playback is driven by scroll position. Requires careful encoding. |
| **Frame sequence** | Med–High | Scroll-scrubbed visual narrative. Individual frames rendered to canvas. Higher fidelity than compressed video, more control. |
| **Canvas / procedural** | Med–High | Generative graphics, data visualization, particle systems with real data association. |
| **Pre-rendered 3D sequence** | Med–High | 3D scene with fixed camera path, high visual fidelity, no user interaction needed. Offline rendered, delivered as frame sequence. |
| **Real-time 3D (GLB/Three.js)** | High | Interactive 3D: user-controlled camera, object inspection, spatial exploration, configuration. |
| **WebGL/WebGPU shader** | High | Custom rendering effects that cannot be achieved with standard 3D or CSS. |

## Decision procedure

For each visual moment in the design:

### Step 1 — Purpose check

> Why does this visual exist?

- **Content** — it IS the thing being shown (product, artwork, data).
- **Identity** — it carries the brand's visual signature.
- **Explanation** — it makes a concept legible that words alone cannot.
- **Atmosphere** — it establishes an earned emotional context (not decoration).
- **State** — it communicates a system state or transition.
- **Storytelling** — it narrates a progression the user follows.

If none apply, the visual does not ship. The v5 decoration-vs-structure test (`v5/DECORATION_VS_STRUCTURE.md`) governs.

### Step 2 — Interaction check

Does the user need to:

- **View only** → static image, video, or pre-rendered sequence.
- **Scrub through a progression** → frame sequence or scroll-controlled video.
- **Inspect from multiple angles** → real-time 3D.
- **Configure or manipulate** → real-time 3D with interaction.
- **Trigger state changes** → Rive, Lottie with state, or CSS state transitions.

### Step 3 — Camera freedom check

- **No camera / fixed view** → 2D medium (image, video, sequence).
- **Fixed camera path** → pre-rendered 3D sequence (cheaper than realtime).
- **User-controlled camera** → real-time 3D.
- **Limited camera (orbit only)** → real-time 3D at minimal complexity.

### Step 4 — Fidelity check

- **Photorealistic / raytraced** → pre-rendered sequence (offline render quality exceeds realtime).
- **Stylized / low-poly / PBR standard** → real-time 3D is feasible.
- **Flat / vector / diagrammatic** → SVG or CSS.

### Step 5 — Performance check

Evaluate against `v6/PERFORMANCE_BUDGET_ENGINE.md`:

- Expected device tier (high-end desktop, average mobile, etc.)
- Network assumption (fast broadband, variable mobile)
- Transfer budget for this visual moment
- GPU budget (texture memory, draw calls)
- Concurrent animation budget

If the chosen medium exceeds the budget, **downgrade**:

```
real-time 3D → pre-rendered sequence → video → static image
frame sequence → video → static image
shader effect → CSS effect → static
```

The downgrade is not a failure. It is a correct decision.

### Step 6 — Mobile strategy

The mobile variant is decided **now**, not after desktop is built. See `v6/MOBILE_MEDIA_STRATEGY.md`.

Desktop and mobile may use different mediums for the same visual moment:

- Desktop: 180-frame AVIF sequence / Mobile: 80-frame WebP sequence
- Desktop: real-time 3D / Mobile: pre-rendered animation or static key visual
- Desktop: shader background / Mobile: CSS gradient

### Step 7 — Accessibility check

- `prefers-reduced-motion`: what is the static fallback?
- Screen reader: what text describes this visual moment?
- Keyboard: is the experience navigable without pointer?
- Essential information: does any critical content exist only inside the animation?

If essential content lives only inside the animation, the architecture is wrong. Fix the architecture — HTML carries content, media carries atmosphere and illustration.

### Step 8 — Output

```json
{
  "visual_moment": "hero product reveal",
  "purpose": "content — the product IS what is being shown",
  "interaction": "scrub through assembly progression",
  "camera_freedom": "fixed camera path",
  "fidelity": "PBR standard",
  "chosen_medium": "pre-rendered 3D frame sequence",
  "rationale": "fixed camera path + high fidelity + scroll control = pre-rendered sequence beats realtime 3D on cost and mobile performance",
  "desktop_variant": "180 frames AVIF at 1920w",
  "mobile_variant": "80 frames WebP at 960w",
  "reduced_motion_fallback": "static poster frame of final assembled product",
  "transfer_estimate_kb": 2400,
  "downgrade_chain": ["pre-rendered sequence", "compressed video", "static poster"]
}
```

## Common decision shortcuts

These are not rules — they are high-probability outcomes of the decision procedure.

- Simple icon transition → **SVG / CSS**
- Authored interface animation with precise timing → **Lottie or Rive**
- Cinematic fixed-camera product reveal → **pre-rendered frame sequence**
- Interactive object inspection (rotate, zoom) → **real-time GLB / Three.js**
- Complex raytraced scene with fixed choreography → **pre-rendered sequence**
- Simple atmospheric background → **CSS / SVG / procedural canvas**
- Static editorial artwork → **generated or curated static image**
- Data visualization → **SVG or Canvas with real data**
- Ambient texture or grain → **CSS (no asset needed)**

## What this engine rejects

- Choosing 3D because "3D feels premium."
- Choosing video because "video adds energy."
- Choosing frame sequences because "scroll-driven feels immersive."
- Choosing generated images because "AI generation is available."
- Choosing shaders because "WebGL impresses."

The medium follows the idea. If the idea does not need the medium, the medium does not ship.

## Integration with v5

Every medium decision passes the v5 decoration-vs-structure test:

1. What job does this visual do?
2. What breaks if it is removed?
3. Is a simpler medium already doing the same job?

A 3D object that fails these questions is decoration, same as a divider line that fails them.
