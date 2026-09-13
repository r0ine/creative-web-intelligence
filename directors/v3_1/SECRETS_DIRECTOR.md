# SECRETS DIRECTOR

## Core law

If browser code can read a value, a user can read it too. Obfuscation, minification, Base64, environment-variable replacement during frontend build, or hiding a value in source maps does not convert it into a secret.

## Classify credentials

- public client identifier: intentionally public, restricted by origin/scope where provider supports it
- server API credential: server/worker only
- database credential: server only, least privilege
- webhook signing secret: server only
- encryption key: managed secret/KMS boundary
- deploy credential: CI/deployment boundary only

## Lifecycle

create → inject → use minimally → redact → rotate → revoke → audit.

Never place real values in docs/examples. Use placeholders and `.env.example` names only.
