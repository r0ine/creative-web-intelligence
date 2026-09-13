# Video → Motion Timeline

For a supplied screen recording/video:

- record video duration and frame rate if available,
- identify scene boundaries and scroll-direction changes,
- sample key frames at transitions plus periodic checkpoints,
- map each scene to normalized local progress rather than absolute video timestamps,
- identify pinned vs naturally scrolling regions,
- record when elements enter, become dominant, transform, hand off and exit,
- distinguish scroll-driven motion from autoplay/hover/cursor motion,
- infer easing class only when enough frames support it,
- flag uncertain behaviors instead of inventing them.

Output `reference-motion-timeline.json`.
