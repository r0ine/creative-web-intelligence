# Color Role Assignment

## Required core roles
Every serious palette should define tokens for:

- `background`
- `surface-1`
- `surface-2`
- `text-primary`
- `text-secondary`
- `border`
- `accent`
- `accent-hover`
- `focus-ring`

Applications should additionally define:

- `success`
- `warning`
- `danger`
- `info`
- `disabled-bg`
- `disabled-text`
- `selection`

## Rules
- Do not use `accent` as `danger` unless the brand itself is semantically red and ambiguity is solved another way.
- Do not use muted text by setting arbitrary `opacity: .4` over every background. Use a token that is tested on the actual surface.
- Do not make border color identical across every elevation if surface separation disappears.
- Focus is a first-class role, not an afterthought.
- Hover should not depend on hue shift alone; luminance, border, motion or underline can reinforce state.
- In 3D sites, DOM `accent` and WebGL emissive/key-light accents should be coordinated, not independently invented.

## Example token skeleton
```css
:root {
  --c-bg: #f7f7f2;
  --c-surface-1: #ffffff;
  --c-surface-2: #efefe8;
  --c-text: #151515;
  --c-text-muted: #5e625f;
  --c-border: #d9dbd4;
  --c-accent: #1f6f5f;
  --c-focus: #0b6cff;
}
```
The values are only an example. The role architecture is the reusable part.
