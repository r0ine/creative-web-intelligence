# Creative Web Intelligence v8

1. Kullanıcının brief'ini açık istekler, çıkarımlar ve bilinmeyenler olarak ayır. Sonucu değiştirecek kısa soruları sor. Yeni site veya köklü yeniden tasarımda [referans öncelikli akış](reference-engine/BRIEF_TO_REFERENCE.md) ile önce tek ekranlık prototip ve inceleme notu hazırla.
2. Kullanıcının verdiği referansı önce incele. Kaynak verilmediyse [v8 danışmanından](tools/v8/source_advisor.py) yüzey, framework ve motion ihtiyacına göre **bir** başlangıç referansı seç. Katalog sırası tasarım kalitesi sırası değildir.
3. [Beş mercekli kaynak incelemesini](source-intelligence/V8_SOURCE_INTELLIGENCE.md) yap. GitHub açıklamasını görsel inceleme sanma; bilinmeyenleri açık bırak. Diğer kaynakları yalnızca çözülmemiş bileşen, 3D veya hareket ihtiyacı için aç.
4. Design DNA'yı projeye özgü kur. v5 özgünlük kapısı, [v7 görsel kalibrasyonu](quality/V7_VISUAL_CALIBRATION.md) ve [v6 medya kararı](v6/MEDIA_DECISION_ENGINE.md) seçimleri sınırlar. Hareketin ve 3D'nin görevi yoksa statik anlatım seç.
5. Kod veya paket almadan önce kaynağın lisans dosyasını, sürüm uyumunu, component/theme çakışmasını ve mobil/reduced-motion karşılığını doğrula. `--check` ile seçilen kaynakları birlikte denetle; otomatik kurulum yapma.
6. Uygulamayı gerçek tarayıcıda masaüstü ve mobilde aç; aynı viewport'ta referansla karşılaştır. Performans ve erişilebilirlik kapılarını çalıştır. Kütüphane değişiklikleri için `python tools/v8/validate_v8.py` kullan.

```sh
python tools/v8/source_advisor.py --surface portfolio --framework next --motion 3d
python tools/v8/source_advisor.py --source dillionverma/portfolio
python tools/v8/source_advisor.py --check pmndrs/react-three-fiber pmndrs/drei --framework react
python tools/v8/validate_v8.py
```

Araçlar mevcut depolardan kod indirmez. Kaynak listesi ve kanıt düzeyleri [v8 kaynak rehberinde](source-intelligence/V8_SOURCE_INTELLIGENCE.md) açıklanır. Önceki sürümlerin mobil scroll, 3D, medya ve referans araçları kullanılmaya devam eder.
