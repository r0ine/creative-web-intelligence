# Mobile Media Strategy v6

Desktop and mobile must NOT automatically use the same cinematic implementation. Mobile is recomposed, not shrunk.

## Decision matrix

| Desktop medium | Mobile options (in order of preference) |
|:--|:--|
| Real-time 3D (interactive) | Reduced-LOD 3D → pre-rendered animation → static key visual |
| Real-time 3D (scroll-driven) | Reduced-frame pre-rendered sequence → static key visual |
| 180-frame sequence | 60–80 frame sequence at lower resolution |
| Scroll-controlled video | Shorter auto-playing clip → static poster |
| Shader background | CSS gradient or static → nothing |
| Large canvas animation | Reduced-complexity canvas → CSS → static |

## Rules

- Mobile budget is always one tier below desktop (see Performance Budget Engine).
- Touch replaces hover. Any hover-dependent 3D interaction must have a touch equivalent or be removed.
- Pinned scroll ranges are shorter on mobile (smaller viewports mean less comfortable sticky distance).
- `devicePixelRatio` is not doubled for sequences or textures — frame rate matters more than pixel density on mobile.
- Test on a real mid-range phone (e.g., 2-year-old mid-tier Android), not on the latest flagship.

---

# Cinematic Accessibility v6

Every cinematic experience must work without the cinematic part.

## Non-negotiable

### `prefers-reduced-motion`

- **Frame sequences:** show the poster frame. No scrubbing. Optionally, show a static filmstrip of 3–5 key frames.
- **3D animation:** static pose at the final camera position. Model visible, not animated.
- **Scroll-controlled video:** show a static poster frame or the first frame.
- **Shader effects:** disabled; show the content behind them.
- **Auto-playing video:** paused at first frame.
- **Parallax, camera drift, continuous animation:** all disabled.

### Screen readers

- `<canvas>` elements get `role="img"` and a descriptive `aria-label`.
- No essential content exists only inside animation/video/3D. All text is HTML.
- Interactive 3D controls get `aria-label` descriptions.

### Keyboard

- Scroll-driven sequences work with native keyboard scrolling (they do, by default, if scroll is not hijacked).
- Interactive 3D: provide keyboard controls (arrow keys for orbit, +/- for zoom) or label as decorative.

### Flashing

- No more than three flashes per second (WCAG 2.3.1).
- Frame sequences with rapid light changes must be reviewed frame-by-frame.

### Essential information

> If content exists only inside an animation, video, or 3D scene, the architecture is wrong.

HTML carries content. Media illustrates and enhances. This is not a guideline — it is a structural requirement.

---

# Scroll Experience Director v6

Upgrades the existing scroll system (`scroll/SCROLL_DIRECTOR.md`) with cinematic medium awareness.

## Scroll modes

| Mode | Description | Default? |
|:--|:--|:--|
| **Normal document scroll** | Content flows naturally. The default and most common. | Yes |
| **Scroll-triggered event** | An element changes state when it enters/exits viewport. | Selective |
| **Scroll-scrubbed animation** | Animation progress is mapped to scroll position. Requires pinned container. | Rare |
| **Sticky storytelling** | A pinned visual updates as the user scrolls through text/chapters beside it. | Rare |
| **Frame sequence** | Canvas frame tied to scroll progress. Requires a tall scroll region. | Rare |
| **Camera progression** | 3D camera position mapped to scroll. Requires pinned 3D canvas. | Rare |
| **Horizontal scroll** | Content moves horizontally within a pinned container. Use with extreme caution. | Very rare |

### Native scroll is the default

Never hijack scrolling. Native scroll behavior is correct until proven otherwise. Pinned sequences, scroll-scrubbed animations, and horizontal scroll are exceptions that must be justified by narrative purpose.

### Pinned section limits

- Maximum one pinned section per page (rare: two with strong justification).
- Pinned scroll range should not exceed 400vh (desktop) or 300vh (mobile).
- Between pinned sections, at least one full viewport of flowing content.
- Rest zones (v5) apply: after an intense scroll experience, the next section is calm.

### Scroll technology selection

| Need | Technology |
|:--|:--|
| Simple in-view triggers | `IntersectionObserver` (native) |
| Scroll progress for CSS | `animation-timeline: scroll()` (native, progressive enhancement) |
| Complex timelines with pinning | GSAP ScrollTrigger |
| Smooth scroll feel | Lenis (optional, use only when native scroll-behavior is insufficient) |
| 3D camera mapping | Custom scroll-to-progress → Three.js camera lerp |
| Frame sequence mapping | Custom scroll-to-progress → canvas drawImage |

Do not install GSAP for a single IntersectionObserver trigger. Do not install Lenis when `scroll-behavior: smooth` suffices.

---

# Implementation Intelligence v6

The library knows WHEN to use each technology. Technology follows the design requirement.

| Need | First choice | When to upgrade |
|:--|:--|:--|
| Simple hover/focus transition | CSS transition | — |
| State animation (toggle, tab) | CSS animation or Web Animations API | Complex choreography → GSAP |
| Scroll in-view trigger | `IntersectionObserver` | — |
| Scroll-mapped animation | `animation-timeline: scroll()` | Browser support gap → GSAP ScrollTrigger |
| Authored vector animation | Lottie (dotLottie) | Interactive state machine → Rive |
| Interactive state animation | Rive | — |
| Frame sequence canvas | Vanilla JS + `<canvas>` | — |
| Single model viewer | `<model-viewer>` | Custom camera/interaction → Three.js |
| Custom 3D scene | Three.js | React project with 3D state → R3F |
| Data visualization | D3 + SVG | Real-time particles/large datasets → Canvas/WebGL |
| Smooth scrolling | CSS `scroll-behavior: smooth` | Physics-based → Lenis |
| Custom shader effect | Three.js ShaderMaterial | Compute-heavy → WebGPU (progressive) |

**Rule:** do not install a library for one use. If the project needs a single GSAP tween, use CSS. If it needs a full scroll timeline with pinning, GSAP earns its place.

---

# Media Storyboard v6

Before implementing complex media, create an internal storyboard. This prevents random effects.

## For each major visual moment, define:

```json
{
  "moment_id": "hero-product-reveal",
  "purpose": "content — show the product assembling from components",
  "medium": "pre-rendered 3D frame sequence",
  "start_state": "components separated in exploded view",
  "end_state": "assembled product in hero framing",
  "user_control": "scroll scrub forward/backward",
  "scroll_relationship": "pinned canvas over 350vh scroll range",
  "camera_choreography": "approach + orbit 60° + settle",
  "desktop_spec": "120 frames AVIF 1920w",
  "mobile_spec": "50 frames WebP 960w",
  "fallback": "static poster of assembled product",
  "reduced_motion": "poster frame only",
  "performance_cost": {
    "transfer_kb": 2400,
    "decoded_memory_mb": 45,
    "gpu_impact": "none (canvas 2D)"
  },
  "rest_zone_after": true,
  "accessibility": {
    "aria_label": "Product assembly animation showing components coming together",
    "essential_text_in_media": false,
    "keyboard_scrollable": true
  }
}
```

Every complex visual moment gets a storyboard entry before implementation begins. If the storyboard entry cannot justify the medium, the medium downgrades or the moment is removed.

---

# Asset Pipeline v6

Standardized directory structure for project assets:

```
assets/
  images/
    editorial/       — curated photography and illustrations
    product/         — product shots, screenshots
    generated/       — AI-generated originals (with provenance)
    icons/           — SVG icon set
  video/
    source/          — raw/original video files
    optimized/       — web-compressed versions
    posters/         — poster frames for each video
  sequences/
    {name}/          — one directory per frame sequence
      manifest.json  — frame count, formats, dimensions, loading strategy
      poster.avif    — poster frame
      frame-{n}.avif — individual frames
      mobile/        — mobile-resolution variant
  models/
    source/          — original Blender/FBX/OBJ files
    optimized/       — web-ready GLB files
    textures/        — compressed textures (KTX2, WebP)
    provenance.json  — source, license, optimization status per model
  animations/
    lottie/          — .lottie / .json Lottie files
    rive/            — .riv Rive files
  shaders/           — GLSL/WGSL shader files
```

### Provenance manifest

Every asset directory includes a provenance file:

```json
{
  "assets": [
    {
      "filename": "hero-product.glb",
      "source": "custom-modeled in Blender from client CAD",
      "license": "project-owned",
      "optimization": "draco compressed, textures KTX2, 87K triangles",
      "mobile_variant": "hero-product-mobile.glb (reduced LOD, 32K triangles)",
      "fallback": "hero-product-poster.avif",
      "estimated_cost_kb": 1800,
      "created": "2026-09-01",
      "last_optimized": "2026-09-10"
    }
  ]
}
```
