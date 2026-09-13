# Agent Selection Rules — External Libraries

Future Claude/Codex agents MUST use this sequence before adding a dependency.

## 1. Describe the problem, not the desired package
Examples: `persistent R3F canvas`, `accessible popover`, `scroll-synced camera`, `2D particle field`, `route transition`, `spring gesture`.

## 2. Search internal capability catalog first
If internal primitives already solve it, reuse them.

## 3. Search `open_source_library_registry.json`
Score candidates on:
- exact capability fit
- framework fit
- license/redistribution safety
- performance cost
- overlap with installed dependencies
- accessibility
- maintenance/update burden
- ability to preserve Design DNA

## 4. Choose one owner per responsibility
- 3D renderer: Three/R3F **or** Babylon **or** OGL, normally not multiple.
- route lifecycle: Swup **or** Barba **or** framework/native transition lifecycle.
- primary DOM motion: Motion **or** React Spring for most work; secondary utilities may exist for narrow jobs.
- dev controls: Leva for React/R3F, Tweakpane for framework-neutral workflows.

## 5. Generate an integration decision record
```json
{
  "problem": "scroll-synced 3D product story",
  "selected": ["threejs", "r3f", "drei", "lenis"],
  "rejected": {
    "babylonjs": "duplicates the scene engine",
    "ogl": "project benefits more from R3F ecosystem"
  },
  "risks": ["mobile GPU budget", "smooth-scroll accessibility"],
  "fallback": "native scroll + simplified scene"
}
```

## 6. Never auto-install a visual component library because it looks cool
Magic UI, Motion Primitives, UI Layouts, Kokonut UI and similar sources are pattern/capability pools. Select individual primitives and restyle them; never paste five libraries into one page.
