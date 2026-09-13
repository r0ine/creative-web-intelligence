# External Library License & Redistribution Matrix

This is an engineering triage document, not legal advice. Before releasing a distributable package, re-check the current upstream license. The library must preserve required notices.

| Library | Upstream | License observed | Local policy | Tier |
|---|---|---|---|---|
| three.js | `mrdoob/three.js` | MIT | allowed-with-license-notice | primary |
| React Three Fiber | `pmndrs/react-three-fiber` | MIT | allowed-with-license-notice | primary |
| Drei | `pmndrs/drei` | MIT | allowed-with-license-notice | primary |
| React Postprocessing | `pmndrs/react-postprocessing` | MIT | allowed-with-license-notice | primary |
| postprocessing | `pmndrs/postprocessing` | Zlib | allowed-with-license-notice | primary |
| React Three Rapier | `pmndrs/react-three-rapier` | MIT | allowed-with-license-notice | secondary |
| three-mesh-bvh | `gkjohnson/three-mesh-bvh` | MIT | allowed-with-license-notice | secondary |
| Troika | `protectwise/troika` | MIT | allowed-with-license-notice | secondary |
| Lenis | `darkroomengineering/lenis` | MIT | allowed-with-license-notice | primary |
| Motion | `motiondivision/motion` | MIT | allowed-with-license-notice | primary |
| React Spring | `pmndrs/react-spring` | MIT | allowed-with-license-notice | secondary |
| use-gesture | `pmndrs/use-gesture` | verify-at-install | dependency-only-until-verified | secondary |
| Theatre.js | `theatre-js/theatre` | Apache-2.0 core; AGPL-3.0 studio | core-allowed-studio-is-development-tool-with-separate-terms | secondary |
| Tweakpane | `cocopon/tweakpane` | MIT | allowed-with-license-notice | secondary |
| Leva | `pmndrs/leva` | MIT | allowed-with-license-notice | secondary |
| PixiJS | `pixijs/pixijs` | MIT | allowed-with-license-notice | secondary |
| Babylon.js | `BabylonJS/Babylon.js` | Apache-2.0 | allowed-with-license-notice | secondary |
| OGL | `oframe/ogl` | verify-at-install | dependency-only-until-verified | secondary |
| Radix Primitives | `radix-ui/primitives` | MIT | allowed-with-license-notice | primary |
| shadcn/ui | `shadcn-ui/ui` | MIT | allowed-with-license-notice | primary |
| Floating UI | `floating-ui/floating-ui` | MIT | allowed-with-license-notice | primary |
| Motion Primitives | `ibelick/motion-primitives` | MIT | allowed-with-license-notice | primary |
| Magic UI | `magicuidesign/magicui` | MIT | allowed-with-license-notice | primary |
| UI Layouts | `ui-layouts/uilayouts` | MIT | allowed-with-license-notice | secondary |
| Kokonut UI | `kokonut-labs/kokonutui` | MIT | allowed-with-license-notice | secondary |
| Origin UI | `shadcn/originui` | MIT | allowed-with-license-notice | secondary |
| AutoAnimate | `formkit/auto-animate` | MIT | allowed-with-license-notice | secondary |
| Swup | `swup/swup` | MIT | allowed-with-license-notice | secondary |
| Barba.js | `barbajs/barba` | MIT | allowed-with-license-notice | secondary |
| p5.js | `processing/p5.js` | LGPL-2.1 | dependency-only-preferred | optional |
| React Bits | `DavidHDev/react-bits` | MIT + Commons Clause | DO-NOT-REDISTRIBUTE-AS-LIBRARY | restricted |
| LYGIA | `patriciogonzalezvivo/lygia` | Prosperity License + commercial path | RESTRICTED | restricted |
| React Three Offscreen | `pmndrs/react-three-offscreen` | MIT | allowed-with-license-notice | experimental |
| pmndrs market | `pmndrs/market` | MIT app; listed assets advertised CC0 | verify-asset-provenance | secondary |
| PixiJS AI Skills | `pixijs/pixijs-skills` | MIT | allowed-with-license-notice | secondary |
| Three.js Claude Skill Package | `OpenAEC-Foundation/Three.js-Claude-Skill-Package` | MIT | allowed-with-license-notice | secondary |

## Hard rules

1. **Permissive does not mean attribution-free.** Preserve license/copyright notices when required.
2. **Dependency != vendored source.** Prefer npm dependency/adapters for large maintained projects.
3. **React Bits:** do not redistribute its component code as part of this competing reusable library; keep it reference/app-level only under its current Commons Clause terms.
4. **LYGIA:** treat as restricted/reference-only by default; do not copy shader source into this library without appropriate rights.
5. **Theatre.js:** core and studio have different licenses. Keep Studio as a development authoring tool and out of production bundles.
6. **p5.js:** LGPL means it deserves separate compliance review; prefer dependency use over vendoring.
7. **Unknown/unclear:** `verify-at-install` blocks vendoring until a current license check is recorded.
