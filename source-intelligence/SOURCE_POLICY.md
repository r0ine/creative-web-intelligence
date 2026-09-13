# v4 Source Policy

External-source intelligence is opt-in and license-aware.

## Preferred order
1. internal rules/recipes
2. open-source package metadata already in the project
3. documented public/read-only API
4. official source docs
5. manual marketplace/reference selection

Generic scraping is not a fallback. If a source forbids automated search/download or requires an integration agreement, mark it `manual` or `restricted`.

The system may learn **facts about a source** (license, formats, API capability, style taxonomy) without copying its asset catalog into the library.
