# Pixel-Close QA

At each required viewport compare:

- section start/end positions
- major bounding boxes
- alignment axes
- text block width and line wrapping
- headline baseline/line-height behavior
- media crop and focal point
- corner radius / border / stroke families
- background role and contrast
- sticky/pinned states
- transition state at chosen progress checkpoints

Fix order:

`wrong structure -> wrong scale -> wrong alignment -> wrong text metrics -> wrong crop -> wrong color/material -> micro decoration`.

Never compensate for a wrong container model with dozens of magic margins.
