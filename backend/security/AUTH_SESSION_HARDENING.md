# Authentication and Session Hardening

- Separate authentication (who) from authorization (what they may do).
- Validate authorization at server resource boundaries.
- Rotate/invalidate sessions on meaningful security events where appropriate.
- Cookie sessions should use Secure, HttpOnly and an appropriate SameSite policy.
- Define CSRF protection for cookie-authenticated state-changing requests.
- Avoid exposing session tokens to unnecessary JavaScript.
- Apply rate limits/backoff to abuse-prone authentication flows.
- Verification/reset tokens need expiration and single-use semantics.
- Do not reveal more account-existence detail than the product requires.
- Administrative actions should have a stronger audit trail and may require stronger re-authentication depending on risk.
