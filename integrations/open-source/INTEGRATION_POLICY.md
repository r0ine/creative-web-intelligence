# Open-Source Integration Policy

## Goal
External libraries expand capability; they must not turn Creative Web Intelligence into a dependency dump or a recognizable template pack.

## Selection order
1. Internal native/CSS/browser capability when it solves the problem cleanly.
2. Existing internal primitive/recipe.
3. Small permissive external primitive.
4. Larger framework/renderer only when the project genuinely needs its capabilities.

## Integration modes
- **core-engine**: approved foundational technology (e.g. Three.js).
- **adapter**: thin local wrapper preserving escape hatches.
- **source-registry**: copy-paste upstream components may be selectively ingested only when license permits; immediately normalize tokens, accessibility, API and visual language.
- **dev-only**: authoring/tuning tools excluded from production.
- **alternate-renderer**: mutually exclusive rendering stack; choose by project, never combine by default.
- **reference-only**: study patterns but do not redistribute code.

## Anti-library-soup gate
A project fails review when it uses multiple overlapping libraries for the same responsibility without a written reason. Examples: Motion + React Spring + AutoAnimate for the same DOM animation layer; Swup + Barba for the same route lifecycle; Three + Babylon in one ordinary scene.

## Wrapper contract
Adapters must expose:
- capability ID and upstream package
- supported runtimes/frameworks
- initialization and cleanup
- reduced-motion behavior
- SSR/client constraints
- performance tier
- escape hatch to upstream instance/API
- known incompatibilities

## Source ingestion contract
When ingesting MIT copy-source UI:
- preserve license notices as required
- remove upstream brand styling
- remap typography/color/radius/spacing to project Design DNA
- re-run accessibility and motion QA
- de-duplicate behavior against existing recipes
- record upstream repo + commit/tag when practical

## Update policy
Do not pin design knowledge to star counts. Re-check repository status, license and breaking changes before major upgrades.
