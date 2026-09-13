# Authenticity Audit Prompt v5

Audit an existing website (or design mock) for v5 authenticity. Do not redesign yet. Report what is wrong first.

## Return the following

### 1. Scan result

For each fingerprint in `data/v5/authenticity_fingerprints.json`, report presence with evidence and location:

```
[AF-B01] · sections#features, #testimonials, #pricing · 3 sections use the same fade-up-30 helper (js:reveal.js:14)
[AF-C02] · content · 74% of leaf blocks share (border-radius: 12px, border: 1px rgba(255,255,255,0.06), padding: 24px)
[AF-D01] · body · #0A0A0B surface + rgba(255,255,255,0.08) strokes + purple radial glow behind hero
```

### 2. Divider audit

List every divider in the design. For each:

- Location.
- Whether a `divider_justification` exists (usually no).
- The specific separation method from `data/v5/divider_decision_matrix.json` that would replace it.

### 3. Motion audit

- Dominant motion family (or list of grammars if the page has no dominant one).
- Number of sections animating in.
- Whether entrance recipes repeat.
- Easing token count (want ≥ 3 distinct across UI/editorial/object).
- Rest zone coverage percentage.

### 4. Composition audit

- Region-vs-card ratio.
- Symmetry vs asymmetry usage.
- Density rhythm (list of zones in page order: dense / quiet / transition).
- Presence of centered-hero cliché.
- Uniform section geometry check.

### 5. Typography audit

- Number of hierarchy axes in use (size / weight / width / case / tracking / family).
- Presence of gradient text.
- Presence of mono-as-body.
- Presence of all-caps eyebrow spam.

### 6. Color audit

- Surface strategy (chosen or defaulted).
- Accent count.
- Presence of blue-purple gradient identity.
- Presence of dark + hairlines + accent glow default.

### 7. Summary tests

Run all three:
- Decoration off — does composition hold?
- Motion off — does composition hold?
- Identity — is this identifiably *this* brand?

### 8. Gate verdict

`PASS` / `PASS-WITH-NOTES` / `FAIL`. State the reason in one sentence.

### 9. Top 5 required reworks

Ordered by leverage. Each rework should target a doctrine, not a symptom:

> "Delete the reveal helper (kills MG-B01/AF-B01)." — not — "Change the fade-up duration to 800ms."

## What you must not do

- Do not soften findings to protect the client's stated preferences.
- Do not produce a numeric score.
- Do not recommend "more variety" as a fix. Reduce, do not vary.
- Do not add new decorative devices to fix existing decorative devices.

## Tone

Direct. Critical. No hedging. If the page is a generic AI-slop composition, name it as such. The point of the audit is to make the required rework unmissable.
