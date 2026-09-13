# Decoration vs Structure v5

Every visual element on a page is either **structural** (it does compositional or informational work) or **decorative** (it is there to make the page feel finished).

Structural is fine. Decorative is a problem when it stands in for a decision that wasn't made.

This document defines the test.

## The three-question functional test

For every visible element that is not content itself, ask:

### 1. What job does this element do?

State it in one sentence. Not "it looks good" — an actual job. Examples of real jobs:

- "It marks the boundary between the editorial section and the reference index."
- "It separates the primary CTA from the secondary."
- "It contains the media so the caption reads as belonging to the image."
- "It signals the state change from draft to published."

Examples of not-a-job:

- "It makes the section feel complete."
- "It matches the rest of the page."
- "It gives the page a technical feel."
- "It's a nice visual detail."

### 2. What breaks if it is removed?

Delete the element mentally. What is lost?

- If **understanding, hierarchy, or comprehension** is lost, the element is structural. Keep it.
- If **finish or polish** is lost but nothing communicative changes, the element is decorative. Delete it.

### 3. Is a stronger structural device already doing the same job?

If a hairline separates two sections but the whitespace, alignment shift, or heading already communicates the boundary, the hairline is redundant. Remove it.

## Structural elements

Elements that legitimately carry compositional or informational load:

- **Type hierarchy** — display, heading, body, label. Structural by nature.
- **Whitespace and vertical rhythm** — structural. The most under-used structural device in generative outputs.
- **Alignment axes** — the columns and edges the composition uses. Structural.
- **Deliberate surface changes** — a real tonal shift between sections. Structural if it communicates mode change.
- **Media edges** — image or video bounds that mark composition. Structural.
- **Containers that hold interactive units** — cards for clickable items. Structural.
- **State indicators** — a fill color or badge that shows something *is* something. Structural.

## Commonly decorative elements

Elements that are decorative unless they earn structural status:

- Dividers, hairlines, `<hr>` — decorative by default. Structural only if they meet `DIVIDER_POLICY.md`.
- Corner brackets, register marks, viewfinder marks — decorative unless the interface is genuinely about measurement.
- Background grid overlays — decorative unless the grid is doing work (labels, measurements, alignment guides).
- Card borders on non-interactive content — decorative.
- Metadata pills that do not filter or link — decorative.
- Radial gradient auras — decorative unless they describe light source, focus, or heat/energy semantics.
- Gradient text fills — decorative.
- Glass panels without a scene behind them — decorative.
- Emoji feature icons — decorative shorthand.
- Fake terminals, fake dashboards, fake code windows — decorative and often dishonest.
- Hover-lift on non-interactive cards — decorative.
- Blur-in on entrance — decorative.
- All-caps eyebrows on every section — decorative once repetition sets in.

## The elimination pass

At QA time, run an elimination pass:

1. List every decorative element on the page.
2. Delete them one by one.
3. Note which deletions caused a real loss.
4. Anything whose deletion caused no loss → confirm delete.
5. Anything whose deletion caused a loss → understand *what* was lost, then decide whether a stronger structural device should carry that job.

The result is a page where every visible element is doing work.

## Decoration that has earned its place

Decoration is not banned. It is allowed when:

- It is a **chosen editorial device** used sparingly and consistently as brand voice.
- It is part of a **material or scene** the composition is genuinely about (light, texture, atmosphere).
- It carries an **information association** even if it also carries visual pleasure (a colored dot that indicates status also happens to be beautiful).

The test is not "is it pretty." The test is "is it doing anything."

## Symptoms of decoration filling gaps

If you find yourself reaching for any of these, pause and check the composition instead:

- "The section feels empty, let's add a grid pattern."
- "The card looks bare, let's add a subtle border."
- "The hero needs energy, let's put a glow behind it."
- "The list feels flat, let's put a hairline between each row."
- "The page feels quiet, let's add a floating 3D object."

Every one of these is decoration papering over a composition decision that was not made. Make the composition decision instead.

## The final decoration vs structure test

Print the page (or view it in a preview tool). For each visible element, mark it **S** (structural) or **D** (decorative). Count both.

- Ratio strongly toward **S** with a small number of well-placed **D** items → healthy.
- Ratio toward **D**, or heavy **D** noise between the **S** elements → decoration is doing too much of the work.

Fix by deleting **D** items, not by adding more **S** ones.
