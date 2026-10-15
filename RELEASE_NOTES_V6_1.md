# v6.1 — Medya planı denetimi

## Kaynaklar ve video akışı

4 Ekim eklemesi: [medya atölyesi](examples/v6/media-studio/index.html) kaynakları rol, framework ve kullanım kapsamına göre filtreler. React Bits hedef React uygulamasına resmi kurulumla; 21st.dev resmi Copy prompt veya kullanıcı tarafından alınmış kaynakla bağlanır. Koleksiyonlar topluca kopyalanmaz. Kaynak rehberi lisans, yazar, sürüm, bağımlılık ve uyarlama kaydını tanımlar.

`creative_media.mjs`, brief’ten masaüstü ve mobil için ChatGPT video promptu üretir. Arka plan döngüsü ile ileri/geri scroll anlatımı farklı storyboard kullanır. `video_to_web.py`, yerel videodan bütçe sınırında WebP kareleri, poster, sessiz MP4 ve dosya hash’lerini içeren manifest hazırlar. `background-video.mjs`, görünürlük, hareket azaltma, veri tasarrufu, durdurma ve oynatma hatalarında kaynak yaşam döngüsünü yönetir. Gerçek video üretim servisi çağrılmaz.
Video promptu isteğe bağlıdır; atölye açıldığında boş kalır ve sadece kullanıcı düğmeye basınca hazırlanır. ChatGPT veya Claude API bağlantısı gerekmez.

## Mobil ve scroll uygulaması

22 Eylül eklemesi: mobil sekans 48 kareye çıktı; kare sayısı üretici, örnek ve test arasında ortak konfigürasyondan okunur. Cache bütçesi aynı kaldı. Küçük parçalardaki gereksiz gölge çizimleri kaldırıldı; masaüstü sahne 41 yerine 29 çizim çağrısı kullanır. Sekans yükleme hatasından sonra tek tıkla yeniden deneme eklendi. Geciken 3D modülünün hareket azaltma tercihini geçersiz kılmadığı da tarayıcı testine alındı.

21 Eylül eklemesi: [çalışan örnek](examples/v6/mobile-scroll/index.html) gerçek bir Three.js lambasına geçti. Kaydırma parçaları ayırır, kamera iç bağlantıyı gösterir, birleşmeden sonra ışık açılır. Masaüstünde üç renk ve bakış açısı kontrolü vardır. Mobilde aynı sahneden hazırlanmış, her renk için 24 WebP kare yüklenir; Three.js indirilmez. WebGL kaybı sekansa, sekans hatası statik düzene geçer. Sahne yalnız konum, boyut veya kontrol değişince çizilir. [Sahne API'si ve yeniden üretim](runtime/three/README.md).

20 Eylül eklemesi: `runtime/scroll` altında doğal kaydırma gözlemcisi ve sınırlı cache kullanan kare oynatıcısı bulunur. İlk 2D SVG kareleri kaynaklarıyla korunur. Hareket azaltma, veri tasarrufu, durdurma ve kısa ekran durumlarında statik düzene geçilir. [Kullanım ve sınırlar](runtime/scroll/README.md), [doğrulama kaydı](docs/MOBILE_SCROLL_VALIDATION.md).

Mobil belgelerde zorunlu pin, `4vh`/dört viewport karışıklığı, klavyesiz 3D'yi dekoratif sayma ve Canvas 2D'nin GPU maliyetini sıfır kabul etme hataları düzeltildi.

## Plan denetimi

v6 medya kararlarını belgelerle tarif ediyordu. Bu sürüm, verilen bir planı aynı kataloglarla denetleyen `tools/v6/audit_media_plan.py` komutunu ekler.

- Masaüstü ve mobil maliyetler görsel anlar üzerinden toplanır; bütçe aşımı raporlanır.
- Amaç, HTML içerik karşılığı, klavye erişimi, mobil katman, hareket azaltma ve düşürme zinciri denetlenir.
- Tahminler ve beyan edilen ölçümler ayrılır. Ölçüm yokken `PLANNED`, iki cihaz için sınırlar içindeki ölçüm girildiğinde `MEASURED` raporlanır. `--require-measurements` eksik ölçümü engeller.
- Medya planı için JSON Schema ve biri geçerli, biri bütçeyi aşan iki örnek eklenir.
- v6 katalog doğrulayıcısı yanlış veri tiplerini, kimlik tekrarlarını, kopuk medyum referanslarını ve geçersiz bütçeleri yakalar.
- Profil fallback kimlikleri medya kataloğuyla eşleştirilir. İlk medya yükü sınırları, mevcut JSON değerleri esas alınarak bütçe belgesinde tutarlı hale getirilir.
- Testler GitHub Actions üzerinde Linux ve Windows'ta Python 3.11 ve 3.14 ile çalışacak şekilde yapılandırılır.

Önceki serbest metin medya kararları tasarım notu olarak kullanılabilir; CLI girdisi için [yeni plan sözleşmesini](schemas/v6/media_plan.schema.json) kullan. Katalog bütçeleri yükseltilmedi. Yeni denetim, v5 ve v6 görsel inceleme kapılarının yerine geçmez.
