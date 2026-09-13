# Defensive Security Testing Playbook

Security testing should be non-destructive and owned by the project team.

## Automated
- secret-pattern scan
- dependency/advisory scan
- unit tests for authorization matrix
- input-boundary tests
- CSRF/cookie/CORS configuration tests where relevant
- webhook signature/replay tests
- idempotency/concurrency tests for critical mutations
- migration rollback/forward checks
- production configuration lint

## Integration
Create test users/roles/resources and verify allowed/denied actions. Change resource IDs and role inputs in test requests to confirm server rules—not UI—enforce ownership.

## Runtime
Verify safe error payloads, secure cookie attributes, expected security headers, rate-limit responses, logging redaction and absence of secrets in built frontend assets.

Never treat a scanner’s “0 findings” as proof of security.
