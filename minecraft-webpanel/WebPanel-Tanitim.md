# WebPanel — Sunucunuz İçin Web Kontrol Paneli

## Bu Nedir?

Minecraft sunucunuza **tek bir eklenti dosyası** (plugin) atıyorsunuz ve sunucunuzun kendi web sitesi/paneli oluyor. Oyuncularınız tarayıcıdan (Chrome, telefon, ne olursa) siteye girip kullanıcı adı ve şifresiyle giriş yapabiliyor, kendi istatistiklerini görebiliyor: ne kadar oynamış, kaç blok kırmış, kaç kişi öldürmüş, en son ne zaman girmiş gibi.

Yani sunucunuzun bir "hesap sayfası" oluyor — tıpkı büyük sunucularda gördüğünüz "stats.sunucuadi.com" gibi siteler.

## Neden Önemli?

- **Oyuncu bağlılığı artar.** İnsanlar istatistiklerini görmeyi sever, "acaba ben kaç saat oynadım" merakı onları siteye çeker, siteye gelen oyuncu sunucuyu unutmaz.
- **Profesyonel görünüm.** Sadece oyun içi değil, web sitesi olan bir sunucu daha ciddi ve güvenilir algılanır.
- **Reklam / duyuru alanı.** İleride bu panel üzerine mağaza, duyuru, sıralama tabloları gibi şeyler eklenebilir.
- **Ekstra maliyet yok.** Ayrıca bir web sunucusu kiralamanıza gerek yok — her şey zaten sahip olduğunuz Minecraft sunucusunun içinde, tek dosya olarak çalışıyor.

## Nasıl Kuruluyor?

Tek adım: Dosya `plugins` klasörüne atılıyor, sunucu yeniden başlatılıyor. Başka hiçbir program kurmanıza gerek yok — ne Node.js, ne PHP, ne ayrı bir hosting. Zaten çalışan Minecraft sunucunuzun içinde otomatik olarak bir web sitesi de açılmış oluyor.

## Güvenlik Nasıl Sağlanıyor?

Bu konu en çok merak edilen kısım olduğu için sade anlatıyorum:

1. **Şifreler asla açık halde tutulmuyor.** Sisteminizde zaten kullandığınız AuthMe (giriş/kayıt eklentisi) hangi şifreleme yöntemini kullanıyorsa, web paneli de aynı yöntemi kullanarak doğrulama yapıyor. Yani şifreleri tekrar yazmıyoruz, sadece var olan güvenli kaydı kontrol ediyoruz.

2. **Web paneli, oyuncu kayıt sistemine asla yazma yapmıyor.** Sadece okuyor. Yani bir hata olsa bile AuthMe'nin veritabanına zarar veremez — bu bilinçli bir güvenlik tercihi.

3. **Şifre deneme saldırılarına karşı koruma var.** Biri şifre tahmin etmeye çalışırsa (bot ile), sistem belirli sayıda yanlış denemeden sonra o kişiyi geçici olarak engelliyor. Bu, "brute-force" denilen saldırı türüne karşı standart bir önlem.

4. **Oturum bilgileri (giriş yapmış olma durumu) tarayıcıda güvenli şekilde saklanıyor.** Kod enjeksiyonu (XSS) ve oturum çalma gibi yaygın saldırılara karşı standart web güvenlik önlemleri (HttpOnly, Secure cookie) uygulanıyor.

5. **Veritabanı bağlantısı şifreli (TLS/SSL).** Sunucu ile veritabanı arasındaki trafiğin araya girilip okunmasını engelliyor.

6. **HTTPS desteği var** — yani tarayıcıda kilit simgesiyle güvenli bağlantı gösterilebiliyor (sertifika kurulumu gerektirir, bunu nasıl yapacağınızı ayrıca anlatırım).

## Sunucu Performansını Etkiler mi?

Hayır. Web paneli, oyunun çalıştığı ana sistemden **tamamen ayrı bir hat üzerinde** çalışacak şekilde tasarlandı. Yani 50 kişi aynı anda web sitesine girse bile oyuncuların yaşadığı "lag" hiçbir şekilde artmaz — bu iki sistem birbirine karışmıyor, sadece aynı dosyanın içinde birlikte paketleniyor.

## Özetle

| Soru | Cevap |
|---|---|
| Ekstra sunucu/hosting gerekiyor mu? | Hayır, tek dosya, mevcut sunucunun içinde |
| Kurulumu zor mu? | Hayır, dosyayı atıp sunucuyu yeniden başlatmak yeterli |
| Şifreler güvende mi? | Evet, mevcut güvenli sistem (AuthMe) kullanılıyor, tekrar yazılmıyor |
| Oyun performansı etkilenir mi? | Hayır, tamamen ayrı çalışıyor |
| Saldırılara karşı korumalı mı? | Evet, şifre deneme sınırlaması ve şifreli bağlantılar var |
| Sonradan geliştirilebilir mi? | Evet, mağaza, sıralama tablosu, duyuru gibi özellikler eklenebilir |

---

*Bu belge, sistemin teknik mimarisini açıklayan detaylı doküman ile birlikte hazırlanmıştır. Teknik detaylar (veritabanı yapısı, kod mimarisi, güvenlik implementasyonu) ayrı bir belgede mevcuttur; bu belge yalnızca genel tanıtım amaçlıdır.*
