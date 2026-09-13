# Auth / Session / RBAC

Choose one authentication model deliberately. Authorization is never inferred from “the button is hidden”.

For each protected operation define:

- actor identity source
- session/token validation
- resource ownership or role requirement
- organization/tenant boundary when applicable
- re-authentication requirement for sensitive actions
- revocation/logout behavior
- expiry/rotation behavior
- audit event

Prefer least privilege and server-side enforcement.
