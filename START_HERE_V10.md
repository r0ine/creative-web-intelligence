# Creative Web Intelligence v10

v10, kullanıcının verdiği referans siteyi gerçekten indirip ölçen bir **referans laboratuvarı** ekler. v9 geri bildirim ve kural önceliği akışları ile v8 kaynak seçimi aynen geçerlidir ([v9 başlangıcı](START_HERE_V9.md)).

1. Kullanıcı bir site adresi verdiyse [referans laboratuvarı](reference-engine/REFERENCE_LAB.md) ile çalış: wget ile indir, JavaScript'li sitelerde Playwright ile canlı yakala, analiz raporunu oku.
2. `capture.json` içindeki kullanım kararına uy. `study-only` kopyadan kod, görsel, metin veya font yayınlanacak işe taşınmaz; düzen ve davranış yeni kodla kurulur. `owned` veya lisansı uygun kopya düzenlenebilir.
3. Analizdeki ölçüleri Design DNA'ya girdi olarak kullan. Referansın kütüphane kurallarıyla çakıştığı yerleri (Inter başlık fontu, aşmalı eğri, `transition: all` gibi) kendi projene taşıma.
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

wget ve Python araçları ek paket istemez. Canlı yakalama ve karşılaştırma için Playwright ile Chromium, ayrıntılı erişilebilirlik taraması için isteğe bağlı axe-core gerekir.
