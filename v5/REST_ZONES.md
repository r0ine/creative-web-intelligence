# Rest Zones v5

A rest zone is a region of the page where **nothing moves** — no scroll effect, no parallax, no hover response, no entrance animation, no drifting object.

Rest zones are mandatory on any page longer than two viewports.

## Why rest zones exist

Reading is an interaction. Composition is a form of communication. When everything on the page is moving all the time, three things happen:

1. **Hierarchy flattens.** If everything moves, nothing is "the moment." The eye has no landing.
2. **Reading fails.** Motion in peripheral vision breaks reading concentration. Users skim or leave.
3. **The page feels generated.** A hallmark of generative outputs is uniform motion coverage — every section animates, so no motion means anything.

Rest zones fix all three. They restore hierarchy, allow reading, and read as intentional restraint.

## The rule

On a page longer than two viewports:

- **At least 30% of the page height** must be a rest zone.
- **At least one continuous rest zone of 1+ viewport** must exist.
- **The primary reading section** (body copy of any length beyond one paragraph) must be a rest zone.

## What counts as motion (and therefore breaks rest)

- Any scroll-triggered entrance animation
- Any parallax layer, however subtle
- Any element that drifts, floats, rotates, or breathes
- Any hover effect that transforms the element (color changes are fine)
- Any always-on shader or WebGL animation in the viewport range
- Any Lottie or looped animation

## What does not break rest

- Static images
- Typography, however expressive
- Deliberate hover feedback on **interactive** elements (buttons, links)
- Cursor position tracking that is invisible or off-screen
- Motion in the offscreen page area

## Placement

A rest zone works best positioned:

1. **After a high-motion scene** — the reader has just been moved; give them ground.
2. **Around dense content** — long paragraphs, tables, data blocks.
3. **Before a peak moment** — silence before emphasis is the oldest editorial trick.

Avoid placing rest zones at the very start (users expect the hero to land) or at the very end (footer is already low-attention).

## What a rest zone looks like

- A long editorial paragraph in a calm column with generous margins.
- A single large image with a caption, no crop reveal.
- A section that is mostly whitespace with one headline anchored in it.
- A dense feature list where each item is legible without any scroll effect.
- A quote at editorial scale on a clean surface.

## What does not count as a rest zone

- A section that is "static" but has a hover-lift on cards. Rest is total.
- A section without entrance animation but with a slow background gradient shift. Rest is total.
- A section that is static above the fold but scrolls into a parallax layer as it exits. Rest is total until it visibly ends.

## Fail conditions

The V5 Authenticity Gate flags:

- **Zero rest zones** on a page longer than two viewports → blocker.
- **Less than 20% rest coverage** on a page longer than three viewports → blocker.
- **Rest zone interrupted by an always-on background animation** → blocker (the rest zone is not actually resting).

## The visible pause is the point

A page that alternates between motion and rest reads as considered — someone chose when to move and when to hold. A page that moves everywhere reads as automatic — the system moves everything because it can.

Rest is the harder choice. That is why it works.
