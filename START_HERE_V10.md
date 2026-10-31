# Creative Web Intelligence v10

v10, kullanıcının verdiği referans siteyi gerçekten indirip ölçen bir **referans laboratuvarı** ekler. v9 geri bildirim ve kural önceliği akışları ile v8 kaynak seçimi aynen geçerlidir ([v9 başlangıcı](START_HERE_V9.md)).

1. Kullanıcı bir site adresi verdiyse [referans laboratuvarı](reference-engine/REFERENCE_LAB.md) ile çalış: wget ile indir, JavaScript'li sitelerde Playwright ile canlı yakala, analiz raporunu oku.
2. `capture.json` içindeki kullanım kararına uy. `study-only` kopyadan kod, görsel, metin veya font yayınlanacak işe taşınmaz; düzen ve davranış yeni kodla kurulur. `owned` veya lisansı uygun kopya düzenlenebilir.
3. Tipografi seçerken Türkçe glif kapsamını `python tools/v10/font_coverage.py "<aile>" --lang tr` ile doğrula; eksikse araç çevrimdışı sistem-font yığını önerir. Analizdeki ölçüleri Design DNA'ya girdi olarak kullan. Referansın kütüphane kurallarıyla çakıştığı yerleri (Inter başlık fontu, aşmalı eğri, `transition: all` gibi) kendi projene taşıma.
4. Kullanıcı bir yüzeyi beğenmezse [revizyon akışını](reference-engine/REVISION_FEEDBACK.md) uygula; düzenleme haritası o yüzeyin dosya ve satırını gösterir.
5. Yeni çalışmayı referansla aynı ekran ölçüsünde karşılaştır; en büyük farktan başla.
6. Kütüphanede değişiklik yaptıysan `python tools/validate_all.py` çalıştır.

```sh
python tools/v10/mirror_reference.py https://www.orneksite.com
node tools/v10/capture_reference.mjs --workspace reference-workspace/www.orneksite.com/<zaman>
python tools/v10/analyze_reference.py reference-workspace/www.orneksite.com/<zaman>
node tools/v10/compare_reference.mjs reference-workspace/www.orneksite.com/<zaman>/live/desktop.png http://localhost:3000
python tools/v10/template_catalog.py --kind template --rights permissive
```

wget ve Python araçları ek paket istemez. Canlı yakalama ve karşılaştırma için Playwright ile Chromium kurulur:

```sh
npm install playwright && npx playwright install chromium
npm install axe-core   # isteğe bağlı: ayrıntılı erişilebilirlik taraması
```

Tarayıcı kurulamıyorsa bu adımları atla; statik analiz (`analyze_reference.py`) ile devam et ama görsel kapıyı "geçildi" sayma.

## Küçük bir site için asgari yol

Her şeyi okumana gerek yok. Küçük/tek sayfalık bir iş için: `SKILL.md` → bu dosya → `reference-engine/BRIEF_TO_REFERENCE.md` → `quality/V7_VISUAL_CALIBRATION.md` (zemin/metin/işaret, şekil, hareket) → teslimden önce `v5/CORE_DOCTRINE.md` özet testleri. Aynı alanda birden fazla director görürsen `v9/RULE_PRECEDENCE.md`.

`data/v9/visibility_ranking.json` **görsel yüzeyleri** (zemin, hero, renk, başlık...) önem sırasına koyar; bu içerik bölümü listesi değildir. Revizyonda "neresi?" için kullanılır, ama ilk inşada da kompozisyon kararlarını bu sırayla vermek iyi bir başlangıçtır: önce zemin ve hero, sonra renk oranı ve başlık tipografisi, en son mikro detay.
