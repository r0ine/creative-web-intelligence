# Mobile Scroll Recomposition

Mobilde önce normal belge akışını kurun. Masaüstünün pin süresini, yatay düzenini ve kare sayısını doğrudan küçültmeyin.

## Yerleşim kararları

| Masaüstü davranışı | Mobil karşılığı |
|---|---|
| Uzun pinned sahne | Kısa sticky görsel veya normal akışta poster |
| Dikey scroll ile yatay hikâye | Okuma sırasını koruyan dikey bölümler |
| Scroll sırasında hareket eden küçük metin | Sabit HTML metin; hareket yalnız görselde |
| Hover ile açılan açıklama | Dokunma ve klavyeyle çalışan görünür kontrol |
| Yoğun canvas/3D | Daha düşük bütçeli varyant; katman izin vermiyorsa poster |

CTA ve metinler ekran yüksekliğini aşıyorsa sahneyi pinlemeyin. Dokunma hedefleri hareket etmez; yakınlaştırma engellenmez. Sticky öğe bir sonraki bölüme taşmaz.

## Viewport ve sticky ölçümü

`svh`, tarayıcı arayüzünün açık olduğu küçük viewport'a göre sabit bir yükseklik sağlar. `dvh` görünür alanla değişir; uzun hikâyenin yüksekliğinde kullanılması adres çubuğu hareket ederken ilerlemeyi değiştirebilir. Kararlı bir sahne için önce `vh` yedeği, destekleniyorsa `svh` kullanın. [MDN: viewport birimleri](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/length#relative_length_units_based_on_viewport)

Scroll ilerlemesini gerçek bölüm ve sahne ölçülerinden hesaplayın. Örneğin 100svh sahneye 200svh hareket mesafesi ayırmak, 300svh bölüm gerektirir. Bölümün tamamı ile hareket mesafesi raporda ayrı tutulur.

- Pencere boyutu, cihaz yönü veya bölüm içeriği değişince geometriyi yeniden ölçün; okuma ve stil yazımını aynı karede karıştırmayın.
- `VisualViewport` yakınlaştırma ve ekran klavyesiyle layout viewport'tan bağımsız küçülebilir. `visualViewport.resize` görünür kontrol alanını yeniden değerlendirmek için kullanılabilir; bu yüksekliği doğrudan belge scroll mesafesi yapmayın. [MDN: VisualViewport](https://developer.mozilla.org/en-US/docs/Web/API/VisualViewport)
- Sahnenin `top` uzaklığını ve gerçek yüksekliğini hesaba katın; sticky öğe zorunlu olarak tam ekran değildir. `ResizeObserver`, içerik ve kapsayıcı boyutu değişimlerini izlemek için uygundur. [MDN: ResizeObserver](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver)
- Resize sonrasında eski kare numarasını saklamak yerine yeni ölçülerle mevcut scroll konumunu değerlendirin. Kullanıcıyı eski konuma zorla geri kaydırmayın.

## Hareket ve veri tercihleri

Reduced-motion açıkken poster veya sabit ana kareler gösterilir; scrub, parallax, otomatik oynatma ve uzun pin mesafesi kaldırılır. Tercih çalışma sırasında değişirse görünüm de güncellenir. HTML metin hiçbir durumda animasyonun bitmesini beklemez.

Veri tasarrufunda sequence ön yüklemesi başlamaz. `navigator.connection?.saveData` bulunmaması hızlı bağlantı anlamına gelmez. Mobil asset sınırları geçerli kalır. Tercih ve hata davranışları: [Mobile Media Strategy](../../v6/MOBILE_MEDIA_STRATEGY.md#tercih-ve-hata-durumları).

## Doğrulama

| Kontrol | Kabul edilen sonuç |
|---|---|
| 360px ve 390px genişlik, kısa yatay ekran | Yatay taşma yok; metin ve CTA normal kaydırmayla erişilebilir. |
| Hızlı ileri/geri kaydırma | İlerleme 0–1 aralığında; bozuk veya negatif kare seçimi yok. |
| Adres çubuğu açılıp kapanması, yön değişimi | Sahne ve bölüm sınırları güncel; kontroller kesilmez, boş alan oluşmaz. |
| Ekran klavyesi ve pinch zoom | Odaklanan alan görülebilir; yakınlaştırma ve doğal kaydırma çalışır. |
| Space, PageDown/PageUp, Home/End, Tab | Animasyon tuşları yutmaz; görünür odak belge sırasını izler. |
| Reduced-motion açık başlangıç ve sonradan değişim | Poster görünür; ek kare indirme durur; boş pin mesafesi kalmaz. |
| Save-Data açık, kapalı ve API yok | Tasarrufta poster; bilinmeyen bağlantıda mobil bütçe korunur. |
| JavaScript kapalı veya medya isteği başarısız | Metin, poster ve bağlantılar kullanılabilir. |
| Bölüme tekrar girme ve sayfadan ayrılma | Gereksiz çizim/indirme döngüsü veya biriken dinleyici yok. |

Tarayıcı emülasyonu yerleşim kanıtıdır; gerçek dokunma momentumu, adres çubuğu, ısınma ve decode performansı için fiziksel telefonda ayrıca ölçüm gerekir. Test raporu hangi kontrolün emülasyonda, hangisinin cihazda yapıldığını belirtir.
