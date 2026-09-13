# 3D / WebGL Color Direction

## Principle
The DOM and WebGL scene should appear to live in the same art direction.

## Build in this order
1. model/material base colors
2. environment/background family
3. light temperature
4. DOM neutrals
5. brand/action accent
6. emissive accents
7. post-processing

## Material rules
- Metallic surfaces inherit a large part of their perceived color from the environment. Do not judge them from albedo alone.
- Glass/transmission can distort background and accent relationships; test the final composite.
- Matte surfaces tolerate stronger base hue identity than highly reflective chrome-like materials.
- Emissive accent should usually be scarcer than DOM accent.

## Lighting rules
- Warm key + cool fill can create separation, but it should support the brand world rather than imitate a generic cinematic preset.
- If the background transitions hue during scroll, text and focus tokens may need coordinated state transitions.
- Bloom should be selective; a palette in which every bright color blooms loses hierarchy.

## Recommended scene palette record
Store:
- `environmentBase`
- `keyLightTemperature`
- `fillLightTemperature`
- `rimAccent`
- `materialFamilies`
- `emissiveAccent`
- `domBackground`
- `domText`
- `domAccent`
- `transitionStates`
