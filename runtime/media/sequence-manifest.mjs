function assetPath(path) {
  if (typeof path !== 'string' || !/^[a-zA-Z0-9_./-]+$/.test(path)
    || path.startsWith('/') || path.split('/').some(part => !part || part === '.' || part === '..')) {
    throw new TypeError('Manifest yalnızca klasör içindeki göreli dosya yollarını kullanmalı.');
  }
  return path;
}

export function resolveSequenceFiles(manifest, files) {
  if (manifest?.version !== 1 || manifest.kind !== 'video-frame-sequence'
    || !Number.isInteger(manifest.frameCount) || manifest.frameCount < 12 || manifest.frameCount > 120
    || !Array.isArray(manifest.frames) || manifest.frames.length !== manifest.frameCount) {
    throw new TypeError('video_to_web.py ile üretilmiş 12–120 karelik manifest gerekiyor.');
  }
  const byPath = new Map();
  for (const file of files) {
    const relative = file.webkitRelativePath ? file.webkitRelativePath.split('/').slice(1).join('/') : file.name;
    if (byPath.has(relative)) throw new TypeError(`Yinelenen dosya: ${relative}`);
    byPath.set(relative, file);
  }
  const seen = new Set();
  const frames = manifest.frames.map(record => {
    const path = assetPath(record?.file);
    if (!path.endsWith('.webp') || seen.has(path)) throw new TypeError('Her kare farklı bir WebP dosyası olmalı.');
    seen.add(path);
    const file = byPath.get(path);
    if (!file || !file.size) throw new TypeError(`Kare bulunamadı: ${path}`);
    if (file.size !== record.bytes) throw new TypeError(`Kare boyutu manifest ile uyuşmuyor: ${path}`);
    return file;
  });
  if (frames.reduce((sum, file) => sum + file.size, 0) > 4_000_000) throw new RangeError('Önizleme kareleri toplam 4 MB sınırını aşıyor.');
  const posterPath = assetPath(manifest.poster?.file);
  const poster = byPath.get(posterPath);
  if (!poster || !posterPath.endsWith('.webp') || !poster.size || poster.size !== manifest.poster.bytes || poster.size > 1_000_000) {
    throw new TypeError('Manifest ile boyutu eşleşen, 1 MB altında bir WebP poster gerekiyor.');
  }
  return { frames, poster };
}
