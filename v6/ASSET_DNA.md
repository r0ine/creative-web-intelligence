# Asset DNA v6

Every visual asset on a project — generated, photographed, modeled, illustrated — must belong to **one coherent visual world**. That world is defined by the Asset DNA, derived from the project's Design DNA.

## What Asset DNA contains

| Dimension | Example values |
|:--|:--|
| **Palette relationship** | Warm neutral range from Design DNA; assets use the same surface and accent temperatures. |
| **Lighting language** | Soft diffused top-left key; no harsh rim lights. Matches the brand's calm voice. |
| **Material language** | Matte surfaces with subtle grain. No chrome, no glass unless the product is chrome/glass. |
| **Contrast** | Medium contrast. No crushed blacks. Shadows are readable. |
| **Texture** | Subtle paper/fabric grain. No noise, no heavy film grain. |
| **Camera behavior** | Static or slow approach. No orbital. See Camera Director. |
| **Depth** | Shallow. Foreground subject, soft background. No infinite DOF. |
| **Geometry language** | Rounded, organic forms. No sharp mechanical edges unless the product demands it. |
| **Illustration language** | (if applicable) Flat color, thin line, restrained palette. |
| **Photographic treatment** | Desaturated 10%, warm white balance +200K. No heavy color grading. |
| **Motion character** | Slow, deliberate. Ease-in-out. No bounce, no overshoot. |

## Why this matters

Without Asset DNA, a page accumulates incoherent visuals:

- Section 1: glossy 3D product render with dramatic lighting.
- Section 2: flat stock photograph with daylight white balance.
- Section 3: AI-generated abstract gradient.
- Section 4: hand-drawn illustration with thick lines.

Each asset may be individually "good." Together, they read as a collage of unrelated sources. This is an anti-pattern the library rejects unless the concept explicitly requires mixed-world contrast (rare and must be stated).

## How to derive Asset DNA

1. Start from the project's Design DNA (typography voice, color palette, compositional logic).
2. Translate each Design DNA dimension into an asset-level equivalent (see table above).
3. Write 3–5 bullet points describing "what every visual on this site looks and feels like."
4. Test: could a new team member produce a new asset that fits, using only these bullets?

## Enforcement

Before any generated image, 3D model, video, or illustration is approved:

- Does it match the Asset DNA's lighting language?
- Does it match the palette relationship?
- Does it match the material language?
- Does it match the contrast and depth?
- Does it match the motion character (if animated)?

If any answer is no, rework the asset or reject it.

## Generated asset quality gates

### Generated images

Before using an AI-generated image:

1. **Purpose check.** Why does this image exist? (See Media Decision Engine step 1.)
2. **Quality check.** No deformed hands, faces, text, logos, or impossible geometry.
3. **Consistency check.** Matches Asset DNA.
4. **Uniqueness check.** Does not replicate a common AI-generation pattern (symmetric mandala, oversaturated landscape, "concept art" glow).
5. **Provenance.** Document the generation tool, prompt strategy, and any post-processing.

### Generated 3D models

1. **Topology check.** Clean mesh, no self-intersections, reasonable poly count.
2. **UV check.** No overlapping UVs, no stretched textures.
3. **Material check.** PBR-compliant, no hallucinated material properties.
4. **Scale check.** Real-world scale, not arbitrary.

### Generated video

See `v6/FRAME_SEQUENCE_DIRECTOR.md` § Frame quality inspection. Reject temporal instability, deformation, flickering.

## Output contract

```json
{
  "asset_dna_version": "6.0",
  "palette_relationship": "warm neutrals from brand palette; accent only in data points",
  "lighting_language": "soft diffused, top-left key, no rim",
  "material_language": "matte with subtle grain, no chrome/glass",
  "contrast": "medium, readable shadows",
  "texture": "subtle paper grain",
  "camera_behavior": "static or slow approach",
  "depth": "shallow, soft background",
  "geometry_language": "rounded organic forms",
  "motion_character": "slow, deliberate, ease-in-out",
  "coherence_rule": "all assets share this world; reject mixed-aesthetic sourcing"
}
```
