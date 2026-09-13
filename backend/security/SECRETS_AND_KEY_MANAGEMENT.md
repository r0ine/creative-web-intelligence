# Secrets and API Key Management

## The browser boundary

A value embedded in client HTML/CSS/JS, a public `NEXT_PUBLIC_*`/`VITE_*`-style variable, downloadable JSON, source map, or network request is observable by the user. Do not call such values “hidden”.

## Recommended pattern

Browser → your backend/BFF/edge worker → third-party service.

The server holds the privileged credential. The browser sends only the data necessary for the requested operation. The backend authenticates/authorizes, validates, applies limits, calls the provider, and returns a minimized result.

## Storage

Prefer platform secret stores / protected environment injection. Avoid committed `.env` files. Keep `.env.example` values blank/placeholders. Separate development/staging/production credentials.

## Least privilege

Prefer credentials restricted to the exact API, environment, resources and operations needed. Separate read-only and write/admin credentials where practical.

## Rotation

Design credentials so they can be replaced without code changes. Track owner, purpose, environment, creation/rotation date and revocation path. Support overlapping old/new key windows only where necessary.

## Logging

Redact authorization headers, cookies, session tokens, API keys, database URLs containing passwords, reset tokens and webhook secrets. Do not dump whole request objects in production by default.

## Repository hygiene

- `.gitignore` local secret files
- pre-commit/CI secret scanning
- never rely on “deleting the latest commit” after a secret was published; revoke/rotate it
- do not paste production credentials into AI prompts, tickets, screenshots or docs
