# v8: Turning sources into design decisions

v8 indexes the 46 GitHub URLs supplied for this release with access, redirect and license metadata. For a portfolio, landing page or dashboard, it chooses one starting reference and adds motion or 3D studies only when requested. It does not install templates or copy source code.

[The v8 workflow](START_HERE_V8.md) starts with a short visual prototype. [The source intelligence guide](source-intelligence/V8_SOURCE_INTELLIGENCE.md) defines five review lenses, evidence levels and compatibility gates. [The registry](data/v8/source_registry.json) preserves the requested URL alongside the current canonical URL. Metadata was checked on 17 October 2026 and may change.

```sh
python tools/v8/source_advisor.py --surface portfolio --framework next --motion 3d
python tools/v8/source_advisor.py --source ibelick/motion-primitives
python tools/v8/source_advisor.py --check greensock/gsap framer/motion --framework react
python tools/v8/validate_v8.py
```

The advisor reads local data and needs no API key. Its source card separates README findings from questions that still require rendered desktop, mobile and interaction inspection. The conflict check flags multiple application shells, styled UI foundations or motion owners. It treats React Three Fiber and Drei as a compatible dependency pair. License metadata alone never authorizes copying code or assets.

Two requested repository URLs returned 404 during this review, and GitHub did not provide recognized license metadata for 12 repositories. Their status remains visible rather than being silently treated as verified.
