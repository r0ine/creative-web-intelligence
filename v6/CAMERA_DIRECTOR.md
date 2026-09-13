# Camera Director v6

Camera motion on the web is cinematography. It follows the same rules as film: every move communicates something. Random movement communicates nothing.

## Camera vocabulary

| Move | Communicates | Example |
|:--|:--|:--|
| **Static** | Stability, contemplation, display | Product beauty shot, editorial moment |
| **Approach / dolly in** | Intimacy, focus, detail | Moving toward a product to see material |
| **Retreat / dolly out** | Context, reveal of scale | Pulling back to show an object in its environment |
| **Orbit (limited arc)** | Dimension, materiality | 45°–90° arc showing product form |
| **Pan** | Survey, lateral context | Scanning across a landscape or lineup |
| **Tilt** | Verticality, scale | Looking up at architecture |
| **Crane / vertical move** | Gravitas, establishment | Rising above a scene to establish geography |
| **Reveal** | Surprise, discovery | Camera moves past an obstruction to show something hidden |
| **Follow** | Connection, journey | Camera tracks an object through a process |
| **Focal length shift** | Emotional register | Telephoto compression → wide expansion |

## Hard rejects

The following camera behaviors are v6 fingerprints. They fail the Cinematic Purpose Gate.

### CAM-R01 · Constant 360° orbit

The object spins endlessly. No start, no end, no framing intention. This is the camera equivalent of `animation: spin 10s linear infinite` and reads as "3D was added, but no cinematography was applied."

**Correction:** Choose a start angle and an end angle. The arc should be 45°–120°, not 360°. The resting state matters.

### CAM-R02 · Random/aimless camera drift

The camera floats without a focal target, moving continuously in a slowly changing direction. The movement is decorative — it does not show, reveal, or approach anything.

**Correction:** Every camera move has a subject. If there is no subject, the camera is static.

### CAM-R03 · Disorienting rapid motion

Fast camera movements that induce motion sickness — rapid orbiting, whip pans, or sudden direction reversals, especially during scroll.

**Correction:** Camera velocity during scroll should be proportional to scroll velocity. No camera move should exceed 120° per viewport of scroll.

### CAM-R04 · Camera motion just to demonstrate 3D

The camera moves to show that the scene is three-dimensional, not to show the subject. The movement is about the technology, not the content.

**Correction:** If the user would learn the same thing from a static view, the camera should be static.

### CAM-R05 · Every section has camera motion

The 3D equivalent of "every section animates." Rest zones apply to camera as much as they apply to 2D motion. See `v5/REST_ZONES.md`.

## Scroll-driven camera choreography

When camera movement is mapped to scroll position, it must be authored as a cinematic timeline.

### Timeline structure

```
progress 0.00 — ESTABLISHING SHOT
  camera at rest, showing the complete object in context
  
progress 0.10–0.25 — APPROACH
  camera moves toward the subject, increasing intimacy
  
progress 0.25–0.40 — DETAIL
  camera frames a specific area of interest
  
progress 0.40–0.55 — TRANSITION
  camera shifts to a new angle or reveals a new aspect
  
progress 0.55–0.70 — INTERNAL / EXPLODED
  if applicable: components separate, interior becomes visible
  
progress 0.70–0.85 — REASSEMBLY / RESOLUTION
  components return, camera reframes
  
progress 0.85–1.00 — FINAL STATE
  camera settles into a hero framing, object at rest
```

This is an example, not a template. The choreography must be derived from the content. Never reuse this exact progression as a default.

### Choreography rules

- **Every segment must have a named purpose.** "Camera orbits" is not a purpose. "Camera reveals the hinge mechanism" is.
- **Rest moments within the timeline.** Not every scroll increment moves the camera. Hold the camera steady for 10–20% of the total scroll range.
- **Velocity curve.** Camera movement should ease in and out, not move at constant speed. Scroll-mapped motion uses normalized progress with easing applied.
- **Reverse scroll.** The choreography must work naturally in both directions. No one-way reveals.
- **No more than 180° total rotation** unless the subject genuinely has distinct views at every angle.

### Scroll-to-camera mapping

```javascript
const progress = clamp01((scrollY - sectionTop) / scrollRange);
const easedProgress = easeInOutCubic(progress);

camera.position.lerpVectors(startPosition, endPosition, easedProgress);
camera.lookAt(targetPosition);
```

Do not use `scrollY * magicNumber` directly. Normalize to 0–1 progress, apply easing, then map to camera parameters.

## Framing

- **Subject centered or off-center with intention.** The camera's framing of the subject is a composition decision. Apply the same asymmetry thinking as v5 `COMPOSITION_RESTRAINT.md`.
- **Negative space around the subject.** The 3D object does not fill the entire canvas. The viewer needs spatial context.
- **Focal point.** Every frame has a clear focal point. If the camera is moving, the focal point may shift — but at any given moment, one thing is "the thing."

## Environment and context

- The 3D object exists in a context — even if that context is a clean studio. The lighting, floor plane, and background contribute to the framing.
- **Do not float objects in a void** unless the void is a chosen concept (e.g., product photography on white).
- **Environment consistency.** The environment map, lighting direction, and shadow behavior stay consistent through the entire camera path. Lighting does not change arbitrarily during scroll.

## Output contract

```json
{
  "camera_director_version": "6.0",
  "choreography_type": "scroll-driven | interactive | static",
  "total_arc_degrees": 75,
  "segments": [
    {
      "progress_range": [0.0, 0.25],
      "move": "approach",
      "purpose": "move from establishing shot to product detail",
      "easing": "ease-in-out-cubic"
    },
    {
      "progress_range": [0.25, 0.40],
      "move": "static-hold",
      "purpose": "rest — viewer reads the detail at close range"
    }
  ],
  "max_scroll_velocity_deg_per_vh": 45,
  "rest_ranges_pct": 20,
  "reverse_scroll_behavior": "natural reverse of forward path",
  "reduced_motion": "static final-state framing"
}
```

## The final camera test

Watch the camera choreography at 2× speed. If it looks like a tech demo, the cinematography is missing. If it looks like a product film, it is working.
