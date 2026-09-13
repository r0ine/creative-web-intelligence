# Anti-generic — Quality Gates

Entries: **12**

## ANT-024 — Ban hardcoded desktop-only art direction

Mobile gets its own composition.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** responsive

## ANT-025 — Ban accessibility sacrifice

Premium does not mean motion that ignores reduced-motion or unreadable contrast.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** accessibility

## ANT-027 — Require design rationale→implementation check

If the plan says asymmetry, custom type hierarchy or reduced motion, verify the code actually implements it.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** qa

## ANT-028 — Require cross-project similarity check

Detect when two generated sites share too much layout/motion structure.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** qa

## ANT-029 — Require recipe diversity

100 variants cannot be color swaps of 5 behaviors.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** library

## ANT-032 — Require effect purpose field

Catalog effect entries should store why/when to use, not just how.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** library

## ANT-033 — Require incompatible-combination metadata

E.g. heavy DOF + tiny labels or multiple smooth-scroll engines should be flagged.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** library

## ANT-034 — Require performance level

Each recipe gets low/medium/high/very-high cost metadata.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** performance

## ANT-035 — Require mobile strategy

Every heavy effect has mobile adaptation/fallback.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** responsive

## ANT-036 — Require reduced-motion strategy

Every motion-heavy recipe has a reduced variant.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** accessibility

## ANT-037 — Require asset dependency list

Fonts/models/HDR/video dependencies are explicit.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** library

## ANT-039 — Require screenshot acceptance test

Generated examples are visually reviewed at multiple viewports.

**Why:** The goal is deliberate, project-specific design—not detector evasion.

**Tags:** qa
