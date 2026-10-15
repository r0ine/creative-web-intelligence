# Kaydırmayla açılan 3D lamba

[Çalışan örnek](../../examples/v6/mobile-scroll/index.html) bir masa lambasının gövdesini, duyunu ve şapkasını ayırır. Kamera iç bağlantıya döner; parçalar birleşince ampul ve zemindeki ışık açılır. Sayfanın metinleri HTML içinde kalır.

Depo kökünden `python -m http.server 22222 --bind 127.0.0.1` çalıştırıp [yerel örneği](http://127.0.0.1:22222/examples/v6/mobile-scroll/) aç. Port doluysa mevcut uygulamayı durdurma. Tarayıcıya ayrıca paket kurmak gerekmez; Three.js dosyaları `runtime/vendor/three/` altında bulunur.

## Sahne API'si

```js
import { createLampScene } from './runtime/three/lamp-scene.mjs';

const lamp = createLampScene({
  canvas: document.querySelector('canvas'),
  onError: showStaticView,
});
lamp.resize(720, 720);
lamp.setProgress(0.45);
lamp.setFinish('forest');
lamp.setView(12);

function showStaticView() {
  lamp.destroy();
  document.querySelector('.poster').hidden = false;
}
```

`createLampScene` bir WebGL2 renderer kurar; destek yoksa hata fırlatabilir. Çağıran uygulama bu hatayı yakalayıp poster veya sekans göstermelidir. Render sırasında oluşan hatalar ve `webglcontextlost` ise `onError(error)` callback'ine gelir. [Demo bağlantısı](../../examples/v6/mobile-scroll/demo.mjs) her iki yolu ve geciken modül yüklemesini ele alır.

- `resize(width, height)`: CSS pikseli cinsinden pozitif boyutlar. İlk çizim için çağır. DPR üst sınırı 1,5; `compact: true` seçeneğinde 1'dir.
- `setProgress(progress)`: 0–1 arasında ilerleme; dışarıdaki sonlu değerler sınıra çekilir. Değişmeyen konum yeniden çizilmez.
- `setFinish('clay' | 'forest' | 'chalk')`: kil, orman veya tebeşir kaplama.
- `setView(degrees)`: kaydırma kamerasına −25° ile +25° arasında açı ekler.
- `stats`: ilerleme, renk, açı, render sayısı, draw call, üçgen, geometri, doku, çözünürlük ve yaşam döngüsü durumu.
- `destroy()`: geometri, malzeme, doku, gölge ve renderer kaynaklarını bırakır; tekrar çağrılabilir. Yeniden kullanım için yeni bir sahne oluştur.

Runtime zamanlayıcı veya scroll dinleyicisi kurmaz. Sayfa görünürlüğünü, boyut değişimini ve temizliği çağıran uygulama yönetir. Demo sekme arka plandayken render almaz; sayfadan ayrılırken sahneyi kapatır, geri gezinme cache'inden dönüşte yeniden kurar.

Gölge yalnız nesnenin siluetini taşıyan ana parçalarda hesaplanır. Küçük halkalar, vida ve düğmeler görünür kalır; ayrı gölge çizimi yapmaz. Tarayıcı ölçümünde sahne 29 çizim çağrısı ve gölge geçişleri dahil 28.046 üçgen kullanır; çizim çağrısı Rich katmanın 30 sınırına uyar. Gerçek GPU süresi ayrıca ölçülmelidir.

## Hareketin akışı

`sampleLampMotion(progress)` DOM ve Three.js gerektirmeyen bir fonksiyondur. 0–0,12 arasında nesne dinlenir. 0,12–0,38 parçalar ayrılır; 0,38–0,60 kamera 66° dönerek duy ve ampulü gösterir. 0,60–0,82 yeniden birleşme, 0,82–0,94 ışığın açılması ve kameranın dönüşüdür. Son bölüm sabittir. Geri kaydırma aynı yolu tersine izler.

Masaüstünde kullanıcı renk ve açı değiştirebildiği için gerçek zamanlı sahne kullanılır. 760 piksel ve altı ya da kaba işaretçili ekranlarda yalnız WebP sekansı yüklenir; mobilde açı kontrolü gösterilmez, renk seçimi korunur. Mobil ilerleme intro bittikten sonra başlar ve gerçek sticky sahne yüksekliğinden hesaplanır.

Hareket azaltma, veri tasarrufu, kullanıcı durdurması veya 480 pikselden kısa ekran statik düzene geçer. JavaScript kapalıyken de poster, üç açıklama ve bölüm görselleri görünür. Bu koşullarda Three.js ve animasyon kareleri istenmez. WebGL kaybında sekansa; sekans yükleme hatasında statik düzene geçilir. Bağlantı düzelince “Hareketi yeniden dene” düğmesi sekansı tek tıkla tekrar açar.

## Mobil kare üretimi

Yerel sunucu açık, Playwright, Chromium ve sharp kurulu olmalı:

```sh
node tools/v6/render_lamp_fallbacks.cjs http://127.0.0.1:22222/examples/v6/mobile-scroll/render.html
```

Betik 720 × 720 pikselde, DPR 1 ile gerçek sahneyi yakalar. Her renk için 48 WebP kare, bir poster ve üç bölüm görseli çıkarır. WebP kalitesi 82'dir. Toplam 156 dosya `examples/v6/mobile-scroll/frames-3d/` altına yazılır. `manifest.json` boyutları, dosya ve kaynak SHA256 değerlerini, Chromium sürümünü ve sahne istatistiklerini kaydeder. Boş görüntü, değişmeyen poz, farklı renk, tekrarlanabilir poz ve tarayıcı hata kontrolleri tamamlanmadan varlıklar değiştirilmez.

Renk başına yalnız hedef ve komşu kareler yüklenir. Cache bütçesi 8.000.000 bayttır; 720 × 720 RGBA kare 2.073.600 bayt tuttuğundan pratik üst sınır üç saklanan karedir. Geçici decode, canvas ve tarayıcı iç kopyaları bu hesaba dahil değildir.

Kare sayısı ve renkler [sequence-config.mjs](../../examples/v6/mobile-scroll/sequence-config.mjs) içindedir. Üretici, örnek ve tarayıcı kontrolü aynı kare sayısını kullanır. 48 kare, önceki 24 kareye göre kaydırma boyunca daha küçük poz adımları verir; cache ve eşzamanlı yükleme sınırları artmaz. Konfigürasyon değişince kareleri yeniden üret; manifest bu dosyanın hashini de kaydeder.

```sh
node --test tests/lamp-motion.test.mjs tests/scroll-progress.test.mjs tests/frame-sequence.test.mjs
node tools/v6/check_scroll_demo.cjs http://127.0.0.1:22222/examples/v6/mobile-scroll/
```

Playwright ve sharp başka bir ortamda kuruluysa `NODE_PATH` o ortamın `node_modules` klasörünü gösterebilir. Tarayıcı emülasyonundaki kontroller gerçek telefonda FPS, pil veya ısınma ölçümü yerine geçmez.
