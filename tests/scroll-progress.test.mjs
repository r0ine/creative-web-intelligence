import assert from 'node:assert/strict';
import test from 'node:test';
import { observeScrollProgress, scrollProgress, selectScrollMode } from '../runtime/scroll/scroll-progress.mjs';

function eventSource() {
  const listeners = new Map();
  return {
    listeners,
    addEventListener(type, callback, options) {
      const entries = listeners.get(type) ?? new Map();
      entries.set(callback, options);
      listeners.set(type, entries);
    },
    removeEventListener(type, callback) {
      listeners.get(type)?.delete(callback);
    },
    emit(type) {
      for (const callback of listeners.get(type)?.keys() ?? []) callback();
    },
    listenerCount() {
      return [...listeners.values()].reduce((count, entries) => count + entries.size, 0);
    },
  };
}

function scrollHarness({ hidden = false, resizeObserver = true, visualViewport = true } = {}) {
  const frames = new Map();
  const cancelledFrames = [];
  const observers = [];
  const samples = [];
  let frameId = 0;
  const geometry = { top: 0, height: 1800, stageHeight: 600, stageTop: '0px', reads: 0 };
  const section = {
    getBoundingClientRect() {
      geometry.reads++;
      return { top: geometry.top, height: geometry.height, bottom: geometry.top + geometry.height };
    },
  };
  const stage = { getBoundingClientRect: () => ({ height: geometry.stageHeight }) };
  const document = { ...eventSource(), hidden };
  const viewport = {
    ...eventSource(),
    document,
    innerHeight: 800,
    getComputedStyle: () => ({ top: geometry.stageTop }),
    requestAnimationFrame(callback) {
      frames.set(++frameId, callback);
      return frameId;
    },
    cancelAnimationFrame(id) {
      const callback = frames.get(id);
      if (callback) cancelledFrames.push(callback);
      frames.delete(id);
    },
  };
  if (visualViewport) viewport.visualViewport = eventSource();
  if (resizeObserver) {
    viewport.ResizeObserver = class {
      targets = new Set();
      disconnected = false;
      constructor(callback) {
        this.notify = callback;
        observers.push(this);
      }
      observe(target) { this.targets.add(target); }
      disconnect() { this.disconnected = true; this.targets.clear(); }
    };
  }
  return {
    viewport, document, section, stage, geometry, frames, cancelledFrames, observers, samples,
    start(overrides = {}) {
      return observeScrollProgress({ section, stage, window: viewport, onProgress: sample => samples.push(sample), ...overrides });
    },
    flush() {
      const pending = [...frames.values()];
      frames.clear();
      for (const callback of pending) callback();
    },
  };
}

test('ilerleme bölümün sınırlarında 0 ve 1 arasında kalır', () => {
  assert.equal(scrollProgress(300, 1800, 600), 0);
  assert.equal(scrollProgress(0, 1800, 600), 0);
  assert.equal(scrollProgress(-600, 1800, 600), 0.5);
  assert.equal(scrollProgress(-1200, 1800, 600), 1);
  assert.equal(scrollProgress(-1500, 1800, 600), 1);
});

test('sabit sahnenin üst boşluğu ilerleme hesabına katılır', () => {
  assert.equal(scrollProgress(80, 1800, 600, 80), 0);
  assert.equal(scrollProgress(-520, 1800, 600, 80), 0.5);
  assert.equal(scrollProgress(-1120, 1800, 600, 80), 1);
  assert.equal(scrollProgress(-680, 1800, 600, -80), 0.5);
});

test('ters kaydırma önceki ilerleme değerlerine döner', () => {
  const positions = [0, -300, -600, -1200, -600, -300, 0];
  assert.deepEqual(positions.map(top => scrollProgress(top, 1800, 600)), [0, 0.25, 0.5, 1, 0.5, 0.25, 0]);
});

test('kaydırma mesafesi yoksa sahne eşiğinde doğrudan tamamlanır', () => {
  for (const height of [0, 400, 600]) {
    assert.equal(scrollProgress(65, height, 600, 64), 0);
    assert.equal(scrollProgress(64, height, 600, 64), 1);
    assert.equal(scrollProgress(-100, height, 600, 64), 1);
  }
});

test('geçersiz ölçüler sessizce ilerlemeye dönüştürülmez', () => {
  for (const value of [NaN, Infinity, -Infinity, '600', undefined, null]) {
    for (let index = 0; index < 4; index++) {
      const measures = [0, 1800, 600, 0];
      measures[index] = value;
      if (index === 3 && value === undefined) continue;
      assert.throws(() => scrollProgress(...measures), TypeError);
    }
  }
  assert.throws(() => scrollProgress(0, -1, 600), RangeError);
  assert.throws(() => scrollProgress(0, 1800, -1), RangeError);
});

test('hareket ve veri tercihleri ekran boyutundan önce gelir', () => {
  const screen = { width: 1200, height: 900 };
  assert.deepEqual(selectScrollMode({ ...screen, reducedMotion: true, saveData: true, paused: true }), { mode: 'poster', reason: 'reduced-motion' });
  assert.deepEqual(selectScrollMode({ ...screen, saveData: true, paused: true }), { mode: 'poster', reason: 'save-data' });
  assert.deepEqual(selectScrollMode({ ...screen, paused: true }), { mode: 'poster', reason: 'paused' });
  assert.deepEqual(selectScrollMode({ width: 390, height: 400, saveData: true }), { mode: 'poster', reason: 'save-data' });
});

test('dar ekran ve kaba işaretçi kompakt sahneyi seçer', () => {
  assert.deepEqual(selectScrollMode({ width: 760, height: 800 }), { mode: 'compact', reason: 'scroll' });
  assert.deepEqual(selectScrollMode({ width: 761, height: 800 }), { mode: 'desktop', reason: 'scroll' });
  assert.deepEqual(selectScrollMode({ width: 1400, height: 800, coarsePointer: true }), { mode: 'compact', reason: 'scroll' });
  assert.deepEqual(selectScrollMode({ width: 390, height: 480 }), { mode: 'compact', reason: 'scroll' });
  assert.deepEqual(selectScrollMode({ width: 1400, height: 479, coarsePointer: true }), { mode: 'poster', reason: 'short-viewport' });
});

test('ekran boyutları pozitif ve sonlu olmalı', () => {
  for (const value of [0, -1, NaN, Infinity, '390', undefined]) {
    assert.throws(() => selectScrollMode({ width: value, height: 800 }), RangeError);
    assert.throws(() => selectScrollMode({ width: 390, height: value, reducedMotion: true }), RangeError);
  }
});

test('gözlemci ilk ölçümü sonraki karede yapar ve kaydırmayı engellemez', () => {
  const harness = scrollHarness();
  const controller = harness.start();
  assert.equal(harness.samples.length, 0);
  assert.equal(harness.frames.size, 1);
  assert.equal([...harness.viewport.listeners.get('scroll').values()][0].passive, true);
  harness.flush();
  assert.deepEqual(harness.samples, [{ progress: 0, visible: true }]);
  assert.deepEqual(harness.observers[0].targets, new Set([harness.section, harness.stage]));
  controller.destroy();
});

test('aynı karedeki kaydırma olayları tek güncel ölçüm üretir', () => {
  const harness = scrollHarness();
  const controller = harness.start();
  harness.flush();
  harness.geometry.reads = 0;
  for (const top of [-100, -300, -600]) {
    harness.geometry.top = top;
    harness.viewport.emit('scroll');
  }
  controller.refresh();
  assert.equal(harness.frames.size, 1);
  assert.equal(harness.geometry.reads, 0);
  harness.flush();
  assert.equal(harness.geometry.reads, 1);
  assert.deepEqual(harness.samples.at(-1), { progress: 0.5, visible: true });
  controller.destroy();
});

test('boyut değişimleri bölüm, sahne ve üst boşluğun yeni ölçülerini kullanır', () => {
  const harness = scrollHarness();
  const controller = harness.start();
  harness.flush();
  harness.geometry.top = -600;
  harness.geometry.height = 2200;
  harness.geometry.stageHeight = 800;
  harness.geometry.stageTop = '100px';
  harness.viewport.emit('resize');
  harness.flush();
  assert.equal(harness.samples.at(-1).progress, 0.5);
  harness.geometry.stageHeight = 1000;
  harness.geometry.stageTop = 'auto';
  harness.viewport.visualViewport.emit('resize');
  harness.flush();
  assert.equal(harness.samples.at(-1).progress, 0.5);
  harness.geometry.height = 3400;
  harness.observers[0].notify();
  harness.flush();
  assert.equal(harness.samples.at(-1).progress, 0.25);
  controller.destroy();
});

test('görünürlük bölümün ekranla kesişmesini izler', () => {
  const harness = scrollHarness();
  const controller = harness.start();
  for (const [top, visible] of [[800, false], [799, true], [-1799, true], [-1800, false]]) {
    harness.geometry.top = top;
    controller.refresh();
    harness.flush();
    assert.equal(harness.samples.at(-1).visible, visible);
  }
  controller.destroy();
});

test('arka plana geçen belge bekleyen kareyi iptal eder ve dönüşte güncel ölçümü alır', () => {
  const harness = scrollHarness();
  const controller = harness.start();
  harness.document.hidden = true;
  harness.document.emit('visibilitychange');
  assert.equal(harness.frames.size, 0);
  for (const callback of harness.cancelledFrames) callback();
  harness.geometry.top = -900;
  harness.viewport.emit('scroll');
  harness.viewport.emit('resize');
  harness.viewport.visualViewport.emit('resize');
  harness.observers[0].notify();
  controller.refresh();
  assert.equal(harness.frames.size, 0);
  assert.equal(harness.samples.length, 0);
  assert.equal(harness.geometry.reads, 0);
  harness.document.hidden = false;
  harness.document.emit('visibilitychange');
  assert.equal(harness.frames.size, 1);
  harness.flush();
  assert.deepEqual(harness.samples, [{ progress: 0.75, visible: true }]);
  controller.destroy();
});

test('başlangıçta gizli belge görünene kadar iş planlamaz', () => {
  const harness = scrollHarness({ hidden: true });
  const controller = harness.start();
  assert.equal(harness.frames.size, 0);
  harness.document.hidden = false;
  harness.document.emit('visibilitychange');
  harness.flush();
  assert.equal(harness.samples.length, 1);
  controller.destroy();
});

test('belge kare çalışmadan gizlenirse callback çağrılmaz', () => {
  const harness = scrollHarness();
  const controller = harness.start();
  harness.document.hidden = true;
  harness.flush();
  assert.equal(harness.samples.length, 0);
  assert.equal(harness.geometry.reads, 0);
  controller.destroy();
});

test('kapatma dinleyicileri temizler ve geciken callbackleri etkisiz kılar', () => {
  const harness = scrollHarness();
  const controller = harness.start();
  controller.destroy();
  controller.destroy();
  assert.equal(harness.frames.size, 0);
  assert.equal(harness.viewport.listenerCount(), 0);
  assert.equal(harness.viewport.visualViewport.listenerCount(), 0);
  assert.equal(harness.document.listenerCount(), 0);
  assert.equal(harness.observers[0].disconnected, true);
  for (const callback of harness.cancelledFrames) callback();
  harness.observers[0].notify();
  harness.viewport.emit('scroll');
  harness.document.emit('visibilitychange');
  controller.refresh();
  harness.flush();
  assert.equal(harness.frames.size, 0);
  assert.equal(harness.samples.length, 0);
  assert.equal(harness.geometry.reads, 0);
});

test('isteğe bağlı tarayıcı APIleri yokken ölçüm ve kapatma çalışır', () => {
  const harness = scrollHarness({ resizeObserver: false, visualViewport: false });
  const controller = harness.start();
  harness.flush();
  harness.geometry.top = -600;
  harness.viewport.emit('resize');
  harness.flush();
  assert.equal(harness.samples.at(-1).progress, 0.5);
  controller.destroy();
  assert.equal(harness.viewport.listenerCount(), 0);
});

test('sahne belirtilmezse bölüm kullanılır ve bir kez gözlenir', () => {
  const harness = scrollHarness();
  harness.geometry.top = 1;
  const controller = harness.start({ stage: undefined });
  harness.flush();
  assert.equal(harness.samples.at(-1).progress, 0);
  assert.deepEqual(harness.observers[0].targets, new Set([harness.section]));
  harness.geometry.top = 0;
  controller.refresh();
  harness.flush();
  assert.equal(harness.samples.at(-1).progress, 1);
  controller.destroy();
});

test('eksik bölüm, sahne veya callback gözlemci kurulmadan reddedilir', () => {
  const harness = scrollHarness();
  for (const overrides of [{ section: null }, { stage: {} }, { onProgress: null }]) {
    assert.throws(() => harness.start(overrides), TypeError);
    assert.equal(harness.viewport.listenerCount(), 0);
    assert.equal(harness.frames.size, 0);
  }
});
