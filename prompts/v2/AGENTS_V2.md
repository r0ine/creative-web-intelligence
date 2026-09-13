# AGENTS v2

## Mandatory workflow
1. Read `docs/V2_OVERVIEW.md`.
2. Search `data/v2/*recipes.json`.
3. Select recipes by project intent, not popularity.
4. Check `compatibility_graph.json`.
5. Apply QA rubric before shipping.
6. For a new reference, use `REFERENCE_ANALYZER_V2.md` and preserve evidence status.
7. Do not rebuild capabilities already in the library without a documented gap.


## External-library discovery
Use `python tools/select_external_library.py <capability terms>` before adding major dependencies. Restricted entries are excluded by default. Record why selected alternatives were chosen and why overlaps were rejected.

8. For any scroll-driven experience, read `prompts/v2/SCROLL_AGENT_RULES.md`, select from `data/v2/scroll_recipes.json`, and check `data/v2/scroll_compatibility.json` before writing custom scroll behavior.
