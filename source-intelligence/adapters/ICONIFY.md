# Iconify Adapter

Supported documented queries:
- `/collections`
- `/collection?prefix={prefix}`
- `/search?query={query}&limit={limit}`
- `/keywords?keyword={keyword}`
- `/{prefix}.json?icons={icons}`
- `/{prefix}/{icon}.svg`

The adapter retrieves metadata/candidates. Before bundling an icon, inspect the icon-set license from the collection response/registry. Iconify's framework license is not the icon's license.

For production-critical builds, consider package-local icon data rather than a hard dependency on a public network request.
