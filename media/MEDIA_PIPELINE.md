# Media Pipeline Intelligence

Images/video are part of composition and performance, not an afterthought.

For each media asset define:

- role and priority (hero / evidence / ambient)
- intrinsic dimensions/aspect ratio
- crop/focal behavior
- responsive source strategy
- loading priority
- decoding/playback strategy
- poster/fallback
- reduced-data/mobile fallback when useful
- accessibility text/caption requirement
- cache/CDN behavior

Scroll-scrubbed image sequences require an explicit frame budget and fallback; do not ship hundreds of huge frames by default.
