export function selectCreativeSources(catalog, { role = 'all', framework = 'react', scope = 'project' } = {}) {
  if (!['all', 'hero', 'background', 'scroll', 'gallery', 'template', 'primitives'].includes(role)) throw new RangeError('Kaynak rolü geçersiz.');
  if (!['react', 'vanilla'].includes(framework)) throw new RangeError('Framework react veya vanilla olmalı.');
  if (!['project', 'library'].includes(scope)) throw new RangeError('Kapsam project veya library olmalı.');
  if (!Array.isArray(catalog?.sources)) throw new TypeError('Kaynak kataloğu bulunamadı.');
  return catalog.sources.filter(source => (role === 'all' || source.roles.includes(role))
    && source.frameworks.includes(framework)
    && (scope === 'project' || source.libraryRedistribution === 'license-notice')).map(source => ({
      ...source,
      nextStep: scope === 'library'
        ? 'Seçilen dosyanın lisansını ve bağımlılıklarını yeniden doğrula; yazar, sürüm ve lisans bildirimini kaydet.'
        : source.acquisition,
    }));
}
