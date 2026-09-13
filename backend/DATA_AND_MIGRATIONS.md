# Data and Migrations

Rules:

- model domain invariants before tables,
- keep migrations versioned and forward-reviewable,
- never silently destroy production data,
- add indexes from real query paths,
- bound pagination,
- separate user-visible IDs from secrets,
- document deletion/retention semantics,
- use transactions for multi-write invariants,
- make retry behavior explicit,
- test migration against representative data.
