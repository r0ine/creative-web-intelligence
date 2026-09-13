# MASTER META-PROMPT — CREATIVE WEB INTELLIGENCE LIBRARY

You are operating inside a reusable creative-development knowledge/library repository. **Do not build a generic website from scratch before inspecting this library.**

## Mission
Use research, rules, recipes and engines in this repository to create project-specific 2D/3D web experiences with strong typography, color, layout, motion, WebGL integration, performance and accessibility.

## Mandatory workflow
1. Read `research/INDEX.md` and `research/methodology.md`.
2. Search `data/source_registry.json` only when a reference/source claim matters.
3. Read the relevant category intelligence files instead of loading everything blindly.
4. Search `data/initial_recipes.json` for reusable behavior before implementing a new one.
5. For any supplied screenshot/video/site, create a structured ReferenceProfile before coding.
6. Separate OBSERVED, INFERRED and PROPOSED decisions.
7. Create a project Design DNA: typography, palette, geometry, grid, spacing, motion language, 3D role, camera language and performance tier.
8. Select a small coherent set of recipes. Do not use features simply because they exist.
9. For 3D work, define the central 3D concept and scene states before shaders/post-processing.
10. Build mobile/reduced-motion behavior at the same time as desktop.
11. Run anti-AI/generic-quality checks before delivery.

## Non-negotiable rules
- The output must not default to centered hero + gradient headline + two buttons + three cards.
- Do not default to purple/blue gradients, glass panels, huge radii, neon glow, chrome spheres, toruses, black voids or star particles.
- Do not fabricate testimonials, clients, metrics, press or research claims.
- Do not claim a reference uses a font/shader/easing/tool unless verified.
- If the input Reel is inaccessible, mark details `NEEDS_CAPTURE` and work from verified principles only.
- 3D must change information architecture, storytelling, product understanding or interaction; otherwise remove it.
- Keep critical content in accessible DOM.
- Respect reduced motion and touch/no-hover devices.
- Measure performance and scale down expensive effects on weak/mobile devices.

## ReferenceProfile fields
- source
- confidence
- composition
- grid
- typography roles
- color relationships
- surface/geometry language
- spacing/rhythm
- media role
- motion triggers
- motion responses
- camera behavior
- 3D object role
- lighting/material language
- shader/postFX observations
- navigation
- interaction model
- mobile behavior
- signature details
- anti-patterns to avoid
- capability mapping to library recipes

## Recipe selection rules
Prefer 1 primary concept + supporting behaviors. Example:
- primary: `Product exploded view`
- support: `Camera state interpolation`, `Part focus + DOM label`, `Pinned chapter timeline`, `Adaptive DPR`

Avoid combining unrelated spectacle such as GPGPU particles + heavy DOF + constant cursor deformation + route shader wipes unless the concept truly requires them.

## Agent reuse rule
Before writing a new creative behavior:
1. Search recipe catalog.
2. Search capability docs.
3. Reuse/extend an existing primitive.
4. Create project-local code only if no reusable primitive fits.
5. If the behavior will recur across projects, promote it back into the library with schema/docs/tests.

## Quality gate
Before finalizing, answer:
- If logo/copy changed, could this be any startup? If yes, redesign.
- If 3D is removed, is the experience basically unchanged? If yes, integration is too weak.
- Are typography, color, layout and motion driven by one Design DNA?
- Are multiple sections mechanically identical?
- Are there fake or generic content blocks?
- Does mobile feel composed rather than shrunk?
- Does reduced motion retain all meaning?
- Are effects justified by content/brand/interaction?
- Did the implementation actually match the rationale?

## Research expansion
When adding new YouTube/Instagram/Awwwards/Codrops/studio research:
- append source to `data/source_registry.json`
- capture exact observable claims only
- write derived principles separately
- deduplicate semantic repeats
- tag confidence
- add useful recipes only when they represent a distinct behavior, not cosmetic variations

This repository is a living creative-development intelligence system, not a template pack.


# COLOR INTELLIGENCE REQUIREMENT
The library must teach color combination logic, not merely store swatches. Implement harmony models, semantic role assignment, light/dark adaptation, contrast metadata, area guidance, 3D lighting/material integration, machine-readable palette recipes and a Color Director agent fragment. See `color/` and `data/color_combination_recipes.json`.
