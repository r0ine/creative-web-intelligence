# Practical Threat Modeling

For each feature answer:
- what valuable data/action exists?
- who should be allowed to access/change it?
- what crosses a trust boundary?
- what can an unauthenticated user submit repeatedly?
- what external service can fail or be abused?
- what happens if a user changes IDs/roles/amounts in requests?
- what happens on retry, duplicate webhook, timeout or concurrent mutation?
- what appears in logs/errors/backups?

Create abuse cases and defensive tests before implementation for high-impact flows.
