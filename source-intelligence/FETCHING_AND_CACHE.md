# Fetching and Cache Policy

- Cache public metadata, not restricted marketplace assets.
- Every cache record stores retrieval time, source, request and license status.
- Do not cache passwords, API tokens, signed download URLs or private asset URLs.
- Respect documented rate limits and backoff on 429/5xx.
- Use conditional refresh when the source provides last-modified/version metadata.
- A stale result may inform style exploration but must not be presented as current licensing information.
- `tools/v4/source_intelligence.py` uses only Python standard library and writes normalized JSON snapshots.
