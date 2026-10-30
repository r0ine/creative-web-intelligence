# Kütüphane araçları

Komutlar depo kökünden çalıştırılır. Python araçları 3.11+ ve yalnız standart kütüphane ister.

## Doğrulama

- `validate_all.py`: aşağıdaki bütün doğrulayıcıları sırayla çalıştırır; CI aynı komutu kullanır.
- `check_links.py`: Markdown dosyalarındaki kırık göreli bağlantıları bulur.
- `validate_library.py`: v2 tariflerinde yinelenen kimlikleri, uyumluluk grafiğinde yinelenen veya bilinmeyen tarife bağlanan kenarları ve `manifest.json` sayılarını denetler.
- `validate_scroll_library.py`: 100 scroll tarifinin sayısını, kimliklerini ve zorunlu alanlarını denetler.
- `validate_external_registry.py`: harici kütüphane kaydını denetler.
- `v3/validate_v3_library.py`, `v3_1/validate_v31.py`: v3 ve v3.1 katalogları.
- `v8/validate_v8.py`: 46 kaynağın kapsamını denetler; ardından v7 → v6 → v5, v4, v3.2 zincirini çalıştırır.
- `v9/validate_v9.py`: geri bildirim sözlüğünü, director önceliğini, çakışma kaydını ve dosyalar arası kimlik çakışmalarını denetler; ardından v8 zincirini çalıştırır.

## Revizyon ve öncelik

- `v9/feedback_triage.py "<geri bildirim>" [--answer "<cevap>"]`: belirsiz geri bildirimi konum, yön, korunacak yer ve sorulacak soruya çevirir. [Akış](../reference-engine/REVISION_FEEDBACK.md).
- `v9/precedence.py [--domain | --file | --id | --conflict]`: geçerli director'ı ve bir kaydı etkileyen sürümler arası çakışmayı gösterir. [Kural önceliği](../v9/RULE_PRECEDENCE.md).

## Seçim ve arama

- `v8/source_advisor.py`: tek başlangıç referansı seçer, kaynak fişi üretir ve şablon/UI/motion/3D çakışmalarını denetler. Çevrimdışı çalışır; [v8 rehberi](../source-intelligence/V8_SOURCE_INTELLIGENCE.md).
- `v8/experience_plan.mjs`: CLI ajanı için videosuz temel, fare bakışı ve açık isteğe bağlı video promptu planını brief'ten üretir.
- `v8/refresh_source_registry.py`: GitHub CLI oturumuyla depo meta verisini yeniler; tasarım veya lisansı dosya düzeyinde doğruladığını iddia etmez.
- `v4/source_intelligence.py`: font, ikon ve kaynak lisans politikalarını sorgular.
- `compose_spec.py "<brief>"`: brief'ten deterministik başlangıç özeti üretir; sanat yönetiminin yerini tutmaz.
- `search_capabilities.py <sorgu>`, `search_scroll_recipes.py <sorgu>`, `v3_1/query_recipes.py <sorgu>`: makine okunur tariflerde metin araması.
- `select_external_library.py`, `select_integration_profile.py`: harici kütüphane ve entegrasyon profili seçimi.

## Medya ve görsel denetim

- `v6/audit_media_plan.py <plan.json>`: medya planının bütçesini, mobil ve hareket azaltma kararlarını denetler. [Kullanım](v6/README.md).
- `v6/video_to_web.py`: videoyu poster, sessiz MP4 ve WebP kare sekansına dönüştürür (FFmpeg gerekir).
- `v6/creative_media.mjs`: kaynak filtreleme ve video promptu.
- `v5/authenticity_check.py <yol>`: regex düzeyinde özgünlük taraması.
- `v7/audit_visual_defaults.mjs <klasör>`: CSS'te tekrar eden kutu ve animasyon kalıplarını işaretler.
- `v6/check_scroll_demo.cjs`, `v6/check_media_studio.cjs`: Playwright ile tarayıcı denetimi; `v6/serve_preview.mjs` sunucusu açıkken çalıştırılır.
