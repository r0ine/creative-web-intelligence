# Scroll Debugging

Debug geometry before easing.

Record:
- actual trigger positions
- section height/pin spacer height
- progress values at key visual states
- viewport size and DPR
- font/media load state
- route transition state

Typical root causes: font swap changed geometry, image has no intrinsic dimensions, nested transformed ancestor changed sticky behavior, pin spacer changed flow, timeline initialization ran twice, breakpoint cleanup failed.
