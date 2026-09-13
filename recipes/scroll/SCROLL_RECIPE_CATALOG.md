# Scroll Recipe Catalog (100)

Machine-readable source: `data/v2/scroll_recipes.json`.

## depth-parallax

- **scroll-001 — Layered Depth Drift**: Separate foreground, midground and background with different scroll amplitudes so depth reads before decoration. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 2/5.
- **scroll-002 — Foreground Pass-By**: Move near-edge foreground geometry faster than the camera plane to create a convincing pass-by moment. Tech: gsap-scrolltrigger, r3f. Cost: 2/5.
- **scroll-003 — Perspective Scale Compression**: Scale nearer layers non-linearly while distant layers remain restrained, suggesting forward travel. Tech: gsap-scrolltrigger, r3f. Cost: 2/5.
- **scroll-004 — Depth Fog Progression**: Change fog/contrast by scroll depth instead of moving every layer. Tech: r3f, css-scroll-timeline. Cost: 1/5.
- **scroll-005 — Occlusion Reveal**: Let a foreground plane naturally hide/reveal content as the user moves through the composition. Tech: gsap-scrolltrigger, r3f. Cost: 2/5.
- **scroll-006 — Parallax Breathing Room**: Use intentionally low-amplitude parallax only around focal transitions, leaving reading zones almost still. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-007 — Reverse Depth Countermotion**: Move one distant layer slightly against the dominant direction to increase spatial separation without large travel. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-008 — Near-Plane Expansion**: Allow near geometry to enlarge and exit the viewport while the background remains stable. Tech: gsap-scrolltrigger, r3f. Cost: 2/5.
- **scroll-009 — Atmospheric Depth Fade**: Progressively lower saturation/contrast in distant layers as scroll advances through a deep scene. Tech: css-scroll-timeline, r3f. Cost: 1/5.
- **scroll-010 — Depth Window Transition**: Treat a section as a window into a deeper layer, then enlarge that window until it becomes the next scene. Tech: gsap-scrolltrigger. Cost: 2/5.

## pinned-narrative

- **scroll-011 — Pinned Scene Chapters**: Keep one visual stage pinned while content chapters advance and update a centralized scene state. Tech: gsap-scrolltrigger. Cost: 4/5.
- **scroll-012 — Sticky Visual Handoff**: Hold a visual while adjacent text changes, then hand the sticky role to the next visual at a deliberate beat. Tech: css-sticky, gsap-scrolltrigger. Cost: 2/5.
- **scroll-013 — Persistent Object Story**: Keep one hero object present across multiple sections and transform it rather than replacing it. Tech: gsap-scrolltrigger, r3f. Cost: 4/5.
- **scroll-014 — Pinned Split Narrative**: Pin either text or media while the other side advances, then swap dominance once for emphasis. Tech: css-sticky, gsap-scrolltrigger. Cost: 2/5.
- **scroll-015 — Chapter State Corridor**: Map scroll ranges to named states such as intro/detail/explode/reassemble/outro instead of scattered triggers. Tech: gsap-scrolltrigger, r3f. Cost: 4/5.
- **scroll-016 — Short Pin Emphasis**: Use a brief pinned beat to make one transformation legible, not a long forced scroll jail. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-017 — Pinned Canvas Longform**: Maintain one Canvas across a long section while DOM content controls scene states and camera targets. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-018 — Progressive Sticky Stack**: Use sticky layers that overlap in a controlled hierarchy, each retiring before visual clutter accumulates. Tech: css-sticky, gsap-scrolltrigger. Cost: 2/5.
- **scroll-019 — Narrative Rest Stop**: Insert a nearly static pinned/rest state between high-motion chapters to restore reading focus. Tech: gsap-scrolltrigger, css-sticky. Cost: 1/5.
- **scroll-020 — Pin-to-Flow Release**: Transition from pinned choreography back to normal document flow without a visible jump or spacer artifact. Tech: gsap-scrolltrigger. Cost: 2/5.

## typography-scroll

- **scroll-021 — Tracking Expansion Exit**: Gradually increase headline tracking as it recedes or yields to the next scene. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-022 — Line Mask Reveal**: Reveal text lines through a clipping window synchronized to section progress. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-023 — Foreground Text Occlusion**: Allow spatial foreground layers to cover portions of oversized text without destroying semantic DOM text. Tech: r3f, gsap-scrolltrigger. Cost: 2/5.
- **scroll-024 — Variable Font Axis Shift**: Animate a variable font width/weight axis subtly as the narrative changes emphasis. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-025 — Word Sequence Focus**: Bring one phrase at a time into emphasis while nonactive words remain readable but visually quiet. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-026 — Vertical Type Conveyor**: Move a restrained column of labels through a fixed reading zone for chapter navigation or credits. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-027 — Headline Scale Transfer**: Reduce a hero title while a section title grows, visually transferring hierarchy rather than fading both independently. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-028 — Text Window Media Reveal**: Use large text as a temporary clipping window for media, then release the media into its own frame. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-029 — Pinned Headline Retire**: Hold one headline long enough to establish a chapter, then mask it away as the next chapter takes focus. Tech: gsap-scrolltrigger, css-sticky. Cost: 2/5.
- **scroll-030 — Reading Progress Accent**: Use a minimal rule, glyph or index that advances with reading progress without becoming a HUD. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.

## media-scroll

- **scroll-031 — Cinematic Crop Reveal**: Animate image crop rather than whole-image movement, preserving a deliberate focal point. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-032 — Cover-to-Frame Transition**: Start media as full-bleed and progressively resolve it into a framed editorial composition. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-033 — Focal Point Drift**: Shift object-position or transform subtly to follow the subject while the viewport crop changes. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-034 — Gallery Rail Progression**: Translate a curated media rail horizontally from vertical scroll with clear beginning and end states. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-035 — Filmstrip Scrub**: Advance through a short sequence of stills/frames tied to scroll, with preloading and reduced-motion fallback. Tech: gsap-scrolltrigger. Cost: 4/5.
- **scroll-036 — Video Timeline Scrub**: Bind a short optimized video segment to scroll progress only when seeking performance is acceptable. Tech: gsap-scrolltrigger. Cost: 4/5.
- **scroll-037 — Media Layer Peel**: Peel one media layer away to reveal the next, using masks instead of arbitrary card motion. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-038 — Image Depth Stack**: Use two or three media planes with distinct depth speeds and strict overlap control. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 2/5.
- **scroll-039 — Panorama Window**: Move a wide image behind a narrower viewport as scroll progresses, keeping typography outside the moving crop. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-040 — Media-to-Background Handoff**: Expand selected media until it becomes the environmental background for the following section. Tech: gsap-scrolltrigger. Cost: 2/5.

## camera-3d

- **scroll-041 — Cinematic Dolly In**: Move camera forward toward a focal object while target and FOV remain controlled. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-042 — Arc Around Product**: Travel along a shallow arc to reveal geometry without a full orbit-demo look. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-043 — Detail Target Handoff**: Transition camera target from whole object to one detail while position movement stays restrained. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-044 — Spline Journey**: Move along an authored spline only when spatial storytelling genuinely benefits from a continuous route. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-045 — FOV Compression Reveal**: Use a small FOV change to flatten or deepen perspective during a product/detail transition. Tech: r3f. Cost: 2/5.
- **scroll-046 — Foreground Flyby**: Pass one authored foreground element near the lens while the main camera path remains readable. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-047 — Camera Rest Plateau**: Hold camera nearly static over a progress range so content can be read without constant spatial motion. Tech: r3f, gsap-scrolltrigger. Cost: 1/5.
- **scroll-048 — Responsive Camera Reframe**: Use separate authored camera states for mobile instead of scaling desktop coordinates. Tech: r3f. Cost: 2/5.
- **scroll-049 — Depth Reveal Pullback**: Begin in a close detail and pull back to reveal the larger object/environment as context arrives. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-050 — Low-Angle Rise**: Combine a small vertical camera rise with target interpolation to reveal monumentality without dramatic rotation. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.

## object-3d

- **scroll-051 — Exploded View Scrub**: Move registered parts from assembled to authored exploded transforms with normalized progress. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-052 — Assembly Sequence**: Bring object parts together in a controlled dependency order rather than random stagger. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-053 — Component Highlight Relay**: Shift material/light emphasis between parts as explanatory content changes. Tech: r3f, gsap-scrolltrigger. Cost: 2/5.
- **scroll-054 — Material State Shift**: Interpolate roughness/emissive/transmission carefully to indicate mode/state change. Tech: r3f. Cost: 2/5.
- **scroll-055 — Object Turntable Restraint**: Rotate an object only through the angle needed to expose information, never continuous 360-degree spinning. Tech: r3f, gsap-scrolltrigger. Cost: 2/5.
- **scroll-056 — Morph Target Story**: Drive authored morph targets from scroll when geometry transformation is semantically meaningful. Tech: r3f. Cost: 4/5.
- **scroll-057 — Dissolve State Transition**: Use a restrained shader dissolve to transition between object states, with static fallback. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-058 — Object-to-UI Alignment**: Move a 3D object into alignment with a DOM information region before presenting details. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-059 — Scale-to-Detail**: Scale/reposition an object toward one detail while maintaining camera stability for legibility. Tech: r3f, gsap-scrolltrigger. Cost: 2/5.
- **scroll-060 — Reassembly Resolution**: Return transformed/exploded parts to a clean final state before the CTA/outro instead of ending in visual chaos. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.

## section-transition

- **scroll-061 — Geological Mask Wipe**: Use an irregular but controlled mask edge inspired by material/brand geometry to reveal the next section. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-062 — Shared Object Handoff**: Carry one object/image from one composition into the next rather than fading it out and recreating it. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-063 — Depth Fade Handoff**: Let the outgoing section recede in contrast/depth while the incoming section gains clarity. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-064 — Color Temperature Drift**: Transition environmental temperature slowly across a section boundary instead of abrupt background-color swaps. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-065 — Curtain Plane Reveal**: Use one large plane/media edge as a physical wipe between sections. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 2/5.
- **scroll-066 — Sticky Overlap Transition**: Allow the incoming section to overlap a sticky outgoing visual with a controlled z-order and retirement point. Tech: css-sticky, gsap-scrolltrigger. Cost: 2/5.
- **scroll-067 — Background Role Swap**: Promote an existing media/object from content role to background role across a transition. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-068 — Light-to-Dark Passage**: Use luminance progression as the transition itself, with typography contrast adapting continuously. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-069 — Frame Dissolve**: Reduce a visual frame/container until content visually joins the page field, avoiding another card-like box. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-070 — Scene Opening Release**: Move from a dense/narrow composition to a visually open composition as a narrative payoff. Tech: gsap-scrolltrigger, r3f. Cost: 4/5.

## horizontal-spatial

- **scroll-071 — Horizontal Editorial Rail**: Map vertical scroll to a horizontal sequence with readable section widths and an obvious exit. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-072 — Diagonal Story Track**: Move content along a shallow diagonal path when the composition itself establishes that direction. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-073 — Spatial Map Traverse**: Move a viewport/camera across a larger 2D/3D map where each stop represents a chapter. Tech: gsap-scrolltrigger, r3f. Cost: 4/5.
- **scroll-074 — Stepped Panorama**: Advance through panorama zones with short smooth ranges and rest plateaus, not a constant endless pan. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-075 — Orbital Chapter Navigation**: Move labels/objects along a partial orbital path while preserving normal DOM reading order. Tech: gsap-scrolltrigger, r3f. Cost: 4/5.
- **scroll-076 — Depth Tunnel Sections**: Translate successive planes through depth to create a tunnel-like journey with strict motion limits. Tech: r3f, gsap-scrolltrigger. Cost: 4/5.
- **scroll-077 — Sticky Track with Milestones**: Pin a track while milestone markers and content update at authored progress thresholds. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-078 — Alternating Side Passage**: Shift the focal composition left/right across chapters using spatial continuity rather than repeated slide-ins. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-079 — Large Canvas Pan**: Move through a deliberately composed oversized canvas, with boundaries and mobile re-authoring. Tech: gsap-scrolltrigger. Cost: 4/5.
- **scroll-080 — Path-Following Media Sequence**: Advance media anchors along a brand-specific SVG/curve path as the story progresses. Tech: gsap-scrolltrigger. Cost: 2/5.

## data-diagram

- **scroll-081 — Path Draw Explanation**: Reveal an SVG path progressively while associated labels enter at semantic milestones. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-082 — Node Network Sequence**: Activate diagram nodes in dependency order while keeping inactive structure visible. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-083 — Comparison Scrub**: Use scroll to interpolate between two visual states with a stable reference frame. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-084 — Timeline Milestone Progress**: Advance a timeline indicator and chapter content together, avoiding separate counters with no context. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-085 — Radial Progress Narrative**: Advance a radial indicator only when circular structure is semantically appropriate. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-086 — Map Route Progress**: Draw a route/path while the map view or annotations update at key locations. Tech: gsap-scrolltrigger. Cost: 2/5.
- **scroll-087 — Layered System Diagram**: Reveal architecture layers from foundational to dependent layers without hiding the overall topology. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-088 — Metric Context Reveal**: Bring numeric changes into focus alongside the visual evidence that explains them; avoid free-floating counters. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-089 — Before-After Split**: Move a single comparison boundary through an image/diagram while labels remain fixed and readable. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-090 — Diagram Focus Lens**: Emphasize one region of a complex diagram while dimming rather than removing context. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.

## ambient-scroll

- **scroll-091 — Light Direction Drift**: Shift key/rim light subtly across long scroll ranges to support chapter mood. Tech: r3f, gsap-scrolltrigger. Cost: 2/5.
- **scroll-092 — Fog Density Breathing**: Change atmospheric density slowly as the user moves deeper or exits a spatial scene. Tech: r3f. Cost: 2/5.
- **scroll-093 — Grain Intensity Modulation**: Adjust grain/noise intensity slightly between chapters; never animate noisy grain at high salience. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-094 — Background Tone Drift**: Interpolate background tones across large ranges to support narrative temperature shifts. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-095 — Shadow Length Shift**: Change shadow direction/length subtly as a physical cue for environmental progression. Tech: css-scroll-timeline, r3f. Cost: 2/5.
- **scroll-096 — Atmospheric Particle Calm**: Vary particle density/velocity within a narrow range based on section state, not raw wheel speed. Tech: r3f. Cost: 4/5.
- **scroll-097 — Texture Contrast Progression**: Adjust texture contrast or overlay strength to move between calm and dramatic chapters. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-098 — Edge Highlight Progress**: Use a thin line/edge highlight as subtle progress feedback on glass or structural UI. Tech: css-scroll-timeline. Cost: 1/5.
- **scroll-099 — Environmental Desaturation**: Reduce or restore saturation slowly to guide focus toward typography/media at specific chapters. Tech: css-scroll-timeline, gsap-scrolltrigger. Cost: 1/5.
- **scroll-100 — Idle-to-Scroll Energy**: Slightly increase environmental motion while scrolling and settle back to idle after input stops, with strict limits. Tech: gsap-scrolltrigger, r3f. Cost: 2/5.
