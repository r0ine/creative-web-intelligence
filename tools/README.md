# Library Tools

- `v8/source_advisor.py`: tek başlangıç referansı seçer, kaynak fişi üretir ve şablon/UI/motion/3D çakışmalarını denetler. Çevrimdışı çalışır; [v8 rehberi](../source-intelligence/V8_SOURCE_INTELLIGENCE.md).
- `v8/experience_plan.mjs`: CLI ajanı için videosuz temel, fare bakışı ve açık isteğe bağlı video promptu planını brief'ten üretir.
- `v8/validate_v8.py`: 46 kaynağın kapsamını ve önceki sürümlerin doğrulamasını çalıştırır.
- `v8/refresh_source_registry.py`: GitHub CLI oturumuyla depo meta verisini yeniler; tasarım veya lisansı dosya düzeyinde doğruladığını iddia etmez.
- `v6/audit_media_plan.py <plan.json>`: medya planının toplam bütçesini, mobil ve hareket azaltma kararlarını denetler. [Kullanım ve örnekler](v6/README.md).
- `v6/validate_v6.py`: v6 kataloglarının yapısını ve referanslarını, ardından önceki sürümlerin doğrulayıcılarını çalıştırır.

- `validate_library.py`: duplicate-ID / basic relationship validation.
- `search_capabilities.py`: text-search machine-readable recipes.
- `compose_spec.py`: deterministic discovery bootstrap from a brief. It intentionally does **not** replace Claude/Codex art-direction reasoning.

These tools make the archive inspectable before a full npm/TypeScript runtime is built.

- `search_scroll_recipes.py <query>` — search the 100 scroll choreography recipes.
- `validate_scroll_library.py` — validate scroll recipe count, IDs and required fields.
