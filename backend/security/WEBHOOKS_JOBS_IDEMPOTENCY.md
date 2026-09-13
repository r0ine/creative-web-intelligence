# Webhooks, Background Jobs and Idempotency

- Verify provider signatures using the provider’s documented scheme.
- Check timestamp/replay rules where available.
- Make duplicate deliveries safe.
- Persist an event/idempotency identifier when side effects must occur once.
- Acknowledge within provider timeout budgets and move slow work to a queue where appropriate.
- Separate “received”, “validated”, “processed”, “failed/retryable” states.
- Do not log raw secrets/signature material unnecessarily.
