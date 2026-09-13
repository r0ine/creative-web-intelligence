# Creative Web Intelligence v3.1 — Production Hardening

v3.1 keeps every v3.0 module and adds a deeper production layer for **backend security, secret/key handling, encryption decisions, API contracts, typography systems, scroll choreography, reference fidelity, and automated QA**.

## Read order

1. `prompts/v3_1/MASTER_META_PROMPT_V3_1.md`
2. `directors/v3_1/SECURITY_DIRECTOR.md`
3. `directors/v3_1/TYPOGRAPHY_DIRECTOR.md`
4. `directors/v3_1/SCROLL_DIRECTOR.md`
5. `backend/security/SECRETS_AND_KEY_MANAGEMENT.md`
6. `backend/security/ENCRYPTION_AND_DATA_PROTECTION.md`
7. `typography/v3_1/TYPOGRAPHY_SYSTEM.md`
8. `scroll/v3_1/SCROLL_CHOREOGRAPHY_SYSTEM.md`
9. `quality/V3_1_PRODUCTION_GATE.md`

## Non-negotiable ideas

- A browser cannot safely hide a server secret. Secret values belong on a trusted server/runtime or managed secret store.
- Passwords are **hashed**, not reversibly encrypted.
- Encryption is selected from a data classification/threat model; “encrypt everything manually” is not a strategy.
- Authorization is checked on the server for every protected action.
- Scroll animation is choreography with states, ownership and handoffs—not a library-wide `fadeUp()` call.
- Typography is a system of metrics, hierarchy, optical behavior, language coverage, loading and fallback—not simply two font names.
- Reference recreation works from user-provided/authorized visible references and independently authored implementation; do not copy proprietary source code or restricted assets.
- QA is evidence-driven: build, runtime, browser capture, network behavior, accessibility and security checks must agree.

## v3.1 decision stack

`Brief/Reference → Rights/Scope → Design DNA → Typography System → Color System → Composition → Scroll State Machine → optional 3D → Backend Need → Threat Model → Secrets/Data Classification → API/Auth/Data → Full-stack Contract → Implementation → Runtime Test → Visual/Fidelity QA → Security QA → Performance/Accessibility → Release Gate`
