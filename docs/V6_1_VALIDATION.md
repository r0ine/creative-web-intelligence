# v6.1 doğrulama kaydı

19 Eylül 2026, Windows üzerinde Python 3.12.14 ile çalıştırıldı.

| Kontrol | Sonuç |
| --- | --- |
| `python -m unittest discover -s tests -v` | 73 test geçti |
| `python tools/v6/validate_v6.py` | 29 dosya, 0 hata; v5, v4 ve v3.2 doğrulayıcıları da geçti |
| `python tools/validate_library.py` | 404 kimlik, 0 hata |
| `python tools/validate_scroll_library.py` | 100 tarif, 10 kategori, kimlikler benzersiz |
| `python tools/validate_external_registry.py` | 36 kayıt, 0 hata |
| `python -m compileall -q tools tests` | Derleme hatası yok |
| Değişen belgelerin yerel bağlantıları | 32 bağlantı, eksik hedef yok |
| `git diff --check` | Boşluk hatası yok |
| Doğallık taraması | 0 kritik, 0 uyarı; mevcut belgelerdeki 3 bilgi bulgusu gözden geçirildi |

Geçerli örnek `PLANNED / NOT_PROVIDED` ve çıkış kodu `0` üretti. Bütçeyi aşan örnek, standard katmanda 2600 KB sekansın 1500 KB sınırını aştığını bildirdi ve `1` döndürdü. Geçerli örneğe `--require-measurements` eklendiğinde eksik ölçüm nedeniyle `1` döndü. JSON ve metin çıktıları test edildi.

Testler toplam bütçeyi anlara bölerek aşma girişimini, tüm bütçe alanlarını, cihaz katmanlarını, hareket azaltmayı, fallback zincirini, kısmi ölçümü, yanlış türleri, NaN/Infinity değerlerini, sayısal taşmayı ve Unicode hata çıktısını kapsıyor. Katalog testleri bozuk türleri, eksik alanları, kimlik tekrarlarını, kopuk referansları ve şema/katalog ayrışmasını denetliyor.

GitHub Actions için Linux/Windows ve Python 3.11/3.14 matrisi eklendi; uzak CI bu çalışma sırasında çalıştırılmadı. Yukarıdaki sonuçlar yerel Python 3.12 çalıştırmasına aittir.

Harici AI hakemleri `audit_media_plan.py`, `validate_v6.py` ve `README.md` için denendi. DeepSeek ve GLM uçları HTTP 410 döndürdüğünden puanlama alınamadı. Bu adım erişim yokluğu nedeniyle atlandı; otomatik tarama ve kod incelemesi tamamlandı.
