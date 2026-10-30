# Creative Web Intelligence

**Dil:** Türkçe · [English](README.en.md)

**Kurulum ve kullanım:** [Türkçe](docs/INSTALL_TR.md) · [English](docs/INSTALL_EN.md)

**v10 sürüm notları:** [Türkçe](RELEASE_NOTES_V10.md) · [English](RELEASE_NOTES_V10.en.md)

Kreatif web projeleri için tasarım kararları, kaynak katalogları, denetim araçları ve çalışan medya örnekleri. Tipografi, kompozisyon, renk, hareket ve medya seçiminde kullanılır.

v10 bir **referans laboratuvarı** ekler. Verilen site wget ile indirilir; JavaScript'li siteler Playwright ile canlı ölçülür. Renk, font, boşluk, hareket, kütüphane, erişilebilirlik ve ağırlık raporu çıkar. Kullanıcı bir yeri beğenmezse düzenleme haritası o yüzeyin CSS dosyasını ve satırını gösterir. Yeni iş referansla aynı ekran ölçüsünde karşılaştırılır ([laboratuvar akışı](reference-engine/REFERENCE_LAB.md), [v10 başlangıcı](START_HERE_V10.md)).

```sh
python tools/v10/mirror_reference.py https://www.orneksite.com
python tools/v10/analyze_reference.py reference-workspace/www.orneksite.com/<zaman>
```

v9 kullanıcıyı anlamaya odaklanır. Kullanıcı “içime sinmedi” dediğinde ajan rastgele değişiklik yapmaz; önce **neresi** olduğunu sorar. “Genel” cevabında arka plan, ilk ekran, baskın renk ve başlık tipografisi gibi en çok görünen yüzeylerden başlar ve beğenilen yerleri korur ([revizyon akışı](reference-engine/REVISION_FEEDBACK.md)). Kütüphane büyüdükçe artan kural çakışmaları için [kural önceliği](v9/RULE_PRECEDENCE.md) hangi director'ın geçerli olduğunu ve bilinen sekiz çelişkinin çözümünü tek yerde toplar. [v9 başlangıcı](START_HERE_V9.md) iki akışı da özetler.

```sh
python tools/v9/feedback_triage.py "içime sinmedi" --answer "genel"
python tools/v9/precedence.py --id font-029
```

v8, 46 GitHub kaynağını araştırma ve seçim sistemine dönüştürür. Tek başlangıç referansı seçer; README bulgularını görsel olarak incelenmemiş alanlardan ayırır ve şablon, UI, animasyon, 3D ve lisans çakışmalarını denetler. v7'nin görsel karşılaştırması ile v6'nın mobil scroll ve 3D araçları korunur.

## Başlangıç

Tasarım çalışması için [v10 başlangıcını](START_HERE_V10.md), [v9 başlangıcını](START_HERE_V9.md) ve [v8 başlangıcını](START_HERE_V8.md) oku. İhtiyaca göre v5 görsel özgünlük ve kompozisyon kurallarını, v6 medya kararlarını aç.

[v8 kaynak danışmanı](README_V8.md), kullanıcının verdiği 46 adresin güncel durumunu ve [beş mercekli inceleme akışını](source-intelligence/V8_SOURCE_INTELLIGENCE.md) birleştirir. Katalog kod indirmez; seçilen kaynağın gerçek lisansı ve görsel davranışı uygulamadan önce ayrıca doğrulanır.

[İsteğe bağlı video ve fare bakışı akışı](v8/OPTIONAL_VIDEO_POINTER_WORKFLOW.md), CLI ajanının siteyi video olmadan bitirmesini; video seçilirse promptu hazırlayıp sağlanan dosyayı sonradan entegre etmesini tarif eder. [Deneyim planı aracı](tools/v8/experience_plan.mjs) bu ayrımı brief üzerinden çalıştırır.

```sh
python tools/v8/source_advisor.py --surface portfolio --framework next --motion 3d
python tools/v8/source_advisor.py --check greensock/gsap framer/motion --framework react
```

Yeni site veya köklü yeniden tasarımda [brief → ilk referans akışı](reference-engine/BRIEF_TO_REFERENCE.md) kullanılır. Kullanıcının istediği sonuç kısa sorularla netleştirilir; her site için tam uygulamadan önce tek ekranlık çalışan bir görsel önizleme ve kısa inceleme notu hazırlanır. Sağlanan UI/UX referansı masaüstü, mobil ve etkileşim durumlarıyla incelenir; “bire bir” isteniyorsa [aynı ekranlarda karşılaştırma](reference-recreation/PIXEL_CLOSE_QA.md) yapılır.
[Tek ekranlık örnek](examples/v6/reference-first/reference-preview.html) ve [kısa notu](examples/v6/reference-first/reference-note.md) bu aşamanın kapsamını gösterir.

[v7 karşılaştırma aracı](examples/v7/reference-compare/index.html), kaynak ve uygulama ekran görüntülerini yerel tarayıcıda üst üste koyar, fark haritası ve ayarlanabilir eşik gösterir. Dosyalar dışarı gönderilmez. Aynı ölçü şartı ve sonuçların sınırları [v7 rehberinde](README_V7.md) açıklanır.

Renk, köşe ve hareket kararları için [v7 görsel kalibrasyonunu](quality/V7_VISUAL_CALIBRATION.md) uygula. CSS'teki tekrar eden kutu ve animasyon kalıplarını `node tools/v7/audit_visual_defaults.mjs <site-klasörü>` ile tarayabilirsin. Araç uyarıları görsel incelemenin yerine geçmez.

Katalog ve plan denetimi için Python 3.11 veya üzeri yeterli. Bu araçlar ek paket istemez. Video dönüşümü için FFmpeg; prompt ve kaynak seçimi için Node 18+ gerekir. Depo kökünden:

```sh
python tools/validate_all.py
python tools/v6/audit_media_plan.py examples/v6/media_plan.json --format text
python -m unittest discover -s tests -v
```

`validate_all.py` bütün sürüm doğrulayıcılarını ve Markdown bağlantı denetimini tek seferde çalıştırır; CI de aynı komutu kullanır. Örnek plan `PLANNED` döndürür: tahminler bütçeye uyar, ölçüm henüz yoktur. Kendi planını [örnek JSON](examples/v6/media_plan.json) üzerinden oluştur. Alanlar, ölçüm biçimi ve çıkış kodları [medya denetimi rehberinde](tools/v6/README.md) açıklanır.

Araç yerel dosyalarla çalışır; API anahtarı istemez. Bir sitenin erişilebilirliğini, görsel kalitesini veya gerçek performansını kendiliğinden doğrulamaz. [v5 özgünlük kapısı](quality/V5_AUTHENTICITY_GATE.md) ve [v6 sinematik kapıları](quality/V6_CINEMATIC_GATES.md) tasarım incelemesinin parçasıdır.

## Mobil ve scroll uygulaması

[Çalışan scroll örneği](examples/v6/mobile-scroll/index.html), lambanın parçalarını açar, iç bağlantıyı gösterir ve sonunda ışığı yakar. Masaüstünde gerçek Three.js sahnesi, üç yüzey rengi ve bakış açısı kontrolü vardır. Mobilde aynı sahneden üretilen 48 WebP kare gösterilir. Hareket azaltma ve veri tasarrufu tercihlerinde sabit görsellere geçilir.

Doğal kaydırma ve sınırlı kare cache'i [scroll runtime rehberinde](runtime/scroll/README.md); sahne API'si, kamera hareketi ve kare üretimi [3D rehberinde](runtime/three/README.md).

```sh
node --test tests/scroll-progress.test.mjs tests/frame-sequence.test.mjs tests/lamp-motion.test.mjs
```

## Kaynaklar ve 3D video

Yerel önizlemeyi depo kökünden başlat:

```sh
node tools/v6/serve_preview.mjs
```

Ardından `http://127.0.0.1:22222/examples/v7/reference-compare/` veya `http://127.0.0.1:22222/examples/v6/media-studio/` adresini aç. Sunucuyu durdurmak için terminalde `Ctrl+C` kullan.

[Medya atölyesi](examples/v6/media-studio/index.html), React Bits ve 21st.dev dahil yedi sağlayıcıyı ihtiyaca ve framework’e göre filtreler. Nesne, ışık, malzeme ve paletten ChatGPT’ye verilecek masaüstü/mobil video promptunu hazırlar. Yerel video arka planını ve dönüştürülmüş WebP klasörünü önizler. Kaynakları topluca kopyalamaz; resmi kurulum ve lisans kontrolü [kaynak rehberinde](source-intelligence/CREATIVE_COMPONENT_WORKFLOW.md).
Video üretimi isteğe bağlıdır: prompt yalnızca ilgili düğmeye basılınca hazırlanır ve hiçbir ChatGPT/Claude API bağlantısı kurulmaz.

```sh
node tools/v6/creative_media.mjs sources template react project
node tools/v6/creative_media.mjs prompt examples/v6/video-brief.json
```

Gelen videoyu poster, sessiz MP4 ve scroll karelerine dönüştürmek için [video runtime rehberini](runtime/media/README.md) kullan. Kare sayısı, uzun kenar ve aktarım bütçesi denetlenir. Prompt üreticisi video servisi çağırmaz; video üretimi ilgili ChatGPT oturumunda yoksa üretim aracına verilecek prompt istenir.

Bu modüllerin Node testleri Node 22 veya üzerini ister. Three.js 0.185.1, MIT lisansıyla yerel olarak paketlenmiştir. Örnek çalışma sırasında CDN veya harici API kullanmaz; mobil ve sabit görünüm Three.js indirmez.

## Kütüphanede yol bulma

| İhtiyaç | Başlangıç noktası |
| --- | --- |
| Tipografi ve palet | [v3.2 başlangıcı](START_HERE_V3_2.md) |
| Font, ikon ve görsel kaynağı | [v4 başlangıcı](START_HERE_V4.md) |
| Kompozisyon, süsleme ve hareket sınırları | [v5 doktrini](v5/CORE_DOCTRINE.md) |
| Video, kare sekansı ve 3D seçimi | [Medya karar motoru](v6/MEDIA_DECISION_ENGINE.md) |
| Medya bütçeleri | [Bütçe rehberi](v6/PERFORMANCE_BUDGET_ENGINE.md) |
| Kaydırma koreografisi | [Scroll Director](directors/scroll/SCROLL_DIRECTOR.md) |
| Referans rekreasyonu | [v3 başlangıcı](START_HERE_V3.md) |
| Brief ve ilk görsel referans | [Referans öncelikli akış](reference-engine/BRIEF_TO_REFERENCE.md) |
| Harici kütüphane seçimi | [Entegrasyon politikası](integrations/open-source/INTEGRATION_POLICY.md) |
| Araştırma kanıtları | [Araştırma yöntemi](research/methodology.md) |

Katalogdaki bir kaynak, otomatik indirme veya lisans izni anlamına gelmez. Kanıt durumları (`VERIFIED`, `INDEXED`, `SYNTHESIZED`, `NEEDS_CAPTURE`) korunur; doğrulanmamış referanslar incelenmiş gibi sunulmaz.

## Sürüm belgeleri

[v8 değişiklikleri](RELEASE_NOTES_V8.md), [v7](RELEASE_NOTES_V7.md), [v6.1](RELEASE_NOTES_V6_1.md), [v6](README_V6.md), [v5](README_V5.md), [v4](README_V4.md), [v3.2](README_V3_2.md), [v3.1](README_V3_1.md) ve [v3](README_V3.md). Önceki sürümlerin katalogları ve tasarım kuralları kullanılmaya devam eder.
