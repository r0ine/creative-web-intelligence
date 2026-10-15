# Mobil ve masaüstü scroll örneği

İki bağımsız ES modülü var: `scroll-progress.mjs` doğal kaydırmadan ilerleme üretir; `frame-sequence.mjs` bu ilerlemeye karşılık gelen kareyi yükleyip canvas'a çizer. GSAP, Lenis veya başka bir çalışma zamanı bağımlılığı gerekmez.

Çalışan örnek [examples/v6/mobile-scroll](../../examples/v6/mobile-scroll/index.html) altında. Depo kökünden bir yerel sunucu başlat:

```sh
python -m http.server 22222 --bind 127.0.0.1
```

Ardından [örneği aç](http://127.0.0.1:22222/examples/v6/mobile-scroll/). Port başka bir uygulamaya aitse onu kapatma; boş bir port seç. ES modülleri nedeniyle sayfayı `file://` üzerinden açma.

## Örnekteki davranış

- Masaüstü: [gerçek 3D sahne](../three/README.md), renk ve bakış açısı kontrolü; WebGL kullanılamazsa 48 karelik sekans.
- Mobil/dokunmatik: aynı 3D sahneden 48 WebP kare, 720 × 720 piksel, en fazla 4 kare ve 8.000.000 bayt cache sınırı; daha kısa sticky sahne. Three.js yüklenmez.
- Hareket azaltma, veri tasarrufu veya 480 pikselden kısa ekran: animasyon kareleri yüklenmez; poster ve üç statik açıklama gösterilir.
- Durdurma düğmesi aynı statik düzene geçer. Sistem tercihini bu düğmeyle geçersiz kılmak mümkün değildir.
- Kaydırma ileri ve geri çalışır. Fare tekerleği, dokunma ve klavye olayları engellenmez. “Animasyonu atla” bağlantısı doğrudan sonraki bölüme gider.
- Sahnedeki zaman çizgisi dokunma ve klavyeyle hedef konuma götürür; sürükleme doğal sayfa konumunu günceller. Hareket kapalıyken çizgi gösterilmez.
- Sayfa arka plana geçince bekleyen kareler iptal edilir, cache bırakılır. Geri dönünce mevcut konumdan devam edilir. 3D sahne yalnız scroll, boyut veya kontrol değiştiğinde render alır.

Üç yüzey rengi için mobil kareler ve sabit görseller [3D üretim betiğiyle](../../tools/v6/render_lamp_fallbacks.cjs) hazırlanır. İlk 2D sürümün SVG kaynakları da `frames/` altında korunmuştur; yeniden üretme komutu:

```sh
node examples/v6/mobile-scroll/create-frames.mjs
```

## İlerleme modülü

`scrollProgress(sectionTop, sectionHeight, stageHeight, offset = 0)` sıfır ile bir arasında ilerleme döndürür. Bölüm ve gerçek sahne yüksekliği kullanılır; dört viewport `400vh` demektir. Hareket mesafesi `sectionHeight - stageHeight` olarak hesaplanır.

`observeScrollProgress({ section, stage, onProgress })` DOM elemanlarını izler. Callback `{ progress, visible }` alır. Scroll ve boyut değişiklikleri aynı bekleyen animasyon karesinde birleştirilir; boşta sürekli döngü çalışmaz. Dönüş nesnesindeki `refresh()` yeniden ölçüm ister, `destroy()` dinleyicileri ve observer'ı kaldırır. Sticky düzen kurmak bu fonksiyonun işi değildir; örnekte CSS kullanılır.

`selectScrollMode({ width, height, reducedMotion, saveData, paused, coarsePointer })`, örneğin `desktop`, `compact` veya `poster` kararını döndürür. Bu eşikler örnek için seçilmiştir. `saveData` API'si yoksa kullanıcı tercihi biliniyor sayılmaz. Reduced-motion ve bağlantı tercihlerinin canlı değişimini bağlamak çağıran uygulamanın sorumluluğundadır; tamamlanmış bağlantılar [demo.mjs](../../examples/v6/mobile-scroll/demo.mjs) içinde görülebilir.

## Kare oynatıcısı

`createFrameSequence({ canvas, urls, maxFrames, maxDecodedBytes, preload, concurrency, onFrame, onError })` bir oynatıcı döndürür. `urls` sıralı kare adresleridir. Varsayılan sınırlar 6 kare, 24.000.000 bayt cache, 2 komşu adımı ve 2 eşzamanlı yüklemedir.

- `seek(progress)` hedef kareyi öncelikli yükler. Çizim gerçekleşirse `true`, istek eski kaldıysa veya başarısızsa `false` ile tamamlanan Promise döndürür.
- `clear()` bekleyen istekleri iptal eder ve cache'i bırakır. Son çizilmiş canvas'ı silmez.
- `destroy()` aynı temizliği yapıp oynatıcıyı kapatır. Yeniden çağrılabilir.
- `stats`: `cachedFrames`, `decodedBytes`, `pending`, `requests`, `displayedFrame` değerleri anlık olarak okunabilir. Kare indeksi sıfırdan başlar; henüz çizim yoksa `null` olur.
- `onFrame({ index, progress, width, height })` başarılı çizimden sonra çalışır.
- `onError(error, { index, url })` yükleme veya çizim hatasını bildirir. Poster, açıklamalar ve hata durumunun sayfada gösterilmesi çağıran uygulamaya aittir.

Bellek hesabı `width × height × 4` üzerinden cache tahminidir. Canvas yüzeyi, geçici decode ve tarayıcının iç kopyaları bu sınıra dahil değildir. Tek kare bütçeden büyükse çizilir fakat cache'e alınmaz; büyük kaynak boyutlarını hazırlama aşamasında azalt. `loadFrame(url, { signal })` seçeneğiyle özel yükleyici verilebilir; `{ width, height, image, close() }` döndürmeli ve iptal sinyaline uymalıdır. Sinyali yok sayan yükleyici bitene kadar eşzamanlı istek yuvasını tutar.

Varsayılan yükleyici HTTP hatalarını yakalar, ImageBitmap kullanabildiğinde kullanır; SVG ve desteklenmeyen decode için Image yoluna geçer. Uzak kareler için sunucunun CORS izni gerekir. Saydam kareler önceki çizimin yerini alır; örnekte canvas zemini posterin arkadan görünmesini de önler.

## Kontroller

Node 22 veya üzeriyle bağımlılıksız birim testleri:

```sh
node --test tests/scroll-progress.test.mjs tests/frame-sequence.test.mjs
```

Playwright, Chromium ve piksel karşılaştırması için sharp kurulu bir geliştirme ortamında, yerel sunucu açıkken:

```sh
node tools/v6/check_scroll_demo.cjs http://127.0.0.1:22222/examples/v6/mobile-scroll/
```

Playwright farklı bir yerde kuruluysa `NODE_PATH` o ortamın `node_modules` klasörünü gösterebilir. `CWI_SCREENSHOT_DIR` verilirse ekran görüntüleri oraya yazılır; verilmezse test dosya üretmez. Gerçek telefondaki adres çubuğu, ekran klavyesi, ısınma ve kare süreleri ayrıca ölçülmelidir; tarayıcı emülasyonu bu sonuçları kanıtlamaz.
