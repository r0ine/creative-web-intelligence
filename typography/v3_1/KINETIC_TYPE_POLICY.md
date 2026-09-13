# Kinetic Typography Policy

Text motion must preserve legibility and reading order.

Prefer transform/opacity/clip/reveal techniques that do not repeatedly reflow layout. If splitting text into lines/words/chars for animation, preserve accessible reading text and rebuild splits after responsive reflow when necessary.

Use kinetic type for hierarchy or narrative state changes, not on every heading. Reduced-motion mode should present final readable content without dependence on animation.
