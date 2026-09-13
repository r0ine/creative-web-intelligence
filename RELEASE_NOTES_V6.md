# Release Notes — v6.0 Cinematic Media + 3D Web Intelligence

## Summary

v6 extends the library's vocabulary to the full spectrum of visual mediums — generated imagery, video, frame sequences, 3D, shaders, procedural graphics — and teaches it when NOT to use them.

The core insight: the library must be equally capable of producing a completely static editorial website, a cinematic frame-sequence website, or an interactive 3D experience — and consider all three equally valid. The medium follows the idea.

## New version number: 6.0

## Files added (24 new files)

### Doctrine (`v6/`)
- `CORE_DOCTRINE.md`
- `MEDIA_DECISION_ENGINE.md`
- `THREE_D_DIRECTOR.md`
- `FRAME_SEQUENCE_DIRECTOR.md`
- `CAMERA_DIRECTOR.md`
- `BLENDER_WEB_PIPELINE.md`
- `ASSET_DNA.md`
- `PERFORMANCE_BUDGET_ENGINE.md`
- `MOBILE_MEDIA_STRATEGY.md` (also contains Cinematic Accessibility, Scroll Experience Director, Implementation Intelligence, Media Storyboard, Asset Pipeline)
- `CINEMATIC_ANTI_AI_FINGERPRINTS.md`

### Machine-readable data (`data/v6/`)
- `media_decision_matrix.json`
- `three_d_decision_matrix.json`
- `cinematic_anti_ai_fingerprints.json` (13 fingerprints)
- `cinematic_profiles.json` (frame sequence profiles, camera patterns, performance budgets, fallback hierarchy)

### Directors (`directors/v6/`)
- `MEDIA_DIRECTOR.md`
- `CINEMATIC_QA_DIRECTOR.md`

### Quality gates
- `quality/V6_CINEMATIC_GATES.md` (Cinematic Purpose Gate + 3D Performance Gate + Frame Sequence Gate)

### Prompts
- `prompts/v6/MASTER_META_PROMPT_V6.md`

### Tools
- `tools/v6/validate_v6.py`

### Examples
- `examples/v6/media_decision_walkthrough.md` (static vs sequence vs 3D — same product, three briefs, three correct answers)

### Entry docs
- `README_V6.md`, `START_HERE_V6.md`, `RELEASE_NOTES_V6.md`, `docs/V6_OVERVIEW.md`

## Files modified (1)

- `README.md` — updated to point to v6 first.

## New machine-readable systems

- **Media decision matrix** (`data/v6/media_decision_matrix.json`) — 16-medium spectrum, decision steps, downgrade chains, interaction-to-medium mapping, camera-freedom-to-medium mapping.
- **3D decision matrix** (`data/v6/three_d_decision_matrix.json`) — justified/not-justified criteria, realtime-vs-prerendered routing, technology selection, optimization targets.
- **Cinematic fingerprints** (`data/v6/cinematic_anti_ai_fingerprints.json`) — 13 new fingerprints (AF-G01..G06, AF-H01..H04, AF-I01..I03) with per-pattern detection and correction.
- **Cinematic profiles** (`data/v6/cinematic_profiles.json`) — frame sequence tiers, camera vocabulary, performance budget tiers, asset fallback hierarchy.

## New QA gates

- **V6 Cinematic Purpose Gate** — every complex visual moment must have a stated purpose, pass the cinematic fingerprint scan, survive the simplest-medium test, have a mobile and reduced-motion fallback.
- **V6 3D Performance Gate** — GLB size, texture memory, draw calls, triangle count, mobile frame rate, WebGL context count.
- **V6 Frame Sequence Gate** — transfer limits, manifest, mobile variant, poster frame, reduced-motion fallback, narrative progression test.

## Research sources referenced

Technical decisions in v6 are grounded in:

- **Three.js** — official documentation (threejs.org/docs) for scene, camera, renderer, loader, animation patterns.
- **glTF 2.0 specification** — Khronos Group (github.com/KhronosGroup/glTF) for material model, extensions, compression.
- **Draco / Meshopt compression** — Google Draco (github.com/google/draco), Meshopt (github.com/zeux/meshoptimizer) for geometry compression tradeoffs.
- **KTX2 / Basis Universal** — Khronos (github.com/KhronosGroup/KTX-Software) for GPU texture compression.
- **AVIF / WebP** — format specifications and browser support for frame sequence delivery.
- **`<model-viewer>`** — Google (modelviewer.dev) for declarative 3D on the web.
- **GSAP ScrollTrigger** — GreenSock (gsap.com/docs) for scroll-driven animation patterns.
- **Lottie / dotLottie** — LottieFiles documentation for vector animation delivery.
- **Rive** — rive.app documentation for state-machine animation.
- **`prefers-reduced-motion`** — MDN Web Docs for accessibility-aware motion.
- **Web Vitals** — Google (web.dev/vitals) for performance metric targets.
- **Blender glTF export** — Blender manual for PBR material translation and animation baking.
- **`createImageBitmap()`** — MDN for off-main-thread image decoding.
- **CSS `animation-timeline: scroll()`** — W3C spec for native scroll-driven animations.

No unauthorized scraping, no copied tutorials. Principles extracted from official documentation.

## Validation results

All validators pass:
- `tools/v3_2/validate_v3_2.py` — PASS
- `tools/v4/validate_v4.py` — PASS
- `tools/v5/validate_v5.py` — PASS
- `tools/v5/authenticity_check.py` — PASS (on the library itself)
- `tools/v6/validate_v6.py` — PASS

## Remaining limitations

1. **No actual static analyzer for cinematic fingerprints.** The v5 `authenticity_check.py` handles HTML/CSS fingerprints. A v6 cinematic analyzer would need to read Three.js scene code, which is beyond regex-level. Cinematic fingerprints require human review or an agent-based audit using `prompts/v6/MASTER_META_PROMPT_V6.md`.

2. **Frame sequence pipeline is documented, not automated.** The library describes the pipeline (extract → optimize → manifest → load → render) but does not ship a frame extraction tool. This is intentional — frame extraction requires ffmpeg or Blender CLI, which are external dependencies.

3. **Performance budgets are guidelines, not enforced at build time.** The budgets are defined and the gates specify the limits, but no build-time tool checks GLB size or texture memory automatically. Measurement instructions are provided; automation is project-level.

4. **Blender pipeline assumes Blender knowledge.** The library documents what to do in Blender but does not automate it. An agent using this library should be able to guide a developer through the pipeline, not run Blender itself.

5. **`<model-viewer>` vs Three.js vs R3F decision is not automated.** The 3D Director provides criteria, but the choice ultimately depends on project context (framework, team expertise, feature needs) that the library evaluates heuristically.

6. **Asset DNA is a creative document, not a computed one.** Deriving it from Design DNA requires creative judgment. The library provides the structure and the dimensions but cannot auto-generate the specific lighting language or material language — that is the designer's or agent's creative work.

7. **Generated video quality inspection is manual.** The library defines what to reject (temporal instability, deformation, artifacts) but does not ship a video analysis tool. Frame-by-frame inspection is human or agent work.

8. **The "simplest medium" test is subjective.** Two reasonable reviewers might disagree on whether a frame sequence or a video is the simpler choice for a given moment. The library provides the decision procedure and the criteria, but final judgment is human.

9. **Rest zone doctrine for 3D is inferred from v5.** v5 rest zones were defined for 2D motion. v6 extends them to 3D camera and scene animation, but the coverage metrics (30% rest) were not recalibrated for pages with a single large 3D moment that occupies 40% of the page. This edge case should be addressed in v6.1.

10. **No cinematic example spec JSON.** The `examples/v6/media_decision_walkthrough.md` is prose. A machine-readable example spec (like `examples/v5/refactored_landing_spec.json`) for a cinematic project would be valuable — earmarked for v6.1.
