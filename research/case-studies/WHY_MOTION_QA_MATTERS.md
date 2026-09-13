# Why motion QA must be separate from screenshot QA

2026 research such as Animation2Code reports that contemporary vision-language systems can achieve stronger appearance similarity while still struggling with temporal consistency. For this library, a reference recreation should therefore be judged on **appearance + timing + continuity + trigger/response behavior**, not a single screenshot.

Practical implication: Visual QA must include scrubbed recording comparison or state-by-state checks for important motion recipes.
