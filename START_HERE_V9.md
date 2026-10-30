# Creative Web Intelligence v9

v9, v8 akışını korur ve iki şey ekler: kullanıcının revizyon geri bildirimini anlamak ve büyüyen kütüphanede hangi kuralın geçerli olduğunu bilmek.

1. Yeni site veya köklü yeniden tasarımda [brief → ilk referans](reference-engine/BRIEF_TO_REFERENCE.md) ile başla; kaynak seçimi ve uygulama için [v8 başlangıcını](START_HERE_V8.md) izle.
2. Bir kural, tarif veya director seçmeden önce [kural önceliğine](v9/RULE_PRECEDENCE.md) bak. Aynı alanda birden fazla dosya varsa yalnız geçerli olanı izle; eski katalog kaydını kullanmadan önce `precedence.py --id <kimlik>` ile çakışma olup olmadığını sor.
3. Kullanıcı sonucu gördükten sonra memnun değilse [revizyon akışını](reference-engine/REVISION_FEEDBACK.md) uygula:
   - “İçime sinmedi”, “olmamış” gibi yalnız his varsa hiçbir şeyi değiştirmeden **“Neresi?”** diye seçeneklerle sor.
   - Cevap “genel” ise en çok görünen yüzeylerden başla: arka plan, ilk ekran, baskın renk, başlık tipografisi.
   - Beğenilen yerleri koru; “eskisi daha iyiydi” denirse yeni yön üretme, geri al.
4. Her revizyonda değişen dosyaları tam yollarıyla ve projenin nerede çalıştığını kullanıcıya söyle; kararları `reference-note.md` sonuna yaz.
5. Kütüphanede değişiklik yaptıysan `python tools/validate_all.py` çalıştır. Yeni director, katalog kimliği veya çelişen kural kayda alınmadıysa doğrulama başarısız olur.

```sh
python tools/v9/feedback_triage.py "içime sinmedi"
python tools/v9/feedback_triage.py "içime sinmedi" --answer "genel"
python tools/v9/feedback_triage.py "renkler güzel ama genel olarak ucuz duruyor"
python tools/v9/precedence.py
python tools/v9/precedence.py --id font-029
python tools/validate_all.py
```

Araçlar çevrimdışı çalışır ve yalnız standart Python kütüphanesini kullanır. Geri bildirim aracı karar önerir; ekranı görmeden tasarım hükmü vermez.
