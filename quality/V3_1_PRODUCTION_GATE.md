# V3.1 Production Gate

Release status: PASS / PASS-WITH-NOTES / FAIL.

## Security critical blockers
- frontend contains privileged API secret/credential
- protected action lacks server authorization
- password storage policy unsafe
- raw SQL constructed from untrusted input
- debug/admin endpoint accidentally exposed
- sensitive token appears in logs/errors
- required webhook verification absent

## Typography blockers
- required language glyphs missing
- body copy unreadable at target mobile viewport
- fallback causes destructive layout shift
- heading wraps destroy composition at supported breakpoint
- animation hides text without accessible final state

## Scroll blockers
- content unreachable without JS/motion
- pinned timeline traps/breaks navigation
- reduced-motion path missing for substantial motion
- mobile layout uses broken desktop scrub/pin behavior
- severe layout thrashing/jank in key chapter

## Backend/data blockers
- migration can destroy data without explicit plan
- multi-write critical invariant has no transaction/idempotency design
- upload/outbound fetch unrestricted
- secret lifecycle/environment separation undefined

## Reference blockers
When a close recreation is requested, major geometry/typography mismatch at required viewport blocks “pixel-close” status even if the implementation looks attractive.
