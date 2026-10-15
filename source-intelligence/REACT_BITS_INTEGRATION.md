# React Bits’i hedef projeye ekleme

[React Bits](https://reactbits.dev/) CWI’nin kaynak kataloğuna dahil. Resmi siteden seçilen bileşen, hedef React uygulamasına eklenir; tüm koleksiyon CWI içine yeniden paketlenmez. [Depo](https://github.com/DavidHDev/react-bits) kurulum için shadcn ve jsrepo yollarını, JS/TS ile CSS/Tailwind varyantlarını açıklıyor.

## Seçim ve kurulum

```sh
node tools/v6/creative_media.mjs sources hero react project
```

Hedef projede React sürümünü ve stil sistemini doğrula. Resmi bileşen sayfasındaki varyantı seç; kurulum komutunu ve registry dosyasını incele. Resmi README’de verilen TypeScript/Tailwind örneği:

```sh
npx shadcn@latest add @react-bits/BlurText-TS-TW
```

Bu komut CWI deposunda çalıştırılmaz; seçilen React uygulamasının kökünde çalıştırılır. İsimdeki `TS-TW` varyantını proje ihtiyacına göre resmi sayfadan değiştir. `latest` komutu örnektir; kurulum sırasında çözülen sürüm, registry kaynağı ve eklenen bağımlılıklar hedef projede kaydedilir.

Bileşeni import etmeden önce dosyanın export biçimini kontrol et. İsim veya dosya yolu tahmin ederek import üretme. `window`, canvas, WebGL ve ölçüm kodu olan bileşenlerde SSR sınırını doğrula. React cleanup sırasında listener, observer, requestAnimationFrame ve WebGL kaynakları bırakılmalı.

## Görsel uyarlama

Davranış seçimi, sayfanın görevine göre yapılır. Başlık vurgusu gerekiyorsa tek bir metin etkileşimi; proje galerisinde inceleme gerekiyorsa galeri etkileşimi; arka plan kimliğe katkı veriyorsa sınırlı bir yüzey hareketi seç. Birçok örneği yan yana eklemek tutarlı art direction sağlamaz.

Hareket azaltma tercihinde metin hemen görünür kalmalı; görsel efekt kapansa da düzen ayakta olmalı. Mobilde hover tek etkileşim yolu olamaz. Ağır bir WebGL arka planı kullanılacaksa mobil poster ve veri tasarrufu karşılığı tasarlanmalı. CWI’deki 3D lamba örneği React Bits’e bağımlı değildir; vanilla projelerde React kurmak zorunlu tutulmaz.

React Bits lisansı proje düzeyinde kullanıma izin verir, lisans bildirimini korumayı ister ve bileşenlerin kendisinin yeniden dağıtımını kısıtlar. Güncel koşul: [MIT + Commons Clause](https://raw.githubusercontent.com/DavidHDev/react-bits/main/LICENSE.md), son kontrol 4 Ekim 2026.
