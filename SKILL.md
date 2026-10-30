---
name: creative-web-intelligence
description: Kreatif portföyler, stüdyo siteleri ve deneyim odaklı landing page'ler için v10 referans laboratuvarı (wget ile indirme, canlı ölçüm, karşılaştırma), v9 revizyon geri bildirimi ve kural önceliği, v8 kaynak zekâsı, referans akışı, görsel karşılaştırma, motion, 3D/WebGL ve performans karar kütüphanesi. Rutin uygulama ekranları için kullanma.
---

# Creative Web Intelligence v10

Bu paket tasarım kararlarını destekleyen bir kütüphanedir; kullanıcının isteği, mevcut ürün davranışı, erişilebilirlik ve güvenlik sınırları önceliklidir. Katalog girdilerini doğrudan bağımlılık veya indirme talimatı sayma.

## Başlangıç

1. Yeni site veya köklü yeniden tasarımda önce `reference-engine/BRIEF_TO_REFERENCE.md` akışını uygula: isteği açık/çıkarılan/bilinmeyen olarak çöz, sonucu değiştiren soruları erken sor, her site için tek ekranlık kısa referans önizlemesi ve notu hazırla. Küçük düzeltmeler için yeni önizleme üretme. Kullanıcı kaynak gösterdiyse onu ayrıntılı incele; site adresi verdiyse `reference-engine/REFERENCE_LAB.md` ile `tools/v10/mirror_reference.py` (wget), JavaScript'li sitelerde `tools/v10/capture_reference.mjs` ve `tools/v10/analyze_reference.py` çalıştır, `capture.json` kullanım kararına (`owned`, `license-review`, `study-only`) uy; “bire bir” talebinde görülebilen durumları aynı ekran ölçülerinde karşılaştır.
2. Yön netleşince `START_HERE_V10.md`, `START_HERE_V9.md` ve `START_HERE_V8.md` ile işe başla. Aynı alanda birden fazla director veya katalog varsa `v9/RULE_PRECEDENCE.md` hangisinin geçerli olduğunu söyler; eski katalog kaydını kullanmadan önce `tools/v9/precedence.py --id <kimlik>` ile çakışmayı sor. Ardından v5 özgünlük doktrinini ve görevle ilgili v6 director'larını gerektiği kadar aç. `docs/V6_OVERVIEW.md` genel çerçeve gerektiğinde kullanılır. Aynı turda bütün katalogları yükleme.
   - Kullanıcı bir kaynak verdiyse önce onu incele. Vermediyse `tools/v8/source_advisor.py` ile tek başlangıç referansı seç. `source-intelligence/V8_SOURCE_INTELLIGENCE.md` içindeki beş merceği kullan; GitHub meta verisini veya README'yi görsel kanıt sayma. Başka kaynağı yalnız somut eksik için aç.
3. Projeye özgü Design DNA'yı tanımla: tip ve palet rolleri, geometri, kompozisyon, boşluk ritmi, motion dili, scroll görevi ve performans seviyesi. `quality/V7_VISUAL_CALIBRATION.md` ile renklerin kaynağını, köşe dilini ve her animasyonun görevini açıkla; otomatik koyu tema, parlak vurgu, eş kutular ve genel fade-up üretme.
4. Her görsel an için `v6/MEDIA_DECISION_ENGINE.md` ile en sade yeterli medyumu seç. Güçlü tipografi ve statik kompozisyon geçerli birincil sonuçtur.
5. 3D, frame sequence veya sinematik kamera ancak bilgi mimarisine, anlatıya ya da etkileşime ölçülebilir katkı sağlıyorsa ilgili v6 director'ını kullan.
6. Karmaşık medya için amaç cümlesi, mobil fallback, reduced-motion davranışı ve performans düşürme zinciri tanımla.
   - Fareyle 3D kamera ve isteğe bağlı video için `v8/OPTIONAL_VIDEO_POINTER_WORKFLOW.md` akışını kullan. Scroll ana pozu, fare sınırlı bakış ofsetini yönetir. Video olmadan siteyi bitir; kullanıcı açıkça video istemedikçe prompt üretme.
   - Video üretimi isteğe bağlıdır. Kullanıcı video veya videodan kare üretimini açıkça isterse `runtime/media/README.md` akışını kullan. Nesne, malzeme, palet, ışık ve storyboard içeren promptu `tools/v6/creative_media.mjs prompt` ile üret; masaüstü ve mobil kompozisyonlarını ayrı ver. Yalnızca 3D veya scroll isteyen kullanıcı için video promptu üretme; gerçek zamanlı 3D, yerel sahne ve statik seçenekleri değerlendir. Video asset’i gelmeden üretildiğini iddia etme. Gelen videoyu istenen arka plana veya `tools/v6/video_to_web.py` ile WebP sekansına bağla.
   - Harici bileşen/şablon seçiminde önce v8 kaynak fişi ve `--check` çakışma denetimi, ardından `source-intelligence/CREATIVE_COMPONENT_WORKFLOW.md` ile `data/v6/creative_sources.json` kullan. React Bits resmi hedef-proje kurulumu; 21st.dev resmi Copy prompt veya kullanıcının sağladığı kaynak üzerinden değerlendirilir. Lisans, yazar ve framework uyumu doğrulanmadan kütüphaneye kaynak paketleme.
7. Referans ve uygulama ekran görüntüleri varsa aynı viewport'ta `examples/v7/reference-compare/` ile farkları incele; davranış ve animasyonu ayrıca doğrula. Teslimden önce v7 görsel kalibrasyonu, v5 özgünlük kapısını ve `quality/V6_CINEMATIC_GATES.md` içindeki uygulanabilir kapıları çalıştır. Site CSS'i için `tools/v7/audit_visual_defaults.mjs` kullan; kütüphane değişirse `tools/validate_all.py` ile doğrula.
8. Kullanıcı sonucu gördükten sonra memnun değilse `reference-engine/REVISION_FEEDBACK.md` akışını uygula. “İçime sinmedi”, “olmamış” gibi yalnız his varsa hiçbir şeyi değiştirmeden “Neresi?” diye seçeneklerle sor. Cevap “genel” ise en çok görünen yüzeylerden başla: arka plan, ilk ekran, baskın renk, başlık tipografisi. Beğenilen yerleri koru; “eskisi daha iyiydi” geri alma isteğidir. Emin olmadığın cümlede `tools/v9/feedback_triage.py` kullan. Her revizyonda değişen dosyaları tam yollarıyla ve projenin nerede çalıştığını söyle.

## Yönlendirme

- Referans siteyi indirme, ölçme, düzenleme haritası, açık kaynak şablonlar ve karşılaştırma: `reference-engine/REFERENCE_LAB.md`, `tools/v10/`, `runtime/reference/style-metrics.mjs`.
- Revizyon geri bildirimi ve görünürlük sırası: `reference-engine/REVISION_FEEDBACK.md`, `data/v9/feedback_lexicon.json`, `data/v9/visibility_ranking.json`, `tools/v9/feedback_triage.py`.
- Kural önceliği ve sürümler arası çakışmalar: `v9/RULE_PRECEDENCE.md`, `data/v9/rule_precedence.json`, `tools/v9/precedence.py`.
- Özgünlük ve görsel kısıtlar: `v5/`, `directors/v5/`, `quality/V5_AUTHENTICITY_GATE.md`.
- Medya ve sinematik kararlar: `v6/`, `directors/v6/`, `quality/V6_CINEMATIC_GATES.md`.
- İsteğe bağlı video, ajan planı ve fare bakışı: `v8/OPTIONAL_VIDEO_POINTER_WORKFLOW.md`, `runtime/media/experience-plan.mjs`, `runtime/three/pointer-look.mjs`.
- Kaynak, ikon, font ve asset: `directors/v4/`, `source-intelligence/`, `icons/`, `assets/`, `data/v4/`.
- GitHub kaynak seçimi, kanıt ve çakışma kapısı: `source-intelligence/V8_SOURCE_INTELLIGENCE.md`, `data/v8/`, `tools/v8/source_advisor.py`.
- Kreatif bileşen/şablon ve video: `source-intelligence/CREATIVE_COMPONENT_WORKFLOW.md`, `source-intelligence/REACT_BITS_INTEGRATION.md`, `runtime/media/README.md`, `examples/v6/media-studio/`.
- Renk ve tipografi: `color/`, `typography/`, `directors/v3_2/`.
- Motion ve scroll: `motion/`, `scroll/`, `recipes/scroll/`.
- Temel 3D bilgisi: `three/`; v6 3D ve kamera director'ları seçim ve sahne kararlarında önceliklidir.
- Brief, kısa önizleme ve referans rekreasyonu: `reference-engine/BRIEF_TO_REFERENCE.md`, `reference-recreation/`, `directors/reference/`.
- Görsel karşılaştırma: `START_HERE_V7.md`, `examples/v7/reference-compare/`, `runtime/reference/pixel-compare.mjs`.
- Renk, şekil ve hareket kalibrasyonu: `quality/V7_VISUAL_CALIBRATION.md`, `tools/v7/audit_visual_defaults.mjs`.

## Değişmezler

- İki kural çelişirse daha yeni olanı varsayma; `v9/RULE_PRECEDENCE.md` sırasını uygula. Yeni bir çelişki bulursan kayda ekle, eski dosyayı sessizce değiştirme.
- Belirsiz memnuniyetsizlikte rastgele bir ayrıntıyı değiştirip düzelttim deme; önce neresi olduğunu öğren.
- Bir v5 veya v6 blocker tespit edildiğinde tasarımı teslim etme; sorunu yapısal düzeyde düzelt ya da daha sade bir medyuma düşür.
- Dekoratif 3D blob, anlamsız parçacık alanı, sürekli dönen obje, sahte HUD ve her bölüme WebGL yerleştirme kullanma.
- Uydurma müşteri, ödül, metrik, referans veya araştırma iddiası üretme.
- `study-only` olarak indirilen bir sitenin kodunu, görselini, metnini veya fontunu teslim edilen işe kopyalama; erişim engeli, giriş veya robots.txt kısıtını aşma.
- Esas metni video, canvas, frame sequence ya da 3D sahne içine gömme.
- Animasyon ve karmaşık medya kapalıyken içerik, hiyerarşi ve marka kimliği ayakta kalmalı.
- Ayrışmayı teknik gösteriden değil; fikir, tipografi, kompozisyon ve ürün davranışından çıkar.
