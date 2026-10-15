import { comparePixels } from '../../../runtime/reference/pixel-compare.mjs';

const MAX_FILE_BYTES = 25 * 1024 * 1024;
const MAX_PIXELS = 8_000_000;
const allowedTypes = new Set(['image/png', 'image/jpeg', 'image/webp']);
const byId = (id) => document.getElementById(id);
const fields = {
  reference: byId('reference-file'), candidate: byId('candidate-file'),
  status: byId('status'), results: byId('results'),
  blend: byId('blend'), threshold: byId('threshold'),
  stage: byId('comparison'), canvas: byId('heatmap'),
};
const images = { reference: null, candidate: null };
let pendingComparison = 0;

function report(message, error = false) {
  fields.status.textContent = message;
  fields.status.classList.toggle('error', error);
}

async function loadImage(file) {
  if (!allowedTypes.has(file.type)) throw new Error('Yalnızca PNG, JPG veya WebP seçebilirsin.');
  if (file.size > MAX_FILE_BYTES) throw new Error('Görüntü 25 MB sınırını aşıyor.');

  const url = URL.createObjectURL(file);
  try {
    const image = new Image();
    image.src = url;
    await image.decode();
    if (!image.naturalWidth || !image.naturalHeight) {
      throw new Error('Görüntü ölçüleri okunamadı.');
    }
    if (image.naturalWidth * image.naturalHeight > MAX_PIXELS) {
      throw new Error('Görüntü 8 milyon piksel sınırını aşıyor. Daha küçük bir ekran görüntüsü seç.');
    }
    return { url, image, width: image.naturalWidth, height: image.naturalHeight };
  } catch (error) {
    URL.revokeObjectURL(url);
    throw error;
  }
}

function pixelsOf(loaded) {
  const canvas = document.createElement('canvas');
  canvas.width = loaded.width;
  canvas.height = loaded.height;
  const context = canvas.getContext('2d', { willReadFrequently: true });
  context.drawImage(loaded.image, 0, 0);
  return context.getImageData(0, 0, loaded.width, loaded.height).data;
}

function renderComparison() {
  const reference = images.reference;
  const candidate = images.candidate;
  if (!reference || !candidate) {
    fields.results.hidden = true;
    return;
  }
  if (reference.width !== candidate.width || reference.height !== candidate.height) {
    fields.results.hidden = true;
    report(`Ölçüler farklı: kaynak ${reference.width} × ${reference.height}, çıktı ${candidate.width} × ${candidate.height}. Aynı viewport ile yeniden çek.`, true);
    return;
  }

  const width = reference.width;
  const height = reference.height;
  const comparison = comparePixels(pixelsOf(reference), pixelsOf(candidate), width, height, Number(fields.threshold.value));
  fields.canvas.width = width;
  fields.canvas.height = height;
  fields.canvas.getContext('2d').putImageData(new ImageData(comparison.heatmap, width, height), 0, 0);
  byId('reference-image').src = reference.url;
  byId('candidate-image').src = candidate.url;
  byId('candidate-image').style.opacity = String(Number(fields.blend.value) / 100);
  byId('dimensions').textContent = `${width} × ${height}`;
  byId('mean-error').textContent = `${comparison.meanError.toFixed(1)} / 255`;
  byId('mismatch').textContent = `${comparison.mismatchPercent.toFixed(1)}%`;
  fields.results.hidden = false;
  report('Karşılaştırma hazır. Önce büyük yapısal farklara bak.');
}

function scheduleComparison() {
  cancelAnimationFrame(pendingComparison);
  pendingComparison = requestAnimationFrame(() => {
    try { renderComparison(); }
    catch { fields.results.hidden = true; report('Görüntü işlenemedi. Daha küçük bir dosya dene.', true); }
  });
}

for (const kind of ['reference', 'candidate']) {
  fields[kind].addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const next = await loadImage(file);
      if (images[kind]) URL.revokeObjectURL(images[kind].url);
      images[kind] = next;
      byId(`${kind}-name`).textContent = file.name;
      scheduleComparison();
      if (!images.reference || !images.candidate) report('Diğer görüntüyü de seç.');
    } catch (error) {
      report(error instanceof Error ? error.message : 'Görüntü açılamadı.', true);
    }
  });
}

fields.blend.addEventListener('input', () => {
  byId('blend-value').textContent = `${fields.blend.value}%`;
  byId('candidate-image').style.opacity = String(Number(fields.blend.value) / 100);
});
fields.threshold.addEventListener('input', () => {
  byId('threshold-value').textContent = fields.threshold.value;
  scheduleComparison();
});
for (const button of document.querySelectorAll('[data-view]')) {
  button.addEventListener('click', () => {
    fields.stage.classList.toggle('heatmap', button.dataset.view === 'heatmap');
    for (const tab of document.querySelectorAll('[data-view]')) {
      const active = tab === button;
      tab.classList.toggle('active', active);
      tab.setAttribute('aria-pressed', String(active));
    }
  });
}
