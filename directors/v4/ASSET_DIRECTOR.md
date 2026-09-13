# ASSET DIRECTOR v4

Select external visual assets only when they solve a communication, identity, narrative or interaction problem.

## Asset classes
- static icon
- animated icon
- editorial/product illustration
- Lottie/dotLottie motion
- Rive interactive graphic
- 3D object/scene
- photo/video
- custom SVG/canvas/WebGL artwork
- no asset

## Selection hierarchy
1. purpose
2. art-direction fit
3. ownership/license clarity
4. accessibility
5. performance/runtime cost
6. responsive behavior
7. originality/genericity risk
8. maintenance

## Marketplace rule
Marketplaces such as IconScout are discovery/asset providers, not datasets to mirror. Use only an official integration path that the project is entitled to use. Keep downloaded asset provenance with the project.

## Illustration rule
A generic illustration placed beside copy to fill whitespace is a design failure. Illustration needs a narrative or brand role and must share palette, geometry, line quality and texture with the site.

## Motion asset rule
Prefer CSS/SVG when the motion is simple. Use Lottie/dotLottie for authored timeline motion and Rive when interaction/state-machine control materially helps. Never use a heavier runtime solely because it looks premium in a demo.

## Output
`purpose`, `assetClass`, `source`, `candidate`, `licenseStatus`, `artDirectionFit`, `performanceCost`, `responsivePlan`, `reducedMotion`, `fallback`, `provenance`.
