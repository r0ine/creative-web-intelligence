# Web Type Composition v3.2

Typography determines composition before animation.

## Display type

Do not define hero type as simply `text-8xl font-bold`. Define:

- intended line count
- maximum measure
- width behavior
- optical-size behavior if available
- line-height transition across breakpoints
- tracking by size/case
- wrap strategy
- relationship to media/3D

Use `text-wrap: balance` selectively for short headings when it improves line shape. Do not use it as a substitute for authored copy or container width.

## Body type

Define reading measure, size, line height, paragraph spacing and link emphasis together. Consider `text-wrap: pretty` only where quality is worth the extra wrapping work. Long-form content should not inherit hero typography decisions.

## Hyphenation

Automatic hyphenation is language-dependent. If used, set the correct HTML `lang` and test the target browser/language. Do not turn it on globally without reviewing product copy.

## UI type

Buttons and labels need compactness, state clarity and consistent vertical metrics. Avoid aggressive negative tracking on small UI text. Use case changes for hierarchy only when readability survives.

## Responsive recomposition

Mobile is not desktop multiplied by 0.6. Re-author line count, measure, weight, tracking and sometimes font role. A three-line desktop hero may need different copy or width on mobile rather than a tiny font.
