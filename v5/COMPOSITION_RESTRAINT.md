# Composition Restraint v5

The generative-web default is to enclose everything in a container. Cards, panels, tiles, frames, boxes. The result is a page of boxes floating on a surface — a shape that reads as templated regardless of what is inside the boxes.

This document sets the discipline for containment decisions.

## The four questions before every container

Before wrapping content in a card, panel, or bordered region, answer these:

1. **Does this section need containment at all?** A section is not a card. A section is a region of vertical space. Most sections do not need any frame.

2. **Does this content need a box?** A box implies boundary. A boundary implies something inside is different from what surrounds it — a selection target, an interactive object, a piece of media that would otherwise bleed, a functional unit that can be swapped or removed. Plain prose does not need a box.

3. **Does this layout become stronger if the box is removed?** Try it. If deleting the container makes the composition read more clearly, delete the container.

4. **Is this line replacing a missing composition decision?** If a border, divider, or background block is doing the job that hierarchy, spacing, or typography should be doing, the composition has a hole.

If any answer is "no" or "yes" in the wrong direction, remove the containment.

## Legitimate reasons for containment

A container is justified when:

- **The content is an interactive target.** A card the user can click, drag, select, or expand.
- **The content is a functional unit.** A settings group, a form section, an item that can be removed or reordered.
- **The content is media that would otherwise leak.** An image or video whose bounds need to be respected by adjacent content.
- **The content is genuinely a peer of siblings.** Product tiles, article cards, gallery items where the container defines "one of many equivalent things."
- **The content changes state visibly.** A panel that expands, a card that flips, a tile that highlights.

Not justified:

- "It looks better with the box."
- "It matches the other sections."
- "The section needed a background."
- "The border makes it feel finished."

## The default rendering unit is a region, not a card

A **region** is a vertical space with:
- deliberate top and bottom spacing
- content arranged on a chosen alignment axis
- typography that carries the hierarchy
- no frame, unless the four questions above justified one

Build sections as regions first. Convert to cards only if the four questions demand it.

## Asymmetry

If every section is centered, the page reads as templated. Introduce asymmetry where content suggests it:

- Feature blocks with a dominant primary and smaller supports rather than three equal cards.
- Editorial paragraphs offset to one column, not centered on the page.
- Hero content in a 60/40 or 40/60 split with media rather than stacked and centered.
- A heading placed against a large calm area rather than framed by decoration.

Asymmetry is not a style. It is what happens when composition decisions reflect content rather than templates.

## Calm areas are compositional decisions

Large stretches of quiet space — a section that is mostly empty with one headline, or a paragraph placed against a wide margin — read as intentional restraint. They are also structural. They:

- signal a mode change (from dense to reflective, or vice versa)
- give the eye a place to rest between denser sections
- create rhythmic contrast that reads as art direction

Do not fill calm areas with decoration to make them "feel productive." Calm is the value.

## Rhythm and density contrast

A well-composed page moves between:
- **dense zones** — data, tables, dense product blocks, information architecture
- **quiet zones** — a single headline, an image, a paragraph in wide margin
- **transition zones** — media, section shifts, chapter markers

The alternation itself is the rhythm. Repeating dense-dense-dense or quiet-quiet-quiet reads as monotone.

## Grid decisions come after content decisions

Do not open composition with "12-column grid at 1440." Open with:

1. What is the content hierarchy?
2. What is the reading path?
3. What are the density zones?
4. What is the focal moment?
5. What does mobile want, not what does mobile shrink to?

Then choose the grid family that makes the answers legible.

## Mobile is not a scaled desktop

Mobile composition is *recomposed*, not shrunk. A three-column feature block on desktop may become a stacked pair-plus-one on mobile. A 60/40 hero may become media-then-copy stacked. The composition changes because the viewport changes what a good reading path is.

If mobile is `flex-direction: column` applied to the desktop layout, mobile was skipped.

## The containment test

Take the finished design. Ask:

- How many of the containers on this page have a real containment reason?
- If the containers were removed and only spacing and typography carried the hierarchy, would the page still communicate?
- Are there any regions that would read *better* without a container?

If the answer to the middle question is no, the page is over-contained.

## The final composition test

Grayscale the design. Remove borders, dividers, glows, gradients, and shadows. Look at what remains: pure typography and layout.

- Does the hierarchy still read?
- Does the reading path still lead the eye?
- Does the composition still have identity?

If yes, the composition is doing its job and everything else is honest support. If no, the composition was hiding behind decoration.
