# Scroll Choreography System v3.1

## Model

Each scroll-driven chapter has:
- `purpose`
- `owner`
- `trigger_start`
- `trigger_end`
- `progress` 0..1
- `states`
- `handoff`
- `reverse_behavior`
- `mobile_variant`
- `reduced_motion_variant`
- `performance_tier`

## State phases

### Approach
Prepare visual focus before the section owns the viewport.

### Acquire
The section becomes dominant. Optional pin/sticky begins.

### Transform
Media/type/object/camera changes with bounded progress.

### Transfer
Introduce the next owner while reducing current dominance.

### Release
End pin/sticky cleanly and restore document flow.

## Rules

- Avoid nested independent scrub systems unless their progress relationship is explicit.
- Do not pin huge sections simply to make them feel “premium”.
- Do not tie layout-changing properties to every frame when transforms can express the motion.
- Avoid moving essential buttons away from users during interaction.
- Use one dominant choreography language and a smaller supporting language.
