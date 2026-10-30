// İlerleyici iyileştirme: JS kapalıyken sayfa tam çalışır.
// Tek görev: bölüm bağlantısına gidildiğinde odağı hedef başlığa taşımak (klavye/ekran okuyucu).
for (const link of document.querySelectorAll('.top a[href^="#"]')) {
  link.addEventListener('click', () => {
    const target = document.querySelector(link.getAttribute('href'));
    const heading = target && target.querySelector('h2');
    if (heading) {
      heading.setAttribute('tabindex', '-1');
      heading.focus({ preventScroll: true });
    }
  });
}
