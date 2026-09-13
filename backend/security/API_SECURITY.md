# API Security Baseline

For every endpoint:
- schema-validate body/query/path/header inputs
- cap strings, arrays, page sizes, upload sizes and batch counts
- normalize identifiers in one place
- verify resource ownership/role on server
- parameterize database queries
- use transactions for multi-write invariants
- define safe errors without stack traces/secrets
- define rate/abuse class
- define idempotency for retryable create/payment/webhook-like operations
- define timeout and retry policy for upstream calls
- never blindly proxy arbitrary user-selected URLs/headers to privileged upstream services
