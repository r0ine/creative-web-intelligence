# v9 release notes

**Language:** [Türkçe](RELEASE_NOTES_V9.md) · English

## Understanding revision feedback

- [Revision workflow](reference-engine/REVISION_FEEDBACK.md) (Turkish): when the user gives only a feeling ("içime sinmedi", "doesn't feel right"), the agent changes nothing and first asks **"Where?"** with concrete options. If the answer is "overall", it starts with the most visible surfaces: background, first screen, dominant color, display typography. Parts the user liked are preserved; "the previous one was better" is treated as a revert.
- [`data/v9/visibility_ranking.json`](data/v9/visibility_ranking.json): 11 surfaces ranked by first-impression weight, each with what can change and where to look in CSS.
- [`data/v9/feedback_lexicon.json`](data/v9/feedback_lexicon.json): 11 Turkish/English feelings and directions (cheap, boring, cluttered, AI-looking, too dark, cold, flashy, empty, dated, revert), each with likely causes, first moves and fixes to avoid.
- `tools/v9/feedback_triage.py`: turns a sentence into location, direction, preserved parts and the question to ask. Handles Turkish casing and ASCII spelling, separates negations such as "güzel değil", and never proposes more than three questions.

## Rule precedence and conflict register

- [Rule precedence](v9/RULE_PRECEDENCE.md) and [`data/v9/rule_precedence.json`](data/v9/rule_precedence.json): 34 director files mapped to 22 domains. Older files in a shared domain now begin with an **Öncelik (v9)** note naming the winning file.
- 8 cross-version contradictions recorded with a resolution: atmospheric particles, decorative glass/chrome 3D, unjustified dark palettes, shared easing across all roles, reduced motion as "shorter", animated dividers, mono body text and default fonts, overshoot easing.
- 13 cross-file id collisions listed with reasons.
- `tools/v9/precedence.py`: shows a domain's winning director, a file's status and the conflict affecting a catalog record.

## Guarding growth

`tools/v9/validate_v9.py` fails on an unregistered director, an older director without a pointer to its winner, an unlisted id collision, an open conflict whose old data was fixed, removed evidence, or one phrase mapped to two meanings. `tools/validate_all.py` now runs the v9 chain.

## Fixes

- Corrected the non-existent `scroll/SCROLL_DIRECTOR.md` path in `v6/MOBILE_MEDIA_STRATEGY.md`.
- v7 and v8 validators accept manifest version `9.0`.
