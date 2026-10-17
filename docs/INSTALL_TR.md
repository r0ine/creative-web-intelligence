# Kurulum ve kullanım

Creative Web Intelligence; tasarım karar belgeleri, yerel denetim araçları ve çalışan örneklerden oluşur. Paket yöneticisi veya API anahtarı gerektirmez. Komutları depo kökünde çalıştır.

## Gereksinimler

- Git, Node.js 22 veya üzeri ve Python 3.11 veya üzeri.
- Videoyu WebP karelere dönüştüreceksen FFmpeg. Diğer akışlarda gerekli değildir.
- Örnekler için güncel bir Chromium, Firefox veya Safari tarayıcısı. Gerçek zamanlı 3D için WebGL desteği gerekir.

```sh
git clone https://github.com/r0ine/creative-web-intelligence.git
cd creative-web-intelligence
python tools/v8/validate_v8.py
```

Doğrulama, önceki katalogları ve v7'nin Node testlerini de çalıştırır. Python veya Node komutu sisteminde farklı adla kuruluysa o adı kullan.

## Yerel örnekleri aç

```sh
node tools/v6/serve_preview.mjs
```

Sunucu yalnız `127.0.0.1:22222` adresini dinler. Port doluysa başka bir süreci durdurmaz; boş bir port için `CWI_PREVIEW_PORT` ortam değişkenini ayarla. Sunucuyu durdurmak için `Ctrl+C` kullan. Örnekleri `file://` adresiyle açma; JavaScript modülleri için yerel HTTP gerekir.

| Örnek | Adres |
| --- | --- |
| Referans karşılaştırma | `http://127.0.0.1:22222/examples/v7/reference-compare/` |
| Mobil/3D scroll | `http://127.0.0.1:22222/examples/v6/mobile-scroll/` |
| Medya atölyesi | `http://127.0.0.1:22222/examples/v6/media-studio/` |
| Tek ekranlık ilk referans | `http://127.0.0.1:22222/examples/v6/reference-first/reference-preview.html` |

## Codex'e beceri olarak kur

```sh
python tools/v7/install_codex_skill.py
```

Bu komut ana kütüphaneyi `~/.codex/skills/creative-web-intelligence`, kısayolu `~/.codex/skills/crative-web` altına kopyalar. Mevcut aynı isimli beceri dosyalarını günceller; depodaki iç kısayolu ana beceriye ikinci kez kurmaz. Codex farklı bir beceri dizini kullanıyorsa `--skills-dir` ile o dizinin tam yolunu ver. Yeni bir sohbette şöyle yaz:

```text
/crative-web Mobilde doğal kaydırma kullanan, 3D nesneyi yalnız ürünün yapısını göstermek için açan bir sayfa tasarla. Önce kısa görsel referans hazırla.
```

Başka bir kod asistanıyla çalışıyorsan depo kökündeki `SKILL.md` ve `START_HERE_V8.md` dosyalarını bağlam olarak ver. `/crative-web` kısayolu yalnız onu destekleyen beceri ortamlarında çalışır.

## Çalışma akışı

1. Yeni site için `reference-engine/BRIEF_TO_REFERENCE.md` ile isteği netleştir; tam uygulamadan önce bir ekranlık önizleme ve kısa not üret. Küçük düzeltmelerde bu adımı tekrar etme.
2. Kullanıcı kaynak vermediyse v8 danışmanıyla tek referans seç; kaynak verilmişse önce onu incele. Kaynak fişindeki soruları gerçek masaüstü/mobil görüntüyle yanıtla. Kurulum veya kod kopyalama öncesi çakışma ve lisans kontrolü yap:

```sh
python tools/v8/source_advisor.py --surface portfolio --framework next --motion 3d
python tools/v8/source_advisor.py --source ibelick/motion-primitives
python tools/v8/source_advisor.py --check greensock/gsap framer/motion --framework react
```

3. Renk, köşe ve hareket kararlarını `quality/V7_VISUAL_CALIBRATION.md` ile gerekçelendir. Gerekli medyum için `v6/MEDIA_DECISION_ENGINE.md` kullan.
4. Kaynak ve uygulama ekran görüntülerini aynı viewport ve scroll konumunda alıp karşılaştırma aracına yükle. Üst üste görünüm ve fark haritası yapı hatalarını gösterir; davranış ve erişilebilirliği ayrıca denetle. PNG, JPG ve WebP desteklenir. Dosya başına 25 MB, görüntü başına 8 milyon piksel sınırı vardır. Dosyalar tarayıcıda kalır.
5. CSS'teki tekrarları ve otomatik hareket kalıplarını tara:

```sh
node tools/v7/audit_visual_defaults.mjs examples/v7/reference-compare
```

Sıfır uyarı tasarımın iyi olduğunu tek başına kanıtlamaz; masaüstü ve mobil önizlemeyi görsel olarak incele.

## Scroll, medya ve video

Mobil/3D örneğinde doğal scroll masaüstündeki Three.js sahnesini yönetir; mobilde yerel WebP karelere, hareket azaltma veya veri tasarrufunda sabit görsele geçer. Kendi sitene taşırken `runtime/scroll/README.md` ve `runtime/three/README.md` ile başlayıp örnekteki poster ve temizleme davranışını koru.

Medya atölyesinde React Bits, 21st.dev ve diğer kaynaklar ihtiyaca göre filtrelenir. Katalog, bu sitelerin kaynak kodunu kütüphaneye gömmez; seçtiğin bileşenin lisansını ve bağımlılıklarını ayrıca doğrula. Video üretimi isteğe bağlıdır. Prompt düğmesine basınca ChatGPT'ye elle yapıştırılacak metin hazırlanır; ChatGPT/Claude API bağlantısı kurulmaz.

CLI ile aynı metni üretmek için:

```sh
node tools/v6/creative_media.mjs prompt examples/v6/video-brief.json
```

Elinde yerel video ve FFmpeg varsa dönüştürme adımları `runtime/media/README.md` içindedir. Video gelmeden oynatılabilir varlık üretildiğini varsayma.

## Testler

```sh
python tools/v8/validate_v8.py
python -m unittest discover -s tests -v
node --test tests/*.test.mjs
```

FFmpeg entegrasyon testleri `CWI_TEST_FFMPEG` ayarlanmadığında atlanır. Katalog ve karşılaştırma testleri ek paket istemez. Daha önce kurulmuş beceriyi güncellemek için depoda `git pull` yaptıktan sonra `install_codex_skill.py` komutunu yeniden çalıştır.
