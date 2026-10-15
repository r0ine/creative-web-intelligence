# v7 değişiklikleri

Bu sürüm referans öncelikli tasarım akışını çalışan araçlara bağlar; mobil scroll, 3D, medya ve doğrulama çalışmalarını da açık depoya taşır.

- **Referans akışı:** Yeni sitede brief yorumu, sonucu değiştiren kısa sorular, tek ekranlık görsel önizleme ve inceleme notu hazırlanır. Tam uygulama aynı yön üzerinden ilerler; her bölüme ayrı başlangıç prototipi üretilmez.
- **Görsel karşılaştırma:** Kaynak ve uygulama ekran görüntüleri yerel tarayıcıda üst üste gösterilir. Fark haritası ve aynı ölçülerde piksel karşılaştırması vardır; PNG, JPG ve WebP kabul edilir. Piksel yakınlığı etkileşim, erişilebilirlik veya hareket eşleşmesi anlamına gelmez.
- **Görsel kalibrasyon:** Renk ve köşe biçimlerinin kaynağını, animasyonların görevini açıklayan rehber eklendi. Yerel CSS denetimi tekrar eden çerçeveli yüzeyleri, koyu zemindeki çizgi yoğunluğunu, genel fade-up'ı, `transition: all` ve sonsuz hareketi işaretler. Karşılaştırma ekranı kâğıt tonlu sakin bir görünüme geçti.
- **Mobil scroll ve 3D:** Lamba örneği masaüstünde gerçek Three.js sahnesi, mobilde 48 yerel WebP kare, hareket azaltma veya veri tasarrufunda sabit görseller kullanır. Scroll ve kare runtime'ları sınırlı yükleme, temizleme ve ters kaydırma davranışlarını kapsar.
- **İsteğe bağlı video:** Medya atölyesi ChatGPT'ye elle yapıştırılacak prompt üretir, seçilen yerel videoyu ve dönüştürülmüş kare dizisini önizler. Model API'si gerekmez. Video dönüştürme aracı yalnız kullanıldığında FFmpeg ister.
- **Kaynak seçimi:** React Bits, 21st.dev ve diğer sağlayıcılar kurulum/lisans rehberiyle kataloglandı. Bileşen kodları depoya topluca kopyalanmadı.
- **Doğrulama:** Medya planı denetimi, v7 katalog kontrolü, Node/Python testleri ve GitHub Actions akışı yeni çalışma parçalarını kapsar. Harici bileşenlerin lisansı ve uyumu seçilen dosya için ayrıca doğrulanmalıdır.

Kurulum ve kullanım: [Türkçe](docs/INSTALL_TR.md) · [English](docs/INSTALL_EN.md).
