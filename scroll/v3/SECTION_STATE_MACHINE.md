# Section State Machine

Each complex scroll scene should be specifiable as named states, for example:

- `S0_PRE`: section approaches
- `S1_LOCK`: primary frame becomes dominant
- `S2_REVEAL`: content layer 1 resolves
- `S3_TRANSFORM`: spatial/visual transformation
- `S4_HANDOFF`: next section starts to own attention
- `S5_EXIT`: scene releases cleanly

For every transition record:

- progress range
- affected properties
- easing or scrub behavior
- visibility/readability constraints
- z-index/layer rules
- pointer interaction state
- mobile alternative
- reduced-motion alternative
- cleanup behavior

This prevents magic offsets and overlapping animations that cannot be reasoned about.
