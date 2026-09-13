# Font Loading & Variable Axes v3.2

## Loading strategy

- Prefer WOFF2 for web delivery where available.
- Load only styles/axes actually used.
- Preload only truly critical faces; too many preloads compete with other critical resources.
- Test cold load, cached load, slow network and web-font blocked states.
- Keep fallback text usable.

## Fallback metrics

Use compatible system fallbacks first. Where justified, evaluate `size-adjust`, ascent/descent/line-gap overrides and `font-size-adjust` to reduce layout shift. Validate visually; do not copy metric values from another font.

## Variable fonts

Prefer high-level CSS properties for registered axes when possible:

- weight -> `font-weight`
- width -> `font-stretch`
- slant/italic -> `font-style`
- optical size -> `font-optical-sizing`

Use `font-variation-settings` for custom or deliberately low-level control.

If the font supports optical sizing, `font-optical-sizing: auto` is normally the starting point. Do not animate variable axes merely because the file supports them.

## Kinetic typography gate

Axis animation must communicate state, progression, identity or spatial continuity. Continuous breathing width/weight animation on ordinary headings is rejected by default.
