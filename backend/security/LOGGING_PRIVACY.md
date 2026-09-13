# Logging, Observability and Privacy

Logs should explain failures without becoming a second database of sensitive data.

Log: request correlation ID, route, status, duration, safe actor/resource IDs when justified, retry counts, dependency health.

Redact/avoid: passwords, authorization headers, cookies, raw API keys, reset/verification tokens, complete payment data, database credentials, encryption keys, sensitive form bodies.

Separate user-safe error messages from internal diagnostics. Production errors should not reveal stack traces or environment details to clients.
