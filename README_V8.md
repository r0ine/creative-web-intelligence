# v8: Kaynaklardan tasarım kararı üretme

v8, 46 GitHub adresini erişim ve lisans durumu belli bir araştırma kataloğuna ekler. Bir portföy, landing page veya dashboard çalışmasında tek başlangıç referansı seçer; hareket ve 3D kaynaklarını yalnız gerekliyse yanına koyar. Bu, otomatik şablon kurucusu değildir.

[Başlangıç akışı](START_HERE_V8.md) brief'ten tek ekranlık referansa gider. [Kaynak rehberi](source-intelligence/V8_SOURCE_INTELLIGENCE.md) her depoyu beş mercekle inceleme, kanıt düzeyi ve çakışma kapılarını anlatır. [Kayıt](data/v8/source_registry.json) kullanıcının özgün adresi ile varsa taşındığı adresi saklar. Lisans ve erişim meta verisi 17 Ekim 2026'da denetlendi; zaman içinde değişebilir.

```sh
python tools/v8/source_advisor.py --surface portfolio --framework next --motion 3d
python tools/v8/source_advisor.py --source ibelick/motion-primitives
python tools/v8/source_advisor.py --check greensock/gsap framer/motion --framework react
python tools/v8/validate_v8.py
```

Danışman API anahtarı istemez. Tek kaynak fişi README'den doğrulanmış kısa bulguları ve henüz görsel olarak incelenmemiş beş alanı açıkça gösterir. `--check`, birden çok şablon, stilli UI temeli veya hareket motorunun aynı işte çakışmasını bildirir; lisansı belirsiz kod aktarımını engeller. React Three Fiber ve Drei uyumlu bağımlılık çifti olarak değerlendirilir.

İki verilen depo adresi bu taramada 404 döndü; 12 depo için GitHub'ın lisans meta verisi yeterli değildi. Bunlar katalogdan gizlenmez, durumları belirtilir. Kod, medya veya şablon kopyalamadan önce gerçek lisans dosyasını ve hedef projenin koşullarını denetle.
