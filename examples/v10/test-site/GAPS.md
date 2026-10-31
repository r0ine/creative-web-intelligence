# GAPS — r0ine test sitesini kütüphaneyle kurarken bulunanlar

Kapsam: `examples/v10/test-site/` (index.html, style.css, app.mjs, reference-note.md). Kütüphane, araç ve test dosyalarına dokunulmadı; araç hataları yalnız burada kayıtlı. Ağ engeli nedeniyle sebg.ch, r0ine.dev, majesteleri.net ve builtbybit.com hiç açılmadı. Bir tarayıcı olmadığı için sayfa **hiç render edilip görülmedi** (bkz. G-07).

Önem: **B** = bloklayanıcı/yanıltıcı, **O** = orta (çözümü bana kaldı), **K** = küçük.

## Araç hataları ve yanlış güvence

### G-01 (B) `analyze_reference.py` font sınıflaması `var()` arkasındaki fontu hiç görmüyor; CF-007 kontrolü fiilen atlanıyor
- Dosya: `tools/v10/analyze_reference.py` (satır 325-326, font-family regex'i; satır 448-450 CF-007 kontrolü).
- Bulgu: Siteme `--font-display` / `--font-body` ile font verdim. Çıktı: `Fontlar: bulunamadı`, `Erişilebilirlik (0 bulgu)`, kural çakışması bölümü boş.
- Kanıt: aynı siteyi geçici kopyada (`scratchpad/t1`, `t2`) yalnız `--font-display: "Inter"` yapınca hâlâ `bulunamadı`; `font-family: "Inter"` doğrudan yazılınca `CF-007` çıktı. Yani başlığa Inter vermek, kütüphanenin kendi önerdiği `--font-display` token'ı (`data/v9/visibility_ranking.json`, `display-type.cssHints`) üzerinden yapılırsa kural yakalanmıyor.
- Etki: Tam da kütüphanenin önerdiği yazım biçimi kontrolü atlatıyor. "Kütüphane kurallarıyla çakışanlar" bölümünün yokluğu "temiz" değil "görülmedi" anlamına gelebiliyor. Aynı kör nokta `--ref-font-display` üretimini (satır 511) de boş bırakır.
- Öneri: `var(--x)` çöz (custom property tablosu zaten toplanıyor), `Fontlar:` boşsa açıkça "çözülemedi" uyarısı ver.

### G-02 (O) Erişilebilirlik bölümü "0 bulgu" diyor ama hangi kontrolleri yaptığını söylemiyor; kontrast taraması dar
- `tools/v10/analyze_reference.py` yalnız şunları bakıyor (satır ~234-250, 431): `lang`, `img alt`, `h1` sayısı, bazı kontrast çiftleri. Odak göstergesi, `prefers-reduced-motion` varlığı, başlık sırası atlaması, form etiketi, skip link, dokunma hedefi **kontrol edilmiyor**; çıktı bunu belirtmiyor, "(0 bulgu)" yeterince iddialı okunuyor.
- Kontrast kör noktası: geçici kopyada `.note { color: #B5ADA0 }` (zemin `#F4EFE5` üzerinde ~1.9:1) **yakalanmadı**; aynı değer `.foot` içinde 1.68:1 olarak yakalandı. Araç yalnız bazı seçicileri/çiftleri çözüyor, hangilerini çözdüğü belgelenmemiş. Gerçek kontrastı elle hesaplamak zorunda kaldım (G-08).

### G-03 (O) Üç denetim aracı farklı şeyleri kapsıyor ve birbirini tamamlamıyor; hiçbiri diğerinin kapsamını söylemiyor
Aynı kötü CSS'e (geçici kopya `t2`: `transition: all`, `infinite` animasyon, `cubic-bezier(0.34,1.56,0.64,1)`):
- `tools/v7/audit_visual_defaults.mjs`: `transition-all` ve `infinite-motion` buldu; aşmalı eğriyi **bulmadı**.
- `tools/v10/analyze_reference.py`: `transition: all` ve aşmalı eğriyi (CF-008) buldu; `infinite` animasyonu çakışma olarak **bildirmedi**.
- `tools/v5/authenticity_check.py`: üçünü de geçirdi (`GATE: PASS`); `.mjs` dosyalarını taramıyor (`Files scanned: 2`: html+css). SKILL.md "v5 özgünlük kapısını çalıştır" diyor ama CF-007/CF-008 gibi kapılar bu araçta yok; PASS kelimesi "CF-008 yok" anlamına gelmiyor.
- `tools/v7/audit_visual_defaults.mjs` çıktısı sıfır bulguda yalnız `0 görsel kalıp incelemesi.` yazıyor. Belge (`quality/V7_VISUAL_CALIBRATION.md`) "sıfır bulgu kanıt sayılmaz" diyor ama araç hangi kalıpları baktığını listelemiyor; "temiz" ile "hiçbir şey denetlenmedi" ayırt edilemiyor.
- Eksik: tek bir `tools/check_site.py` veya her aracın "kapsadığım kurallar" çıktısı. Şimdi üç aracı elle çalıştırıp birleştirmek gerekiyor.

### G-04 (K) `analyze_reference.py` düzenleme haritası boş yüzeyler üretiyor
Haritada `spacing` → `style.css:27 body {margin: 0}` (bölüm boşlukları değil), `palette`, `surfaces`, `navigation`, `imagery`, `details` hiç yok; 11 yüzeyin 5'i listenlenmiş. Kullanıcı "menü kötü" derse `REVISION_FEEDBACK.md` bu haritaya yönlendiriyor ama burada karşılık yok. `tools/v10/analyze_reference.py` ayrıca `--no-write` dışında hedef klasöre dosya yazar; kendi sitemizi analiz ederken (kaynak klasör) bu çıktının nereye gideceği `START_HERE_V10.md`'de yok (referans çalışma alanı varsayılıyor). Bu yüzden `--no-write` kullandım.

## Eksik rehberlik

### G-05 (B) Font seçimi: araç, rehber ve görev metni birbiriyle ve gerçek makineyle çelişiyor
- `python tools/compose_spec.py "r0ine kişisel geliştirici sitesi minimal editorial"` → `font-093`, "luxury-editorial": **Cormorant Garamond + DM Sans**, bestFor "fashion, architecture, premium products". Kişisel geliştirici sitesi için alakasız; ikisi de web fontu, kurulu değil, yedek yığın (fallback stack) yok, `sourceStatus: SYNTHESIZED_FROM_TYPOGRAPHY_PRINCIPLES`. `designDNA` yalnızca `"CLI bootstrap only; agent should refine"`: palet, boşluk, ölçek yok.
- Görev metni "Fraunces, Bitstream Charter, Caladea mevcut" dedi. `fc-list`: **Fraunces yok**. **Bitstream Charter Türkçe glifleri içermiyor**: `fc-list ':family=Bitstream Charter:charset=130'` (İ), `11e` (Ğ), `11f` (ğ), `15e` (Ş), `15f` (ş) hepsi boş; yalnız ı (131) var. "İletişim", "Geliştirdiklerim" başlıkları ortasında yedek fonta düşerdi. Caladea, DejaVu Serif, Liberation Serif, Carlito tam kapsıyor. Sonunda `Cambria, Caladea, Georgia, "Liberation Serif", serif` yığınını seçtim.
- `directors/v3_2/TYPOGRAPHY_DIRECTOR.md` "Türkçe İ/ı/Ğ/ğ/Ş/ş kapsamını doğrula" diyor ama bunu yapacak araç/komut yok (`fc-list charset` hilesini kendim buldum); 20 alanlı "Output contract" için şablon yok. Kütüphane, "çevrimdışı/sistem fontu" için bir tablo (Charter→Cambria→Georgia gibi, glif kapsamıyla) sunmuyor.
- Öneri: `tools/` altına `font_coverage.py <aile> --lang tr` ve `data/` altına dil kapsamı işaretli sistem-font yığınları.

### G-06 (O) `data/v9/visibility_ranking.json` "yüzey sırası" olarak veriliyor ama geri bildirim aracı; ilk inşa için kullanım tanımsız
- `SKILL.md` ve `REVISION_FEEDBACK.md` onu *revizyon* için tanımlar ("Genel" cevabında). Görev bunu kompozisyonu yönlendirmek için kullanmamı istedi. Dosya ise **içerik bölümü** değil **görsel yüzey** sıralıyor (zemin, hero, renk, başlık, medya...). "Visibility order'daki bölümler: hero, ne yapıyorum, ..." ile bu liste farklı kavramlar; ikisi aynı sözcükle anılıyor. Ben yüzeyleri karar sırası olarak kullandım: önce zemin, sonra hero, sonra palet oranı, sonra başlık tipografisi, sonra boşluk. Bu yorum benim.
- Yüzeylerin `changes` alanı neyin değişebileceğini söylüyor ama hiçbir yüzey için "iyi başlangıç değeri" veya karar kuralı yok. Dosya revizyon sözlüğü; yeni inşa için karşılık gelen "ilk inşa kontrol listesi" yok.

### G-09 (O) `BRIEF_TO_REFERENCE.md` akışı tam tanımlı bir brief ve etkileşimsiz ortam için uyarlanmamış
- Akış `reference-preview.html` + ≤350 kelimelik `reference-note.md` ve "en fazla üç soru" bekliyor. Brief burada eksiksiz (içerik ve bölümler verilmiş) ve soru soracak kimse yok. İkisinden hangisini atlayabileceğim yazmıyor ("küçük düzeltmelerde atla" var, "tam tanımlı brief'te" yok). `reference-preview.html` üretmedim (tam site zaten tek sayfa); yalnız `reference-note.md` yazdım. Şablonu yok; alan listesinden kendim çıkardım.
- Kaynak sitesi erişilemezse `NEEDS_CAPTURE` yazılacağı söyleniyor (`BRIEF_TO_REFERENCE.md`) ama bunu yazacak araç/format yok: `NEEDS_CAPTURE` yalnız `schemas/*.json` ve `research/methodology.md` içinde geçiyor. `reference-note.md` içine metin olarak yazdım.
- `SKILL.md` Başlangıç 1: "site adresi verdiyse wget ile indir". Engelli ağda ne yapılacağı (kaynağı es geç, `NEEDS_CAPTURE`, tasarımı yine de kur) yazılı değil. Hızlı çıkış yolu `RIGHTS_SAFE_RECREATION` altında aranabilirdi; ben `NEEDS_CAPTURE` + "önerilen özgün yön" ifadesinden çıkardım.

### G-10 (O) Renk: üç rol zorunlu ama kaynak yoksa paleti üretecek/doğrulayacak araç yok
- `quality/V7_VISUAL_CALIBRATION.md`: zemin/metin/işaret, "kaynak yoksa nötr çalışma paleti seç ve geçici de". Nasıl nötr seçileceğine dair örnek yok; `v5/COLOR_RESTRAINT.md` "calm off-neutral" diyor ama hex yok. `color/accessibility_contrast.md` var, fakat kontrast hesaplayan bir komut yok; `#A33A1B` / `#F4EFE5` / `#E8DFCE` çiftlerini Python ile elle hesapladım (metin 15.3:1, ikincil 6.7:1, işaret 5.8:1 ve derin yüzeyde 5.0:1). `analyze_reference.py` paleti raporluyor ama eksik çiftleri tüketmiyor (G-02).
- "Tek işaret rengi sadece yönlendirdiği yerde" kuralı ölçülmüyor. Bağlantı alt çizgisi + hover + odak halkası olarak 3 kullanım yaptım; araç `#a33a1b (3)` sayısını palet özeti olarak veriyor ama "kaç yerde kullanıldı" sınırı yok.

### G-11 (O) Portfolyo/kredi bölümü için desen yok; bilinmeyen içerik için yer tutucu kuralı yok
- `SKILL.md` "uydurma müşteri, ödül, metrik yok" diyor ama "bilinmeyen içerik sayfada nasıl görünür" söylemiyor. `[doldurulacak]` işaretlerini görünür bıraktım ve `.todo` ile italik yaptım; bunun kütüphane-uyumlu olup olmadığı belli değil (`F-03` gibi bir kapı yok, ama yer tutucuların yayına gitmesini engelleyen bir denetim de yok). Tek kontrol `grep '\[doldurulacak'` olur; kütüphane bunu yapmıyor.
- İki kredi bölümü (tek öğeli "Geliştirdiklerim", iki öğeli "Birlikte geliştirdiklerim") için bölüm tipi/desen yok. `layout/` ve `directors/v5/COMPOSITION_DIRECTOR_V5.md` hero, grid ve kart odaklı; "tek bağlantıyı dev tipografi yap", "numaralı iş listesi" gibi kutusuz desenler yok. Üç içerik türünü üç ayrı biçime ben böldüm (düz yazı / dev bağlantı / numaralı liste / tanım listesi).
- "Developer by" / "Developed with me" İngilizce başlıkları Türkçeye çevrilirken anlam belirsiz kalıyor: "Birlikte geliştirdiklerim" kimlerle? `[birlikte çalışılan kişi veya ekip: doldurulacak]` ekledim. Kütüphanede çok dilli başlık/mikro metin rehberi yok (Türkçe UI metni için hiçbir `copy/` dizini yok).
- Dış bağlantı erişilebilirliği (yeni sekme mi, "harici site" ibaresi mi, `rel`) için kural yok. Yeni sekme açmadım, görünmez "(harici site)" metni ekledim; bu da benim kararım.

### G-12 (K) Kanıt kaynağı zayıf: "r0ine'in çalışması" yalnız Java paket adından çıkarılıyor
- `minecraft-webpanel/WebPanel-Tanitim.md` yazarı belirtmiyor; `WebPanel-Mimari.md` içinde `r0ine` yalnızca `com.r0ine.webpanel` paket yolunda geçiyor (satır 364-392, 613, 663). Yani "r0ine bu paneli geliştirdi" çıkarımı, belgeden değil paket adından. Görev bunu "adil" saydı; kütüphanede bunu `görüldü / çıkarıldı / önerildi` ayrımıyla (BRIEF_TO_REFERENCE bölüm 2) kaydedecek bir yer yok: bu ayrım kaynak sitesi bulguları için tanımlanmış, içerik kanıtı için değil. Sayfa metnini bilinçli olarak genel tuttum ("araçlar ve web panelleri geliştiriyorum", "örnek bir yön") ve sayıları/özellikleri taşımadım.

### G-07 (B) Tarayıcı yok: kütüphanenin zorunlu görsel kapıları çalıştırılamıyor ve alternatifi yok
- Playwright (Node ve Python) ve Chromium kurulu değil (`import('playwright')` → `ERR_MODULE_NOT_FOUND`; `which chromium firefox` boş). `tools/v10/capture_reference.mjs`, `compare_reference.mjs` atlandı. `SKILL.md` 7. adım ve `START_HERE_V8.md` 6. adım "gerçek tarayıcıda masaüstü ve mobilde aç" diyor; kuruluma dair `README.md`/`tools/README.md` içinde `playwright` geçmiyor. `START_HERE_V10.md` yalnız "Playwright ile Chromium gerekir" cümlesi içeriyor, `npm i`/`npx playwright install` komutu yok.
- Sonuç: yerleşimi (26vw dev başlık, 4/8 iki sütun, `overflow-wrap`) yalnız hesapla doğruladım (5 karakterli Cambria başlık ≈2.7em, 320px genişlikte 88px*2.7=237px < 280px); gerçek taşma, satır kırılımı ve glif render kontrolü yapılmadı. Statik analizle bu kapı geçilmiş sayılmamalı.

### G-13 (K) Okuma yükü ve sıra
- Başlamadan önce açmam gereken zincir: `SKILL.md` → `BRIEF_TO_REFERENCE` → `REVISION_FEEDBACK` → `START_HERE_V10` → `V9` → `V8` (SKILL ve V10 atıf yapıyor, görev listesi V8'i saymamış) → `RULE_PRECEDENCE` → `CORE_DOCTRINE` → `V7_VISUAL_CALIBRATION` → `TYPOGRAPHY_DIRECTOR` → `COLOR_RESTRAINT` → `DIVIDER_POLICY` → `V5_AUTHENTICITY_GATE` → `COMPOSITION_RESTRAINT`. 14 dosya, yinelenen içerik (özgünlük kuralları en az üç yerde). "Yeni küçük site için asgari yol" tek sayfa yok. `START_HERE_V10.md` tasarım kuralı içermiyor, yalnız araç komutları.

## Kural çelişkileri / belirsizlikler

### G-14 (K) CF-007 iki ayrı kuralı tek kimliğe sığdırıyor ve metni görevle birebir uyuşmuyor
- `v9/RULE_PRECEDENCE.md` CF-007: "Mono gövde yok; Inter / Space Grotesk ancak gerekçeyle." Görev "Inter/Space Grotesk varsayılan başlık fontu olmasın" dedi; `analyze_reference.py` mesajı "varsayılan başlık fontu olarak seçme". Üç ifade üç ayrı katılıkta. Sistemde Inter **kurulu** (`fc-list`) olması bile bir tuzak: kurulu olduğu için kolay seçilir, kural yalnız bir not.
- `quality/V5_AUTHENTICITY_GATE.md` E-01..E-03 / F-03 blocker listeleri ve `data/v5/authenticity_fingerprints.json` kimlikleri ile `authenticity_check.py` kapsamı bire bir eşleşmiyor (G-03).

### G-15 (K) "Her bölüm başlığında büyük etiket yok" ile "bölüm başlığı sol sütun" arasında kütüphane yönlendirmesi eksik
- `v5/COMPOSITION_RESTRAINT.md` asimetri öneriyor ama "başlık-solda iki sütun" kalıbının kendisinin (üç bölümde tekrarı) C-04 ("her bölüm aynı geometri") sayılıp sayılmayacağını söylemiyor. Hem `prose`, `with`, `contact` aynı 4/8 grid'i paylaşıyor; `made` ve `hero` farklı. Ölçülebilir eşik yok (yalnız C-01 için %60).
- `v5/DIVIDER_POLICY.md` öncelik listesi net ve işe yaradı: çizgi kullanmadım, ayrımı boşluk + tek yüzey değişimi ile yaptım. Bu bölümü olumlu not olarak kaydediyorum.

## Hareket

### G-16 (K) Hareket "görevi" şablonu var ama sıfır-hareket sitesi için yol yok
- `V7_VISUAL_CALIBRATION.md` her animasyon için tetik/durum/geri dönüş/reduced-motion ister; ben yalnız bağlantı renk geçişi bıraktım (`color`, `text-decoration-color`, 140 ms, `ease-out`) ve `prefers-reduced-motion: reduce` kolu ekledim. CF-005 "kısaltmak yetmez, kaldır" diyor; ben `transition: none` ile kaldırdım. `app.mjs` isteğe bağlıydı; tek görevi başlığa odak taşımak. Kütüphane "JS olmayan, hareketsiz bir site de geçerli" diye açıkça söylemiyor (SKILL.md 4. adım "güçlü tipografi ve statik kompozisyon geçerli birincil sonuçtur" der; bu işe yaradı, olumlu not).

## Son araç çıktıları (sitenin son hali)

| Araç | Sonuç |
| --- | --- |
| `python tools/v10/analyze_reference.py examples/v10/test-site --no-write` | 0 erişilebilirlik bulgusu, 0 çakışma; ama `Fontlar: bulunamadı` (G-01), kapsam dar (G-02). |
| `node tools/v7/audit_visual_defaults.mjs examples/v10/test-site` | `0 görsel kalıp incelemesi.` (G-03). |
| `python tools/v5/authenticity_check.py examples/v10/test-site` | `GATE: PASS`; yalnız html+css tarandı. Üç özet testi (dekorasyon kapalı, hareket kapalı, kimlik) araç tarafından yargılanmıyor, aracın kendi notu bunu söylüyor. |
| `node tools/v10/capture_reference.mjs ...` | Atlandı: Playwright yok (G-07). |

Elle yapılan özet testler: **Dekorasyon kapalı**: hiyerarşi tipografiyle taşınıyor (çizgi, gölge, gradyan yok). **Hareket kapalı**: etkilenen bir şey yok. **Kimlik**: ad ve bağlantılar değişirse yapı genel bir kişisel site iskeleti kalır; ayırt edici kişi bilgisi bilerek eksik (`[doldurulacak]`), bu eksik özgünlük değil kaynak kıtlığı.

## Bilinçli seçimler (araç ya da kural işaretlese de savunulur)
- İkincil metin rengi `#5B5246`: 6.7:1 (zemin), 5.8:1 (derin yüzey). Yer tutucular `italic` ve ikincil renkte; kontrast ≥ 4.5.
- İletişim bölümü ve alt bilgi `#E8DFCE` yüzeyinde: tek yüzey değişimi (`DIVIDER_POLICY` öncelik 4), çizgi yerine. Gerekçe: sayfanın son "kapanış" bölgesi.
- Bağlantılar her yerde altı çizili (işaret renginde): renk tek başına taşımasın diye.

## Düzeltmeler (bu değişiklikte giderildi)

Dogfooding sonrası kütüphaneye işlenen düzeltmeler:

- **G-01** (font `var()` kör noktası) → `analyze_reference.py` artık `var(--font-*)` değişkenlerini çözüp gerçek aileyi bulur; CF-007 atlanmıyor. (önceki commit)
- **G-02** (kontrast kör noktası) → kalıtımla gelen sayfa zemini üzerinde metin kontrastı artık denetleniyor ("sayfa zemini varsayıldı" etiketiyle).
- **G-02/G-03** (yanlış güvence) → `analyze_reference.py`, `audit_visual_defaults.mjs` ve `authenticity_check.py` artık çıktılarında neyi kapsadıklarını ve neyi kapsamadıklarını yazıyor; "0 bulgu/PASS" tek başına kanıt sayılmaz. Ek olarak `tools/v10/check_site.py` üç aracı tek komutla çalıştırıp birleşik rapor üretiyor; artık elle üçünü ayrı ayrı çalıştırıp sonuçları birleştirmek gerekmiyor.
- **G-05** (Türkçe glif kapsamı) → `tools/v10/font_coverage.py` + `data/v10/font_stacks.json` eklendi; `font_coverage.py "<aile>" --lang tr` kapsamı denetler (fontconfig varsa canlı) ve çevrimdışı sistem-font yığını önerir. TYPOGRAPHY_DIRECTOR ve compose_spec buna yönlendiriyor.
- **G-07** (tarayıcı kurulumu) → START_HERE_V10 ve REFERENCE_LAB'e `npm install playwright && npx playwright install chromium` ve "kurulamıyorsa görsel kapıyı geçildi sayma" notu eklendi.
- **G-09** (tam-tanımlı brief / ağsız kaynak) → BRIEF_TO_REFERENCE artık eksiksiz brief'te soru üretmemeyi ve erişilemeyen kaynakta `NEEDS_CAPTURE` yazıp tasarımı yine de kurmayı tarif ediyor.
- **G-06/G-13** (yüzey sırası ve asgari yol) → START_HERE_V10'a "küçük site için asgari okuma yolu" ve visibility_ranking'in görsel yüzey (içerik bölümü değil) sıralaması olduğu, ilk inşada da kullanılabileceği açıklaması eklendi.

Açık kalan, kullanıcı/tasarım kararı gerektirenler: G-04 (harita bazı yüzeylerde seyrek), G-10 (palet üretici yok), G-11 (kredi/yer-tutucu deseni), G-14/G-15 (ölçülebilir eşikler). Bunlar araç hatası değil, rehber derinliği.
