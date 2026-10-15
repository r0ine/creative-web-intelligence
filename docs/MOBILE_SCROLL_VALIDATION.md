# Mobil ve 3D scroll doğrulaması

15 Ekim 2026: mobil ve masaüstü sahnesine kaydırma konumuyla eşleşen bir zaman çizgisi eklendi. 385 ve 320 piksel genişlikte çizgiye dokunma, klavyeyle başa/sona gitme, 48 karelik sekansın doğru kareyi göstermesi ve yatay taşma olmaması tarayıcıda kontrol edildi. 1440 pikselde aynı kontrol WebGL sahnesini son konuma getirdi. Hareket durdurulunca çizgi gizlendi; tarayıcı hata kaydı boştu. 57 Node testi geçti, v6 doğrulaması 42 dosyada 0 hata bildirdi. Gerçek telefonda dokunma gecikmesi ve pil tüketimi ayrıca ölçülmeli.

22 Eylül 2026: scroll ve 3D kontrolleri Windows, Node 24 ve Playwright Chromium ile çalıştırıldı. Önizleme: `http://127.0.0.1:22222/examples/v6/mobile-scroll/`.

| Kontrol | Sonuç |
| --- | --- |
| Scroll ilerlemesi ve yaşam döngüsü | 19 Node testi geçti |
| Kare yükleme, cache ve iptal | 20 Node testi geçti |
| 3D koreografi, geri sarma ve geçiş sürekliliği | 8 Node testi geçti |
| `tools/v6/check_scroll_demo.cjs` | 12 tarayıcı senaryosu geçti |
| Kare üretimi | 156 WebP, 1.079.988 bayt; kaynak ve dosya SHA256 değerleri doğrulandı |
| Üç renk ve on ileri/geri poz | 30 ölçümün tamamında 29 çizim çağrısı |
| Doğallık taraması | 0 kritik, 0 uyarı; mevcut belgelerde 3 bilgi bulgusu |
| `git diff --check` | Boşluk hatası yok |

Medya planı ve katalog kodu bu turda değişmedi. 21 Eylül kaydı: 73 Python testi geçti; katalog doğrulaması 29 dosyada 0 hata bildirdi.

Masaüstünde gerçek WebGL canvas pikselleri kontrol edildi. Parçaların ayrılması, renk seçimi ve klavyeyle açı değiştirme görüntüyü değiştirdi. Kontroller ve kaydırma durduğunda render sayısı sabit kaldı. Küçük ve örtülü parçalardaki gölge çizimleri kaldırılınca çizim çağrısı 41'den 29'a, gölge geçişleri dahil üçgen sayısı 34.582'den 28.046'ya indi. Görünür geometri değişmedi. 29 çağrı, Rich katmanın 30 tavanına uyar; bu sonuç gerçek cihazdaki FPS ölçümü değildir.

Masaüstünde WebGL çalışırken animasyon WebP isteği oluşmadı. 390 × 844 mobil emülasyonda ileri/geri kaydırma, renk seçimi, durdurma ve devam etme kontrol edildi; Three.js isteği oluşmadı. Mobil sekans 24 yerine 48 kare kullanır. Bellek bütçesi artmadı; yalnız hedef ve komşu kareler istenir.

Masaüstü → mobil → masaüstü geçişi ve canlı reduced-motion açma/kapatma sınandı. Kapatılan WebGL context'in aynı canvas'ta tekrar kullanılması engellenir; yeniden açılışta taze canvas oluşturulur. PageDown doğal kaydırmayı ilerletti; anlatımı atla bağlantısı sonraki bölüme odak verdi.

Başlangıçta açık reduced-motion, veri tasarrufu, kısa yatay ekran ve kapalı JavaScript koşullarında animasyon karesi veya Three.js isteği oluşmadı. Poster, üç bölüm metni ve sabit görseller erişilebilir kaldı.

WebGL context oluşturma hatası simülasyonunda sekansa geçildi. Sentetik `webglcontextlost` olayı da aynı yolu doğruladı; bu, gerçek GPU sürücüsü çökmesi testi değildir. Mobil karelere 503 yanıtı verilince statik düzene geçildi. Bağlantı düzeldikten sonra “Hareketi yeniden dene” düğmesi tek tıkla sekansı açtı. Hata görünümü 320 piksel genişlikte de yatay taşma yapmadı.

Three.js modülü ağda bekletilirken hareket azaltma açıldı. Gecikmiş modül serbest bırakıldıktan sonra hiçbir WebGL context kurulmadı; hareket tercihi tekrar açılınca gerçek 3D sahne yüklendi. Beklenen 503 ve context oluşturma hata mesajları yalnız ilgili hata senaryolarında kabul edildi; diğer senaryolarda konsol veya JavaScript hatası oluşmadı.

Mobil kareler masaüstüyle aynı prosedürel sahneden 720 × 720, DPR 1 ve WebP kalitesi 82 ile üretildi. Kil seti 423.196, orman 384.320, tebeşir 272.472 bayt; her sette 48 kare ve dört sabit görsel bulunur. Toplam 156 dosyanın boyutu ve SHA256 değeri manifestle eşleşti. Sahne, hareket ve sekans konfigürasyonunun kaynak hashleri doğrulandı. Üretimde boş canvas, farklı poz, farklı renk, aynı pozun tekrar üretimi ve tarayıcı hata kontrolleri geçti.

Masaüstü ve mobil görüntüler gözle incelendi. Ana gölge silueti ve nesne geometrisi korundu. İlk poz, ayrışmış poz, ışıklı son poz ve yükleme hatası görünümü kontrol edildi.

Cache sınırı yalnız saklanan çözülmüş kareleri kapsar. Geçici decode, canvas yüzeyi ve tarayıcı iç tahsisleri ayrıca maliyet oluşturur. Gerçek telefonda FPS, ısınma, pil, ekran klavyesi veya adres çubuğu davranışı ölçülmedi.

Harici AI hakemlerine kaynak kod aktarımı önceki otomatik onay incelemesinde veri aktarımı riski nedeniyle engellendi. Bu adım tekrar denenmedi; dış hakem puanı yok. Yerel tarama, bağımsız kod incelemesi ve çalıştırma kontrolleri tamamlandı.
