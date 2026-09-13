# SCROLL AGENT RULES v2.2

Before writing custom scroll code:
1. Search `data/v2/scroll_recipes.json` by intent/category.
2. Pick one dominant recipe.
3. Check `data/v2/scroll_compatibility.json`.
4. Write named progress ranges/state transitions before implementation.
5. Select CSS/sticky/GSAP/R3F based on `scroll/SCROLL_TECH_DECISION.md`.
6. Define mobile and reduced-motion behavior.
7. Only implement a new project-local primitive when the library has a documented gap.

When a user says “add scroll animations”, do not interpret that as “animate everything on viewport entry”. Ask the design system: what should scroll communicate?
