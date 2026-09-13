# Creative Web Intelligence v6 — Core Doctrine

## What v6 adds

v5 fixed the AI-fingerprint problem with a blocker gate. That gate remains fully in force.

v6 extends the library's vocabulary. Until now, the library thought in HTML, CSS, typography, icons, and static images. v6 teaches it to think in **all visual mediums** — generated imagery, video, frame sequences, 3D, shaders, procedural graphics — and most importantly, teaches it **when not to use them.**

## The v6 thesis

> The medium follows the idea. The simplest medium capable of delivering the intended experience is always correct.

A website with excellent typography and composition should beat a technically impressive website with meaningless effects. v6 does not make every website cinematic. It makes the library *capable* of choosing cinematic when cinematic is the right answer — and choosing static when static is the right answer.

## What v6 does NOT do

- Does not make websites more animated by default.
- Does not encourage 3D, video, or generated imagery as a premium signal.
- Does not override the v5 Authenticity Gate. Every v5 blocker remains a blocker.
- Does not reintroduce dividers, hairlines, grid overlays, fade-up animations, or any pattern the v5 doctrine rejected.
- Does not treat complex media as an excuse to weaken composition or typography.

Complex media that lacks purpose is decoration. The v5 `DECORATION_VS_STRUCTURE.md` test applies to 3D objects, video sequences, and generated images exactly as it applies to dividers and borders.

## The single question v6 forces at every media decision

> Why does this visual exist?

Valid answers: content, identity, explanation, atmosphere (earned), state, storytelling.

Invalid answers: "it looks impressive," "it shows technical capability," "3D feels premium," "the hero needs energy."

If the answer is invalid, the visual does not ship. Same rule as v5 — different medium, same discipline.

## Five doctrinal additions from v6

### 1. Media Decision Engine

Every visual moment on the page passes through a decision engine that evaluates narrative purpose, interaction needs, performance cost, and device capability — then selects the **simplest sufficient medium.** Not the most impressive.

See `v6/MEDIA_DECISION_ENGINE.md`.

### 2. 3D is justified or rejected

A 3D object on a webpage is not inherently better than a static image. The library evaluates whether the third dimension adds meaning — inspection, spatial understanding, reveal, interaction — and rejects 3D when a 2D medium would communicate the same thing at lower cost.

See `v6/THREE_D_DIRECTOR.md`.

### 3. Camera is cinematography

Camera movement in 3D or scroll-driven sequences follows cinematic language: framing, approach, reveal, focal point. Random orbiting, constant spinning, and aimless camera motion are rejected as fingerprints of generated work.

See `v6/CAMERA_DIRECTOR.md`.

### 4. Performance is not optional

Complex media requires budgets. Initial transfer, texture memory, GPU load, frame count — all budgeted per project, not globally. The library can downgrade: realtime 3D → prerendered sequence → video → static image. The fallback chain is designed, not accidental.

See `v6/PERFORMANCE_BUDGET_ENGINE.md`.

### 5. Asset DNA enforces consistency

Every generated or authored visual asset belongs to one coherent visual world derived from the project's Design DNA. Random aesthetic mixing — glossy 3D here, stock photography there, AI gradient elsewhere — is rejected.

See `v6/ASSET_DNA.md`.

## What v6 keeps from v5

Everything. The v5 blocker gate, divider policy, motion grammar, composition restraint, typography-first premium, decoration-vs-structure test, rest zones, color restraint, and QA visual authenticity gate are all in force. v6 is additive.

## The relationship between v5 and v6

v5 answers: **is this design honest?** (no fingerprints, no decoration without purpose)

v6 answers: **what medium should this design use?** (and is that medium justified?)

Both gates must pass. A cinematic 3D experience that triggers v5 blockers (fade-up repetition, cardification, gradient text) still fails. A static page that passes v5 but uses a 3D blob for no reason fails v6.

## The one-sentence version

**The library now has access to every visual medium and knows that most of the time, the right answer is the simplest one.**
