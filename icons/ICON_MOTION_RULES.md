# Icon Motion Rules

Motion types:
1. **render** — one-shot appearance; acceptable for first meaningful state.
2. **transition** — preferred for toggles and mode/state changes.
3. **progress** — may repeat while a task is actually in progress.
4. **ambient loop** — default reject.

A loop must answer: *what ongoing state does this communicate?* If the answer is "it looks cool", remove it.

Do not synchronize icon motion with generic bottom-up section reveals. Icon motion follows interaction/state, not page-builder choreography.
