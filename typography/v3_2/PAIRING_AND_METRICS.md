# Font Pairing & Metrics v3.2

## Pair roles, not labels

"Serif + sans" is not a pairing strategy. Pairing must explain what each family does.

Good contrasts can come from:

- expressive display + quiet reading face
- wide display + compact UI family
- high-contrast editorial face + low-contrast utilitarian body
- one variable superfamily using width/weight/optical-size changes
- body family + mono accent for data/code only

## Compatibility checks

Compare actual specimens for:

- x-height relationship
- cap-height relationship
- glyph width/rhythm
- stroke contrast
- terminal shapes
- round forms
- punctuation
- numerals and tabular numbers if data-heavy
- lowercase texture
- italic behavior
- Turkish and all other required glyphs

Too-similar can look accidental. Too-different can look like two brands fighting.

## One-family preference

Before adding a second family, ask whether weight, width, optical size, italics and case can create enough hierarchy inside one family. One-family systems are often stronger and cheaper to load.

## Genericity rule

Popular families are not banned. Context-free use is. A family earns a place when its metrics, voice, language coverage, licensing and role support the brief.

## Turkish coverage gate

For Turkish projects, render at minimum:

`abcçdefgğhıijklmnoöprsştuüvyz ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ`

Also test punctuation, currency, dates, numerals and any English fallback content.
