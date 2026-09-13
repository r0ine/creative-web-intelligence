# Performance Budget Engine v6

Complex visual experiences consume bandwidth, GPU, CPU, and memory. Budgets prevent unchecked accumulation.

## Prime rule

**Budgets are per-project, not universal.** A marketing hero for a flagship product has a different budget than an editorial article page. Determine budgets from project type, expected devices, and network assumptions.

## Project tiers

| Tier | Typical project | Initial media | Total page media | GPU expectation |
|:--|:--|:--|:--|:--|
| **Lean** | Editorial, blog, documentation | < 500KB | < 2MB | Integrated GPU / mobile |
| **Standard** | Marketing page, product site | < 1.5MB | < 5MB | Mid-range discrete / recent mobile |
| **Rich** | Product launch, portfolio | < 3MB | < 10MB | Discrete GPU / high-end mobile |
| **Cinematic** | Campaign hero, immersive experience | < 5MB | < 15MB | High-end desktop; mobile gets fallback |

Cinematic tier is rare and must be justified by the brief.

## Budget categories

### Transfer budgets (over the wire)

| Category | Lean | Standard | Rich | Cinematic |
|:--|:--|:--|:--|:--|
| Initial payload (above fold) | 200KB | 500KB | 1MB | 2MB |
| Frame sequences total | 0 | 1.5MB | 3MB | 5MB |
| 3D models (GLB) total | 0 | 0 | 2MB | 5MB |
| Textures (KTX2/compressed) | 0 | 0 | 1MB | 3MB |
| Video | 0 | 2MB | 4MB | 8MB |
| Images total | 500KB | 1.5MB | 3MB | 5MB |

### Runtime budgets

| Category | Lean | Standard | Rich | Cinematic |
|:--|:--|:--|:--|:--|
| Decoded image memory | 20MB | 40MB | 80MB | 120MB |
| Texture memory (GPU) | 0 | 0 | 32MB | 64MB |
| Draw calls per frame | 0 | 0 | 30 | 50 |
| Concurrent animations | 1 | 2 | 3 | 4 |
| Frame sequence cache | 0 | 30MB | 60MB | 80MB |
| WebGL contexts | 0 | 0 | 1 | 1 |

### Timing budgets

| Metric | Target | Hard limit |
|:--|:--|:--|
| First Contentful Paint | < 1.5s | 2.5s |
| Largest Contentful Paint | < 2.5s | 4.0s |
| First meaningful 3D frame | < 3s | 5s |
| Frame sequence poster visible | < 1.5s | 2.5s |
| Total Blocking Time | < 200ms | 500ms |
| Cumulative Layout Shift | < 0.1 | 0.25 |

## Downgrade chain

When a visual moment exceeds its budget, downgrade — do not optimize endlessly.

```
real-time 3D
  → pre-rendered frame sequence
    → compressed video (autoplay muted)
      → static image (poster frame / key visual)
```

```
high-fidelity frame sequence (180 frames AVIF)
  → reduced frame sequence (60 frames WebP)
    → compressed video
      → static image
```

```
shader / WebGL effect
  → CSS effect
    → static (no effect)
```

Each step is a valid design outcome, not a failure. The downgrade chain is designed as part of the creative direction, not patched after the fact.

## Mobile budget

Mobile is always **one tier below** desktop, minimum:

- Desktop Rich → Mobile Standard
- Desktop Cinematic → Mobile Rich (or Standard with static fallback for the most expensive moments)
- Desktop Standard → Mobile Lean

See `v6/MOBILE_MEDIA_STRATEGY.md`.

## Measurement

Performance is measured, not estimated:

- **Transfer:** Chrome DevTools Network panel, or `performance.getEntriesByType('resource')`.
- **GPU memory:** Chrome `chrome://gpu` or Three.js `renderer.info.memory`.
- **Draw calls:** Three.js `renderer.info.render.calls`.
- **LCP / FCP / TBT:** Lighthouse, Web Vitals.
- **Frame rate:** `requestAnimationFrame` loop measuring frame time. Target: 60fps on desktop, 30fps minimum on mobile.

## Output contract

```json
{
  "performance_budget_version": "6.0",
  "project_tier": "rich",
  "budgets": {
    "initial_payload_kb": 1000,
    "frame_sequences_total_kb": 3000,
    "glb_total_kb": 2000,
    "texture_memory_mb": 32,
    "draw_calls": 30,
    "concurrent_animations": 3
  },
  "actual_measured": {
    "initial_payload_kb": 870,
    "frame_sequences_total_kb": 2400,
    "glb_total_kb": 1800,
    "lcp_ms": 2100,
    "tbt_ms": 150,
    "frame_rate_desktop_fps": 60,
    "frame_rate_mobile_fps": 42
  },
  "budget_status": "WITHIN",
  "mobile_tier": "standard",
  "downgrade_decisions": [
    { "moment": "hero 3D", "desktop": "realtime Three.js", "mobile": "prerendered 30-frame WebP sequence" }
  ]
}
```
