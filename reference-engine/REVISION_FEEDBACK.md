# Revizyon geri bildirimini anlamak

Bu akış, kullanıcı bir sonucu gördükten sonra memnuniyetsizliğini söylediğinde kullanılır. Amaç kullanıcının kastettiği yeri ve yönü bulmak; rastgele detay değiştirmemek, her şeyi baştan yapmamak ve beğenilen kararları bozmamaktır. İlk referans ve brief için [brief → ilk referans](BRIEF_TO_REFERENCE.md) akışı geçerlidir.

## 1. Geri bildirimin türünü ayır

Her cümleyi dört sorudan geçir: **nerede** (yüzey), **ne yönde** (his), **neyi beğendi** (korunacak) ve **geri mi almak istiyor**.

| Tür | Örnek | Yapılacak |
| --- | --- | --- |
| Konumlu | “Arka plan olmamış”, “hero başlığı çok büyük” | Yalnız o yüzeye dokun; soru yerine 2-3 alternatif göster. |
| Yalnız his | “İçime sinmedi”, “olmamış”, “bir şey eksik” | Hiçbir şeyi değiştirmeden **“Neresi?”** diye sor. |
| Genel | “Geneli”, “hepsi”, “genel olarak” | En çok görünen yüzeylerden başla (bölüm 3). |
| Yön | “Ucuz”, “sıkıcı”, “kalabalık”, “AI gibi” | Olası nedenleri incele; konumu seçeneklerle sor. |
| Geri alma | “Eskisi daha iyiydi”, “geri al” | Yeni yön üretme; hangi değişikliğin geri alınacağını netleştir. |
| Onay | “İçime sindi”, “arka plan güzel” | Değiştirme; beğenilen kararı revizyon notuna yaz. |

“Renkler güzel ama genel olarak olmamış” gibi cümlelerde *ama* öncesi korunacak, sonrası değiştirilecek kısımdır. “Güzel değil”, “iyi olmamış” olumsuzdur; olumlu sözcüğü tek başına okuma.

## 2. Yalnız his varsa önce “Neresi?” diye sor

Tek soru, somut seçeneklerle sorulur:

> Neresi içine sinmedi? Arka plan ve zemin · İlk ekran (hero) · Renkler · Başlık yazıları · ya da **genel olarak**

Gerekirse ikinci soru: “Beğendiğin ve aynen kalmasını istediğin bir yer var mı?” Bir turda en fazla üç soru sorulur; cevabı beklerken yalnız inceleme yapılır, tasarım değiştirilmez. Kullanıcı yerini söylediyse yön sorma: o yüzey için 2-3 seçeneği yan yana göstermek sormaktan daha hızlı sonuç verir.

## 3. “Genel” cevabında en çok görünenden başla

Kullanıcı “genel” derse ilk izlenimi en çok taşıyan yüzeyleri sırayla ele al. Sıra [`data/v9/visibility_ranking.json`](../data/v9/visibility_ranking.json) dosyasındadır:

1. **Arka plan ve zemin**: ekranın en büyük alanı; ton, sıcaklık, açık/koyu kararı.
2. **İlk ekran (hero)**: başlığın yeri, ana görsel, odak noktası.
3. **Baskın renk ve vurgu oranı**: nötr/destek/vurgu alan dengesi.
4. **Başlık tipografisi**: font, ölçek farkı, ağırlık.
5. **Görsel, medya ve 3D** · 6. **Boşluk ritmi** · 7. **Kart, buton ve köşe dili** · 8. **Menü** · 9. **Gövde metni** · 10. **Hareket** · 11. **İkon ve mikro detay**

İlk üç yüzeyi birlikte değiştiren 2-3 yön hazırla ve yalnız ilk ekranda göster. Her yön için bir cümleyle neyin değiştiğini yaz. Mikro detaylarla, ikonlarla veya hareketle başlama: bunlar büyük yüzeyler doğruyken fark yaratır. Kullanıcının beğendiğini söylediği yüzey listeden çıkarılır.

Genel geri bildirimle birlikte bir yön de söylendiyse (“genel olarak ucuz duruyor”), sıradaki yüzeylerden o yönle ilgili olanları seç. Yönlerin olası nedenleri, ilk hamleleri ve kaçınılacak düzeltmeleri [`data/v9/feedback_lexicon.json`](../data/v9/feedback_lexicon.json) içindedir. Örneğin “ucuz” hissi parlaklık ekleyerek değil; tipografi ölçeği, boşluk ritmi ve kutu azaltarak düzeltilir.

## 4. Yapma

- Konum bilinmeden rastgele bir ayrıntıyı değiştirip “düzelttim” deme.
- Tek bir “içime sinmedi” yüzünden siteyi baştan üretme; [ilk referans](BRIEF_TO_REFERENCE.md) yalnız brief kökten değişirse yeniden yapılır.
- Kullanıcının beğendiği kararları yeni yönle birlikte değiştirme.
- Memnuniyetsizliği süs, efekt, parçacık veya gradyanla örtme; v5 ve v7 kapıları revizyonda da geçerlidir.
- Tasarımı savunma; kullanıcının hissini veri say ve nedenini yüzeylerde ara.

## 5. Revizyon notu ve dosya yolları

Her revizyonda `reference-note.md` sonuna kısa bir kayıt ekle: kullanıcının cümlesi, yorumun, değişen yüzeyler, korunan kararlar ve değişen dosyalar. Kullanıcıya hangi dosyaların değiştiğini **tam yollarıyla** ve projenin nerede çalıştığını söyle. Sonraki “eskisi daha iyiydi” isteğinde geri alınacak değişiklik bu kayıttan bulunur.

## Araç

```sh
python tools/v9/feedback_triage.py "içime sinmedi"
python tools/v9/feedback_triage.py "içime sinmedi" --answer "genel"
python tools/v9/feedback_triage.py "renkler güzel ama genel olarak olmamış" --format json
```

Araç Türkçe ve İngilizce ifadeleri büyük/küçük harf ve Türkçe karakter farkı gözetmeden tanır (“icime sinmedi” = “İÇİME SİNMEDİ”). Çıktı bir karar önerisidir; ekranı görmeden tasarım hükmü vermez. Sözlükte olmayan bir ifadede `unclear` döner ve kısa bir soru önerir.
