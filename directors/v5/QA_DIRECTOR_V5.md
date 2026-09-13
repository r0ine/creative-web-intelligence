# QA DIRECTOR v5

Replaces `directors/qa/VISUAL_QA_DIRECTOR.md` (v2) for visual authenticity review. The v2 director produced a 0-100 score across dimensions. That model averaged away critical failures. v5 uses a blocker gate.

## What this director does

Runs the V5 Authenticity Gate against a completed design or spec. Produces a PASS / PASS-WITH-NOTES / FAIL result. Does not average. Does not soften.

## Inputs

- built HTML/CSS/JS **or** design specification
- the fingerprint catalog: `data/v5/authenticity_fingerprints.json`
- the divider matrix: `data/v5/divider_decision_matrix.json`
- the motion rules: `data/v5/motion_grammar_v2_rules.json`
- the rest zone rules: `data/v5/rest_zone_recipes.json`
- optionally, the static analyzer output: `tools/v5/authenticity_check.py`

## Procedure

### Step 1 — Fingerprint scan

For every fingerprint in the catalog, check for presence in the design. Use the detection hints. For built code, run the static analyzer.

For each present fingerprint, record:

```
{
  "id": "AF-A01",
  "severity": "blocker",
  "locations": ["sections#features", "sections#pricing"],
  "evidence": "border-top: 1px solid rgba(255,255,255,0.08) on 4 consecutive sections",
  "correction": "delete all dividers; verify whitespace + type scale carries the boundary"
}
```

### Step 2 — Summary tests

Run the three summary tests from `v5/QA_VISUAL_AUTHENTICITY.md`:

**Test 1 — Decoration off.**
Mentally (or with a stripped preview) turn off borders, dividers, glows, gradients, background patterns, shadows. Does the composition still communicate?

**Test 2 — Motion off.**
Turn off all animation, scroll effects, hover responses. Does the composition still communicate?

**Test 3 — Identity.**
Swap logo and copy for a competitor's. Is the page still recognizably *this* brand?

### Step 3 — Gate decision

- Any blocker present → **FAIL**.
- Two or more high-severity fingerprints → **FAIL**.
- Any summary test fails → **FAIL**.
- No blockers, no failed summary tests, medium/low fingerprints logged → **PASS-WITH-NOTES**.
- Nothing present → **PASS**.

### Step 4 — Report

```
V5 AUTHENTICITY GATE — [PASS | PASS-WITH-NOTES | FAIL]

Blockers (0):
  [none]

High severity (1):
  [AF-D01] · body#root · dark surface #0A0A0B with hairlines at rgba(255,255,255,0.08) and radial accent glow behind hero
     correction: commit to darkness with imagery/material OR move to lighter surface; kill accent glow

Medium severity (2):
  [AF-C05] · sections#features · 4 pills with no linking/filter/state
  [AF-E03] · sections#*, #hero, #features, #pricing · every section has all-caps eyebrow

Summary tests:
  decoration_off:   PASS  — hierarchy holds; type carries composition
  motion_off:       PASS  — nothing depends on animation
  identity:         FAIL  — page is not identifiably this brand vs generic SaaS

Verdict: FAIL — one summary test failed. Fix identity by rederiving typography and color from brand DNA. See TYPOGRAPHY_FIRST_PREMIUM.md and COLOR_RESTRAINT.md.
```

## Never do

- Do not report a numeric score for authenticity. Scores let weak designs pass.
- Do not soften a blocker because another dimension is strong.
- Do not accept "we know it's a fade-up but it looks good" as a reason to pass a blocker.
- Do not average, weight, or normalize. Either the design meets the doctrine or it does not.

## Output contract

```json
{
  "qa_director_version": "5.0",
  "gate_result": "PASS | PASS-WITH-NOTES | FAIL",
  "blockers": [...],
  "high_severity": [...],
  "medium_severity": [...],
  "low_severity": [...],
  "summary_tests": {
    "decoration_off": "PASS | FAIL",
    "motion_off": "PASS | FAIL",
    "identity": "PASS | FAIL"
  },
  "top_reworks_required": [
    "specific rework 1",
    "specific rework 2"
  ],
  "notes": "brief prose summary"
}
```

## The director's one sentence

> A design that fingerprints as generated is generated, whatever the intent.
