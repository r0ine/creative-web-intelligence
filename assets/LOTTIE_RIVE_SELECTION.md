# Lottie vs Rive vs CSS/SVG

Use **CSS/SVG** for simple deterministic micro-motion.
Use **Lottie/dotLottie** for authored timeline motion that does not need complex runtime state.
Use **Rive** when interactive states, inputs or state-machine control are part of the experience.
Use **video** only when raster/filmic content makes vector formats unsuitable.

Always define reduced-motion and static fallbacks. Runtime capability is not a justification for autoplay loops.
