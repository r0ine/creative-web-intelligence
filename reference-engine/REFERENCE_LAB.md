# Referans laboratuvarı: indir, ölç, düzenle, karşılaştır

Kullanıcı bir site adresini referans verdiğinde bu akış siteyi yerel çalışma alanına indirir, tasarım değerlerini ölçer, düzenlenecek satırları bulur ve yeni çalışmayı referansla aynı ekran ölçüsünde karşılaştırır. Brief ve ilk önizleme kararları için [brief → ilk referans](BRIEF_TO_REFERENCE.md), kullanıcı sonucu beğenmediğinde [revizyon akışı](REVISION_FEEDBACK.md) geçerlidir.

Her şey `reference-workspace/<alan-adı>/<zaman>/` altında toplanır ve git'e girmez.

## 1. İndir (wget)

```sh
python tools/v10/mirror_reference.py https://www.orneksite.com
```

Araç şu komutu çalıştırır: `wget --mirror --convert-links --adjust-extension --page-requisites --no-parent`, ek olarak `--level=2 --quota=200m --wait=1 --random-wait`. Derinlik, kota ve bekleme `--level`, `--quota-mb`, `--wait` ile değişir; `--level 0` sınırsızdır. Görsel ve fontlar başka bir alan adındaysa `--allow-domain cdn.orneksite.com` ekle. Site sana aitse `--own` kullan.

wget robots.txt kurallarına uyar; giriş, ödeme veya erişim engeli aşılmaz. Sonuç `capture.json` dosyasına yazılır: dosya türleri, toplam boyut, giriş sayfası, bulunan lisanslar ve kullanım kararı.

| Kullanım | Anlamı |
| --- | --- |
| `owned` | Site senin; kopya doğrudan düzenlenebilir. |
| `license-review` | Sitede lisans beyanı var; koşulları okuyunca kod düzenlenebilir. |
| `study-only` | Lisans yok; kopya yalnız inceleme ve ölçüm içindir. Yayınlanacak işte kod, görsel, metin ve font kullanılmaz; düzen ve davranış yeni kodla kurulur ([haklara uygun rekreasyon](../reference-recreation/RIGHTS_SAFE_RECREATION.md)). |

wget JavaScript çalıştırmaz. React/Next gibi sitelerde yalnız boş bir kabuk iner; araç bunu `jsShell` olarak işaretler. O durumda 2. adım zorunludur.

## 2. Canlı yakala (Playwright)

```sh
node tools/v10/capture_reference.mjs --workspace reference-workspace/www.orneksite.com/<zaman>
node tools/v10/capture_reference.mjs https://www.orneksite.com --out reference-workspace/canli
```

Site gerçek tarayıcıda masaüstü (1440×900) ve mobil (390×844) ölçüde açılır. `live/` klasörüne ekran görüntüleri, hareket azaltma görüntüsü ve `live.json` yazılır. Ölçülenler:

- ekranda en çok alan kaplayan renkler ve nötr/destek/vurgu alan oranı ([alan planı](../color/v3_2/WADA_WEB_ADAPTATION.md)),
- kullanılan fontlar, animasyonlar ve script adresleri,
- WCAG kontrast bulguları.

axe-core kuruluysa (`npm install axe-core`) erişilebilirlik ihlalleri de eklenir.

## 3. İncele

```sh
python tools/v10/analyze_reference.py reference-workspace/www.orneksite.com/<zaman>
```

Çalışma alanına `analysis.md`, `analysis.json` ve `tokens.css` yazılır. Raporda şunlar bulunur:

- **Tasarım ölçüleri:** zemin/metin/vurgu rolleri, palet, fontlar, tip ölçeği, boşluk, köşe, süre ve easing, kırılımlar, CSS değişkenleri.
- **Kütüphaneler:** GSAP, Three.js, Lenis, React/Next, Tailwind, Webflow, AOS ve benzerleri.
- **Sayfa yapısı:** başlık sırası, bölüm, görsel ve video sayıları.
- **Erişilebilirlik:** dil, alt metin, başlık sırası, boş bağlantı/buton, etiketsiz form alanı, yakınlaştırma engeli, kontrast.
- **Ağırlık:** en büyük dosyalar, eski görsel biçimleri, font dosyaları.
- **Kütüphane kurallarıyla çakışanlar:** referansın [kural önceliği](../v9/RULE_PRECEDENCE.md) ile çeliştiği yerler, örneğin Inter başlık fontu, aşmalı eğri, `transition: all`.

Kendi siteni yeni tasarıma taşıyorsan metinleri, başlıkları, proje ve profil bağlantılarını sayfa sırasıyla çıkar:

```sh
python tools/v10/extract_content.py reference-workspace/kendi-sitem.com/<zaman>
```

`content.md` ve `content.json` yazılır. `study-only` kaynakta araç metnin kopyalanmaması gerektiğini hatırlatır.

Tipografi seçerken Türkçe (veya hedef dil) glif kapsamını doğrula; aksi halde başlık ortasında yedek fonta düşülür:

```sh
python tools/v10/font_coverage.py "Bitstream Charter" --lang tr
python tools/v10/font_coverage.py --lang tr --role display
```

Ölçüler bir başlangıç noktasıdır, tasarım kararı değildir. Referansı aynen taşımak yerine Design DNA'yı kendi içeriğine göre kur.

## 4. Düzenle veya yeniden kur

Raporun **düzenleme haritası**, v9 görünürlük yüzeylerinin (arka plan, ilk ekran, renk, başlık tipografisi, boşluk, kartlar, menü, hareket…) CSS'te hangi dosyanın hangi satırında tanımlandığını gösterir. Kullanıcı “arka plan içime sinmedi” dediğinde önce bu satırlara bakılır.

- `owned` veya lisansı uygun kopya: `site/` klasörünü `edit/` olarak çoğalt, haritadaki satırlardan başlayarak düzenle, `python -m http.server -d <çalışma-alanı>/edit` ile önizle.
- `study-only`: Yeni projeyi kendi koduyla kur. `tokens.css` değerleri ölçüdür; renk ve ölçekleri kendi kararlarınla değiştir. Metin, görsel ve font için kendi veya lisanslı varlıkları kullan.

Lisansı bilinen açık kaynak bir başlangıç istersen:

```sh
python tools/v10/template_catalog.py --kind template --rights permissive --stack next
```

Katalog [v8 kaynak kaydını](../data/v8/source_registry.json) okur. İzin verici lisanslılar (MIT, Apache-2.0…) düzenlenebilir, copyleft olanlar aynı lisansla paylaşılır, lisansı doğrulanmamış olanlar yalnız incelenir. İndirdikten sonra kopyadaki LICENSE dosyasını oku.

## 5. Karşılaştır

```sh
node tools/v10/compare_reference.mjs reference-workspace/.../live/desktop.png http://localhost:3000 --out reference-workspace/karsilastirma/fark.png
node tools/v10/compare_reference.mjs referans.png yeni.png --viewport mobile --threshold 8
```

Girdiler PNG, yerel HTML veya adres olabilir; adresler aynı ekran ölçüsünde çekilir. Araç farklı piksel oranını, fark görüntüsünü ve en farklı bölgeleri (üst/orta/alt × sol/orta/sağ) verir. Üst sıra genelde menü ve ilk ekrandır. Önce büyük farkları düzelt: yapı → ölçek → hiza → yazı ölçüleri → kırpma → renk → mikro detay ([piksel yakınlığı](../reference-recreation/PIXEL_CLOSE_QA.md)). Zemin tonu gibi ince farklar için `--threshold 8` kullan.

## Kullanılan açık kaynak araçlar

| Araç | Lisans | Rolü |
| --- | --- | --- |
| GNU Wget | GPL-3.0 | Siteyi indirir; sistemden çağrılır, kütüphaneye paketlenmez. |
| Playwright + Chromium | Apache-2.0 / BSD | Canlı görünüm, ölçüm, ekran görüntüsü ve karşılaştırma. |
| axe-core | MPL-2.0 | İsteğe bağlı erişilebilirlik taraması. |

Python araçları yalnız standart kütüphaneyi kullanır (font kapsamı aracı fontconfig varsa canlı doğrular, yoksa veri tablosunu kullanır). Canlı yakalama ve karşılaştırma için `npm install playwright && npx playwright install chromium`; ayrıntılı erişilebilirlik için `npm install axe-core`.
