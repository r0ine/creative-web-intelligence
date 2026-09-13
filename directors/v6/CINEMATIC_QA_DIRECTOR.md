# CINEMATIC QA DIRECTOR v6

Runs the V6 Cinematic Purpose Gate, the V6 3D Performance Gate, and the V6 Frame Sequence Gate. Works alongside (not instead of) the v5 QA Director.

## Gate stack

A v6-compliant design must pass ALL of these:

1. **V5 Authenticity Gate** (unchanged — dividers, motion, composition, typography, color, decoration)
2. **V6 Cinematic Purpose Gate** (every complex medium is justified)
3. **V6 3D Performance Gate** (if 3D is present, it meets performance targets)
4. **V6 Frame Sequence Gate** (if sequences are present, they meet performance/quality targets)

## V6 Cinematic Purpose Gate

For every complex visual moment (anything beyond static image / CSS / SVG):

### Check 1 — Purpose

Does the visual moment have a stated purpose from the valid set (content, identity, explanation, atmosphere-earned, state, storytelling)?

- If no → **FAIL**. Remove the visual or downgrade to a simpler medium.

### Check 2 — Cinematic fingerprint scan

Scan against `data/v6/cinematic_anti_ai_fingerprints.json`. For each present fingerprint, report with location, evidence, and correction. Blockers fail the gate.

### Check 3 — Simplest-medium test

Could a simpler medium deliver the same experience?

- Frame sequence where CSS could handle it → **FAIL** (AF-H03).
- 3D where a photo would suffice → **FAIL** (the 3D Director's final test).
- Video where a static image would work → **FAIL**.

### Check 4 — Rest zone compliance

After complex media moments, is there a rest zone? Does the page breathe? v5 rest zone rules apply to cinematic content.

### Check 5 — Mobile fallback

Does every complex desktop moment have a specified mobile variant or fallback? If not → **FAIL**.

### Check 6 — Reduced motion fallback

Does every animated/scrubbed moment have a `prefers-reduced-motion` fallback? If not → **FAIL**.

### Check 7 — Asset DNA consistency

Do all visual assets on the page belong to the same visual world (Asset DNA)? If not → **FAIL** (AF-I02).

## V6 3D Performance Gate

If the project includes real-time 3D:

| Metric | Target | Hard limit | Action on exceed |
|:--|:--|:--|:--|
| GLB total KB | 2000 | 5000 | Optimize or downgrade to prerender |
| Texture memory MB | 32 | 64 | Resize textures or reduce material count |
| Draw calls per frame | 30 | 50 | Merge meshes or reduce scene complexity |
| Triangle count | 100K | 250K | Decimate or use LOD |
| WebGL contexts on page | 1 | 1 | Merge scenes into one context |
| Mobile frame rate (mid-range) | 30fps | 20fps | Downgrade to prerendered fallback |
| Model load time (broadband) | 3s | 5s | Compress further or split loading |

Any hard limit exceeded → **FAIL** with downgrade instruction.

## V6 Frame Sequence Gate

If the project includes frame sequences:

| Metric | Target | Hard limit | Action on exceed |
|:--|:--|:--|:--|
| Desktop transfer per sequence KB | 2500 | 4000 | Reduce frame count or compress further |
| Mobile transfer per sequence KB | 800 | 1500 | Reduce frame count and resolution |
| Concurrent active sequences | 1 | 1 | Ensure only one loads at a time |
| Decoded frame cache MB | 40 | 60 | Reduce preload window |
| Poster frame visible in ms | 1000 | 1500 | Preload poster earlier |
| Generated source frame quality | 95% pass | 100% pass | Reject failing frames, regenerate |
| Essential text inside frames | 0 | 0 | Move all text to HTML overlay |

Sequence-specific checks:

- Does the sequence have a manifest? → required.
- Does the sequence have a mobile variant? → required.
- Does the sequence have a poster frame? → required.
- Does the sequence have a reduced-motion fallback? → required.
- Does scrubbing start to end reveal a narrative? → if no, the sequence is not justified.

## Report format

```
V6 CINEMATIC QA — [PASS | PASS-WITH-NOTES | FAIL]

V5 Authenticity Gate: PASS
V6 Cinematic Purpose Gate: PASS-WITH-NOTES
V6 3D Performance Gate: PASS
V6 Frame Sequence Gate: N/A (no sequences in project)

Cinematic fingerprints:
  [AF-G03] high · hero 3D uses chrome material but product is matte plastic
    correction: match material to product

Purpose checks:
  hero-product: PASS (content — product inspection)
  features-diagram: PASS (explanation — SVG)
  editorial-image: PASS (atmosphere — earned contextual)

Simplest-medium checks: PASS
Rest zone compliance: PASS
Mobile fallback: PASS
Reduced motion: PASS
Asset DNA consistency: PASS-WITH-NOTES (lighting differs slightly between hero render and editorial photo)

Overall: PASS-WITH-NOTES
Notes: harmonize lighting between hero 3D render and editorial photography to match Asset DNA.
```

## The director's one sentence

> A cinematic effect without narrative purpose is a more expensive version of decoration.
