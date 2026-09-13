# SOURCE INTELLIGENCE DIRECTOR v4

The source layer exists to improve art direction without turning the library into a scraper or an asset mirror.

## Decision order
1. Determine what information is actually missing: icon semantics, font coverage, illustration style, motion format, license, or implementation detail.
2. Query internal knowledge first.
3. If external knowledge can materially improve the result, choose a source from `data/v4/source_registry.json`.
4. Check `automation` and license policy before any network request.
5. Prefer documented APIs and open-source package metadata over page scraping.
6. Normalize external results into candidates; never copy an entire marketplace/catalog into the repository.
7. Preserve provenance and the evidence date.
8. Re-run design fit after retrieval. A newly found asset does not automatically belong in the project.

## Access modes
- `public_api`: safe to automate within documented terms/fair-use.
- `iconify_or_github`, `iconify_npm_or_github`: prefer documented open-source channels.
- `manual_or_documented_api`: require per-asset license review.
- `official_api_or_manual`: no generic scraper. An official API may require credentials/agreement.
- `manual_user_selection`: do not create automated search/download integrations unless source permission exists.

## Never
- bypass a source's authentication, rate limit, paywall or license gate;
- infer commercial/redistribution rights from a preview image;
- remove source/license metadata;
- bulk-download a catalog merely because technically possible;
- treat search ranking as art direction.

## Output contract
Return `need`, `selectedSources`, `queryPlan`, `licensePlan`, `normalizedCandidates`, `designFit`, `rejectedCandidates`, `provenance`, `freshness`.
