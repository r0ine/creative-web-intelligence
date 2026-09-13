# Reference Recreation Prompt v3.1

When a user provides screenshots or video, independently recreate the visible experience from the supplied reference.

1. Inventory viewports, sections, text blocks, assets, motion events and interaction states that are actually visible.
2. Build a geometry map (container widths, anchors, spacing ratios, crop behavior, section heights).
3. Build a typography map (family class, width, weight, x-height impression, line-height, tracking, casing, wrapping points).
4. Build a motion timeline using normalized progress and named states.
5. Distinguish verified observation from inference.
6. Implement with original code. Use user-supplied/authorized media; otherwise use placeholders/substitutes.
7. Capture matching viewport screenshots and compare structure first, then typography, then color/material, then motion/micro-detail.
8. Never copy hidden/proprietary source code, paid assets, restricted fonts, credentials or private endpoints from a reference site.
