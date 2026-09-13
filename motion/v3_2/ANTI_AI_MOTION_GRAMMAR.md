# Anti-AI Motion Grammar v3.2

## Prime rule

Motion must describe a relationship, state or hierarchy. It is not proof that a website is premium.

## Default rejected behavior

A global helper that makes every section enter with `opacity: 0; transform: translateY(...)` is rejected as a default design system. The pattern may appear once when semantically appropriate; repetition across sections is the fingerprint.

## Motion grammar families

### 1. Static / rest
No entrance motion. Use when reading, dense content or composition already carries hierarchy.

### 2. Opacity activation
Short tonal transition without travel. Useful for state activation, captions, subtle context.

### 3. Mask / clip reveal
Reveal typography or media through its own bounds. Best when the shape/container matters.

### 4. Crop / viewport reveal
Media framing changes while content remains spatially anchored.

### 5. Settle
Small scale/rotation/position difference resolves into place. Use for objects with perceived mass, not every UI card.

### 6. Spatial transfer
An element visibly moves between states/regions because continuity matters.

### 7. Scrubbed progression
Scroll maps to a meaningful state progression, camera/object story or data/media sequence.

### 8. State morph
Navigation, button, filter or route state changes without pretending to enter from nowhere.

### 9. Pointer response
Small local reaction on precise pointers. Never required for critical understanding and disabled/reduced on touch.

### 10. Typographic transformation
Width, weight, optical size, mask, baseline or line composition changes when typography is the visual driver.

## Grammar limit

A page should normally use one dominant grammar plus at most one or two quiet supports. Do not show competence by using every technique.

## Rest zones

Long pages need ranges where motion nearly stops. Reading itself is an interaction. Continuous stimulation flattens hierarchy because nothing feels important.

## Stagger rule

Reject mechanical ladders (`0.1, 0.2, 0.3, 0.4...`) repeated section after section. Stagger is valid when it expresses order, causality or reading sequence.

## Easing rule

UI feedback, editorial reveals and 3D objects do not share one universal ease. Define motion tokens by perceived mass and function.

## Amplitude rule

Prefer the smallest movement that communicates the intended relationship. Large 40–100px travel, blur-to-sharp and zoom effects need a specific reason.

## Reduced motion

Define the reduced variant while authoring the main motion, not after implementation. Essential information must never depend on travel, scrub or hover.
