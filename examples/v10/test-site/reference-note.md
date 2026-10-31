# Referans notu — r0ine test sitesi

**İstek yorumu:** r0ine için, yalnız doğrulanmış gerçekleri kullanan, tipografi öncülüğünde sakin tek sayfa. Sadakat modu: kaynak verilmediği için yok; bu, **önerilen özgün yön**dür (`inspired` bile değil). sebg.ch ve r0ine.dev ağ engeli nedeniyle incelenemedi: durum `NEEDS_CAPTURE`.

**Korunacak üç karar**
1. Tipografi: sol hizalı, ekranı taşıyan dev `r0ine` adı (Cambria/Caladea serif), gövdede sistem sans.
2. Renk: sıcak kâğıt zemin, sıcak siyah metin, tek işaret rengi (pas kırmızısı) yalnız bağlantı alt çizgisi ve odak halkasında. Çalışma paleti, marka kaynağı yok: geçici.
3. Biçim: her içerik türü ayrı biçimde. Düz yazı, tek dev bağlantı, numaralı iş listesi, tanım listesi. Kart ve çizgi yok; tek yüzey değişimi iletişimde.

**Etkileşim:** yalnız bağlantı renk geçişi (140 ms) ve klavye odağı. Hareket az altılmışsa geçiş yok. JS kapalıyken her şey çalışır.

**Mobil:** tek sütun; ad `26vw` ile ölçeklenir; masaüstünde 4/8 iki sütun.

**Bilinen boşluklar:** gerçek tarayıcıda görülmedi (Chromium/Playwright yok). Tüm `[doldurulacak]` alanları: bio ayrıntısı, majesteleri.net ve iki BuiltByBit kaynağının açıklaması, birlikte çalışılan kişiler, GitHub, e-posta.

**Sorular:** (1) Gerçek GitHub/e-posta? (2) majesteleri.net kısaca ne? (3) "Birlikte" kimlerle?

## Pipeline komutları

Ağ erişimi olsaydı bu site şu komutlarla kurulurdu:

```sh
# 1. Referans siteyi indir, analiz et, içerik çıkar, font denetle → build spec
python tools/v10/build_from_reference.py https://www.sebg.ch --content https://r0ine.dev --lang tr

# 2. Siteyi üç araçla birden denetle
python tools/v10/check_site.py examples/v10/test-site/
```

Her iki site de bu oturumda ağ engeli nedeniyle erişilemedi (`NEEDS_CAPTURE`). Site kütüphane kuralları ve doğrulanmış bilgilerle kuruldu; referans tasarımı ve içerik göçü yapılamadı.
