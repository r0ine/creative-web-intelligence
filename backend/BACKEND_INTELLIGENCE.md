# Backend Intelligence v3

Backend is selected from project requirements; it is not added to make a website appear “advanced”.

## Decision layers

1. runtime constraints
2. data ownership and persistence
3. authentication/session requirements
4. authorization model
5. API shape
6. validation and error contract
7. database/storage model
8. caching/rate limiting/idempotency
9. asynchronous work / queues
10. email/uploads/webhooks/realtime integrations
11. observability
12. security review
13. test strategy
14. deployment/migration strategy

## Supported architecture profiles

- static/frontend-only
- serverless HTTP API
- edge/worker API
- Node service
- framework-integrated server routes
- BFF (backend-for-frontend)
- realtime-enabled service
- queue/worker companion

The library provides capability profiles, not forced vendor lock-in.
