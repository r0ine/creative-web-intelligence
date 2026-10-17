# İsteğe bağlı video ve fare bakışı

Bu akış CLI ajanları içindir. Kullanıcı video istemediyse video promptu üretme, video dosyası bekleme veya siteyi eksik bırakma. Önce içerik, tipografi, gezinme, mobil düzen, görsel temel ve erişilebilir etkileşimleri tamamla. Sahnenin anlamı HTML içinde okunabilmeli; poster ve hareket azaltma durumu da çalışan sonucun parçasıdır.

## Karar sırası

1. Brief ve tek kısa referans prototipiyle sayfanın fikrini doğrula.
2. `video.requested` değerini yalnız kullanıcının açık tercihine göre belirle. Belirsizse video kapalı kalsın; karar sonucu değiştiriyorsa kısa bir soru sor.
3. Fare etkileşiminde hangi şeyin değişeceğini belirle. Kamera/bakış varsayılan örnektir; nesneyi döndürme veya yalnız katman hareketi farklı uygulamalardır.
4. Temel siteyi videosuz bitir. Canlı 3D sahne kullanılıyorsa scroll ana pozu, fare yalnız küçük ofseti yönetir. İki animasyon motoru aynı kamera dönüşümünü yazmaz.
5. Video istenirse sahne, amaç, malzeme, ışık ve palet bilgilerini topla. Bunlar tamamlanınca promptu üret; videonun gerçekten üretildiğini veya hesaba erişim olduğunu varsayma.
6. Kullanıcı video dosyasını sağladığında süreklilik ve kompozisyonu incele. Arka plan için poster + sessiz döngü; scroll için kare sekansı kullan. Hatalı veya tutarsız videoyu siteye zorla bağlama.

```sh
node tools/v8/experience_plan.mjs examples/v8/experience-brief.json
node tools/v8/experience_plan.mjs examples/v8/experience-brief-with-video.json
node tools/v8/experience_plan.mjs examples/v8/experience-brief.json plan.json json
```

İlk örnekte video promptu üretilmez. İkinci örnek, yalnız açık istek olduğu için ChatGPT'ye veya başka bir video aracına elle verilecek promptu çıkarır. Çıktı dosyası verilirse var olan dosyanın üzerine yazılmaz. Plan üretimi video servisi çağırmaz. Eksik video brief'i temel siteyi durdurmaz; yalnız sonucu belirleyen soruları listeler.

## Fare ve scroll sınırı

`runtime/three/pointer-look.mjs` ince işaretçide sahne içindeki fare konumunu normalize eder. Yatay hareket en fazla 7° kamera sapması, dikey hareket en fazla 0,18 sahne birimi ekler; yaklaşık 75 ms ölçeğinde yumuşar. Fare sahneden çıkınca merkezlenir. Sekme gizlendiğinde, hareket azaltma açıldığında veya sahne kapandığında bekleyen iş temizlenir. Mobilde ve kaba işaretçide fare ofseti kullanılmaz.

Scroll'un belirlediği kamera yolu ve nesne koreografisi kalıcı temeldir. Fare ofseti bu pozun üzerine eklenir; scroll ilerlemesini değiştirmez. [Lamba örneği](../examples/v6/mobile-scroll/) bu birleşimi gösterir. Ekran okuyucu için gerekli metin canvas veya video içine gömülmez.

| İstenen etki | Uygun katman | Sınır |
| --- | --- | --- |
| Sakin atmosfer | Döngülü arka plan videosu + poster | Fare videonun kamerasını çeviremez. |
| Scroll ile ileri/geri sahne | Videodan üretilmiş WebP kareleri | Kameranın yeni açısı üretilemez; kareler yalnız kayıtlı hareketi gösterir. |
| Fareyle kamera/bakış | Gerçek WebGL/Three.js sahnesi | Mobil ve reduced-motion için statik/sekans karşılığı gerekir. |
| Video ve fare birlikte | Video arka plan + ayrı 3D özne | Işık, perspektif ve renk uyumu görsel olarak denetlenir. |

Video dosyası geldiğinde [dönüştürme ve yayın akışını](../runtime/media/README.md), yük ve mobil sınırlarını [v6 medya kararını](../v6/MEDIA_DECISION_ENGINE.md) kullan. Video-only scroll sekansına “serbest fare kamerası” özelliği yazma; bunun için ayrıca gerçek 3D model gerekir.
