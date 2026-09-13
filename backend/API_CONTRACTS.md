# API Contracts

Every endpoint recipe should define:

- method + path
- auth requirement
- authorization rule
- request schema
- response schema
- stable error codes
- idempotency behavior
- rate-limit class
- side effects
- persistence transaction boundary
- observability fields
- tests

Do not let UI code depend on random thrown strings or database row shapes.
