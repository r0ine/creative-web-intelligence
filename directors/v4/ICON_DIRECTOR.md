# ICON DIRECTOR v4

Icons are typography-adjacent interface marks, not decorative confetti.

## Pipeline
`communication job -> need/no-need -> family voice -> geometry/stroke -> semantic coverage -> state variants -> motion need -> optical alignment -> license -> implementation -> QA`

## First question: do we need an icon?
Reject the icon when readable text is clearer, when the mark repeats information, or when the icon exists only because a component template usually has one.

## Family coherence
Use one primary icon family per surface. A second family is allowed for a distinct job (for example animated state icons) only with a written reason. Avoid mixing Tabler, Lucide, Heroicons and another thin outline set in the same toolbar; small stylistic differences become visual noise.

## Stroke and optical rules
- Align icon visual mass with the typography, not only the CSS box.
- Compare icon cap-height against adjacent text.
- Match stroke density to text weight and UI density.
- Small icons may need simpler geometry or a slightly stronger stroke.
- Do not globally force every source into the same stroke width if that damages native geometry.

## Motion
Animation must communicate rendering, transition, progress or state. Line-MD is especially strong for one-shot render and state-transition icons. Infinite loops are reserved for genuinely continuous state and must have a reduced-motion/static variant.

## Anti-AI fingerprints
Reject or penalize:
- an icon before every nav item or section heading;
- Sparkles for every AI feature;
- Shield for every security sentence;
- Gear for every settings-related block when text is already clear;
- the same Lucide-style icon language on every brand regardless of concept;
- random outline/fill mixing;
- animated icons that replay whenever a section enters the viewport.

## Output
`required`, `family`, `familyReason`, `icons`, `stateVariants`, `sizeSystem`, `strokePolicy`, `motionPolicy`, `license`, `accessibility`, `fallback`, `antiGenericNotes`.
