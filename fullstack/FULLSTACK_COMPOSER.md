# Full‑Stack Composer v3

The composer merges creative and backend intelligence into one plan without coupling them unnecessarily.

## Output files

- `creative-build-spec.json`
- `reference-recreation-spec.json` when a reference exists
- `backend-build-spec.json` when backend is needed
- `fullstack-integration-spec.json`
- `qa-plan.json`

## Boundary rules

- the frontend never receives private secrets,
- UI state is not treated as authorization,
- backend responses are shaped for the product contract, not database convenience,
- motion does not block essential network/user flows,
- optimistic UI requires rollback/error behavior,
- loading states are authored as part of composition,
- realtime events define ordering/reconnect behavior,
- file/media delivery has performance and security budgets.
