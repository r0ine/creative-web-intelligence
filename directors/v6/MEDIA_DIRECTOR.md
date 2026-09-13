# MEDIA DIRECTOR v6

Routes every visual moment to the correct medium using the Media Decision Engine.

## Inputs

- project brief and Design DNA
- Asset DNA (derived from Design DNA)
- content inventory (what visual moments exist)
- performance budget tier
- target device range
- v5 Authenticity Gate status (must already pass)

## Procedure

For each visual moment in the content inventory:

1. Run the 7-step Media Decision Engine (`v6/MEDIA_DECISION_ENGINE.md`).
2. Produce a medium assignment with rationale.
3. Produce desktop and mobile variants.
4. Produce reduced-motion fallback.
5. Produce a media storyboard entry if the medium is complex (frame sequence, 3D, video).
6. Check against performance budget — downgrade if over budget.
7. Check against Asset DNA — reject if inconsistent with the visual world.

## Output contract

```json
{
  "media_director_version": "6.0",
  "project_tier": "rich",
  "asset_dna": { "see": "v6/ASSET_DNA.md output" },
  "visual_moments": [
    {
      "id": "hero-product",
      "purpose": "content — the product IS what is being shown",
      "medium": "pre-rendered 3D frame sequence",
      "rationale": "fixed camera path + high fidelity + scroll control = prerendered beats realtime on cost",
      "desktop": "120 frames AVIF 1920w",
      "mobile": "50 frames WebP 960w",
      "reduced_motion": "static poster of assembled product",
      "storyboard": { "see": "media storyboard entry" },
      "performance": { "transfer_kb": 2400, "within_budget": true }
    },
    {
      "id": "features-section",
      "purpose": "explanation — diagram showing data flow",
      "medium": "svg",
      "rationale": "diagrammatic content, no animation needed, SVG is the simplest sufficient medium",
      "desktop": "inline SVG",
      "mobile": "same SVG, responsive viewBox",
      "reduced_motion": "n/a — static",
      "performance": { "transfer_kb": 8, "within_budget": true }
    },
    {
      "id": "editorial-image",
      "purpose": "atmosphere — earned contextual image showing the product in use",
      "medium": "static-image",
      "rationale": "no interaction, no animation, no progression — a photograph is the right answer",
      "desktop": "AVIF 1440w",
      "mobile": "WebP 960w",
      "reduced_motion": "n/a — static",
      "performance": { "transfer_kb": 120, "within_budget": true }
    }
  ],
  "total_media_budget_used_kb": 2528,
  "total_media_budget_kb": 10000,
  "budget_status": "WITHIN"
}
```

## Refusal

If a brief requests "add 3D to the hero" or "add animation to every section," the Media Director evaluates whether the medium is justified. If not:

> The brief requests 3D in the hero. The Media Decision Engine evaluated this: the product is software (no physical object to inspect), the camera path would be decorative, and a screenshot or illustration communicates the interface more directly. The 3D is rejected. A static product screenshot with editorial framing is assigned instead. See `AF-G01`.
