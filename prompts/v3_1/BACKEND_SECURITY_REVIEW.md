# Backend Security Review Prompt

Review the project defensively. Produce findings with severity, evidence, affected surface, safe remediation and verification step.

Inspect at minimum:
- secret exposure in client bundles, repository, logs and errors
- authentication/session lifecycle
- server-side authorization on protected actions
- input validation and output encoding
- database parameterization and transaction boundaries
- CORS/CSRF/cookie configuration
- rate limits, lockouts and abuse controls
- file upload constraints and storage boundaries
- outbound URL fetch/SSRF boundaries
- webhook signature + replay handling
- idempotency of retryable mutations
- sensitive logging/redaction
- encryption/key management decisions
- dependency/supply-chain posture
- debug/admin endpoints and production configuration
- backup/migration/recovery failure modes

Do not perform destructive testing or provide exploitation instructions. Prefer non-destructive verification and unit/integration tests.
