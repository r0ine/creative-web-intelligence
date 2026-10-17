# v8 kaynak zekâsı

Bu katman, GitHub adreslerini kurulacak paket listesi olarak değil, tasarım kararlarını araştırma kuyruğu olarak kullanır. [Aday listesi](../data/v8/source_candidates.json) kullanıcının verdiği 46 adresi aynen saklar. [Kayıt](../data/v8/source_registry.json) GitHub API'sinden 17 Ekim 2026'da alınan erişim, taşınma ve lisans meta verisidir. [Profiller](../data/v8/source_profiles.json) her adresin rolünü, olası teknoloji uyumunu ve araştırılacak tek soruyu verir. [README bulguları](../data/v8/readme_findings.json) yalnızca okunan depolardan çıkarılmış kısa notlardır.

Kayıt 41 depo, dört GitHub konu sayfası ve bir organizasyon sayfası içerir. Konu ve organizasyon sayfaları yalnızca keşif içindir; alt depoların erişimi veya lisansı için kanıt sayılmaz. `JavaScript-Mastery-Pro/threejs-portfolio` ve `aceternity/aceternity-ui` adresleri bu taramada 404 döndü. Altı adres başka depoya yönlendi; özgün istek adresi ile kanonik adres ayrı tutuldu. 12 deponun lisansı GitHub meta verisinde doğrulanamadı. Bu sayı, lisansın bulunmadığı değil, bu yöntemle doğrulanamadığı anlamına gelir.

## Kanıt düzeyi

1. **Meta veri:** Deponun varlığı, açıklaması, yönlendirmesi ve GitHub'ın tanıdığı lisans. Görsel kaliteye ilişkin hüküm üretmez.
2. **README incelemesi:** Yazarın açıkladığı teknoloji ve özellikler. Performans iddiası bağımsız ölçüm değildir.
3. **Kaynak incelemesi:** Belirli dosya, sürüm ve bileşen düzeni. Bu sürümde her depo için yapılmış sayılmaz.
4. **Görsel ve davranış incelemesi:** Aynı viewport'ta masaüstü/mobil görüntü, hover, scroll, klavye ve hareket azaltma durumu. Bunlar görülmeden hero, tipografi, grid veya animasyon niteliği “doğrulandı” diye yazılmaz.

Kaynak fişindeki `focus` bir araştırma sorusudur; bulgu değildir. README notundaki “incele”, “kontrol et” gibi cümleler CWI'nin uygulama önerisidir. Ekran görüntüsü veya çalışan demo ile kanıtlanmamış görsel ayrıntı kaynak özelliği olarak aktarılmaz.

## Beş mercekli inceleme

Seçilen **tek** başlangıç referansı için kısa bir görsel prototip ve aşağıdaki not hazırlanır. Diğer kaynaklar yalnızca belirli bir eksik için açılır; bütün kataloğu aynı anda bağlama yükleme.

| Mercek | Kaydedilecek kanıt | Karar |
| --- | --- | --- |
| Design Patterns | Masaüstü/mobil hero oranı, yazı ölçeği, grid, boşluk, renk ve içerik sırası | Fikrin projeye hangi kısmı uyuyor? |
| Motion Intelligence | Scroll tetikleri, hover/focus, süre, easing, çıkış durumu ve 3D kamera görevi | Hareket hangi bilgiyi açıklıyor? |
| Component Architecture | Shell, bileşen sınırları, tema tokenları, veri modeli, bağımlılık sürümleri | Hangi yaklaşım yeniden kullanılabilir? |
| Anti-Generic Design | Tekrarlanan hero/kart/gradient kalıpları, kaynağa özgü fikir, markaya özgü değişiklik | Hazır görünümü değil hangi ilkeyi alacağız? |
| Performance | Mobil yükleme, canvas sayısı, CLS/INP/LCP, reduced-motion, statik fallback | Aynı fikrin daha ucuz karşılığı var mı? |

Her gözleme kaynak URL'si, dosya veya görüntü ve tarih ekle. Görülmeyen alanı `incelenmedi` yaz. “Bire bir” talebinde kaynak ve uygulamayı aynı ölçüde [v7 karşılaştırıcısında](../examples/v7/reference-compare/index.html) karşılaştır; lisans koşulları kod, görsel ve metin için ayrıca geçerlidir.

## Çakışma kapısı

- **Bir site kabuğu:** Bir portföy veya dashboard şablonunu temel al. Başka şablonlardan yalnızca yöntem öğren.
- **Bir stilli UI temeli:** shadcn/ui, DaisyUI, Flowbite, HeroUI ve Ant Design'ın temalarını topluca ekleme. Headless UI görsel stil sağlamaz; davranış katmanı olarak değerlendirilebilir.
- **Bir hareket sahibi:** Aynı DOM öğesini GSAP ve Motion ile eşzamanlı yönetme. Zaman çizelgesi, temizleme ve reduced-motion sorumluluğunu tek yerde tut.
- **3D bağımlılık çifti:** Drei, React Three Fiber'ın yardımcısıdır. React ve `three` sürüm uyumu doğrulanmadan ekleme. 3D sahne anlamlı değilse mevcut statik/sekans seçeneğine dön.
- **Scroll sahibini koru:** Lenis isteğe bağlıdır. Yerel kaydırma, anchor, sticky, klavye, mobil dokunma ve ScrollTrigger ile birlikte doğrula.
- **Lisans sınırı:** Kayıttaki `MIT` veya başka SPDX etiketi yalnız GitHub meta verisidir. Gerçek dosya, alt paket, medya ve atıf koşullarını entegrasyondan önce kontrol et. Lisansı belirsiz kaynaklardan kod taşıma. GPL depoları ayrıca değerlendir. GSAP'in README'si [özel standart lisansına](https://gsap.com/standard-license) yönlendirir; GitHub'da SPDX görünmemesi onu MIT yapmaz.

[Mevcut açık kaynak entegrasyon politikası](../integrations/open-source/INTEGRATION_POLICY.md) ve [v6 yaratıcı bileşen akışı](CREATIVE_COMPONENT_WORKFLOW.md) geçerliliğini korur. v8 kayıtları bunların yerine kopya kütüphane kurmaz; seçim öncesi kanıt ve çakışma katmanı ekler.

## Yerel kullanım

```sh
python tools/v8/source_advisor.py --surface portfolio --framework next --motion 3d
python tools/v8/source_advisor.py --source pmndrs/react-three-fiber
python tools/v8/source_advisor.py --check greensock/gsap framer/motion --framework react
python tools/v8/source_advisor.py --surface landing --framework astro --format json
```

Araç kayıtlı veriyi çevrimdışı okur; API anahtarı istemez ve paket kurmaz. Yalnız kaynak meta verisini yenilemek için GitHub CLI oturumu gerekir: `python tools/v8/refresh_source_registry.py`. Yenilemeden sonra yeni kanonik adres ve lisans değişiklikleri insan tarafından gözden geçirilmelidir.
