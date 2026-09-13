# Frame Sequence Director v6

## What a frame sequence is

A scroll-scrubbed frame sequence replaces a video with individually decoded images rendered to a `<canvas>`. As the user scrolls, the canvas draws the frame corresponding to the scroll position. The user controls time.

```
scroll progress 0.0 → frame 0
scroll progress 0.5 → middle frame
scroll progress 1.0 → final frame
```

Forward and reverse scrolling work naturally.

## When to use a frame sequence

- **Scroll-controlled narrative.** The user scrubs through a visual story — product assembly, process explanation, transformation.
- **Pre-rendered 3D with scroll control.** A Blender/offline render whose camera path maps to scroll. Higher fidelity than realtime 3D.
- **Generated video refined into scroll experience.** An AI-generated or authored video whose best frames are extracted and scroll-mapped.

## When NOT to use a frame sequence

- **The content is a video that should play as video.** If the user should watch, not scrub, use `<video>`.
- **The animation is simple enough for CSS/Lottie.** Frame sequences are heavy — do not use them for transitions that CSS handles.
- **The scroll range is too short.** A sequence needs 2–4 viewport heights of scroll to feel controlled. Shorter ranges make the scrub feel jerky.
- **Every section on the page.** One sequence per page is often the budget. Two is rare. Three is almost never justified.

## The pipeline

```
source material (3D render / video / animation)
  → frame extraction
  → frame quality inspection
  → frame optimization (format, resolution, count)
  → manifest generation
  → progressive loading strategy
  → canvas rendering
  → scroll progress mapping
  → frame selection & interpolation
```

### Frame extraction

- From video: extract at the target frame rate using ffmpeg.
- From 3D: render each frame from Blender/After Effects at target resolution.
- From generated video: extract, then run quality inspection to reject bad frames.

### Frame quality inspection (generated video)

Reject generated video frames that contain:
- Temporal instability (flickering, morphing between frames)
- Object deformation (hands, faces, products changing shape)
- Inconsistent geometry (walls bending, objects shifting)
- Unreadable generated text (do not put important text in video — HTML handles text)
- Broken logos or UI elements
- Inconsistent materials (surface changing between frames)
- Strange camera motion (unnatural acceleration, impossible physics)
- Visual artifacts (banding, smearing, hallucination)

If more than 5% of frames fail inspection, the source video is not suitable. Regenerate or choose a different medium.

### Frame optimization

#### Format selection

| Format | Use when |
|:--|:--|
| **AVIF** | Primary choice for modern browsers. Best compression-to-quality ratio. |
| **WebP** | Fallback for browsers without AVIF. Good compression. |
| **JPEG** | Legacy fallback. Use quality 80–85 for sequences. |

Serve AVIF with WebP fallback using `<picture>` logic in the loader, or content-negotiation.

#### Frame count

Not a fixed number. Calculated from:

```
frame_count = scroll_duration_vh * frames_per_vh
```

| Tier | frames_per_vh | Total for 4vh scroll | Use when |
|:--|:--|:--|:--|
| Smooth | 12–15 | 48–60 | Desktop, high-bandwidth, primary hero moment |
| Standard | 8–10 | 32–40 | Desktop secondary, good mobile |
| Efficient | 5–6 | 20–24 | Mobile, constrained bandwidth |
| Minimal | 3–4 | 12–16 | Extreme constraint, poster-frame priority |

Desktop and mobile may use different tiers for the same sequence.

#### Resolution

| Device | Width | DPR consideration |
|:--|:--|:--|
| Desktop | 1920px | 1x (do not serve 2x for sequences — too expensive) |
| Tablet | 1280px | 1x |
| Mobile | 960px | 1x |

For sequences, skip DPR scaling. The frame rate matters more than pixel density for perceived quality.

### Manifest

Every frame sequence produces a manifest:

```json
{
  "id": "hero-product-reveal",
  "version": "1.0",
  "purpose": "scroll-scrubbed product assembly narrative",
  "frame_count": 60,
  "dimensions": { "width": 1920, "height": 1080 },
  "format": "avif",
  "fallback_format": "webp",
  "poster_frame": 0,
  "poster_url": "sequences/hero/poster.avif",
  "frame_url_pattern": "sequences/hero/frame-{index}.avif",
  "preload_window": 10,
  "scroll_duration_vh": 400,
  "mobile_variant": {
    "frame_count": 30,
    "dimensions": { "width": 960, "height": 540 },
    "format": "webp"
  },
  "estimated_transfer_kb": {
    "desktop": 2400,
    "mobile": 800
  },
  "loading_strategy": "progressive",
  "reduced_motion_fallback": "poster frame only, no scrub"
}
```

### Loading strategy

1. **Poster frame loads first.** The user sees a complete image immediately.
2. **Preload window.** The next N frames ahead of current scroll position are decoded.
3. **Progressive loading.** Frames load in scroll-order, not sequentially from 0.
4. **Frame caching.** Decoded frames are held in an offscreen canvas or ImageBitmap cache.
5. **Frame skipping.** During fast scroll, skip intermediate frames rather than decoding all.
6. **Memory budget.** Do not hold all decoded frames in memory simultaneously. Cache a rolling window.
7. **Decoding strategy.** Use `createImageBitmap()` for off-main-thread decoding where supported.

### Canvas rendering

- Use a `<canvas>` element sized to the sequence dimensions.
- On each scroll frame, `drawImage()` the current frame.
- Use `requestAnimationFrame` to throttle drawing to display refresh rate.
- Do not redraw if the frame index has not changed.

### Scroll progress mapping

```javascript
const progress = (scrollY - sectionTop) / (sectionHeight - viewportHeight);
const clampedProgress = Math.max(0, Math.min(1, progress));
const frameIndex = Math.round(clampedProgress * (frameCount - 1));
```

Use `position: sticky` on the canvas container within a tall scroll region. The canvas stays in view while the scroll range provides the scrub distance.

## Performance gate

See `quality/V6_FRAME_SEQUENCE_GATE.md`. Key limits:

- Total sequence transfer: desktop ≤ 4MB, mobile ≤ 1.5MB per sequence.
- Concurrent sequences: maximum 1 active at a time.
- Decoded frame memory: ≤ 60MB rolling cache.
- First meaningful frame: ≤ 1.5s on broadband.

## Accessibility

- **`prefers-reduced-motion`**: show the poster frame. No scrubbing. Optionally show a static filmstrip of 3–5 key frames.
- **Screen reader**: `aria-label` on the canvas describing the visual content. `role="img"`.
- **Keyboard**: the sequence section should be scrollable via keyboard (it is, by default, if scroll is not hijacked).
- **No essential text inside frames.** All text content is HTML, overlaid on or adjacent to the canvas.

## The final frame sequence test

Replace the sequence with its poster frame (a single static image). If the page works just as well, the sequence was not justified. If the scroll progression genuinely added understanding or narrative, it was justified.
