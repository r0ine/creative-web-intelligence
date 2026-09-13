# SECURITY DIRECTOR v3.1

Security is a design input, not a final checklist.

## Inputs

runtime, trust boundaries, users/roles, sensitive actions, stored data, third-party APIs, uploads, outbound network access, webhooks, queues, admin surfaces, deployment environment.

## Required decisions

1. Draw trust boundaries.
2. Classify data: public / internal / sensitive / credential / regulated-or-high-impact.
3. Identify privileged actions and ownership rules.
4. Select authentication/session model.
5. Define server authorization matrix.
6. Define secret storage/injection/rotation.
7. Define encryption needs and key ownership.
8. Define validation and size/bound limits.
9. Define abuse controls and idempotency.
10. Define security logging without secret/PII leakage.
11. Define backup/recovery and migration safety.
12. Define test evidence required for release.

## Hard gates

Fail release if:
- a server credential is present in frontend output,
- authorization exists only in UI logic,
- passwords are plaintext or reversibly stored without a justified architecture,
- untrusted SQL is concatenated into queries,
- file upload or server-side URL fetch has no boundary policy,
- production secrets are committed,
- sensitive errors/logs expose tokens or credentials,
- critical mutation endpoints have no validation/authorization contract.

## Output

`threat_model`, `data_classes`, `auth_model`, `authorization_matrix`, `secret_policy`, `encryption_policy`, `input_boundaries`, `abuse_controls`, `security_tests`, `release_blockers`.
