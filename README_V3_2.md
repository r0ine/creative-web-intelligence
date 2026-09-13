# Creative Web Intelligence Library v3.2
## Color, Typography & Motion Art-Direction Hardening

v3.2 hardens the part of creative-web work most likely to expose an AI default: **color relationships, typography decisions, section composition and motion language**.

This is not a template collection. It is a decision system for Claude Code/Codex and human developers.

### What v3.2 adds

- Sanzo Wada color-intelligence layer built around the 348 historical combinations / 159-source-color dataset model.
- Source provenance rules: original/converted screen values are never treated as identical to printed pigment.
- A full-palette analyzer that reconstructs and scores every combination from either the Dain-style or mattdesl-style dataset.
- Web-role adaptation: background, surface, text, accent and decorative use are assigned after contrast checks, not by swatch order.
- Typography Director v3.2 with morphology, metrics, pairing, variable-font, fallback and line-breaking decisions.
- Font genericity detector that flags context-free defaults without banning popular families.
- Motion Grammar system: motion is selected by semantic role, not from one global reveal preset.
- Explicit anti-fingerprint rules for universal fade-up, stagger ladders, cardification, gradient blobs, divider spam and identical easings.
- Section-separation recipes that prefer composition and whitespace before borders.
- Visual Fingerprint Gate that scores repetition across color, type, layout and motion.

### Core order

`Reference -> Design DNA -> Color Director -> Typography Director -> Composition -> Motion Grammar -> optional 3D -> Accessibility/Performance -> Visual Fingerprint Gate`

### First files to read

1. `docs/V3_2_OVERVIEW.md`
2. `prompts/v3_2/MASTER_META_PROMPT_V3_2.md`
3. `color/v3_2/SANZO_WADA_COLOR_INTELLIGENCE.md`
4. `directors/v3_2/TYPOGRAPHY_DIRECTOR.md`
5. `motion/v3_2/ANTI_AI_MOTION_GRAMMAR.md`
6. `anti-ai/v3_2/VISUAL_FINGERPRINT_GATE.md`
7. `quality/V3_2_VISUAL_DIRECTION_GATE.md`

### Research integrity

Do not claim the historical print color is exactly represented by a web HEX value. Keep source/conversion metadata. Do not claim a palette is accessible because it is harmonious. Do not claim a font is appropriate because it is fashionable.
