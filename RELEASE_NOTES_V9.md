# v9 sürüm notları

**Dil:** Türkçe · [English](RELEASE_NOTES_V9.en.md)

## Revizyon geri bildirimini anlama

- [Revizyon akışı](reference-engine/REVISION_FEEDBACK.md): “içime sinmedi” gibi belirsiz geri bildirimde ajan hiçbir şeyi değiştirmeden önce **“Neresi?”** diye seçeneklerle sorar. “Genel” cevabında en çok görünen yüzeylerden başlar: arka plan, ilk ekran, baskın renk, başlık tipografisi. Beğenilen yerler korunur. “Eskisi daha iyiydi” bir geri alma isteği olarak okunur.
- [`data/v9/visibility_ranking.json`](data/v9/visibility_ranking.json): 11 yüzeyin ilk izlenimdeki ağırlık sırası. Her yüzey için neyin değiştirilebileceği ve CSS'te nerede aranacağı yazılı.
- [`data/v9/feedback_lexicon.json`](data/v9/feedback_lexicon.json): 11 Türkçe/İngilizce his ve yön (ucuz, sıkıcı, kalabalık, AI gibi, karanlık, soğuk, abartılı, boş, eski, geri al). Her biri için olası nedenler, ilk hamle ve kaçınılacak düzeltme var.
- `tools/v9/feedback_triage.py`: cümleyi konum, yön, korunacak yer ve sorulacak soruya çevirir. Türkçe büyük harf ve ASCII yazımı (“icime sinmedi”) tanır, “güzel değil” gibi olumsuzlamaları ayırır, bir turda en fazla üç soru önerir.

## Kural önceliği ve çakışma kaydı

- [Kural önceliği](v9/RULE_PRECEDENCE.md) ve [`data/v9/rule_precedence.json`](data/v9/rule_precedence.json): 34 director dosyası 22 alana bağlandı. Aynı alandaki eski dosyaların başına geçerli dosyayı gösteren **Öncelik (v9)** notu eklendi.
- Sürümler arasındaki 8 çelişki kayda alındı: atmosfer parçacıkları, dekoratif cam/krom 3D, gerekçesiz koyu paletler, rollerin tamamında ortak easing, hareket azaltmayı yalnız kısaltmak, ayırıcı çizgi animasyonu, mono gövde metni ve varsayılan fontlar, aşmalı eğri. Her biri için çözüm yazıldı.
- 13 dosyalar arası kimlik çakışması gerekçesiyle listelendi.
- `tools/v9/precedence.py`: bir alanın geçerli director'ını, bir dosyanın durumunu ve bir katalog kaydını etkileyen çakışmayı gösterir.

## Kütüphane büyürken koruma

`tools/v9/validate_v9.py` şu durumlarda başarısız olur: kayda alınmamış yeni director, geçerli dosyayı göstermeyen eski director, kayda alınmamış kimlik çakışması, eski verisi düzeltildiği halde açık kalan çakışma, silinen kanıt ve aynı ifadenin iki anlama bağlanması. `tools/validate_all.py` artık v9 zincirini çalıştırır.

## Düzeltmeler

- `v6/MOBILE_MEDIA_STRATEGY.md` içinde var olmayan `scroll/SCROLL_DIRECTOR.md` yolu düzeltildi.
- v7 ve v8 doğrulayıcıları `9.0` manifest sürümünü kabul eder.
