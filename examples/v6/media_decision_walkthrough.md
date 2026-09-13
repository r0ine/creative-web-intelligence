# Media Decision Walkthrough — Static vs Sequence vs Realtime 3D

Three briefs. Same product (a wireless headphone). Three different correct answers.

---

## Brief A — Editorial product page

**Context:** A long-form editorial page about the engineering behind the headphone. Content-driven. Target audience: audiophiles reading a review.

**Media Decision Engine evaluation:**

1. **Purpose:** Content — the product is what is being shown, but the primary vehicle is writing, not visual exploration.
2. **Interaction:** View only. The reader reads; images illustrate.
3. **Camera freedom:** None. Fixed editorial photographs.
4. **Fidelity:** Photographic. Real product shots.
5. **Performance:** Lean tier. Fast loading, editorial pace.
6. **Mobile:** Same images, responsive.

**Decision: static images.**

Three curated product photographs at editorial scale. No animation. No 3D. No frame sequence. The images are content illustrations within an editorial composition.

**Why not 3D?** The reader is not inspecting the product — they are reading about it. A photograph communicates faster and loads in milliseconds.

**Why not a frame sequence?** There is no scroll narrative. The progression is textual, not visual.

---

## Brief B — Product launch hero

**Context:** A hero section for a product launch landing page. The product's key feature is a magnetic hinge mechanism that allows the headband to fold. The folding motion IS the selling point.

**Media Decision Engine evaluation:**

1. **Purpose:** Content + storytelling — the folding mechanism IS the product story.
2. **Interaction:** Scrub through the folding progression. The user controls the reveal.
3. **Camera freedom:** Fixed camera path. The fold is best shown from one carefully chosen angle.
4. **Fidelity:** High. PBR product quality. Pre-rendered offline for material accuracy.
5. **Performance:** Rich tier. This is the hero moment.
6. **Mobile:** Reduced frame count, smaller resolution.

**Decision: pre-rendered 3D frame sequence.**

A Blender scene renders the folding mechanism from a fixed camera. 120 frames extracted as AVIF. Scroll scrubs from fully open (frame 0) to folded (frame 120). Mobile gets 50 frames at 960w WebP.

**Why not realtime 3D?** The camera path is fixed. Pre-rendering delivers higher material fidelity (raytraced reflections, subsurface on ear cushion) at zero GPU cost.

**Why not static?** The folding progression IS the story. A single image cannot show the transformation.

**Why not video?** Scroll control lets the user study the hinge mechanism at their own pace. Video plays at its own pace and cannot be scrubbed.

### Camera choreography

```
0.00  — Full headphone, open position. Camera: front-quarter view.
0.15  — Camera approaches the hinge area.
0.30  — Hold. User sees the hinge mechanism at close range.
0.50  — Fold begins. Left ear cup rotates inward.
0.70  — Fold completes. Right cup follows.
0.85  — Camera pulls back to show the folded product.
1.00  — Final hero framing. Product folded, compact.
```

### Storyboard entry

```json
{
  "moment_id": "hero-fold-reveal",
  "purpose": "content + storytelling — the folding mechanism IS the product story",
  "medium": "pre-rendered 3D frame sequence",
  "start_state": "headphone fully open, camera front-quarter",
  "end_state": "headphone folded, camera pulled back to hero framing",
  "user_control": "scroll scrub",
  "scroll_relationship": "pinned canvas over 350vh",
  "camera_choreography": "approach → hold → fold progression → retreat → settle",
  "desktop_spec": "120 frames AVIF 1920×1080",
  "mobile_spec": "50 frames WebP 960×540",
  "fallback": "static poster of folded product",
  "reduced_motion": "poster frame of folded product, no scrub",
  "performance_cost": { "transfer_kb_desktop": 2800, "transfer_kb_mobile": 900 },
  "rest_zone_after": true,
  "accessibility": {
    "aria_label": "Interactive animation showing the headphone's magnetic folding mechanism",
    "essential_text_in_media": false
  }
}
```

---

## Brief C — E-commerce product detail page

**Context:** An e-commerce PDP where the customer must inspect the headphone before buying. They need to see it from multiple angles, check the material finish, and choose between three color options.

**Media Decision Engine evaluation:**

1. **Purpose:** Content — the customer is evaluating the product visually before purchase.
2. **Interaction:** User-controlled camera. Orbit, zoom. Color configuration.
3. **Camera freedom:** Full user control required.
4. **Fidelity:** PBR standard — good enough for purchase decision, realtime achievable.
5. **Performance:** Standard tier. E-commerce page must load fast.
6. **Mobile:** Same 3D with touch orbit, reduced LOD.

**Decision: realtime 3D (GLB + Three.js or `<model-viewer>`).**

A GLB model with three material variants (black, silver, white). The user orbits freely. Color swatches trigger material swap. `<model-viewer>` is sufficient if no custom camera choreography is needed.

**Why not static images?** The customer needs to see every angle. A 360° photo set is possible but configuration (color change) is harder to implement without 3D.

**Why not a frame sequence?** The user needs free camera control, not a fixed path.

**Why not pre-rendered?** Camera freedom = realtime.

### 3D Director output

```json
{
  "decision": "JUSTIFIED",
  "justification": "product inspection with user-controlled camera and color configuration",
  "realtime_or_prerendered": "realtime",
  "technology": "model-viewer",
  "model_source": "client CAD, adapted for web",
  "optimization": {
    "format": "glb",
    "compression": "draco",
    "texture_format": "webp",
    "texture_budget_mb": 16,
    "estimated_glb_size_kb": 1200,
    "draw_calls_estimate": 12,
    "lod_levels": 2,
    "material_variants": 3
  },
  "camera": {
    "type": "user-controlled orbit",
    "initial_angle": "front-quarter",
    "orbit_limits": { "min_polar": 30, "max_polar": 120 },
    "zoom_limits": { "min_distance": 1.5, "max_distance": 4.0 }
  },
  "mobile_strategy": "same model, reduced LOD (32K triangles), smaller textures (512)",
  "reduced_motion": "static image of product at initial angle; color swatches show static photos"
}
```

---

## What the comparison teaches

Three briefs, same product, three different correct answers:

| Brief | Answer | Why |
|:--|:--|:--|
| Editorial review | Static images | Reader is reading, not inspecting |
| Product launch hero | Pre-rendered frame sequence | Folding mechanism IS the story; scroll scrub reveals it |
| E-commerce PDP | Realtime 3D | Customer needs free inspection and configuration |

The medium followed the idea. Not the other way around.

No brief got 3D "because 3D is better." No brief got animation "because animation is premium." The decision engine evaluated purpose, interaction, camera freedom, fidelity, and performance — and each time, the simplest medium that delivered the experience was chosen.

This is the v6 doctrine working correctly.
