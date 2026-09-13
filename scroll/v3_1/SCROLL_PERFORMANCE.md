# Scroll Performance

- Prefer compositor-friendly transforms/opacity.
- Batch DOM reads/writes; avoid repeated forced layout in frame loops.
- Use requestAnimationFrame/timeline engines rather than raw heavy work per scroll event.
- Pause expensive canvas/WebGL/video work when offscreen.
- Bound device pixel ratio and effects on high-density/mobile devices.
- Predecode/preload only media required soon; do not download an entire image sequence blindly.
- Clean up observers/listeners/timelines on route/component disposal.
- Test CPU-throttled/low-power behavior, not only a development workstation.
