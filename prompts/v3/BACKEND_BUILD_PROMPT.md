# Backend Build Prompt

Determine whether backend is necessary. If yes, write a backend build spec before coding:
- runtime
- persistence/data invariants
- auth/session
- authorization matrix
- API schemas and stable errors
- integrations
- rate limiting/idempotency
- security baseline
- logs/observability
- tests
- deployment/migration

Implement the smallest architecture satisfying the spec. Never hardcode secrets or trust client-side authorization state.
