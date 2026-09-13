# START HERE — v6

## Prerequisites

Read v5 first (`START_HERE_V5.md`). v6 is additive — it requires v5 doctrine to be understood.

## Reading order (v6 additions)

1. `v6/CORE_DOCTRINE.md` — what v6 adds and what it does NOT do.
2. `v6/MEDIA_DECISION_ENGINE.md` — the central routing system.
3. `v6/THREE_D_DIRECTOR.md` — when 3D is justified.
4. `v6/FRAME_SEQUENCE_DIRECTOR.md` — scroll-scrubbed frame sequences.
5. `v6/CAMERA_DIRECTOR.md` — cinematography rules.
6. `v6/BLENDER_WEB_PIPELINE.md` — 3D asset optimization.
7. `v6/ASSET_DNA.md` — visual consistency.
8. `v6/PERFORMANCE_BUDGET_ENGINE.md` — budgets for complex media.
9. `v6/MOBILE_MEDIA_STRATEGY.md` — also contains accessibility, scroll director, implementation intelligence, media storyboard, asset pipeline.
10. `v6/CINEMATIC_ANTI_AI_FINGERPRINTS.md` — what NOT to do.

## Order of use

1. Give the agent `prompts/v6/MASTER_META_PROMPT_V6.md`.
2. The agent will automatically evaluate whether the brief needs complex media.
3. For media decisions, the agent uses the Media Decision Engine.
4. For 3D decisions, the agent uses the 3D Director.
5. For camera, the agent uses the Camera Director.
6. For quality, the agent runs v5 Authenticity Gate + v6 Cinematic Purpose Gate.
7. Run `python tools/v6/validate_v6.py` after modifying v6 files.
8. Run `python tools/v5/authenticity_check.py path/to/build` on built code.

## The one thing to remember

The user should NOT need to ask "add 3D" or "add animation." The library determines whether they are appropriate from the brief. A static website with excellent typography is always a valid — and often superior — outcome.
