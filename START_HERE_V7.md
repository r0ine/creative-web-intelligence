# v7 ile başla

v7, yeni bir sitenin ilk adımını görünür ve denetlenebilir kılar: brief'i çöz, gerekiyorsa kısa sorular sor, tek ekranlık referans önizlemesi hazırla, sonra kaynak ile uygulamayı aynı koşullarda karşılaştır. Eski sürümlerin kompozisyon, medya, scroll ve 3D kuralları bu akışın parçası olmaya devam eder.

1. `reference-engine/BRIEF_TO_REFERENCE.md` ile açık istekleri, çıkarımları ve bilinmeyenleri ayır. Sonucu değiştirecek en fazla üç soruyu erkenden sor.
2. Yeni site veya köklü yeniden tasarım için tek ekranlık çalışan `reference-preview.html` ve kısa `reference-note.md` hazırla. Bu aşamayı tam site uygulamasına dönüştürme.
3. Kullanıcı bir UI/UX kaynağı verdiyse görülebilen masaüstü, mobil ve etkileşim durumlarını incele. Kaynağa erişilemeyen durumları tahmin diye işaretle. Renk, köşe ve hareket kararlarını `quality/V7_VISUAL_CALIBRATION.md` ile gerekçelendir.
4. Aynı viewport ve scroll konumunda ekran görüntüleri al. `examples/v7/reference-compare/` aracıyla üst üste görünümü ve fark haritasını incele. Ölçüler farklıysa önce çekimi düzelt.
5. Yapı, ölçek, hizalama, metin ölçüsü, kırpma ve renk sırasıyla düzelt. Menü, dokunma, klavye, animasyon ve scroll durumlarını ayrıca sınayarak `reference-recreation/PIXEL_CLOSE_QA.md` kontrolünü tamamla.
6. Medya seçimi için `v6/MEDIA_DECISION_ENGINE.md` kullan. Video yalnız istenirse prompt veya varlık akışına girer. Mobilde düşük hareket, veri tasarrufu ve statik karşılığı koru.

Araç çevrimdışı çalışır, seçilen dosyaları sunucuya göndermez. Piksel farkı tek başına tasarım veya kullanılabilirlik puanı değildir; tarayıcı, font rasterizasyonu ve dinamik metin de fark üretir.

Çalıştırma ve test komutları [v7 rehberinde](README_V7.md).
