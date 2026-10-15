# Creative Web Intelligence v7

[Kurulum ve kullanım](docs/INSTALL_TR.md) · [Installation and usage](docs/INSTALL_EN.md) · [English release notes](RELEASE_NOTES_V7.en.md)

Bu sürüm, referansı önceleyen tasarım akışına yerel bir görsel karşılaştırma aracı ekler. Kaynak ve uygulama ekran görüntülerini aynı ölçüde seçince üst üste görünüm, ayarlanabilir fark eşiği ve ısı haritası sunar. Dosyalar tarayıcıdan dışarı aktarılmaz; API anahtarı veya ek paket gerekmez.

`quality/V7_VISUAL_CALIBRATION.md` renklerin kaynağına, köşe diline ve animasyonun görevine bakar. `tools/v7/audit_visual_defaults.mjs` tekrarlanan kutular, koyu çizgi yoğunluğu ve otomatik animasyon kalıpları için yerel bir ilk tarama yapar. Bu araç tasarım beğenisini puanlamaz; işaretlediği noktaları görsel olarak yeniden incelemek gerekir.

Depo kökünden:

```sh
node tools/v6/serve_preview.mjs
```

Ardından `http://127.0.0.1:22222/examples/v7/reference-compare/` adresini aç. Görüntülerin genişlik, yükseklik, cihaz ölçeği ve kaydırma konumu aynı olmalı. PNG, JPG ve WebP kabul edilir; dosya başına 25 MB, görüntü başına 8 milyon piksel sınırı vardır. Araç farklı ölçüleri karşılaştırmaz çünkü o durumda piksel oranı yanıltıcı olur.

```sh
python tools/v7/validate_v7.py
node --test tests/pixel-compare.test.mjs
node tools/v7/audit_visual_defaults.mjs examples/v7/reference-compare
```

Ortalama renk farkı 0–255 ölçeğindedir. “Eşiği aşan piksel” seçilen eşikten büyük ortalama RGB farkına sahip piksellerin oranıdır. Saydam pikseller beyaz zemin üzerinde değerlendirilir. Font yumuşatma, dinamik içerik ve tarayıcı farkı oranı etkiler; sonuç bir kalite puanı değildir. Görsel eşleşmeden sonra menü, odak, dokunma ve animasyon durumları ayrıca sınanır.

İlk karar akışı [v7 başlangıcında](START_HERE_V7.md), araç kodu [karşılaştırma runtime'ında](runtime/reference/pixel-compare.mjs), eski scroll ve 3D örneği [v6 rehberinde](README_V6.md) bulunur.
