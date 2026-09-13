# Upload and Outbound Fetch Security

## Uploads

Treat filename, MIME claim and extension as untrusted metadata. Define allowed types, size/count limits, storage location, generated object names, authorization, retention, and content serving policy. Store uploads away from executable application paths.

## Server-side URL fetching

Do not let an arbitrary user URL become unrestricted server network access. Define allowed protocols, destinations/use cases, redirect policy, timeouts, response-size limits and parsing behavior. Prefer allowlisted provider endpoints for integrations.
