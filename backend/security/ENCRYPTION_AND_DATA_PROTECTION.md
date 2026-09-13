# Encryption and Data Protection

## Transit

Use HTTPS/TLS for browser↔server and server↔service connections. Avoid mixed-content and plaintext credentials.

## At rest

Prefer managed database/object-storage encryption. Record whether backups/snapshots inherit encryption and access controls.

## Field-level/application encryption

Use only for specific sensitive fields when the threat model requires protection beyond storage-layer encryption. The application must define:
- algorithm/library owned by a mature crypto implementation
- authenticated encryption
- key IDs/versioning
- nonce/IV handling by the library
- key storage separate from ciphertext
- rotation/re-encryption plan
- backup/restore behavior
- inability to search/sort certain encrypted fields unless a separate safe design exists

Do not invent custom cryptography.

## Passwords

Store password verifiers with a modern password-hashing function, per-password salt and appropriate cost. Password hashing is intentionally one-way.

## Tokens

Store long-lived sensitive tokens only when needed. Prefer hashing verification-style tokens when the original token never needs to be recovered. Use short expirations and one-time semantics for reset/verification flows.

## Data minimization

The strongest protection for unnecessary sensitive data is not storing it.
