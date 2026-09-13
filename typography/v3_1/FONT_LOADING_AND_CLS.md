# Font Loading, Performance and CLS

- Self-host only when licensing permits and operations are understood.
- Load only weights/styles/character sets actually used.
- Prefer modern compressed font formats supported by the target browsers.
- Preload only truly critical font files; over-preload hurts.
- Define `font-display` strategy intentionally.
- Test first render with cold cache and slow network.
- Ensure fallback metrics do not cause destructive layout shift.
- Avoid dozens of independent font files for tiny visual gains.
