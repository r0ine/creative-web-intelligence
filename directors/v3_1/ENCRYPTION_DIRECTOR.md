# ENCRYPTION / DATA PROTECTION DIRECTOR

Do not use the word “encrypted” as a quality badge. Specify what is protected, from whom, where keys live, and how recovery/rotation works.

## Decision order

1. Is the data necessary to store?
2. Can it be transformed/minimized instead?
3. Is transport protected by TLS?
4. Does the managed database/storage already encrypt at rest?
5. Does the threat model require application/field-level encryption?
6. Where are keys stored and who can decrypt?
7. How are keys rotated/versioned?
8. What happens during backup/restore?
9. What metadata remains visible?
10. How is accidental plaintext logging prevented?

Passwords follow password-hashing policy, not reversible application encryption.
