# Supply Chain and Deployment Hardening

- Pin or lock dependencies using the ecosystem’s lock mechanism.
- Review dependency provenance/license and avoid unnecessary packages.
- Run dependency vulnerability/advisory checks in CI where available.
- Keep production build free of development-only debug tools.
- Use least-privileged deployment/service accounts.
- Separate environments and credentials.
- Protect migration execution and make destructive migrations explicit.
- Keep rollback/backup strategy for schema and data changes.
- Disable accidental public debug/admin endpoints.
- Generate a software/dependency inventory when the deployment requires it.
