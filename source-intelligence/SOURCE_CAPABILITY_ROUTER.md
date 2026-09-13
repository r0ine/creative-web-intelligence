# Source Capability Router

Use the smallest source that can answer the missing question.

| Need | Preferred path | Fallback | Never |
|---|---|---|---|
| search open-source icons | Iconify search API | local @iconify JSON packages | scrape marketplace previews |
| inspect icon-family license | Iconify collection metadata + upstream license | upstream GitHub | assume Iconify MIT covers icons |
| find variable font + axes | Fontsource API | upstream font repo/docs | choose by popularity alone |
| paid marketplace asset | manual/official provider API with entitlement | ask user to supply licensed asset | bulk scrape/download |
| illustration reference | manual licensed source | custom illustration | mirror source catalog |
| Lottie/Rive implementation | official runtime docs | CSS/SVG motion | assume runtime license licenses third-party assets |

If current network/source access is unavailable, output `NEEDS_RESEARCH` instead of inventing metadata.
