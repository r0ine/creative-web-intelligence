# 3D ART DIRECTOR v2

## Order of decisions
1. Narrative purpose of 3D
2. Primary object / environment
3. Camera language
4. Light hierarchy
5. Material family
6. Scene states
7. DOM/WebGL relationship
8. Effects
9. Quality tiers / fallback

## Hard rule
A chrome sphere, particle field, bloom and cursor parallax do not constitute art direction. Effects are added only after the scene works with flat materials and basic lighting.

## Renderer strategy
Support WebGL2 broadly; make WebGPU optional/progressive where suitable. Three.js WebGPURenderer can select WebGPU and fall back to WebGL2, but project compatibility must be tested.

## Performance
Avoid React setState in frame loops. Reuse resources, control DPR, pause offscreen work, and maintain mobile-specific scene states.
