# 3D Experience Director v6

## Prime rule

**3D is justified when the third dimension adds meaning that a 2D medium cannot deliver.** Inspection, spatial understanding, assembly/disassembly, configuration, environment — these are real 3D purposes. "Premium feel" is not.

## When 3D is justified

- **Product inspection.** The user can orbit, zoom, and examine a physical product. The interaction reveals detail that a photo set cannot.
- **Spatial explanation.** Architecture, interior, geography, anatomy — the subject is inherently three-dimensional and understanding benefits from free or guided camera movement.
- **Assembly / exploded view.** Components separate, internal structure becomes visible, parts are identified. The progression is spatial.
- **Configuration.** The user changes materials, colors, or components and sees the result in context. Realtime 3D is the only medium that supports this.
- **Environment / world.** The experience IS a spatial environment — a virtual showroom, a navigable scene, an interactive installation.
- **Data in space.** Three-dimensional data visualization where the third axis carries real information (not decoration).

## When 3D is NOT justified

- **"The hero needs a 3D object."** The hero needs a composition decision, not a medium.
- **Rotating product that could be a photo.** If the user does not need to control the camera, a photo or pre-rendered sequence is cheaper and sharper.
- **Abstract 3D shape for atmosphere.** A metallic sphere, a glass blob, a chrome torus — these are the 3D equivalent of a divider line. Decoration without purpose.
- **3D background for "depth."** Depth is a compositional property. CSS, parallax, or nothing at all can provide it without a WebGL context.
- **Technical demonstration.** The website is not a portfolio of 3D capabilities. 3D serves the content or it does not appear.

## Realtime vs pre-rendered

The Media Decision Engine routes this, but the 3D Director refines it:

### Choose realtime 3D when:

- The user controls the camera (orbit, zoom, pan).
- The user configures the object (material, color, component swap).
- The object responds to user input in ways that cannot be pre-baked.
- The scene is procedural or data-driven.

### Choose pre-rendered 3D when:

- The camera path is fixed or scroll-driven.
- Visual fidelity requirements exceed realtime capability (raytracing, caustics, subsurface scattering).
- The target includes low-end mobile devices.
- The 3D moment is a narrative sequence, not an interactive tool.

### The hybrid pipeline

For many projects, the best answer is:

```
Blender scene → offline render → frame sequence → scroll-controlled canvas
```

This delivers 3D quality without 3D runtime cost. See `v6/BLENDER_WEB_PIPELINE.md`.

## Model requirements

### Sources

- **Custom modeled** — authored for the project. Highest quality, highest cost.
- **Existing project model** — the client's CAD/product model, adapted for web.
- **Procedural geometry** — generated from parameters. Data-driven shapes.
- **Simple primitive composition** — cubes, spheres, planes composed into a scene. Valid when the concept is geometric.
- **Licensed external model** — from a marketplace or library with verified license. Provenance must be documented.
- **Generated model** — from an AI or procedural generation tool. QA required for topology, UV, and material quality.

Every external model must have:
- Source documented
- License verified (commercial use, redistribution rights)
- Optimization status confirmed
- Web-ready validation passed

### Optimization requirements

No raw Blender/CAD asset ships to the web without optimization:

- **Topology.** No n-gons in deforming meshes. Reasonable poly count for the detail level. LOD levels for complex models.
- **Textures.** PBR metallic-roughness workflow. Textures at web-appropriate sizes (1K–2K typical, 4K only with justification). KTX2/Basis compression where supported.
- **Materials.** glTF-compliant PBR. No Blender-specific shader nodes that do not translate.
- **Animation.** Baked to keyframes. No constraints or drivers that require runtime evaluation. Clips named and separated.
- **File size.** GLB with Draco or Meshopt compression. Target: under 2MB for a primary model, under 5MB for a complex scene. Justify anything larger.
- **Draw calls.** Merged meshes where possible. Instancing for repeated elements. Target: under 50 draw calls for a single scene.

### Texture budget

| Tier | Max texture memory | Typical use |
|:--|:--|:--|
| Minimal | 8MB | Simple product, icon-level 3D |
| Standard | 32MB | Product hero, single-model scene |
| Rich | 64MB | Multi-model scene, environment |
| Cinematic | 128MB | Full environment, desktop-only justified |

Mobile targets the tier below desktop.

## Technology selection

### Three.js

The default for custom 3D web experiences. Use when:
- The scene needs custom camera controls, lighting, or post-processing.
- Integration with scroll, pointer, or device orientation is required.
- The project is vanilla JS or framework-agnostic.

### React Three Fiber (R3F)

Use when:
- The project is React-based.
- The 3D scene is a component within a React application.
- Declarative scene description fits the architecture.

Do not use R3F just because the project uses React. If the 3D is a standalone canvas with no React state integration, vanilla Three.js with a canvas element is simpler.

### `<model-viewer>`

Use when:
- The only interaction is orbit + zoom on a single model.
- No custom camera choreography is needed.
- The fastest implementation path matters.
- AR preview (WebXR) is desired.

### Raw WebGL / WebGPU

Use only when:
- Custom shader effects that Three.js abstractions cannot express.
- Extreme performance optimization is required.
- The developer has the expertise.

Never default to raw WebGL. Three.js exists for a reason.

## Lighting and environment

- **Environment map (HDRI/EXR).** Required for any PBR scene. Choose an environment that matches the brand's lighting language (see `v6/ASSET_DNA.md`).
- **Directional/spot lights.** Used in addition to environment, not instead of it. Motivated lighting — the light has a source reason.
- **Ambient light.** Use minimally. Heavy ambient flattens the scene and signals "no lighting decision was made."

## Anti-patterns (hard rejects)

These are v6 cinematic fingerprints — see `v6/CINEMATIC_ANTI_AI_FINGERPRINTS.md` for the full catalog.

- **Random floating 3D blob** — metallic/chrome/glass abstract shape in the hero with no content association.
- **Endless object rotation** — constant `requestAnimationFrame` spin with no user purpose.
- **Chrome sphere in every hero** — the 3D equivalent of the gradient headline.
- **Particle field for atmosphere** — thousands of points drifting without data or narrative reason.
- **3D used on every section** — the 3D equivalent of "every section animates."

## Output contract

```json
{
  "three_d_director_version": "6.0",
  "decision": "JUSTIFIED | REJECTED | HYBRID_PRERENDER",
  "justification": "one sentence explaining why 3D is or is not the right medium",
  "if_justified": {
    "realtime_or_prerendered": "realtime | prerendered | hybrid",
    "technology": "three.js | r3f | model-viewer | raw-webgl",
    "model_source": "custom | existing | procedural | licensed | generated",
    "model_provenance": "...",
    "optimization": {
      "format": "glb",
      "compression": "draco | meshopt",
      "texture_format": "ktx2 | webp | jpg",
      "texture_budget_mb": 32,
      "estimated_glb_size_kb": 1800,
      "draw_calls_estimate": 24,
      "lod_levels": 2
    },
    "camera": "see CAMERA_DIRECTOR output",
    "mobile_strategy": "reduced LOD | prerendered fallback | static key visual",
    "reduced_motion": "static pose at final camera position",
    "performance_gate": "see V6_THREE_D_PERFORMANCE_GATE"
  }
}
```

## The final 3D test

Remove the 3D from the page. Replace it with a single well-chosen photograph.

- If the page works just as well → 3D was not justified.
- If something meaningful is lost (inspection, configuration, spatial understanding) → 3D was justified.

This test is the 3D version of v5's decoration-off test. Apply it honestly.
