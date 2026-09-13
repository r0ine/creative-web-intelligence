# Line-MD Profile

Snapshot: 1,218 icons, 24px grid, MIT, Iconify prefix `line-md`.

## Strength
Line-MD's defining value is authored icon motion. Most icons use short rendering animation; transition and loop variants exist.

## Best use
- menu/open-close transitions
- success/error/status state changes
- media controls
- short action feedback
- one or two signature motion moments in an otherwise quiet interface

## Avoid
- running several loops in the same viewport
- replaying all icon animations on every scroll reveal
- substituting animated icons for clear labels

## Accessibility
CSS-animation variants can respect `prefers-reduced-motion`; always define a static fallback.
