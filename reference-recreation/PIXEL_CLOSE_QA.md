# Pixel-Close QA

At each required viewport compare:

- section start/end positions
- major bounding boxes
- alignment axes
- text block width and line wrapping
- headline baseline/line-height behavior
- media crop and focal point
- corner radius / border / stroke families
- background role and contrast
- sticky/pinned states
- transition state at chosen progress checkpoints

Fix order:

`wrong structure -> wrong scale -> wrong alignment -> wrong text metrics -> wrong crop -> wrong color/material -> micro decoration`.

Never compensate for a wrong container model with dozens of magic margins.

## UI/UX davranış karşılaştırması

Görsel yakınlık tek başına yeterli değildir. Kaynakta görülebilen her önemli kontrol için başlangıç, tetik, sonuç ve geri dönüş durumunu kaydet; hedefte aynı yolu klavye, fare ve dokunmayla dene. Menü açılma/kapanma, odak sırası, form doğrulama, yükleme/hata/boş durumları, sticky davranış ve scroll yönünü ilgiliyse karşılaştır. Video varsa aynı ilerleme noktalarından kare al; tek bir ekran görüntüsünden animasyon süresi uydurma.

Masaüstü ve mobil için ayrı hedef viewport kullan. Aynı genişlik/yükseklikte kaynak ve uygulama görüntülerini yan yana koyup önce büyük kutuları, sonra satır kırılımını ve medya kırpmasını düzelt. Eksik varlık veya erişilemeyen durum nedeniyle doğrulanamayan farkı açıkça yaz. “Bire bir” ifadesini ancak karşılaştırılan ekranlar ve durumlarla sınırlı kullan; tüm siteyi kapsadığı izlenimini verme.

Yerel görüntü karşılaştırması için `examples/v7/reference-compare/` aç. Kaynak ve çıktıyı aynı viewport, cihaz ölçeği ve scroll konumunda çek. Üst üste görünümde hizalama, fark haritasında büyük sapmalar incelenir. Sayısal fark kalite puanı değildir; font rasterizasyonu ve dinamik içerik de piksel değiştirir. Erişilebilirlik ve etkileşim durumları ayrı QA gerektirir.
