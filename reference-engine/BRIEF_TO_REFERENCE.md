# Brief'ten ilk referansa

Bu akış yeni bir kreatif siteye veya mevcut sitenin köklü bir görsel değişikliğine başlarken kullanılır. Amaç, kullanıcının kastettiği deneyimi erken görmek ve yanlış yönde tam sayfa üretmemektir. Her site için önce **bir** küçük referans hazırlanır; her bölüm veya her fikir için ayrı prototip üretilmez. Kullanıcı doğrudan küçük bir düzeltme istiyorsa bu aşamayı tekrar başlatma.

## 1. İsteği çöz

Brief'i üçe ayır: kullanıcının açıkça istediği sonuç, bağlamdan güçlü biçimde çıkan tercihler ve sonucu değiştirecek bilinmeyenler. Bir cümleyle ne anladığını söyle. “Modern”, “3D”, “aynısı” gibi sözcükleri tek başına tasarım kararı sayma; hangi sayfanın, hangi davranışın ve hangi ekranın kastedildiğini bağlamdan kontrol et.

Karar verdiren boşluklar için bir turda en fazla üç kısa soru sor. Önce şu tür belirsizlikleri çöz: referansın hangi yönü bire bir isteniyor, hangi içerik/varlıklar kullanılacak, mobilde ne korunacak, hangi etkileşim zorunlu? Sorulara mümkünse somut seçenek ekle. Cevabı beklerken mevcut proje ve sağlanan referansları incele; cevap gerektirmeyen işleri durdurma. Görsel yönü değiştirmeyen küçük ayrıntılarda varsayımı açıkça yazıp ilerle.

## 2. Kaynağı incele

Kullanıcı URL, ekran görüntüsü veya video verdiyse yalnız ilgili sayfa ve durumları derinlemesine incele. Görülebilen masaüstü ve mobil ölçülerini, bölüm sınırlarını, hizaları, boşlukları, yazı kırılmalarını, medya kırpmasını, navigasyonu, CTA yolunu, hover/dokunma/klavye tepkilerini, yükleme-hata-boş durumlarını ve hareket tetiklerini kaydet. Scroll veya 3D varsa başlangıç, orta ve son durumunu; nesne, kamera, ışık ve metin ilişkisini izle. Görmediğin bir mobil düzeni veya animasyon süresini uydurma.

Kaynak bir site adresiyse [referans laboratuvarı](REFERENCE_LAB.md) ile indir, canlı ölç ve analiz raporunu kanıt olarak kullan. Her bulguyu **görüldü**, **çıkarıldı** veya **önerildi** olarak ayır. Erişilemeyen kaynak için `NEEDS_CAPTURE` yaz ve yalnız eksik kanıtı sağlayacak soruyu sor. Font adı, CSS değeri veya kullanılan teknoloji ancak doğrudan doğrulanıyorsa kesin ifade edilir. İnceleme ayrıntılı olabilir; kullanıcıya verilecek ilk referans kısa kalır. Kaynak kullanım sınırları için [haklara uygun rekreasyon](../reference-recreation/RIGHTS_SAFE_RECREATION.md) geçerlidir.

## 3. Tek ekranlık referansı üret

Tam siteye geçmeden önce projeye özgü, çalıştırılabilir bir `reference-preview.html` hazırla. Bir ekranlık ana kompozisyon ve deneyimi tanımlayan **bir** etkileşim yeterli; alt sayfaları, tüm içerikleri veya geniş bileşen sistemini burada kurma. Masaüstü ile mobildeki temel yerleşimi göster. Gerekli medya henüz yoksa ölçü ve kırpmayı doğru tutan açıkça etiketli geçici görsel kullan; kaynağı görmüş gibi davranma.

Yanına en fazla yaklaşık 350 kelimelik `reference-note.md` koy:

- Kullanıcı isteğinin bir cümlelik yorumu ve sadakat modu: `inspired`, `structure-close`, `pixel-close` veya `behavior-close`.
- Kaynak, incelenen ekran ölçüleri ve güven durumu.
- Korunacak üç ayırt edici karar: örneğin kompozisyon, tipografi, medya veya hareket.
- Önizlemede çalışan etkileşim, mobil karşılığı ve bilinen boşluklar.
- Tam yapıya geçmeden önce cevap gerektiren en fazla üç soru; yoksa yapılan varsayımlar.

Kaynak verilmediyse referans, **önerilen özgün yön** olarak etiketlenir; hayalî bir dış siteye atfedilmez. Kullanıcı “bire bir” istiyorsa önce görünür kaynak durumlarını yeniden üret, sonra tam uygulamada aynı ekran ölçülerinde karşılaştır. İlk küçük prototipi “1:1 tamamlandı” diye sunma.

## 4. Tam uygulamaya geç

Önizlemeyi kullanıcıya göster ve kararı etkileyen tek bir tercih kaldıysa sor. Cevap beklemeyen kurulum veya ölçüm işlerine devam et. Kullanıcı açıkça tam uygulama istediyse ve yön belliyse ayrıca onay bekleme; aynı referans üzerinden ilerle. Brief kökten değişmedikçe ikinci bir başlangıç referansı üretme, mevcut olanı düzelt.

Sadakat isteniyorsa [rekreasyon motoru](../reference-recreation/REFERENCE_RECREATION_ENGINE.md) ve [piksel yakınlığı kontrolü](../reference-recreation/PIXEL_CLOSE_QA.md) ile aynı viewport ve etkileşim anlarını karşılaştır. Ekran görüntülerini [v7 karşılaştırma aracında](../examples/v7/reference-compare/index.html) üst üste koy; büyük farkları önce düzelt. Kaynakta görünmeyen işlevleri gerçek gözlem diye sunma. Tam eşleşme iddiasını yalnız ölçülen kapsam için kur.

## Bağlam bütçesi

Önce brief, bu akış ve ilgili tek referansı oku. Katalogları, bütün sürüm dosyalarını ve ilgisiz kaynak siteleri topluca yükleme. Gerekli tarifleri `rg` ile bulup yalnız seçilenleri aç. Uzun gözlem notlarını dosyada tut; sonraki turlarda kısa referans notunu ve değişen kararları taşı. Her yeni turda sıfırdan araştırma yapma.
