# SCROLL DIRECTOR v2.2

Scroll is not an entrance-animation trigger. It is a **progress and navigation signal** that may control spatial depth, narrative state, media, typography, 3D camera/object state or quiet atmospheric changes.

## Mandatory decision sequence
1. Identify what the user should understand or feel as they move through the section.
2. Decide whether scrolling should be **normal flow**, **threshold-triggered**, **scrubbed**, **pinned/sticky**, or a **hybrid**.
3. Select **one dominant scroll recipe** from `data/v2/scroll_recipes.json`.
4. Add at most a few lower-salience supporting recipes.
5. Check `data/v2/scroll_compatibility.json`.
6. Re-author mobile behavior; never blindly reuse desktop travel/pin distances.
7. Define a reduced-motion version before implementation.
8. Choose technology only after choreography is defined.

## Technology selection
### Native CSS / Scroll-driven Animations
Prefer when the effect is compositor-friendly, local to DOM, and does not require complex pin orchestration or cross-system synchronization.

### CSS sticky
Prefer for simple sticky/persistent compositions where browser-native layout is enough.

### GSAP + ScrollTrigger
Use when the experience needs authored scrub ranges, pinning, timeline sequencing, cross-element choreography, state handoff, or reliable synchronization across several properties.

### Lenis
Use only if the project genuinely benefits from a smoothed scroll signal. It is not a visual-quality switch. Never stack multiple smooth-scroll engines.

### R3F / Three.js
Use scroll as a normalized signal for camera, object, light, fog or shader state. Do not call React `setState` every frame for continuous transforms.

## Normalized progress contract
Every scroll-capable primitive should consume a stable `0..1` progress signal or named section state. Avoid scattered `scrollY * 0.0037` magic math throughout components.

Suggested internal signals:
- `pageProgress`
- `sectionProgress`
- `chapterProgress`
- `scrollVelocity` (secondary only)
- `scrollDirection`
- `isScrolling`

## Motion hierarchy
A scene should normally have:
- **1 dominant scroll idea** (salience 3)
- **0–2 supporting motions** (salience 1–2)
- **reading/rest ranges** where motion nearly stops

## Pinning rules
Pinning is expensive in attention, not just performance. Reject a pin if removing it does not reduce comprehension or spatial continuity.

Never use long pinned distances simply to make a page feel "premium".

## 3D rules
Camera is navigation. Object transformation is explanation. Lighting/atmosphere are support. Do not animate all three at maximum intensity on the same beat.

## Typography rules
Keep semantic text in DOM. Scroll effects may mask, translate, vary axes or transfer scale, but essential copy must remain legible and accessible.

## Mobile rules
- shorten pinned ranges
- reduce camera travel and parallax amplitude
- eliminate hover dependencies
- avoid long horizontal scroll remapping
- lower simultaneous effect count
- preserve normal document escape paths

## Reduced motion
Large spatial motion, parallax, camera travel, velocity reactions and long scrubbed transformations need a reduced alternative. Prefer short state changes and keep content immediately available.

## Anti-slop gate
Reject:
- every section doing `opacity 0 -> 1; y 40 -> 0`
- scroll effects added to every visible element
- raw wheel delta mapped directly to camera/model transforms
- endless parallax on text-heavy pages
- multiple consecutive pinned sections
- identical scrub/ease language for type, camera and micro-UI
- "Awwwards" effects with no information or brand purpose

## Output
For each scroll-driven section emit:
`dominantRecipe`, `supportingRecipes`, `mapping`, `progressRanges`, `technology`, `mobileVariant`, `reducedMotionVariant`, `performanceNotes`, `whyThisExists`.
