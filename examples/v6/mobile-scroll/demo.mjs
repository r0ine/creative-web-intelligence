import { observeScrollProgress, selectScrollMode } from '../../../runtime/scroll/scroll-progress.mjs';
import { createFrameSequence } from '../../../runtime/scroll/frame-sequence.mjs';
import { frameCount } from './sequence-config.mjs';

const section = document.querySelector('.story');
const stage = document.querySelector('.stage');
const visual = document.querySelector('.visual');
let sceneCanvas = document.querySelector('#scene-canvas');
const sequenceCanvas = document.querySelector('#sequence-canvas');
const poster = document.querySelector('.poster');
const toggle = document.querySelector('#motion-toggle');
const note = document.querySelector('#mode-note');
const phaseLabel = document.querySelector('#phase-label');
const scrub = document.querySelector('#story-scrub');
const scrubControl = document.querySelector('.scrub-control');
const finishes = document.querySelector('.finishes');
const angleControl = document.querySelector('.view-control');
const angle = document.querySelector('#view-angle');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const coarsePointer = matchMedia('(pointer: coarse)');
const connection = navigator.connection;
const root = document.documentElement;
let scene;
let player;
let observer;
let paused = false;
let policyKey = '';
let progress = 0;
let finish = 'clay';
let generation = 0;
let webglFailed = false;
let sequenceFailed = false;
let visible = false;

const reasons = {
  'reduced-motion': 'Hareket azaltma tercihin açık. Nesneyi sabit görsellerle inceleyebilirsin.',
  'save-data': 'Veri tasarrufu açık. Yalnızca sabit görseller yüklenir.',
  'paused': 'Hareket kapalı. Parçalar üç sabit görünümde gösteriliyor.',
  'short-viewport': 'Bu ekran yüksekliğinde görseller doğal sayfa akışında gösteriliyor.',
};

function recordScene() {
  if (!scene) return;
  const stats = scene.stats;
  for (const key of ['progress', 'finish', 'viewAngle', 'renderCount', 'drawCalls', 'triangles']) {
    sceneCanvas.dataset[key] = String(stats[key]);
  }
}

function renderProgress() {
  if (!visible || document.hidden) return;
  scene?.setProgress(progress);
  recordScene();
  player?.seek(progress);
}

function resizeScene() {
  if (!scene || document.hidden) return;
  const { width, height } = visual.getBoundingClientRect();
  const stats = scene.stats;
  if (width > 0 && height > 0 && (Math.round(width) !== stats.width || Math.round(height) !== stats.height)) {
    scene.resize(width, height);
    recordScene();
  }
}

function releaseRenderer() {
  if (scene) {
    scene.destroy();
    // A released WebGL context cannot be reused when motion is enabled again.
    const replacement = sceneCanvas.cloneNode(false);
    for (const key of Object.keys(replacement.dataset)) delete replacement.dataset[key];
    sceneCanvas.replaceWith(replacement);
    sceneCanvas = replacement;
  }
  player?.destroy();
  scene = null;
  player = null;
  sceneCanvas.hidden = true;
  sequenceCanvas.hidden = true;
  sequenceCanvas.removeAttribute('data-frame');
  angleControl.hidden = true;
  root.dataset.renderer = 'poster';
}

function startSequence(token) {
  if (token !== generation) return;
  scene?.destroy();
  scene = null;
  player?.destroy();
  sceneCanvas.hidden = true;
  sequenceCanvas.hidden = true;
  sequenceCanvas.removeAttribute('data-frame');
  angleControl.hidden = true;
  root.dataset.renderer = 'sequence';
  note.textContent = root.dataset.motion === 'compact'
    ? 'Kaydır, parçaları keşfet. Yüzey rengini aşağıdan seçebilirsin.'
    : 'Kaydırarak parçaları inceleyebilirsin. Bu cihazda hazır 3D kareler gösteriliyor.';
  const sequenceFinish = finish;
  player = createFrameSequence({
    canvas: sequenceCanvas,
    urls: Array.from({ length: frameCount }, (_, index) => new URL(`./frames-3d/${sequenceFinish}/mobile-${index}.webp`, import.meta.url).href),
    maxFrames: 4,
    maxDecodedBytes: 8_000_000,
    preload: 1,
    concurrency: 2,
    onFrame({ index, progress: frameProgress }) {
      if (token !== generation || sequenceFinish !== finish) return;
      sequenceCanvas.hidden = false;
      sequenceCanvas.dataset.frame = String(index);
      sequenceCanvas.dataset.progress = String(frameProgress);
      sequenceCanvas.dataset.finish = sequenceFinish;
    },
    onError() {
      if (token !== generation || sequenceFinish !== finish) return;
      sequenceFailed = true;
      generation++;
      releaseRenderer();
      root.dataset.motion = 'poster';
      phaseLabel.textContent = 'Bir bütün';
      note.textContent = 'Hareketli görünüm yüklenemedi. Nesneyi sabit görsellerle inceleyebilirsin.';
      toggle.textContent = 'Hareketi yeniden dene';
      observer?.refresh();
    },
  });
  renderProgress();
}

async function updatePolicy() {
  const policy = selectScrollMode({
    width: innerWidth,
    height: innerHeight,
    reducedMotion: reducedMotion.matches,
    coarsePointer: coarsePointer.matches,
    saveData: connection?.saveData === true,
    paused,
  });
  const key = `${policy.mode}:${policy.reason}`;
  if (key === policyKey) {
    resizeScene();
    return;
  }
  policyKey = key;
  sequenceFailed = false;
  const token = ++generation;
  releaseRenderer();
  root.dataset.motion = policy.mode;
  toggle.hidden = false;
  finishes.hidden = false;
  scrubControl.hidden = policy.mode === 'poster';
  scrub.disabled = policy.mode === 'poster';
  toggle.disabled = policy.mode === 'poster' && policy.reason !== 'paused';
  toggle.textContent = paused ? 'Hareketi aç' : 'Hareketi durdur';
  toggle.setAttribute('aria-pressed', String(paused));
  phaseLabel.textContent = 'Bir bütün';
  note.textContent = reasons[policy.reason] ?? 'Sahne hazırlanıyor.';
  observer?.refresh();
  if (policy.mode === 'poster') return;
  if (policy.mode === 'compact' || webglFailed) {
    startSequence(token);
    return;
  }
  try {
    const { createLampScene } = await import('../../../runtime/three/lamp-scene.mjs');
    if (token !== generation) return;
    scene = createLampScene({
      canvas: sceneCanvas,
      onError() {
        if (token !== generation) return;
        webglFailed = true;
        // The renderer may report an error during its own render call.
        queueMicrotask(() => startSequence(token));
      },
    });
    scene.setFinish(finish);
    scene.setView(Number(angle.value));
    resizeScene();
    if (webglFailed) return;
    sceneCanvas.hidden = false;
    angleControl.hidden = false;
    root.dataset.renderer = 'webgl';
    note.textContent = 'Kaydırarak parçaları aç. Rengi ve bakış açısını sen seç.';
    renderProgress();
    observer?.refresh();
  } catch {
    if (token !== generation) return;
    webglFailed = true;
    startSequence(token);
  }
}

observer = observeScrollProgress({
  section,
  stage,
  onProgress(snapshot) {
    visible = snapshot.visible;
    progress = snapshot.progress;
    if (root.dataset.motion === 'compact') {
      const distance = section.getBoundingClientRect().height - stage.getBoundingClientRect().height;
      const introHeight = document.querySelector('.intro').getBoundingClientRect().height;
      progress = Math.max(0, Math.min(1, (progress * distance - introHeight) / Math.max(1, distance - introHeight)));
    }
    const phase = progress < 0.12 ? 'Bir bütün' : progress < 0.38 ? 'Parçalar ayrılıyor'
      : progress < 0.60 ? 'İç bağlantı' : progress < 0.82 ? 'Yeniden bir arada' : 'Işık açık';
    phaseLabel.textContent = root.dataset.motion === 'poster' ? 'Bir bütün' : phase;
    if (root.dataset.motion !== 'poster') {
      scrub.value = String(Math.round(progress * 100));
      scrub.setAttribute('aria-valuetext', phase);
    }
    renderProgress();
  },
});

scrub.addEventListener('input', () => {
  const bounds = section.getBoundingClientRect();
  const distance = Math.max(0, bounds.height - stage.getBoundingClientRect().height);
  const introHeight = root.dataset.motion === 'compact' ? document.querySelector('.intro').getBoundingClientRect().height : 0;
  const offset = Number.parseFloat(getComputedStyle(stage).top) || 0;
  const target = scrollY + bounds.top - offset + introHeight + Math.max(0, distance - introHeight) * Number(scrub.value) / 100;
  window.scrollTo(0, Math.max(0, target));
});

finishes.addEventListener('click', event => {
  const button = event.target.closest('[data-finish]');
  if (!button || button.dataset.finish === finish) return;
  finish = button.dataset.finish;
  for (const option of finishes.querySelectorAll('button')) {
    option.setAttribute('aria-pressed', String(option === button));
  }
  poster.src = `./frames-3d/${finish}/poster.webp`;
  const finishName = { clay: 'kil', forest: 'orman yeşili', chalk: 'tebeşir' }[finish];
  poster.alt = `Kavisli ${finishName} rengi başlığı ve ince gövdesiyle üç boyutlu masa lambası.`;
  for (const [index, image] of [...document.querySelectorAll('.static-step')].entries()) {
    image.src = `./frames-3d/${finish}/step-${index}.webp`;
  }
  if (scene) {
    scene.setFinish(finish);
    recordScene();
  } else if (player) {
    startSequence(++generation);
  }
});
angle.addEventListener('input', () => {
  scene?.setView(Number(angle.value));
  recordScene();
});
toggle.addEventListener('click', () => {
  if (sequenceFailed) policyKey = '';
  else paused = !paused;
  updatePolicy();
});
reducedMotion.addEventListener('change', updatePolicy);
coarsePointer.addEventListener('change', updatePolicy);
connection?.addEventListener('change', updatePolicy);
window.addEventListener('resize', updatePolicy);
const resizeObserver = new ResizeObserver(resizeScene);
resizeObserver.observe(visual);
document.addEventListener('visibilitychange', () => {
  if (document.hidden) player?.clear();
  else {
    resizeScene();
    observer.refresh();
  }
});
window.addEventListener('pagehide', () => {
  generation++;
  releaseRenderer();
});
window.addEventListener('pageshow', event => {
  if (event.persisted) {
    policyKey = '';
    updatePolicy();
  }
  observer.refresh();
});
updatePolicy();
