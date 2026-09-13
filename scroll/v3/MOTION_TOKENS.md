# Motion Tokens

Use project-level tokens before one-off timings.

Recommended token groups:

- `duration.micro`: 90–180ms
- `duration.ui`: 180–320ms
- `duration.section`: 450–900ms
- `duration.hero`: 700–1600ms
- `stagger.tight`: 20–55ms
- `stagger.editorial`: 55–120ms
- `travel.micro`: 4–10px
- `travel.section`: 16–48px
- `travel.hero`: concept-dependent, not a default

Easing families:

- direct / functional
- editorial / soft
- spatial / inertial
- reveal / settling
- mechanical / stepped

Do not use one easing for every component. Do not use overshoot on reading content unless the concept needs it.
