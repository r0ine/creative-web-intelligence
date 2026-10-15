# Scroll Technology Decision Matrix

| İhtiyaç | İlk seçim | Uygulama koşulu |
|---|---|---|
| Bölüm görünür olduğunda tek seferlik değişim | `IntersectionObserver` | JavaScript çalışmasa da içerik görünür kalır. |
| Scroll ilerlemesine bağlı basit CSS animasyonu | CSS scroll-driven animation | Özellik desteği kontrol edilir; statik görünüm başlangıç durumudur. |
| Sabit görsel yanında akan metin | CSS `position: sticky` | Sticky zorunlu değildir; mobilde normal akışa dönülebilir. |
| Birden çok eşzamanlı pin ve zaman çizelgesi | GSAP ScrollTrigger | Kurulum, resize ve temizleme tek yerde yönetilir. |
| Scroll ile kamera ilerlemesi | Three.js/R3F + 0–1 ilerleme | Sürekli değerler React render döngüsüne sokulmaz. |
| Video veya kare dizisi | Medya denetleyicisi + doğal scroll ilerlemesi | ScrollTrigger isteğe bağlıdır; seek/decode maliyeti ve poster yolu test edilir. |
| Bölüm bağlantısına yumuşak geçiş | CSS `scroll-behavior: smooth` | Reduced-motion durumunda `auto`; dokunma fiziğini değiştirmez. |
| Özel scroll fiziği | Gerekçeli Lenis kullanımı | Klavye, dokunma, odak ve geri dönüş davranışı ayrıca doğrulanır. |
| Dikey scroll ile yatay anlatı | CSS veya ScrollTrigger | Mobilde dikey bölümler; içerik sırf efekt için yataya zorlanmaz. |

## Seçim ölçütü

Önce doğal kaydırma ve normal belge akışını kurun. Gerekli anlatıyı ifade eden en küçük aracı seçin. Scroll'a bağlı bir animasyon, pin veya smooth-scroll bağımlılığı gerektirmez.

`scroll-behavior` bağlantı ve programatik kaydırmayı etkiler; tekerlek veya dokunma girdisine yeni fizik eklemez. [MDN: scroll-behavior](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scroll-behavior)

## Mobil kabul koşulları

- `wheel` veya `touchmove` için scroll'u durduran `preventDefault()` kullanmayın. Kullanıcı animasyonu tamamlamadan bölümden çıkabilir.
- Space, PageUp/PageDown, Home/End ve Tab doğal çalışır; odak sticky görselin arkasında kaybolmaz.
- Reduced-motion tercihinde scrub ve parallax durur; poster ile HTML içerik normal akışta görünür. Veri tasarrufunda ağır medya istekleri başlamaz.
- Resize ve içerik değişince başlangıç/bitiş ölçümleri güncellenir. Mobil tarayıcı çubuğunun her hareketi sayfa yüksekliğini yeniden yazdırmaz.
- Bölüm kaldırılırken dinleyiciler, observer'lar, planlanmış çizimler ve medya istekleri temizlenir.

Yerleşim ve gerçek cihaz kontrolü: [Mobile Scroll Recomposition](v3_1/MOBILE_SCROLL_RECOMPOSITION.md). Medya seçimi: [Mobile Media Strategy](../v6/MOBILE_MEDIA_STRATEGY.md).
