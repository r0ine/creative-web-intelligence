# Motion Grammar v2 (v5)

Upgrades `motion/v3_2/ANTI_AI_MOTION_GRAMMAR.md` by moving the strongest anti-patterns from "penalized" to **blocker**.

## Core rule

Motion has one legitimate job: to describe a relationship. Orientation, hierarchy, continuity, feedback, or state — those are relationships. "Feeling premium" is not a relationship. If the motion is not describing something, delete it.

## Motion families (with disciplined use)

Every page uses **one dominant family**. It may use zero, one, or at most two supporting families. Never a full set.

### 1. Static / rest
No entrance motion. This is a family — treat it as a choice, not the absence of a choice. Long editorial pages should be built here by default.

### 2. Opacity activation
Short opacity change with no travel. For state activation, captions, secondary UI, contextual reveals. **Not** for section entrances.

### 3. Mask / clip reveal
The element is revealed through its own bounds. For display type where the shape of the container is part of the composition. Never applied identically to every heading.

### 4. Media crop reveal
Framing changes as viewport reaches the media. The composition itself stays anchored. For editorial images, portfolio work, product hero shots.

### 5. State transition
Component state changes visibly — filter applied, toggle flipped, tab switched. Not "entering from nowhere." State transitions are the workhorse of good product UI motion.

### 6. Physical settle
Small scale/rotation/position resolves into place. For objects with perceived mass — 3D hero artifacts, physical products. **Not** for cards or buttons.

### 7. Spatial transfer / handoff
An element visibly moves between two regions because continuity matters — shared element navigation, expand-collapse where the element grows into place.

### 8. Typographic transformation
Width, weight, optical-size, mask, baseline, or line composition changes on the type itself. When typography is the visual driver, use this instead of translating a text container.

### 9. Scrubbed narrative motion
Scroll drives a meaningful progression — a story, a process, a camera path, a data reveal. Used only when the section is genuinely about progression.

### 10. Pointer reaction
Precise, small local reaction. Never required for critical understanding. Disabled or reduced on coarse pointers.

### 11. Utility feedback
Loading, saving, submitting, error, success. Micro-feedback with a functional purpose. Duration measured in milliseconds.

## Grammar discipline

- **One dominant grammar per page.** If the page is editorial-static, that is the dominant grammar. Static counts.
- **At most two supporting grammars.** They should share visual logic with the dominant one.
- **Rest zones are mandatory** on any page longer than two viewports. See `REST_ZONES.md`.
- **Motion families do not mix at full amplitude.** A page cannot simultaneously scrub, physical-settle, and cursor-drive at full intensity.

## Hard blockers (fails V5 Authenticity Gate)

### MG-B01 · Universal fade-up as page reveal system
`opacity 0 → 1; translateY(20–40px) → 0` applied to multiple sections. **Blocker on first repetition.** The pattern is the single strongest AI motion fingerprint. Delete the helper. Choose one section to animate — with a different, appropriate grammar — and leave the rest static.

### MG-B02 · Stagger ladder (`index * 0.1s`)
Stagger by hierarchy or reading order, not by array index. Repeating this across the page is a blocker.

### MG-B03 · Same easing/duration across UI, editorial, and object motion
A single `--ease-out` token used for button clicks, hero reveals, and 3D moves is a blocker. Define role-specific easing: `ui`, `editorial`, `object`.

### MG-B04 · Every section animates in the same way
If sections A, B, and C all enter with the same motion — regardless of what motion it is — it is a blocker. The fingerprint is *repetition*, not the specific effect.

### MG-B05 · Motion added because "the section felt empty"
Motion cannot fix a composition problem. If a section feels empty without motion, the composition is empty. Fix the composition — do not paint over it with reveals.

## Penalties (log and address)

- **Blur-in on entrance.** Delete unless focal-plane logic is present.
- **Continuous parallax on text-heavy pages.** Reading and drift compete; drift wins in a bad way.
- **Long pinned sections used for atmosphere rather than progression.** Pin only when a real state progression exists.
- **Hover-lift + shadow-grow on every card.** Reserve hover feedback for interactive elements.
- **`scrollY * 0.0037` magic math scattered through components.** Use normalized progress signals (`sectionProgress`, `chapterProgress`).

## Amplitude discipline

Prefer the smallest movement that communicates the relationship.

- Entrance travel > 40px needs a specific reason.
- Zoom scale change > 15% needs a specific reason.
- Rotation on scroll > 10° needs a specific reason.
- Blur > 4px needs a focal-plane reason.

## Rest zones

Long pages **must** include ranges where motion nearly stops. See `REST_ZONES.md`. Reading is an interaction — protect it.

## Reduced motion

The reduced-motion variant is authored *at the same time* as the main motion. Not after. If it cannot be authored (i.e. the content depends on movement to be legible), the movement is doing too much work.

## Technology choice comes last

Never open a motion decision with "we'll use GSAP" or "we'll use Framer Motion." Decide:

1. What the motion communicates.
2. Which grammar fits.
3. What amplitude, mass, easing, duration.
4. What rest ranges surround it.
5. What the reduced-motion path is.
6. What the mobile behavior is.

Then, and only then, pick the tool. Simple CSS transitions cover most needs. Reach for GSAP/ScrollTrigger when the choreography genuinely needs a timeline.

## The final test

Turn off all motion. Does the composition still communicate?

- If **yes**, the motion was correctly supportive. Ship.
- If **no**, the composition depends on animation to work. The composition is broken. Motion cannot fix it.
