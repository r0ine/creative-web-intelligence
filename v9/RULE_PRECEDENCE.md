# Kural önceliği ve çakışma kaydı

Kütüphane v2'den v9'a katman katman büyüdü ve eski sürümler silinmedi. Bu yüzden aynı konuda birden fazla director veya katalog farklı şey söyleyebilir. Bu belge hangisinin geçerli olduğunu tek yerde toplar. Makine okunur kayıt [`data/v9/rule_precedence.json`](../data/v9/rule_precedence.json) dosyasıdır.

## Öncelik sırası

1. Kullanıcının açık isteği ve mevcut ürün davranışı.
2. Erişilebilirlik, güvenlik ve lisans sınırları.
3. [`SKILL.md`](../SKILL.md) değişmezleri ve teslim kapıları: [v5 özgünlük](../quality/V5_AUTHENTICITY_GATE.md), [v6 sinematik](../quality/V6_CINEMATIC_GATES.md), [v7 kalibrasyon](../quality/V7_VISUAL_CALIBRATION.md).
4. Alanın geçerli director'ı.
5. Aynı alanda birlikte kullanılan ve eski director'lar.
6. Eski kataloglar (`data/v2`, `data/v3`, `data/design_rules.json`, `data/color_combination_recipes.json`) fikir havuzudur. Aşağıdaki çakışmalarda adı geçen kayıtlar çözüm uygulanmadan kullanılmaz.

Daha yeni sürüm otomatik olarak kazanmaz; yukarıdaki sıra ve kayıt kazanır. Örneğin v3.1 scroll director'ı sert hatalarda geçerlidir, ama tarif seçimi ve mobil kuralları v2.2 dosyasından gelir.

## Alanlara göre geçerli director

| Alan | Geçerli | Birlikte | Yerini aldığı |
| --- | --- | --- | --- |
| Kompozisyon | `directors/v5/COMPOSITION_DIRECTOR_V5.md` | | `directors/composition/COMPOSITION_DIRECTOR.md` |
| Hareket | `directors/v5/MOTION_DIRECTOR_V5.md` | | `directors/v3_2/MOTION_DIRECTOR.md`, `directors/motion/MOTION_DIRECTOR.md` |
| Kalite denetimi | `directors/v5/QA_DIRECTOR_V5.md` | `directors/v6/CINEMATIC_QA_DIRECTOR.md` | `directors/qa/VISUAL_QA_DIRECTOR.md` |
| Scroll | `directors/v3_1/SCROLL_DIRECTOR.md` | `directors/scroll/SCROLL_DIRECTOR.md` | |
| Tipografi | `directors/v3_2/TYPOGRAPHY_DIRECTOR.md` | | `directors/v3_1/TYPOGRAPHY_DIRECTOR.md`, `directors/font/FONT_DIRECTOR.md` |
| 3D | `v6/THREE_D_DIRECTOR.md` | `v6/CAMERA_DIRECTOR.md` | `directors/three/THREE_ART_DIRECTOR.md` |
| Medya | `directors/v6/MEDIA_DIRECTOR.md` | `v6/FRAME_SEQUENCE_DIRECTOR.md` | |
| Referans | `directors/reference/REFERENCE_RECREATION_DIRECTOR_V3.md` | `directors/v3_1/REFERENCE_FIDELITY_DIRECTOR.md` | |

Renk, özgünlük, referans analizi, font kaynağı, ikon, asset, kaynak seçimi, backend, güvenlik, gizli anahtar, şifreleme, API sözleşmesi, fullstack ve tarif birleştirici alanlarında tek director vardır. Yerini başka dosyanın aldığı veya başka bir dosyayla birlikte kullanılan her director dosyasının başında bu kararı gösteren kısa bir **Öncelik (v9)** notu bulunur.

## Bilinen çakışmalar

| Kimlik | Konu | Çözüm |
| --- | --- | --- |
| CF-001 | Atmosfer için parçacık alanı | Parçacık yalnız veri, fizik veya sayılan varlık gösteriyorsa. |
| CF-002 | Koyu emisif, cam/krom 3D dünyaları | Gerçek ürün malzemesi değilse dekoratif hero nesnesi yapılmaz. |
| CF-003 | Gerekçesiz koyu palet hazır ayarları | Koyu arayüz yalnız yazılı içerik/kullanım gerekçesiyle. |
| CF-004 | Bütün roller için ortak easing ve süre | Tek hareket dili, rol başına ayrı süre ve eğri. |
| CF-005 | Hareket azaltmayı yalnız kısaltmak | Sorunlu hareket kaldırılır, kısaltmak yetmez. |
| CF-006 | Bölüm ayırıcı çizgi animasyonu | Çizgi son seçenek; varsayılan giriş hareketi değil. |
| CF-007 | Mono gövde metni, varsayılan Inter / Space Grotesk | Mono gövde yok; bu fontlar ancak gerekçeyle. |
| CF-008 | Nesne hareketinde aşmalı eğri örneği | Aşma yalnız oyunsu dilde ve etkileşim geri bildiriminde. |

Bir katalog kaydını kullanmadan önce çakışmada olup olmadığını sor:

```sh
python tools/v9/precedence.py                       # sıra ve açık çakışmalar
python tools/v9/precedence.py --id font-029         # bu kaydı etkileyen çakışma ve çözüm
python tools/v9/precedence.py --file directors/motion/MOTION_DIRECTOR.md
python tools/v9/precedence.py --domain scroll
python tools/v9/precedence.py --conflict CF-005     # etkilenen bütün kayıtlar
```

## Kütüphane büyürken

`python tools/v9/validate_v9.py` şu durumlarda başarısız olur:

- Yeni bir director dosyası hiçbir alana kaydedilmemişse ya da iki alanda birden geçiyorsa.
- Yerini başka dosyanın aldığı veya başka bir dosyayla birlikte kullanılan bir director, geçerli dosyayı adıyla göstermiyorsa.
- `data/**/*.json` içinde iki farklı dosya aynı kimliği kullanıyor ve bu `idCollisions` listesinde gerekçelendirilmemişse.
- Açık bir çakışmanın eski tarafı artık hiçbir kayda uymuyorsa. Veri düzeltildiyse kaydı `resolved` yap; böylece çakışma sessizce kaybolmaz.
- Yeni taraftaki kanıt (kimlik veya alıntı) silinmiş ya da değişmişse.
- Geri bildirim sözlüğünde aynı ifade iki farklı anlama bağlanmışsa.

Yeni bir kural eski bir kuralla çelişiyorsa eski dosyayı sessizce değiştirme. Çakışmayı bu kayda ekle, çözümü bir cümleyle yaz ve doğrulamayı çalıştır.
