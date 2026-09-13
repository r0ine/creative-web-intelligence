# API CONTRACT DIRECTOR v3.1

Every route is a contract, not merely a controller function.

Define per operation:
- method/path and purpose
- authentication requirement
- resource ownership/role requirement
- input schema and maximum sizes/counts
- canonical normalization rules
- output schema
- error codes safe for clients
- idempotency/replay behavior
- pagination/cursor semantics where applicable
- rate/abuse class
- transaction boundary
- audit event (if sensitive)
- cacheability
- timeout/retry behavior for upstream calls

Never trust UI-disabled buttons as authorization.
