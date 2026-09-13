# OKLCH & Modern CSS Color Workflow

Use OKLCH when programmatic palette generation or perceptual lightness control is useful.

Conceptually:
- `L` controls perceptual lightness
- `C` controls chroma
- `H` controls hue angle

Useful applications:
- creating predictable light/dark ramps
- reducing chroma while preserving hue identity
- generating hover states
- mixing accents with neutrals
- deriving surface families

Do not assume numeric equality means accessibility. Contrast must still be measured on actual rendered pairs.

Modern CSS relative colors and `color-mix()` can generate variations, but the production code should include browser-support/fallback decisions appropriate to the target project.

Example idea:
```css
:root {
  --brand: oklch(62% 0.14 180);
  --brand-soft: color-mix(in oklch, var(--brand), white 72%);
  --brand-dark: color-mix(in oklch, var(--brand), black 35%);
}
```
Treat this as a technique, not a mandatory syntax.
