# Cinematic Anti-AI Fingerprints v6

Extends the v5 fingerprint catalog (`v5/ANTI_AI_VISUAL_FINGERPRINTS.md`) with patterns specific to 3D, video, frame sequences, and generated visual assets. The v5 fingerprints remain fully in force. This document adds to them — it does not replace them.

**Critical:** complex media must NOT become an excuse to bring back the v5-rejected patterns. A page with a beautiful 3D hero but hairline dividers between every section, gradient text on the headline, and universal fade-up on the remaining sections still fails the v5 gate.

---

## Category G — 3D clichés

### AF-G01 · Random floating 3D blob

**Description.** A metallic, chrome, or glass abstract shape — sphere, torus, blob, icosahedron — placed in the hero section with no content association.

**Why it feels AI-generated.** The 3D equivalent of a gradient glow. It signals "we added 3D" without deciding what the 3D should show. Every generative tool with Three.js access converges on this.

**Severity.** Blocker.

**Detection.** A 3D canvas in the hero containing a single abstract primitive with no product, brand, or content association.

**Correction.** Either the 3D shows the product (justified) or the 3D is removed. An abstract shape earns its place only when it is genuinely part of the brand identity (e.g., a logo element) — not as atmosphere.

### AF-G02 · Endless object rotation

**Description.** `requestAnimationFrame` spin at constant speed with no start, end, or user interaction. The object rotates forever.

**Why it feels AI-generated.** No cinematographic intention. The camera (or object) moves because the code can make it move, not because the movement shows something.

**Severity.** Blocker.

**Detection.** `rotation.y += 0.01` or equivalent in an animation loop with no scroll or interaction dependency.

**Correction.** See Camera Director `CAM-R01`. Choose a start and end angle. Make the object respond to user scroll or hover, not to time.

### AF-G03 · Chrome/glass object as hero

**Description.** A reflective or refractive object with a dramatic HDRI reflection, used as the primary hero visual — but the product being sold is not chrome/glass.

**Why it feels AI-generated.** Chrome and glass are the default demo materials in every 3D tutorial. Choosing them says no material decision was made.

**Severity.** High.

**Detection.** Hero 3D with environment map reflection on a material unrelated to the actual product.

**Correction.** Material must match the product or brand. If the product is matte, the 3D is matte. If the product is plastic, the 3D is plastic.

### AF-G04 · Meaningless particle field

**Description.** Thousands of points drifting in 3D space without data association, interaction, or narrative. Used for "atmosphere" or "technology feel."

**Why it feels AI-generated.** Particles are the `background-grid-overlay` of 3D — technically trivial, visually noisy, narratively empty.

**Severity.** Blocker.

**Detection.** PointsMaterial or particle system with no data source, no user interaction, no narrative endpoint.

**Correction.** Particles are justified when they represent data (a point cloud), a physical phenomenon (smoke, sparks with a source), or a counted entity. Decorative particles are removed.

### AF-G05 · Meaningless WebGL background

**Description.** A full-page shader or Three.js canvas used as a background behind text — gradient blobs, noise patterns, or distortion fields that serve no content purpose.

**Why it feels AI-generated.** It is the cinematic version of the CSS gradient background. The WebGL context consumes GPU for what CSS could do, or for what nothing should do.

**Severity.** High.

**Detection.** Full-viewport WebGL canvas behind text content with no interaction or scroll dependency.

**Correction.** If the background needs motion, CSS or SVG can likely handle it. If it needs complexity, the complexity should be content-associated. If it is atmosphere, evaluate whether calm whitespace is the better choice.

### AF-G06 · 3D on every section

**Description.** Multiple 3D canvases on the same page, each with a decorative object. The page is "3D everywhere."

**Why it feels AI-generated.** The 3D equivalent of "every section animates." It flattens the hierarchy — if everything is 3D, nothing is the 3D moment.

**Severity.** Blocker.

**Detection.** More than two WebGL contexts on the same page, or more than one WebGL canvas that is purely decorative.

**Correction.** One 3D moment per page is typical. Two is possible with justification. Three is almost never correct. Rest zones between 3D moments are mandatory.

---

## Category H — Frame sequence / video clichés

### AF-H01 · Every section is a pinned scroll sequence

**Description.** The entire page is a series of pinned sticky sections, each with a scroll-scrubbed animation. Normal document scrolling is eliminated.

**Why it feels AI-generated.** Scroll hijacking at scale. The page becomes a slide deck controlled by scroll rather than clicks. Users lose scroll agency.

**Severity.** Blocker.

**Detection.** More than 50% of page height is pinned/sticky scroll-driven animation with no flowing document content.

**Correction.** One, maximum two pinned sequences per page. The rest is flowing content. See v5 rest zones.

### AF-H02 · Generated video with temporal artifacts shipped anyway

**Description.** AI-generated video used in production with visible flickering, morphing objects, deformed anatomy, or inconsistent geometry.

**Why it feels AI-generated.** Because it literally is, and the quality gate was skipped.

**Severity.** Blocker.

**Detection.** Visual inspection of frame sequence source. Frame quality inspection pipeline.

**Correction.** Regenerate, find better source material, or drop to static image.

### AF-H03 · Frame sequence for a simple transition

**Description.** A 60+ frame sequence used for what is essentially a fade or a simple CSS transition.

**Why it feels AI-generated.** Overengineering — choosing the heaviest medium for the lightest job.

**Severity.** High.

**Detection.** Frame sequence where the visual difference between first and last frame is achievable via CSS transform or opacity.

**Correction.** Use CSS. The sequence is not needed.

### AF-H04 · Scroll-controlled video with no narrative progression

**Description.** A video scrubbed by scroll, but the video content has no meaningful progression. Nothing builds, reveals, or changes state. The user is scrubbing for the sake of scrubbing.

**Why it feels AI-generated.** Scroll control is justified when the user is navigating a story. When the video is just ambient footage, scroll control is a technology demonstration.

**Severity.** High.

**Detection.** Scrub the sequence from start to end. Does something build? Does understanding increase? Does a transformation occur?

**Correction.** If the video is ambient, play it as a background `<video>` or use a static image. Reserve scroll control for narratives.

---

## Category I — Generated asset clichés

### AF-I01 · AI-generated filler imagery

**Description.** Generated images placed in sections because "the section needed an image" — not because the image communicates something specific.

**Why it feels AI-generated.** Because it is, and its presence reveals that the image decision was "fill the space" rather than "show something."

**Severity.** High.

**Detection.** Generated images in sections where the image topic is generic (abstract shapes, "happy diverse team," "futuristic cityscape") and not specific to the product or content.

**Correction.** Either the image shows something real and specific, or the section does not need an image. Remove filler.

### AF-I02 · Inconsistent asset world

**Description.** Different visual treatments across sections — glossy 3D here, flat illustration there, stock photography elsewhere, AI gradient in another — with no coherent visual language.

**Why it feels AI-generated.** Each asset was generated or sourced independently with no Asset DNA. The page reads as a collage of unrelated visual sources.

**Severity.** High.

**Detection.** Compare lighting, color temperature, material language, and illustration style across all visual assets on the page. Inconsistency = this fingerprint.

**Correction.** Define Asset DNA before producing any asset. See `v6/ASSET_DNA.md`.

### AF-I03 · Fake technical HUD overlay

**Description.** Sci-fi HUD elements, targeting reticles, data readout overlays, and "scanning" animations placed over content to signal "advanced technology."

**Why it feels AI-generated.** Film-UI costume. No real data underneath. Same category as v5's register marks and corner brackets.

**Severity.** Blocker.

**Detection.** SVG/Canvas overlay with readout-style elements that display no real data.

**Correction.** Remove. If the interface actually displays data, design a real data interface.

---

## Scoring

Same as v5: no numeric score.

- Any **blocker** → design fails the V6 Cinematic Purpose Gate.
- Two or more **high** severity → design fails the gate.
- v5 fingerprints remain active simultaneously. A page must pass both v5 and v6 gates.
