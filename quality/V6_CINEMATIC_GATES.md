# V6 Cinematic Purpose Gate

A design fails this gate when impressive effects exist without purpose.

## Blockers (any single one = FAIL)

### 3D clichés
- **G-01** Random floating 3D blob — abstract shape in hero with no content association.
- **G-02** Endless object rotation — constant spin with no interaction dependency.
- **G-04** Meaningless particle field — particles without data, interaction, or narrative.
- **G-06** 3D on every section — multiple decorative 3D canvases.

### Scroll clichés
- **H-01** Every section is a pinned scroll sequence — more than 50% of page pinned.
- **H-02** Generated video with temporal artifacts shipped — quality gate skipped.

### Generated asset clichés
- **I-03** Fake technical HUD overlay — sci-fi UI with no real data.

### Structural
- **No purpose statement** for any complex visual moment.
- **No mobile fallback** for any complex visual moment.
- **No reduced-motion fallback** for any animated/scrubbed moment.
- **Essential text inside animation/video/3D** — content architecture is wrong.

## High severity (two or more = FAIL)

- **G-03** Chrome/glass material mismatch.
- **G-05** Meaningless WebGL background.
- **H-03** Frame sequence for a simple transition.
- **H-04** Scroll video with no narrative progression.
- **I-01** AI-generated filler imagery.
- **I-02** Inconsistent asset world.
- **Camera reject** CAM-R01 through CAM-R05.

## Relationship with v5

The v5 Authenticity Gate must also pass. v6 does not replace it. A project must clear both gates.

---

# V6 3D Performance Gate

Applies only when real-time 3D is present. See `directors/v6/CINEMATIC_QA_DIRECTOR.md` for metric table.

Key hard-limit failures:
- GLB total > 5MB
- Texture memory > 64MB
- Draw calls > 50
- Triangles > 250K
- Mobile frame rate < 20fps
- More than 1 WebGL context on page

Any hard limit exceeded = **FAIL** with instruction to optimize or downgrade.

---

# V6 Frame Sequence Gate

Applies only when frame sequences are present. See `directors/v6/CINEMATIC_QA_DIRECTOR.md` for metric table.

Key requirements:
- Manifest present
- Mobile variant present
- Poster frame present
- Reduced-motion fallback present
- Desktop transfer ≤ 4MB per sequence
- Mobile transfer ≤ 1.5MB per sequence
- No essential text inside frames
- Narrative progression present (scrub reveals a build/transformation)
- Generated source frames pass quality inspection (≥ 95%)

Any structural requirement missing = **FAIL**.
