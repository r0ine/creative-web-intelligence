import { buildVideoPrompts } from '../../../runtime/media/video-prompt.mjs';
import { selectCreativeSources } from '../../../runtime/media/source-selection.mjs';
import { createBackgroundVideo } from '../../../runtime/media/background-video.mjs';
import { resolveSequenceFiles } from '../../../runtime/media/sequence-manifest.mjs';
import { createFrameSequence } from '../../../runtime/scroll/frame-sequence.mjs';
import { observeScrollProgress, selectScrollMode } from '../../../runtime/scroll/scroll-progress.mjs';
import { frameCount as sampleFrameCount } from '../mobile-scroll/sequence-config.mjs';

const form = document.querySelector('#brief-form');
const prompt = document.querySelector('#video-prompt');
const promptStatus = document.querySelector('#prompt-status');
const mediaStatus = document.querySelector('#media-status');
const preview = document.querySelector('#preview');
const stage = document.querySelector('.preview-stage');
const canvas = document.querySelector('#sequence-canvas');
const video = document.querySelector('#background-video');
const poster = document.querySelector('#poster');
const motionToggle = document.querySelector('#motion-toggle');
const frameProgress = document.querySelector('#frame-progress');
const frameControl = document.querySelector('#frame-control');
const frameStatus = document.querySelector('#frame-status');
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const coarse = matchMedia('(pointer: coarse)');
let currentBrief;
let sequence;
let background;
let objectUrls = [];
let urls = [];
let progress = 0;
let paused = false;
let failed = false;
let importRevision = 0;

function renderPrompt() {
  const fields = Object.fromEntries(new FormData(form));
  fields.durationSeconds = Number(fields.durationSeconds);
  fields.frameCount = Number(fields.frameCount);
  const generated = buildVideoPrompts(fields);
  currentBrief = fields;
  prompt.value = generated.chatgpt;
  document.querySelector('#copy-prompt').disabled = false;
  promptStatus.textContent = `${generated.durationSeconds} saniye · ${generated.frameCount} kare · ${generated.mode === 'scroll' ? 'Scroll anlatımı' : 'Arka plan döngüsü'}`;
}
form.addEventListener('submit', event => {
  event.preventDefault();
  try { renderPrompt(); } catch (error) { promptStatus.textContent = error.message; }
});
document.querySelector('#copy-prompt').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(prompt.value);
    promptStatus.textContent = 'Prompt kopyalandı.';
  } catch {
    prompt.focus();
    prompt.select();
    promptStatus.textContent = 'Prompt seçildi; Ctrl+C ile kopyalayabilirsin.';
  }
});
document.querySelector('#download-brief').addEventListener('click', () => {
  try {
    renderPrompt();
    const downloadUrl = URL.createObjectURL(new Blob([JSON.stringify(currentBrief, null, 2) + '\n'], { type: 'application/json' }));
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = 'video-brief.json';
    link.click();
    setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);
  } catch (error) { promptStatus.textContent = error.message; }
});

async function loadSources() {
  const response = await fetch('../../../data/v6/creative_sources.json');
  if (!response.ok) throw new Error('Kaynak kataloğu yüklenemedi.');
  const catalog = await response.json();
  const filters = ['role', 'framework', 'scope'].map(field => [field, document.querySelector(`#source-${field}`)]);
  function renderSources() {
    const selected = selectCreativeSources(catalog, Object.fromEntries(filters.map(([field, control]) => [field, control.value])));
    const list = document.querySelector('#source-list');
    list.replaceChildren();
    for (const source of selected) {
      const article = document.createElement('article');
      article.className = 'source-entry';
      const title = document.createElement('h3');
      title.textContent = source.name;
      article.append(title);
      for (const [copy, className] of [[source.summary, ''], [source.nextStep, 'source-note'], [source.adaptation, 'source-note']]) {
        const paragraph = document.createElement('p');
        paragraph.textContent = copy;
        paragraph.className = className;
        article.append(paragraph);
      }
      const links = document.createElement('p');
      links.className = 'source-links';
      for (const [label, href] of [['Kaynağı aç ↗', source.url], [source.license, source.licenseUrl]]) {
        const link = document.createElement('a');
        link.textContent = label;
        link.href = href;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        links.append(link);
      }
      article.append(links);
      list.append(article);
    }
    if (!selected.length) list.textContent = 'Bu seçim için kaynak yok. Proje kullanımını veya farklı bir ihtiyacı seç.';
  }
  for (const [, control] of filters) control.addEventListener('change', renderSources);
  renderSources();
}

function releaseMedia() {
  sequence?.destroy();
  background?.destroy();
  sequence = null;
  background = null;
  for (const url of objectUrls) URL.revokeObjectURL(url);
  objectUrls = [];
  canvas.hidden = true;
  video.hidden = true;
  poster.hidden = false;
  canvas.dataset.frame = '';
  failed = false;
}

function motionMode() {
  return selectScrollMode({ width: innerWidth, height: innerHeight, reducedMotion: reduced.matches,
    saveData: navigator.connection?.saveData, coarsePointer: coarse.matches, paused }).mode;
}

function refreshMotion() {
  const staticMode = motionMode() === 'poster';
  preview.dataset.static = String(staticMode || failed);
  motionToggle.textContent = paused ? 'Hareketi sürdür' : 'Hareketi durdur';
  motionToggle.setAttribute('aria-pressed', String(paused));
  frameProgress.disabled = staticMode || failed || preview.dataset.mode !== 'sequence';
  if (background) {
    background.setPaused(paused || innerHeight < 480);
    return;
  }
  if (staticMode || failed) {
    sequence?.clear();
    canvas.hidden = true;
    poster.hidden = false;
    return;
  }
  if (sequence) void sequence.seek(progress);
}

function useSequence(sources, posterUrl) {
  urls = sources;
  poster.src = posterUrl;
  poster.alt = 'Kaydırma anlatımının ilk görüntüsü';
  preview.dataset.mode = 'sequence';
  frameControl.hidden = false;
  frameStatus.hidden = false;
  sequence = createFrameSequence({ canvas, urls, maxFrames: 5, maxDecodedBytes: 20_000_000, concurrency: 2,
    onFrame({ index }) {
      if (motionMode() === 'poster' || failed) return;
      canvas.dataset.frame = String(index);
      canvas.hidden = false;
      poster.hidden = true;
      frameStatus.textContent = `${index + 1} / ${urls.length}`;
    },
    onError(error) {
      if (failed) return;
      failed = true;
      mediaStatus.textContent = `${error.message} Sabit görüntü gösteriliyor; klasörü yeniden seçebilir veya lamba örneğine dönebilirsin.`;
      refreshMotion();
    },
  });
  progress = 0;
  frameProgress.value = '0';
  refreshMotion();
  scrollObserver.refresh();
}

function sampleSequence() {
  importRevision += 1;
  releaseMedia();
  useSequence(Array.from({ length: sampleFrameCount }, (_, index) => `../mobile-scroll/frames-3d/clay/mobile-${index}.webp`), '../mobile-scroll/frames-3d/clay/poster.webp');
  mediaStatus.textContent = `${sampleFrameCount} karelik lamba örneği hazır. Aşağı kaydır veya kare kontrolünü kullan.`;
}

const scrollObserver = observeScrollProgress({ section: preview, stage, onProgress({ progress: fraction, visible }) {
  if (preview.dataset.mode !== 'sequence' || motionMode() === 'poster' || failed || !visible) return;
  progress = fraction;
  frameProgress.value = String(Math.round(fraction * 100));
  void sequence?.seek(progress);
} });
frameProgress.addEventListener('input', () => {
  progress = Number(frameProgress.value) / 100;
  if (motionMode() !== 'poster' && !failed) void sequence?.seek(progress);
});
motionToggle.addEventListener('click', () => { paused = !paused; refreshMotion(); scrollObserver.refresh(); });
for (const query of [reduced, coarse]) query.addEventListener('change', refreshMotion);
navigator.connection?.addEventListener('change', refreshMotion);
window.addEventListener('resize', refreshMotion);
document.querySelector('#sample-sequence').addEventListener('click', sampleSequence);

document.querySelector('#sequence-files').addEventListener('change', async event => {
  const revision = ++importRevision;
  try {
    const files = [...event.target.files];
    const manifests = files.filter(file => file.name === 'manifest.json');
    if (manifests.length !== 1 || manifests[0].size > 100_000) throw new Error('Klasörde tek bir manifest.json olmalı (en fazla 100 KB).');
    const manifest = JSON.parse(await manifests[0].text());
    const selected = resolveSequenceFiles(manifest, files);
    if (revision !== importRevision) return;
    releaseMedia();
    objectUrls = [...selected.frames, selected.poster].map(file => URL.createObjectURL(file));
    useSequence(objectUrls.slice(0, -1), objectUrls.at(-1));
    mediaStatus.textContent = `${manifest.frameCount} yerel kare yüklendi. Kaydırarak incele; titreme ve nesne bozulmalarını kontrol et.`;
  } catch (error) {
    if (revision === importRevision) mediaStatus.textContent = error.message;
  }
});

async function videoPoster(videoUrl) {
  const probe = document.createElement('video');
  probe.muted = true;
  probe.preload = 'auto';
  try {
    await new Promise((resolve, reject) => {
      const timer = setTimeout(() => finish(new Error('Video önizlemesi zaman aşımına uğradı.')), 12_000);
      const finish = error => {
        clearTimeout(timer);
        probe.onloadeddata = null;
        probe.onerror = null;
        error ? reject(error) : resolve();
      };
      probe.onloadeddata = () => finish();
      probe.onerror = () => finish(new Error('Video çözümlenemedi. MP4 veya WebM kullan.'));
      probe.src = videoUrl;
    });
    if (!probe.videoWidth || !probe.videoHeight || probe.videoWidth > 4096 || probe.videoHeight > 4096) throw new Error('Video boyutları 4096 pikselin altında olmalı.');
    const snapshot = document.createElement('canvas');
    const scale = Math.min(1, 960 / Math.max(probe.videoWidth, probe.videoHeight));
    snapshot.width = Math.round(probe.videoWidth * scale);
    snapshot.height = Math.round(probe.videoHeight * scale);
    snapshot.getContext('2d').drawImage(probe, 0, 0, snapshot.width, snapshot.height);
    return await new Promise((resolve, reject) => snapshot.toBlob(blob => blob ? resolve(blob) : reject(new Error('Poster üretilemedi.')), 'image/webp', .8));
  } finally { probe.removeAttribute('src'); probe.load(); }
}

document.querySelector('#video-file').addEventListener('change', async event => {
  const selected = event.target.files[0];
  if (!selected) return;
  const revision = ++importRevision;
  let videoUrl;
  try {
    if (selected.size > 30_000_000 || !['video/mp4', 'video/webm', 'video/quicktime'].includes(selected.type)) throw new Error('30 MB altında bir MP4, WebM veya MOV seç.');
    videoUrl = URL.createObjectURL(selected);
    const snapshot = await videoPoster(videoUrl);
    if (revision !== importRevision) { URL.revokeObjectURL(videoUrl); return; }
    releaseMedia();
    const posterUrl = URL.createObjectURL(snapshot);
    objectUrls = [videoUrl, posterUrl];
    poster.src = posterUrl;
    poster.alt = 'Seçilen videonun ilk karesi';
    preview.dataset.mode = 'background';
    frameControl.hidden = true;
    frameStatus.hidden = true;
    video.hidden = false;
    background = createBackgroundVideo({ video, src: videoUrl, poster: posterUrl, onState(state) {
      preview.dataset.videoState = state;
      poster.hidden = state === 'playing';
      video.hidden = false;
      if (state === 'error') mediaStatus.textContent = 'Video oynatılamadı; poster gösteriliyor. Başka bir MP4 veya WebM seçebilirsin.';
    } });
    mediaStatus.textContent = `${selected.name} yerel arka plan olarak seçildi. Döngü birleşimini ve HTML metnin okunmasını kontrol et.`;
    refreshMotion();
  } catch (error) {
    if (videoUrl) URL.revokeObjectURL(videoUrl);
    if (revision === importRevision) mediaStatus.textContent = error.message;
  }
});

window.addEventListener('pagehide', () => { importRevision += 1; releaseMedia(); scrollObserver.destroy(); });
sampleSequence();
loadSources().catch(error => { document.querySelector('#source-list').textContent = error.message; });
