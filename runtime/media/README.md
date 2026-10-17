# Kaynak seçimi ve video akışı

[Medya atölyesi](../../examples/v6/media-studio/index.html), kaynak filtreleme, video promptu ve yerel medya önizlemesini bir araya getirir. Depoyu HTTP üzerinden aç; `file://` modül yükleme için uygun değildir. Yerel video ve kareler sunucuya yüklenmez; tarayıcı yalnızca seçilen dosyalar için `blob:` adresleri oluşturur.

Video akışı isteğe bağlıdır. Sadece 3D veya scroll istendiğinde ChatGPT/Claude video promptu hazırlanmaz. Atölyede prompt, kullanıcı `Video promptunu hazırla` düğmesine bastığında üretilir. Herhangi bir ChatGPT, Claude veya video API bağlantısı bulunmaz; giriş ve API anahtarı gerekmez. Üretilen metin istenen araca elle yapıştırılır.

CLI ajanı için [v8 deneyim planı](../../v8/OPTIONAL_VIDEO_POINTER_WORKFLOW.md) videoyu açık tercihle ayırır. `node tools/v8/experience_plan.mjs examples/v8/experience-brief.json` komutu videosuz tamamlanacak site temelini ve fare bakışını tarif eder; video promptu üretmez. Video istenirse ikinci örnekteki gibi `video.requested: true` ve sahne brief'i verilir. Eksik bilgiler soru olarak döner, temel site bekletilmez.

## Bileşen ve şablon seçimi

[Kaynak kataloğunda](../../data/v6/creative_sources.json) React Bits, 21st.dev, Magic UI, UI Layouts, Kokonut UI, shadcn/ui ve yerel runtime yer alır. Bu, sağlayıcı rehberidir; sitelerin uzak bileşen kataloglarının kopyası değildir. İhtiyaç ve framework eşleşmesini şu komutlarla seçebilirsin:

```sh
node tools/v6/creative_media.mjs sources hero react project
node tools/v6/creative_media.mjs sources template react project
node tools/v6/creative_media.mjs sources scroll vanilla project
node tools/v6/creative_media.mjs sources background react library
```

`project`, tek bir web projesinde kullanımı; `library`, başka projelere dağıtılacak kaynak paketini ifade eder. `library` filtresi yeniden dağıtımı kısıtlı veya bileşen lisansı henüz bilinmeyen sağlayıcıları çıkarır. Bir sağlayıcının MIT deposu olması premium şablonlarına aynı hakları vermez. Seçilen dosyanın lisansını, bağımlılıklarını ve hedef framework uyumunu yeniden doğrula.

[React Bits entegrasyonu](../../source-intelligence/REACT_BITS_INTEGRATION.md), resmi bileşen kurulumunu hedef uygulamada kullanır. React Bits kodu bu kütüphaneye gömülmez. 21st.dev için resmi Copy prompt akışı veya kullanıcının erişimiyle aldığı kaynak kullanılır; otomatik scraping yapılmaz. [Kaynak kabul rehberi](../../source-intelligence/CREATIVE_COMPONENT_WORKFLOW.md), kayıt alanlarını ve uyarlama sırasını açıklar.

## ChatGPT’ye verilecek video brief’i

```sh
node tools/v6/creative_media.mjs prompt examples/v6/video-brief.json
node tools/v6/creative_media.mjs prompt examples/v6/video-brief.json lamp-video-prompt.md
```

İkinci komut yeni bir Markdown dosyası yazar; var olan dosyanın üzerine yazmaz. Atölyede de nesne, malzeme, ışık, palet, amaç, süre ve kare sayısını değiştirip aynı üreticiyi kullanabilirsin. `Brief’i indir` düğmesi CLI ile uyumlu JSON verir.
Lamba örneği için [hazır ChatGPT promptu](../../examples/v6/lamp-video-prompt.md) da depoda bulunur.

`buildVideoPrompts(brief)` üç metin üretir: `desktop`, `mobile` ve ChatGPT’ye yapıştırılacak `chatgpt`. Bir model, API anahtarı veya video üretim servisi çağırmaz. Video üretimi ilgili oturumda yoksa son prompt ve storyboard istenir. Süre ve oran, üretim aracının kendi kontrollerinde de ayarlanmalı; metindeki değerler teknik ayarları garanti etmez.

- `mode: "background"`: sabit nesne/kamera, yavaş ışık hareketi, ilk ve son karenin eşleşmesi.
- `mode: "scroll"`: parçalanma, iç bağlantıyı gösterme ve birleşme; ileri ve geri scrubbing için tek kesintisiz çekim.
- `beats`: isteğe bağlı `[başlangıç, bitiş, eylem]` dizileri. 0–1 aralığını boşluksuz kapsamalı. Örnek: `[[0, 0.5, "Reveal the fold."], [0.5, 1, "Unfold the fabric."]]`.

Varsayılan scroll storyboard’u parçalardan oluşan ürünler içindir. Kumaş, mimari veya soyut bir sahne için kendi `beats` dizini ver. Mobil prompt yatay filmi kırpmak yerine ayrı portre kompozisyonu ister. Renk ve ışık değişirse iki promptu da yeniden üret.

Prompt yapısı için [OpenAI’nin video prompt rehberi](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide) referans alındı. Bu belge arşivlenmiş olarak işaretlidir; buradaki akış model adı, API parametreleri veya hesap erişimi varsaymaz.

## Videoyu karelere bölme

Python 3.11+ ve WebP/H.264 kodlayıcıları içeren FFmpeg gerekir. Node araçları için Node 18+ yeterlidir. FFmpeg PATH’teyse:

```sh
python tools/v6/video_to_web.py film.mp4 public/media/lamp-mobile --frames 48 --width 720
python tools/v6/video_to_web.py film.mp4 public/media/lamp-desktop --frames 96 --width 1280 --budget-kb 4000
```

`film.mp4`, üretim aracından aldığın yerel video dosyasıdır. FFmpeg PATH’te değilse `--ffmpeg` parametresine çalıştırılabilir dosyanın tam yolunu ver. `--start 2 --duration 8` ile 2. saniyeden başlayan 8 saniyelik bölüm seçilir. Bölüm en fazla 20 saniye olabilir. `--width`, portre dahil uzun kenarın üst sınırıdır; görüntü büyütülmez. `--quality` WebP kalitesini belirler, varsayılanı 76’dır.

Çıktı klasöründe `manifest.json`, `poster.webp`, `background.mp4` ve sıralı `frames/frame-000.webp` dosyaları oluşur. Sessiz MP4, H.264/yuv420p ve `faststart` ile hazırlanır. Karelerin toplamı varsayılan 1500 KB sınırını aşarsa araç çıktıyı yayımlamaz. Mevcut klasörlerin üzerine yazmaz; başarısız işlem hedefte yarım dosya bırakmaz.

Kareler, bölüm süresine eşit aralıklarla örneklenir. Son kare tam bitiş anından bir örnekleme aralığı öncedir; boş bitiş karesi oluşturulmaz. `manifest.frames` sırası oynatım sırasıdır. SHA-256 değerleri kaynak ve dosya takibi içindir; telif veya görsel doğruluk kanıtı değildir. Üretim aracı watermark veya provenance verisi gömüyorsa bunları kaldırma.

Arka plan MP4’ünün oluşması filmin döngüye uygun olduğunu göstermez. Manifest’te `temporalArtifacts`, `mobileComposition` ve `loopContinuity` incelemeleri `pending` başlar. Filmde eriyen yüzey, titreyen parça, yanlış birleşme veya döngü sıçraması varsa promptu düzeltip yeniden üret. Raster video, kullanıcının serbestçe döndürebileceği bir 3D model sağlamaz; nesne inceleme ve konfigürasyon için gerçek Three.js/GLB kullan.

## Web’de kullanma

Arka plan:

```js
import { createBackgroundVideo } from './runtime/media/background-video.mjs';

const background = createBackgroundVideo({
  video: document.querySelector('video'),
  src: '/media/lamp/background.mp4',
  poster: '/media/lamp/poster.webp',
});

document.querySelector('#pause-video').addEventListener('click', () => background.setPaused(true));
```

Video `muted`, `loop`, `playsInline` ile oynar. Ekran dışındayken veya sekme gizliyken durur. `prefers-reduced-motion`, Save-Data, kullanıcı durdurması ve oynatma hatasında poster kalır. Canlı tercih değişiklikleri izlenir. Durdurma düğmesini HTML’de görünür tut; sayfa kapatılırken veya React effect cleanup içinde `background.destroy()` çağır. Poster URL’si zorunludur. Bu modül videoya dışarıdan `autoplay` veya `src` atanmasını beklemez; kaynağı kendisi yönetir.

Scroll:

```js
import { createFrameSequence } from './runtime/scroll/frame-sequence.mjs';
import { observeScrollProgress } from './runtime/scroll/scroll-progress.mjs';

const response = await fetch('/media/lamp-mobile/manifest.json');
if (!response.ok) throw new Error('Medya manifesti yüklenemedi.');
const manifest = await response.json();
const player = createFrameSequence({
  canvas: document.querySelector('canvas'),
  urls: manifest.frames.map(frame => `/media/lamp-mobile/${frame.file}`),
  maxFrames: 5,
  maxDecodedBytes: 20_000_000,
});
const scroll = observeScrollProgress({
  section: document.querySelector('.story'),
  stage: document.querySelector('.stage'),
  onProgress: ({ progress, visible }) => { if (visible) void player.seek(progress); },
});
```

Bu kısa bağlantı örneğine hareket tercihi, poster ve durdurma davranışını [atölyedeki çalışan koddan](../../examples/v6/media-studio/studio.mjs) ekle. `createFrameSequence` bunları kendiliğinden seçmez. Cleanup sırasında `scroll.destroy()` ve `player.destroy()` çağır. Canvas dekoratifse `aria-hidden="true"` kullan; anlatım metni ve kontroller HTML’de kalır.

Atölye, dönüştürülen klasörü `Kare klasörünü seç` ile açar. Eksik kare, yinelenen yol, değişmiş dosya boyutu ve dış URL içeren manifest reddedilir. Sekansın bellekte çözülmüş en fazla beş karesi tutulur. Atölye aktarım bütünlüğü için SHA-256 doğrulaması yapmaz; manifest ile dosya boyutlarını eşleştirir. Gerçek yayın için video/kareleri sitenin asset klasörüne yerleştir.

## Doğrulama

```sh
node --test tests/creative-media.test.mjs
python -m unittest discover -s tests -p test_video_to_web.py -v
```

Gerçek kodlama testleri için `CWI_TEST_FFMPEG` ortam değişkenini FFmpeg dosyasının tam yoluna ayarla. Ayarlı değilse yalnızca bağımsız giriş/hata testleri çalışır. Tarayıcı kontrolü `tools/v6/check_media_studio.cjs`, kaynak filtrelerini, yerel video yüklemeyi, kare importunu, ileri/geri kaydırmayı ve mobil/statik davranışı sınar. Playwright paketi ve onun Chromium tarayıcısı gerekir. Çalışan HTTP sunucusu, geçerli yerel video ve dönüştürülmüş klasör ile:

```sh
node tools/v6/check_media_studio.cjs http://127.0.0.1:22222/examples/v6/media-studio/ film.mp4 public/media/lamp-mobile
```

FFmpeg seçenekleri ve örnekleme filtresi: [resmi komut rehberi](https://ffmpeg.org/ffmpeg.html), [fps ve scale filtreleri](https://ffmpeg.org/ffmpeg-filters.html).
