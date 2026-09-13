# Browser Security Headers / CSP Design

Security headers are selected for the actual architecture; copy-pasting an impossible CSP is not useful.

Consider:
- Content-Security-Policy with explicit script/style/connect/img/font/frame sources
- frame embedding policy (`frame-ancestors` or equivalent requirements)
- `X-Content-Type-Options: nosniff`
- Referrer-Policy
- Permissions-Policy appropriate to features
- HSTS only when HTTPS deployment/domain ownership is understood

Prefer nonces/hashes or framework-supported CSP patterns over globally allowing unsafe inline/eval. Test third-party analytics, video, fonts and API origins intentionally.
