# v7 görsel kalibrasyon

Bir ekranın “AI işi” görünmesi tek bir renkten veya köşe yarıçapından çıkmaz. Sorun, neden seçildiği belli olmayan kararların aynı sayfada yığılmasıdır: koyu zemin, parlak vurgu, eş kutular ve her öğeye aynı hareket. Bu kontrol, yeni siteye başlamadan ve teslimden önce uygulanır.

## Renk kararını kaydet

Üç rolü birer cümleyle tanımla: **zemin**, **metin**, **işaret**. Her rolün kaynağı marka, ürün malzemesi, kullanıcı referansı veya içerik fotoğrafı olmalı. Kaynak yoksa nötr bir çalışma paleti seçip bunu geçici diye adlandır. “Kreatif görünür” tek başına gerekçe değildir.

İşaret rengini başlık, buton, çizgi ve arka planın hepsinde aynı anda kullanma. Önce gri ölçekte hiyerarşiyi kontrol et; vurgu yalnız yönlendirdiği yerlerde kalsın. Okunabilirliği gerçek yüzeylerde denetle. Koyu arayüz, ancak içerik veya kullanım koşulu istiyorsa seçilir; koyu zemin + ince çizgiler + parlak renk hazır stil olarak kullanılmaz.

## Şekil dilini içerikten çıkar

Sayfada tek bir **kutu şablonu** dolaştırma. Görsel, alıntı, kontrol ve açıklama aynı dolgu, çizgi ve köşe ile sunulmamalı. Bir öğe bir şeyi seçtiriyor veya içerik sınırını gerçekten tarif ediyorsa yüzeye ihtiyaç duyabilir; yalnızca “tamamlanmış” görünsün diye çerçeve ekleme.

Köşe ailesini referanstaki veya ürünün fiziksel biçimindeki geometriye bağla. Köşelerin hepsinin sıfır olması da hepsinin kapsül olması da otomatik karar olmamalı. Kullanıcı daha yumuşak bir dil istiyorsa önce etkileşim yüzeylerinin ve medyanın köşelerini uyumlu hale getir; metin bölümlerini kartlara dönüştürme.

## Hareketin görevini yaz

Her animasyon için dört bilgi yeterlidir: **tetik**, **hangi durumdan hangi duruma geçtiği**, **geri dönüşü**, **hareket azaltma karşılığı**. Bunlar yazılamıyorsa animasyonu kaldır. Scroll hareketi bölüm veya nesne hakkında yeni bilgi göstermeli. Sabit bir nesnenin sürekli dönmesi, tüm bölümlerin aynı biçimde yükselmesi, bulanıklıkla giriş ve her öğeye aynı easing yasaktır. Uzun sayfalarda hareketsiz okuma aralıkları bırak.

Kullanıcı etkileşimindeki kısa durum geri bildirimi ile 3D nesnenin ağırlık hissi aynı süre ve eğriyi kullanmaz. Mobilde animasyon yerine poster veya statik kompozisyon gerektiğinde anlam kaybolmamalı.

## Denetim

```sh
node tools/v7/audit_visual_defaults.mjs examples/v7/reference-compare
```

Araç CSS ve HTML içindeki tekrar eden kutu yüzeylerini, koyu çizgi yoğunluğunu, genel `transition: all` kullanımını, sonsuz animasyonu ve tekrar eden fade-up kalıbını işaretler. Bulgu, tasarım kararını yeniden inceleme çağrısıdır; dosyayı körlemesine değiştirmenin komutu değildir. **Sıfır bulgu kaliteli tasarım kanıtı sayılmaz.** Önizlemeyi masaüstü ve mobilde görerek şu son kontrolü yap:

1. Renk ve hareket kapatıldığında tipografi ve yerleşim hâlâ anlaşılır mı?
2. Üç farklı içerik türü üç ayrı görevle mi biçimlenmiş, yoksa aynı karta mı dökülmüş?
3. Animasyon kapalıyken bilgi ve etkileşim yolu tam mı?
4. Referans verilmişse renk, şekil ve hareket kararlarının hangisi gerçekten kaynaktan görüldü?

Bu kapı [v5 özgünlük](V5_AUTHENTICITY_GATE.md) ve [v6 sinematik](V6_CINEMATIC_GATES.md) denetimlerinin yerini almaz; onların uygulanabilir kararlarını ilk prototipe taşır.
