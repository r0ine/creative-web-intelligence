# Color + Font + Motion Audit Prompt v3.2

Audit an existing website without redesigning it immediately.

Return:

1. `design_dna`: what the current site appears to be trying to communicate.
2. `color`: source strategy, role logic, contrast risks, accent competition, Wada fit if relevant.
3. `typography`: roles, morphology, pairing rationale, hierarchy, wrap/measure, fallback/load, genericity risks.
4. `composition`: cardification, divider usage, repeated geometry and weak section boundaries.
5. `motion`: dominant grammar, repetition, amplitude, easing, rest zones, reduced-motion behavior.
6. `fingerprint_score`: each Visual Fingerprint Gate category 0–3 with evidence.
7. `keep`: decisions that already work.
8. `change_first`: maximum five high-leverage changes.

Do not recommend an effect simply because it is different. Prefer removing weak devices before adding new ones.
