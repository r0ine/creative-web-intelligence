---
name: creative-web-intelligence
description: Kreatif portföyler, stüdyo siteleri ve deneyim odaklı landing page'ler için v6 art direction, görsel özgünlük, medya seçimi, sinematik motion, 3D/WebGL ve performans karar kütüphanesi. Rutin uygulama ekranları için kullanma.
---

# Creative Web Intelligence v6

Bu paket tasarım kararlarını destekleyen bir kütüphanedir; kullanıcının isteği, mevcut ürün davranışı, erişilebilirlik ve güvenlik sınırları önceliklidir. Katalog girdilerini doğrudan bağımlılık veya indirme talimatı sayma.

## Başlangıç

1. Önce `START_HERE_V5.md` ve v5 özgünlük doktrinini, sonra `START_HERE_V6.md`, `docs/V6_OVERVIEW.md` ve `v6/CORE_DOCTRINE.md` belgelerini oku.
2. Projeye özgü Design DNA'yı tanımla: tip ve palet rolleri, geometri, kompozisyon, boşluk ritmi, motion dili, scroll görevi ve performans seviyesi.
3. Her görsel an için `v6/MEDIA_DECISION_ENGINE.md` ile en sade yeterli medyumu seç. Güçlü tipografi ve statik kompozisyon geçerli birincil sonuçtur.
4. 3D, frame sequence veya sinematik kamera ancak bilgi mimarisine, anlatıya ya da etkileşime ölçülebilir katkı sağlıyorsa ilgili v6 director'ını kullan.
5. Karmaşık medya için amaç cümlesi, mobil fallback, reduced-motion davranışı ve performans düşürme zinciri tanımla.
6. Teslimden önce v5 özgünlük kapısını ve `quality/V6_CINEMATIC_GATES.md` içindeki uygulanabilir kapıları çalıştır; v6 dosyaları değişirse `tools/v6/validate_v6.py` ile doğrula.

## Yönlendirme

- Özgünlük ve görsel kısıtlar: `v5/`, `directors/v5/`, `quality/V5_AUTHENTICITY_GATE.md`.
- Medya ve sinematik kararlar: `v6/`, `directors/v6/`, `quality/V6_CINEMATIC_GATES.md`.
- Kaynak, ikon, font ve asset: `directors/v4/`, `source-intelligence/`, `icons/`, `assets/`, `data/v4/`.
- Renk ve tipografi: `color/`, `typography/`, `directors/v3_2/`.
- Motion ve scroll: `motion/`, `scroll/`, `recipes/scroll/`.
- Temel 3D bilgisi: `three/`; v6 3D ve kamera director'ları seçim ve sahne kararlarında önceliklidir.
- Referans rekreasyonu: `reference-recreation/`, `reference-engine/`, `directors/reference/`.

## Değişmezler

- Bir v5 veya v6 blocker tespit edildiğinde tasarımı teslim etme; sorunu yapısal düzeyde düzelt ya da daha sade bir medyuma düşür.
- Dekoratif 3D blob, anlamsız parçacık alanı, sürekli dönen obje, sahte HUD ve her bölüme WebGL yerleştirme kullanma.
- Uydurma müşteri, ödül, metrik, referans veya araştırma iddiası üretme.
- Esas metni video, canvas, frame sequence ya da 3D sahne içine gömme.
- Animasyon ve karmaşık medya kapalıyken içerik, hiyerarşi ve marka kimliği ayakta kalmalı.
- Ayrışmayı teknik gösteriden değil; fikir, tipografi, kompozisyon ve ürün davranışından çıkar.
