# Backend Security Baseline

For every backend project define explicitly:

- authentication and session lifecycle
- authorization checks at the server boundary
- validation for body/query/path/header inputs
- prepared/parameterized database queries
- safe error responses without secret leakage
- CORS policy
- CSRF strategy when cookie-authenticated browser requests can mutate state
- rate limits for abuse-prone routes
- password/token/secret storage rules
- secure cookie attributes where cookies are used
- upload MIME/size/count/storage constraints
- SSRF protections for server-side URL fetching
- webhook signature verification and replay protection
- idempotency for externally retryable mutations
- audit logs for sensitive admin actions
- environment separation and secret injection

Never place API secrets in frontend bundles.
