# Source Normalization Model

Normalize external results into a small candidate record:

```json
{
  "kind": "icon | font | illustration | lottie | rive | 3d | ...",
  "sourceId": "iconify",
  "identifier": "line-md:home",
  "label": "home",
  "style": ["animated-line"],
  "license": {"status":"verified","name":"MIT"},
  "capabilities": ["animated", "static-fallback"],
  "fitScores": {
    "brandVoice": 0.0,
    "geometry": 0.0,
    "motionPurpose": 0.0,
    "genericityRisk": 0.0
  },
  "provenance": {}
}
```

Do not expose raw source payloads directly to the design decision layer. Normalize, score, then choose.
