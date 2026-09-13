# Creative Web Intelligence Library v5 — Authenticity Correction

v5 is a **correction layer** on top of the full v4 library. It exists because outputs produced under earlier versions kept converging on the same generative-web fingerprints:

- horizontal divider lines between every section
- background grid overlays for atmosphere
- bordered cards for every content block
- `opacity + translateY` as the universal entrance
- centered eyebrow + huge grotesk + two-CTA hero
- black surface + faint hairlines + one accent glow

The previous versions correctly *listed* these as anti-patterns but treated them as soft advice. v5 makes them **blockers**.

## What changed

- Rules were promoted from advisory to gate blockers.
- The 0–3 fingerprint score model was replaced with a blocker gate. Averaging is no longer possible.
- A strict divider hierarchy replaced the peer-equal `section_separation_recipes.json`.
- A stricter motion grammar with five hard blockers replaced the soft penalty list.
- Composition Restraint doctrine added: containers must be justified per unit.
- Typography-First Premium doctrine added: hierarchy uses at least two of six axes.
- Rest Zones added as a mandatory doctrine, not a reminder.
- A working static analyzer (`tools/v5/authenticity_check.py`) was added — regex-level, stdlib only, honest about its limits.
- Worked before/after example added showing what the same brief produces under v4 vs v5.

## What did not change

v4 remains intact. Color intelligence, source-aware asset selection, 3D art direction, scroll director, license/provenance, backend, and reference recreation are all in force. v5 changes how visual decisions are gated, not what they cover.

## Start here

1. Read `START_HERE_V5.md`.
2. Give the agent `prompts/v5/MASTER_META_PROMPT_V5.md`.
3. Read `v5/CORE_DOCTRINE.md` — the whole thesis in one page.
4. Read the six policy documents in `v5/` before making visual decisions.
5. Run the V5 Authenticity Gate via `directors/v5/QA_DIRECTOR_V5.md`.
6. For a built page, run `python tools/v5/authenticity_check.py path/to/build`.

## Core rule

> Design quality comes from decisions about hierarchy, typography, composition, and restraint. Decoration is what happens when those decisions were skipped.

## v4 material still applies

Everything in `README_V4.md`, `directors/v4/`, `data/v4/`, `source-intelligence/`, `quality/V4_SOURCE_ASSET_GATE.md`, and earlier version material remains in effect. v5 is additive.
