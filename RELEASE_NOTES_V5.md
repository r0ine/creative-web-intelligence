# Release Notes — v5.0 Authenticity Correction

## Summary

v5 exists because v4 outputs kept looking generated. The library had the anti-AI rules but treated them as soft advice. v5 makes them blockers, adds a working static analyzer, and tightens the doctrine around the specific patterns that were fingerprinting outputs.

Nothing in v4 was removed. v5 is a correction layer that sits on top.

## What was wrong in v4 (honest self-critique)

- All 42 anti-AI rules shared the same generic "Why" text ("The goal is deliberate, project-specific design—not detector evasion."). It taught nothing.
- The fingerprint gate was a 0–3 score across 13 categories. Averaging allowed weak designs to pass.
- `section_separation_recipes.json` listed dividers as an equal peer of whitespace. That is wrong; they are not peers.
- `MOT-003` said "avoid universal fade-up" but was rule 3 of 52, not a blocker.
- Rest zones were mentioned in one paragraph in `motion/v3_2/ANTI_AI_MOTION_GRAMMAR.md`, not a doctrine.
- No "does this section need containment?" test existed.
- No "would hierarchy hold if decoration were removed?" test existed.
- The QA director produced 0–100 scores across dimensions, letting visual polish hide critical failures.

v5 addresses each of these.

## New files

### Doctrine (`v5/`)
- `CORE_DOCTRINE.md` — one-page thesis.
- `DIVIDER_POLICY.md` — strict 7-level separation hierarchy with justification requirement.
- `ANTI_AI_VISUAL_FINGERPRINTS.md` — 25 fingerprints with description, why-AI, severity, detection, correction each.
- `MOTION_GRAMMAR_V2.md` — 5 hard blockers (MG-B01..B05).
- `COMPOSITION_RESTRAINT.md` — four-question containment test.
- `TYPOGRAPHY_FIRST_PREMIUM.md` — six-axis hierarchy rule.
- `DECORATION_VS_STRUCTURE.md` — three-question functional test.
- `REST_ZONES.md` — ≥30% rest coverage on long pages.
- `COLOR_RESTRAINT.md` — anti-default-dark discipline.
- `QA_VISUAL_AUTHENTICITY.md` — the blocker gate.

### Machine-readable data (`data/v5/`)
- `authenticity_fingerprints.json` — 25 fingerprints, structured.
- `divider_decision_matrix.json` — priority-ordered separation methods + 6 hard blockers.
- `composition_restraint_checks.json` — containment questions and structural/decorative lists.
- `motion_grammar_v2_rules.json` — 11 families, 5 blockers, amplitude ceilings.
- `rest_zone_recipes.json` — coverage rules and shape prompts.
- `decoration_vs_structure_tests.json` — three-question test data.

### Prompts (`prompts/v5/`)
- `MASTER_META_PROMPT_V5.md` — pipeline + non-negotiables + summary tests.
- `AUTHENTICITY_AUDIT_PROMPT.md` — audit existing sites.

### Directors (`directors/v5/`)
- `AUTHENTICITY_DIRECTOR.md` — new director with veto power.
- `COMPOSITION_DIRECTOR_V5.md` — supersedes v2 composition director.
- `MOTION_DIRECTOR_V5.md` — supersedes v3.2 motion director.
- `QA_DIRECTOR_V5.md` — supersedes v2 visual QA director.

### Quality (`quality/`)
- `V5_AUTHENTICITY_GATE.md` — the blocker-based release gate.

### Tools (`tools/v5/`)
- `authenticity_check.py` — static analyzer, stdlib only. Detects the 15+ most common source-level fingerprints via regex. Honest about what it can and cannot see.
- `validate_v5.py` — structural validator for the v5 layer.

### Examples (`examples/v5/`)
- `before_after_notes.md` — worked example: same brief, v4 output vs v5 output.
- `refactored_landing_spec.json` — machine-readable spec produced by the v5 pipeline.

### Docs
- `README_V5.md`, `START_HERE_V5.md`, `docs/V5_OVERVIEW.md`.

## What was superseded (but not deleted)

- The old `anti-ai/v3_2/VISUAL_FINGERPRINT_GATE.md` 0–3 score is retained for retrospective analysis but is no longer the release gate.
- `data/v3_2/section_separation_recipes.json` (dividers as peer of whitespace) is retained as a historical view; the v5 divider matrix is authoritative.
- `directors/qa/VISUAL_QA_DIRECTOR.md` (0–100 score) is retained but `directors/v5/QA_DIRECTOR_V5.md` is used for the release gate.

## What did not change

Full v4 material is intact and in force:
- Color Intelligence v3.2 (Wada + relationship-based color).
- Typography Intelligence v3.2 (morphology, roles, variable axes).
- Source Intelligence v4 (Iconify/Fontsource, license-aware).
- 3D Intelligence.
- Scroll Director.
- Backend Intelligence.
- Reference Recreation.

v5 layers on top. It does not replace them.

## How the AI-fingerprint problem was reduced

Six mechanisms:

1. **Blocker gate instead of score.** A design with any single blocker cannot pass. No averaging.
2. **Divider policy elevated to policy status.** A required `divider_justification` field with three keys forces every divider decision into the open.
3. **Universal fade-up is now a hard blocker** (`MG-B01`). Repetition on the second occurrence fails the gate.
4. **Cardification blocker** (`AF-C02`) triggers when >60% of leaf content shares identical container shape. Composition Director is forced to convert cards to regions.
5. **Rest zones mandatory** with ≥30% coverage on long pages. Motion cannot cover the whole page.
6. **Working static analyzer.** `tools/v5/authenticity_check.py` reads real HTML/CSS/JS and reports fingerprints. It is not perfect but it makes the gate mechanical rather than aspirational.

The combined effect: an output that reaches for the AI-slop patterns hits the gate before it ships. The library no longer *asks* the agent to avoid these patterns — it *requires* it.

## Remaining honest weaknesses

- **The static analyzer is regex-level.** It cannot compute cardification ratio precisely across a full framework build (React/Vue with dynamic class merging). It can flag patterns; a human reviewer still runs the three summary tests.
- **The three summary tests (decoration off, motion off, identity) require human judgment.** No tool in v5 automates them.
- **Fingerprint list is not exhaustive.** New AI-slop patterns will emerge. The catalog will need updates. Each addition should carry the same five-field discipline (description / why-AI / severity / detection / correction) — do not accept new entries with weaker documentation.
- **"Identity" test is subjective.** Two reviewers may disagree on whether a design is identifiably-*this*-brand vs generic. The doctrine is that when in doubt, it fails.
- **The library still contains legacy rule files with the identical generic "Why" text.** They have not been rewritten because v5 supersedes them via the gate, not by editing them in place. A future v5.1 could rewrite `anti-ai/anti-ai_intelligence.md` line by line.
- **Rest zone measurement.** Coverage percentage assumes the page can be measured. Single-page-app rendered content is harder to sample statically.
- **The blocker on centered-hero cliché** is set to "high" rather than "blocker" because there are legitimate uses (single editorial statement). This is a soft edge in the policy — an audit prompt is included to force a justification.
- **The tool exits non-zero on FAIL but does not gate CI automatically.** Wiring into a build pipeline is a project-level responsibility.

## Version compatibility

- v5 requires v4 material in the same repository. v5 doctrine references v4 directors and data.
- v5 does not require v3.1 or v3 material to be present, but they remain useful for backend/reference recreation.
- Downstream consumers should read the v5 gate result as authoritative for visual authenticity; v4 gate as authoritative for source/asset provenance; v3.1 gate as authoritative for production safety.

## Next expected iteration (v5.1)

Not committed, but sketched here so future work knows the direction:

- Rewrite `anti-ai/anti-ai_intelligence.md` rule-by-rule with real per-rule reasoning, replacing the identical generic "Why" text.
- Extend the static analyzer with an optional HTML DOM parser (still stdlib — `html.parser`) to compute cardification ratio and section geometry more accurately.
- Add a visual regression capture recipe for the two summary tests that can be captured (decoration off, motion off) via a Playwright helper.
- Add a "brand DNA identity" scoring rubric that at least structures the third summary test.
