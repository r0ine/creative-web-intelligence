export function scrollProgress(sectionTop, sectionHeight, stageHeight, offset = 0) {
  if (![sectionTop, sectionHeight, stageHeight, offset].every(Number.isFinite)) {
    throw new TypeError('Kaydırma ölçüleri sonlu sayılar olmalı.');
  }
  if (sectionHeight < 0 || stageHeight < 0) {
    throw new RangeError('Bölüm ve sahne yüksekliği negatif olamaz.');
  }
  const distance = sectionHeight - stageHeight;
  if (distance <= 0) return sectionTop <= offset ? 1 : 0;
  return Math.max(0, Math.min(1, (offset - sectionTop) / distance));
}

export function selectScrollMode({ width, height, reducedMotion = false, saveData = false, paused = false, coarsePointer = false }) {
  if (![width, height].every(value => Number.isFinite(value) && value > 0)) {
    throw new RangeError('Ekran genişliği ve yüksekliği pozitif olmalı.');
  }
  if (reducedMotion) return { mode: 'poster', reason: 'reduced-motion' };
  if (saveData) return { mode: 'poster', reason: 'save-data' };
  if (paused) return { mode: 'poster', reason: 'paused' };
  if (height < 480) return { mode: 'poster', reason: 'short-viewport' };
  return { mode: width <= 760 || coarsePointer ? 'compact' : 'desktop', reason: 'scroll' };
}

export function observeScrollProgress({ section, stage = section, onProgress, window: view = globalThis.window }) {
  if (!section?.getBoundingClientRect || !stage?.getBoundingClientRect || typeof onProgress !== 'function') {
    throw new TypeError('Bölüm, sahne ve ilerleme callback’i gerekli.');
  }
  const document = view.document;
  let request = null;
  let disposed = false;

  function measure() {
    request = null;
    if (disposed || document.hidden) return;
    const bounds = section.getBoundingClientRect();
    const stageHeight = stage.getBoundingClientRect().height;
    const top = Number.parseFloat(view.getComputedStyle(stage).top) || 0;
    onProgress({
      progress: scrollProgress(bounds.top, bounds.height, stageHeight, top),
      visible: bounds.bottom > 0 && bounds.top < view.innerHeight,
    });
  }

  function refresh() {
    if (!disposed && !document.hidden && request === null) request = view.requestAnimationFrame(measure);
  }

  function visibilityChanged() {
    if (document.hidden && request !== null) {
      view.cancelAnimationFrame(request);
      request = null;
    }
    if (!document.hidden) refresh();
  }

  view.addEventListener('scroll', refresh, { passive: true });
  view.addEventListener('resize', refresh);
  view.visualViewport?.addEventListener('resize', refresh);
  document.addEventListener('visibilitychange', visibilityChanged);
  const observer = view.ResizeObserver ? new view.ResizeObserver(refresh) : null;
  observer?.observe(section);
  if (stage !== section) observer?.observe(stage);
  refresh();

  return {
    refresh,
    destroy() {
      if (disposed) return;
      disposed = true;
      if (request !== null) view.cancelAnimationFrame(request);
      view.removeEventListener('scroll', refresh);
      view.removeEventListener('resize', refresh);
      view.visualViewport?.removeEventListener('resize', refresh);
      document.removeEventListener('visibilitychange', visibilityChanged);
      observer?.disconnect();
    },
  };
}
