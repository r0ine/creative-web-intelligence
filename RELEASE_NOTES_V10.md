# v10 sürüm notları

**Dil:** Türkçe · [English](RELEASE_NOTES_V10.en.md)

## Referans laboratuvarı

[Referans laboratuvarı](reference-engine/REFERENCE_LAB.md), kullanıcının verdiği siteyi indirip ölçer, düzenlenecek yerleri bulur ve yeni işi referansla karşılaştırır. İndirilenler `reference-workspace/` altında kalır ve git'e girmez.

- `tools/v10/mirror_reference.py`: `wget --mirror --convert-links --adjust-extension --page-requisites --no-parent` komutunu derinlik, kota ve bekleme sınırlarıyla çalıştırır. robots.txt kurallarına uyar. `capture.json` dosyasına dosya türlerini, boyutu, giriş sayfasını ve bulunan lisansları yazar. Sonuç üç kullanım kararından biridir: `owned`, `license-review`, `study-only`. JavaScript ile oluşturulan boş sayfaları ayrıca işaretler.
- `tools/v10/capture_reference.mjs`: siteyi Playwright ile masaüstü ve mobil ölçüde açar. Ekran görüntüsü, hareket azaltma görüntüsü, alan ağırlıklı palet ve nötr/destek/vurgu oranı, fontlar, animasyonlar, script adresleri ve WCAG kontrast bulgularını kaydeder. axe-core kuruluysa erişilebilirlik ihlallerini de ekler.
- `tools/v10/analyze_reference.py`: indirilen kopyadan şunları çıkarır:
  - **tasarım ölçüleri:** renk rolleri, palet, fontlar, tip ölçeği, boşluk, köşe, süre/easing, kırılımlar, CSS değişkenleri,
  - **site bilgisi:** kullanılan kütüphaneler, sayfa yapısı, statik erişilebilirlik bulguları ve ağırlık.
  
  Ayrıca v9 yüzeylerinin CSS'teki dosya ve satırını gösteren **düzenleme haritasını** ve referansın kütüphane kurallarıyla çakıştığı yerleri listeler. Çıktılar `analysis.md`, `analysis.json` ve `tokens.css`.
- `tools/v10/compare_reference.mjs`: referans ile yeni işi aynı ekran ölçüsünde karşılaştırır. Fark görüntüsü, farklı piksel oranı ve en farklı ekran bölgesini verir; v7 piksel karşılaştırma modülünü kullanır.
- `tools/v10/template_catalog.py`: v8 kaynak kaydındaki açık kaynak şablon ve bileşenleri lisansa göre ayırır: düzenlenebilir, aynı lisansla paylaşılır, yalnız incelenir.
- `runtime/reference/style-metrics.mjs`: renk okuma, WCAG kontrastı, alan paleti ve fark bölgeleri için test edilmiş saf fonksiyonlar.

## Denemede bulunanlar

- Statik analiz ile axe-core aynı örnek sitede aynı beş sorunu buldu: boş buton, kontrast, başlık sırası, alt metin, boş bağlantı.
- Az içerikli statik sayfaların JavaScript kabuğu sanılması düzeltildi.

## Bakım

- v7, v8 ve v9 doğrulayıcıları manifest sürümünü sayısal karşılaştırır; her yeni sürümde güncelleme gerekmez.
- `validate_v10.py` iki tutarlılığı denetler: düzenleme haritasının v9 yüzeyleriyle aynı kalması ve analizde atıf yapılan çakışmaların v9 kaydında bulunması. `validate_all.py` v10 zincirini çalıştırır.
