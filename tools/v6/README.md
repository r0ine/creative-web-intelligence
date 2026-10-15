# Medya planı denetimi

Kreatif bileşen/şablon seçimi, ChatGPT video promptu ve videodan WebP kare üretimi
[video araçları rehberinde](../../runtime/media/README.md). Çalışan arayüz: [medya atölyesi](../../examples/v6/media-studio/index.html).

`audit_media_plan.py`, seçtiğin medyumları v6 bütçeleri ve fallback kurallarıyla karşılaştırır. Python 3.11 veya üzeri yeterli; ek paket, API anahtarı ya da ağ bağlantısı gerekmez. Komutları depo kökünden çalıştır.

```sh
python tools/v6/audit_media_plan.py examples/v6/media_plan.json --format text
python tools/v6/audit_media_plan.py examples/v6/media_plan.json
```

İlk komut `PLANNED` ve `NOT_PROVIDED` döndürür: örneğin tahminleri bütçeye uyar, fakat ölçümü yoktur. İkinci komut aynı raporu JSON olarak verir. Örnek maliyetler öğretim amaçlıdır; gerçek bir siteden ölçülmemiştir.

## Planı doldurma

[Örnek planı](../../examples/v6/media_plan.json) kopyala. Her görsel an için amacını, medyumun neden gerektiğini, masaüstü ve mobil varyantlarını yaz. Kimlikler benzersiz olmalı. Alan sözleşmesi [media_plan.schema.json](../../schemas/v6/media_plan.schema.json) dosyasında.

`estimates` içindeki yedi metrik zorunludur. Kullanılmayan kaynak için `0` gir. Eksik ölçüm yerine `0` yazma; ölçüm yapmadıysan `measurements` alanını ekleme.

| Metrik | Anlamı |
| --- | --- |
| `initial_payload_kb` | İlk görünümde yüklenen medya aktarımı |
| `total_page_media_mb` | Sonradan yüklenenler dahil toplam medya aktarımı |
| `frame_sequences_kb` | Kare sekanslarının aktarımı; toplam medyanın alt kümesi |
| `glb_kb` | GLB aktarımı; toplam medyanın alt kümesi |
| `texture_memory_mb` | Sıkıştırılmış dosya boyutu değil, GPU doku belleği tahmini |
| `draw_calls` | Kare başına çizim çağrısı, tam sayı |
| `concurrent_animations` | Aynı anda çalışan animasyon sayısı, tam sayı |

Aktarımda ondalık birim kullanılır: 1 KB = 1000 bayt, 1 MB = 1000 KB. Doku belleği MB olarak normalize edilir. CSS, JavaScript ve font aktarımı bu medya bütçesine dahil değildir; sayfanın toplam performansını ayrıca ölç.

Araç tüm görsel anların maliyetlerini cihaz başına toplar. Çizim, bellek ve animasyon toplamları, anların aynı anda etkin olabileceği varsayımıyla hesaplanır. Çakışmayan sahneler için otomatik indirim yapmaz. Paylaşılan bir dosyanın aktarımını iki kez sayma; ilk kullanan anda kaydet. Her gerçek zamanlı varyantın çizim maliyetini ayrıca belirt.

`downgrade_chain` masaüstü medyumuyla başlar, [medyum kataloğundaki](../../data/v6/media_decision_matrix.json) sırada daha sade seçeneklere ilerler ve statik bir medyumla biter. Ara basamakları atlayabilirsin. Mobil medyum zincirde bulunmalı. `reduced_motion` için statik medyum ve içeriğin nasıl korunacağını anlatan açıklama gerekir. Statik tasarımlarda tek elemanlı zincir geçerlidir.

`essential_content_in_html` ve `keyboard_accessible` gerçek uygulamayı tarif etmeli. Bunların `true` olması erişilebilirlik testi yerine geçmez.

## Ölçüm raporu

Tarayıcıda ölçtükten sonra köke `measurements.desktop` ve `measurements.mobile` ekle. İkisi de `estimates` ile aynı yedi metriği içerir; değerler tek bir görselin değil, sayfanın cihaz başına toplamıdır. Bir cihazın raporu eklendiyse `PARTIAL`, ikisi de eklendiyse ve sınırlar aşılmadıysa `WITHIN` görünür. Üst durum, engel yoksa `MEASURED` olur.

```sh
python tools/v6/audit_media_plan.py examples/v6/media_plan.json --require-measurements --format text
```

Bu komut örnek plan üzerinde bilerek `1` döndürür: ölçüm olmadan geçişe izin vermez. `MEASURED`, dosyaya yazılan ölçümlerin sınırlar içinde olduğunu belirtir. Araç tarayıcıyı açmaz, ölçümün kaynağını doğrulamaz veya görsel kaliteye onay vermez. v5 özgünlük ve v6 sinematik kapıları ayrıca uygulanır.

## Çıkış kodları

- `0`: plan denetimi geçti; ölçüm yoksa durum hâlâ `PLANNED` olabilir.
- `1`: bütçe, amaç, mobil, erişilebilirlik veya fallback engeli var; ya da `--require-measurements` için ölçüm eksik.
- `2`: dosya okunamıyor, JSON geçersiz veya alan sözleşmesi bozuk.

Hatalı plan örneğinde sekansın 2600 KB maliyeti standard katmanın 1500 KB sınırını aşar:

```sh
python tools/v6/audit_media_plan.py examples/v6/over_budget_media_plan.json --format text
```

Bu komut `BLOCKED` ve çıkış kodu `1` üretir. Çözüm, seçilen katmanın bütçesine sığan bir sekans hazırlamak veya daha sade medyuma geçmektir.

## Doğrulama

```sh
python tools/v6/validate_v6.py
python -m unittest discover -s tests -v
```

Katalog doğrulaması veri ilişkilerini, testler ise toplu bütçe aşımı, fallback hataları, geçersiz girişler ve ölçüm durumlarını denetler.
