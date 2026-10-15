# Kaynak ve video doğrulaması

4 Ekim 2026, yerel Windows ortamında çalıştırıldı. Önizleme `127.0.0.1:22222` adresindeki Python HTTP sunucusundan servis edildi. FFmpeg 7.1 ile sentetik iki saniyelik video ve gerçek dosya dönüşümü denendi. Atölyenin varsayılan görseli mevcut Three.js lambasından üretilmiş WebP kareleridir; yeni bir AI video üretildiği iddia edilmez.

| Kontrol | Sonuç |
| --- | --- |
| Node testleri | 57 geçti; prompt, kaynak seçimi, manifest, scroll, cache ve lamba hareketi |
| Python testleri | 83 geçti; FFmpeg entegrasyonu dahil, atlanan test yok |
| v6 katalog doğrulaması | 42 dosya, 0 hata |
| Medya atölyesi tarayıcı kontrolü | 9 senaryo geçti |
| Önceki mobil/3D scroll örneği | 12 senaryo geçti; 29 draw call, 28.046 üçgen |
| Doğallık taraması | 0 kritik, 0 uyarı; eski belgelerde 3 bilgi bulgusu |
| Harici AI-hakem | Atlandı; önceki otomatik onay incelemesi kaynak kodunun dış servise gönderilmesini reddetti |

## Tarayıcıda sınanan davranışlar

React Bits ve 21st.dev, proje kapsamında kaynak seçimine dahil; kütüphane dağıtımı filtresinde çıkarılıyor. Vanilla projeler React bağımlılığına yönlendirilmiyor. Prompt başlangıçta boş ve kopyalama kapalı; düğmeye basınca nesne ve arka plan/scroll seçimi prompta yansıyor. JSON brief’i indiriliyor.

Yerel video için poster üretimi, sessiz döngü, durdurma, tekrar oynatma, ekran dışına çıkınca durma ve canlı reduced-motion değişimi denendi. MP4 ve kare dosyaları ağ üzerinden yüklenmedi. Kare klasörünün manifest’i okunup doğru sırada oynatıldı; ileri ve geri scroll, klavye kontrolü ve örneğe dönüş denendi. Bozuk video ve geçersiz manifest mevcut sahneyi korudu.

390×844 mobil ekran yatay taşmadan geçti. Görsel kontrolde metin ile nesne arasındaki çakışma giderildi. Save-Data açıkken kare isteği gönderilmedi. JavaScript kapalıyken metin ve poster göründü. Statik durumda sticky scroll uzatması kaldırıldı.

## Dosya dönüşümü

320×180 test videosundan 24 WebP kare, poster, sessiz MP4 ve manifest üretildi. Kare aktarımı 101.224 bayttı. Kaynak ve üretilen dosyaların SHA-256 değerleri gerçek dosyalardan denetlendi. Küçük aktarım bütçesinde işlem reddedildi ve hedef klasör oluşmadı; mevcut klasörün üzerine yazılmadı. Kaynak süresinin dışındaki bölüm reddedildi.

Bu sonuçlar kod yolunu doğrular. Gerçek üretilmiş videonun zamansal kalitesi, marka uyumu, mobil kompozisyonu ve döngü devamlılığı ayrıca incelenmeli; manifest bu alanları otomatik olarak geçti saymaz.
