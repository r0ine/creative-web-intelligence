import assert from 'node:assert/strict';
import { setImmediate } from 'node:timers/promises';
import test from 'node:test';
import { createFrameSequence, loadBrowserFrame } from '../runtime/scroll/frame-sequence.mjs';

function frame(index, width = 10, height = 10) {
  return { width, height, image: { index }, closed: 0, close() { this.closed += 1; } };
}

function harness(options = {}) {
  const { ignoreAbort = false, ...settings } = options;
  const draws = [];
  const errors = [];
  const notifications = [];
  const jobs = [];
  const canvas = {
    width: 0,
    height: 0,
    getContext: () => ({ drawImage: (...args) => draws.push(args) }),
  };
  const sequence = createFrameSequence({
    canvas,
    urls: Array.from({ length: 10 }, (_, index) => `/frames/${index}.webp`),
    preload: 0,
    onError: (error, details) => errors.push({ error, ...details }),
    onFrame: details => notifications.push(details),
    loadFrame: (url, { signal }) => new Promise((resolve, reject) => {
      jobs.push({ url, signal, resolve, reject });
      if (!ignoreAbort) signal.addEventListener('abort', () => reject(new DOMException('İptal', 'AbortError')), { once: true });
    }),
    ...settings,
  });
  return { sequence, canvas, draws, errors, notifications, jobs };
}

test('ilk seek çağrısına kadar yükleme başlamaz; sınırlar ve ters kaydırma doğru kareyi seçer', async () => {
  const { sequence, jobs, draws, notifications, canvas } = harness();
  assert.deepEqual(sequence.stats, { cachedFrames: 0, decodedBytes: 0, pending: 0, requests: 0, displayedFrame: null });
  const start = sequence.seek(-2);
  assert.equal(jobs[0].url, '/frames/0.webp');
  jobs[0].resolve(frame(0, 320, 180));
  assert.equal(await start, true);
  assert.equal(canvas.width, 320);
  assert.equal(canvas.height, 180);
  assert.deepEqual(draws[0], [{ index: 0 }, 0, 0, 320, 180]);
  const end = sequence.seek(7);
  jobs[1].resolve(frame(9));
  assert.equal(await end, true);
  assert.equal(sequence.stats.displayedFrame, 9);
  assert.equal(await sequence.seek(0), true);
  assert.equal(jobs.length, 2);
  const middle = sequence.seek(0.5);
  assert.equal(jobs[2].url, '/frames/5.webp');
  jobs[2].resolve(frame(5));
  assert.equal(await middle, true);
  assert.deepEqual(notifications.map(({ index }) => index), [0, 9, 0, 5]);
  sequence.destroy();
});

test('aynı kare için bekleyen çağrılar tek yüklemeyi paylaşır; çizilmiş kare tekrar çizilmez', async () => {
  const { sequence, jobs, draws } = harness();
  const first = sequence.seek(0.1);
  const second = sequence.seek(0.11);
  assert.equal(jobs.length, 1);
  jobs[0].resolve(frame(1));
  assert.deepEqual(await Promise.all([first, second]), [true, true]);
  assert.equal(await sequence.seek(0.12), true);
  assert.equal(draws.length, 1);
  sequence.destroy();
});

test('hızlı sıçramada yeni hedef sıranın başına geçer ve eski komşular yüklenmez', async () => {
  const { sequence, jobs, draws, errors } = harness({ concurrency: 1, preload: 2 });
  const first = sequence.seek(0);
  const last = sequence.seek(1);
  assert.equal(await first, false);
  await setImmediate();
  assert.deepEqual(jobs.map(job => job.url), ['/frames/0.webp', '/frames/9.webp']);
  assert.equal(jobs[0].signal.aborted, true);
  jobs[1].resolve(frame(9));
  assert.equal(await last, true);
  assert.equal(jobs[2].url, '/frames/8.webp');
  jobs[2].resolve(frame(8));
  await setImmediate();
  assert.equal(jobs[3].url, '/frames/7.webp');
  jobs[3].resolve(frame(7));
  await setImmediate();
  assert.equal(jobs.length, 4);
  assert.equal(sequence.stats.pending, 0);
  assert.deepEqual(draws.map(([image]) => image.index), [9]);
  assert.deepEqual(errors, []);
  sequence.destroy();
});

test('iptali yok sayan yükleyici eşzamanlı istek sınırını aşamaz', async () => {
  const { sequence, jobs, draws } = harness({ ignoreAbort: true, concurrency: 2, preload: 1 });
  const first = sequence.seek(0);
  const last = sequence.seek(1);
  assert.equal(await first, false);
  assert.equal(jobs.length, 2);
  assert.equal(sequence.stats.pending, 2);
  const stale = frame(0);
  jobs[0].resolve(stale);
  await setImmediate();
  assert.equal(stale.closed, 1);
  assert.equal(jobs[2].url, '/frames/9.webp');
  assert.equal(sequence.stats.pending, 2);
  jobs[2].resolve(frame(9));
  assert.equal(await last, true);
  assert.deepEqual(draws.map(([image]) => image.index), [9]);
  sequence.destroy();
  jobs[1].resolve(frame(1));
  jobs[3]?.resolve(frame(8));
  await setImmediate();
  assert.equal(sequence.stats.pending, 0);
});

test('ön yükleme iki yöne yayılır ve frame sayısı sınırında durur', async () => {
  const { sequence, jobs } = harness({ preload: 20, maxFrames: 3, concurrency: 1 });
  const selected = sequence.seek(0.5);
  jobs[0].resolve(frame(5));
  await selected;
  jobs[1].resolve(frame(6));
  await setImmediate();
  jobs[2].resolve(frame(4));
  await setImmediate();
  assert.deepEqual(jobs.map(job => job.url), ['/frames/5.webp', '/frames/6.webp', '/frames/4.webp']);
  assert.equal(sequence.stats.cachedFrames, 3);
  sequence.destroy();
});

test('cache hem kare sayısını hem çözülmüş byte bütçesini uygular ve çıkardığı kareyi kapatır', async () => {
  const { sequence, jobs } = harness({ maxFrames: 2, maxDecodedBytes: 800 });
  const loaded = [];
  for (let index = 0; index < 3; index += 1) {
    const selected = sequence.seek(index / 9);
    loaded.push(frame(index));
    jobs[index].resolve(loaded[index]);
    assert.equal(await selected, true);
    assert.ok(sequence.stats.cachedFrames <= 2);
    assert.ok(sequence.stats.decodedBytes <= 800);
  }
  assert.equal(loaded[0].closed, 1);
  assert.equal(loaded[1].closed, 0);
  sequence.destroy();
  assert.equal(loaded[1].closed, 1);
  assert.equal(loaded[2].closed, 1);
  assert.equal(sequence.stats.decodedBytes, 0);
});

test('komşu kare cache bütçesi doluyken seçili kareyi dışarı atmaz', async () => {
  const { sequence, jobs } = harness({ preload: 1, maxDecodedBytes: 400 });
  const selected = sequence.seek(0);
  const target = frame(0);
  const neighbor = frame(1);
  jobs[0].resolve(target);
  assert.equal(await selected, true);
  jobs[1].resolve(neighbor);
  await setImmediate();
  assert.equal(sequence.stats.cachedFrames, 1);
  assert.equal(sequence.stats.decodedBytes, 400);
  assert.equal(target.closed, 0);
  assert.equal(neighbor.closed, 1);
  sequence.destroy();
});

test('tek kare bütçeden büyükse çizilir, cache dışında serbest bırakılır', async () => {
  const { sequence, jobs, draws } = harness({ maxDecodedBytes: 100 });
  const selected = sequence.seek(0);
  const oversized = frame(0);
  jobs[0].resolve(oversized);
  assert.equal(await selected, true);
  assert.equal(oversized.closed, 1);
  assert.equal(sequence.stats.cachedFrames, 0);
  assert.equal(sequence.stats.decodedBytes, 0);
  assert.equal(await sequence.seek(0), true);
  assert.equal(draws.length, 1);
  assert.equal(jobs.length, 1);
  sequence.destroy();
});

test('clear geç gelen kareyi kapatır, eski seek sonucunu iptal eder ve yeniden yüklemeye izin verir', async () => {
  const { sequence, jobs, draws } = harness({ ignoreAbort: true, concurrency: 1 });
  const oldSeek = sequence.seek(0);
  sequence.clear();
  assert.equal(await oldSeek, false);
  assert.equal(jobs[0].signal.aborted, true);
  const newSeek = sequence.seek(0);
  const stale = frame(0);
  jobs[0].resolve(stale);
  await setImmediate();
  assert.equal(stale.closed, 1);
  assert.equal(draws.length, 0);
  assert.equal(sequence.stats.cachedFrames, 0);
  assert.equal(jobs.length, 2);
  jobs[1].resolve(frame(0));
  assert.equal(await newSeek, true);
  sequence.destroy();
});

test('destroy geç gelen görseli cache veya canvas üzerine taşımaz; sonraki seek false döner', async () => {
  const { sequence, jobs, draws, errors } = harness({ ignoreAbort: true });
  const selected = sequence.seek(0.5);
  sequence.destroy();
  sequence.destroy();
  assert.equal(await selected, false);
  assert.equal(await sequence.seek(0.9), false);
  const late = frame(5);
  jobs[0].resolve(late);
  await setImmediate();
  assert.equal(late.closed, 1);
  assert.equal(draws.length, 0);
  assert.equal(sequence.stats.cachedFrames, 0);
  assert.equal(sequence.stats.pending, 0);
  assert.deepEqual(errors, []);
});

test('yükleme hatası son sağlam kareyi korur, hata ayrıntısı verir ve tekrar denenebilir', async () => {
  const { sequence, jobs, draws, errors } = harness();
  const first = sequence.seek(0);
  jobs[0].resolve(frame(0));
  await first;
  const missing = sequence.seek(1);
  jobs[1].reject(new Error('Dosya bulunamadı.'));
  assert.equal(await missing, false);
  assert.equal(sequence.stats.displayedFrame, 0);
  assert.equal(draws.length, 1);
  assert.equal(errors[0].index, 9);
  assert.equal(errors[0].url, '/frames/9.webp');
  const retry = sequence.seek(1);
  jobs[2].resolve(frame(9));
  assert.equal(await retry, true);
  sequence.destroy();
});

test('hatalı decode boyutları reddedilir ve görsel serbest bırakılır', async () => {
  const { sequence, jobs, errors } = harness();
  const selected = sequence.seek(0);
  const invalid = frame(0, 0, 10);
  jobs[0].resolve(invalid);
  assert.equal(await selected, false);
  assert.equal(invalid.closed, 1);
  assert.match(errors[0].error.message, /piksel boyutları/);
  assert.equal(sequence.stats.cachedFrames, 0);
  sequence.destroy();
});

test('tüketici callback hatası yükleme kuyruğunu kilitlemez', async () => {
  const { sequence, jobs } = harness({ onFrame: () => { throw new Error('Callback hatası'); }, onError: () => { throw new Error('Hata callback hatası'); } });
  const selected = sequence.seek(0);
  jobs[0].resolve(frame(0));
  assert.equal(await selected, true);
  assert.equal(sequence.stats.pending, 0);
  sequence.destroy();
});

test('onFrame içinden yeni seek çağrısı yeni hedefi erken tamamlamaz', async () => {
  let next;
  const { sequence, jobs } = harness({
    onFrame: ({ index }) => {
      if (index === 0) next = sequence.seek(1);
    },
  });
  const first = sequence.seek(0);
  jobs[0].resolve(frame(0));
  assert.equal(await first, false);
  assert.equal(sequence.stats.displayedFrame, 0);
  let settled = false;
  next.then(() => { settled = true; });
  await setImmediate();
  assert.equal(settled, false);
  jobs[1].resolve(frame(9));
  assert.equal(await next, true);
  assert.equal(sequence.stats.displayedFrame, 9);
  sequence.destroy();
});

test('canvas çizimi hata verirse kare cache üzerinden tekrar kullanılmaz', async () => {
  let shouldFail = true;
  const { sequence, jobs, errors } = harness({
    canvas: {
      width: 10,
      height: 10,
      getContext: () => ({ drawImage() { if (shouldFail) throw new Error('Görsel çizilemedi.'); } }),
    },
  });
  const selected = sequence.seek(0);
  const broken = frame(0);
  jobs[0].resolve(broken);
  assert.equal(await selected, false);
  assert.equal(sequence.stats.cachedFrames, 0);
  assert.equal(broken.closed, 1);
  assert.equal(errors.length, 1);
  shouldFail = false;
  const retry = sequence.seek(0);
  jobs[1].resolve(frame(0));
  assert.equal(await retry, true);
  sequence.destroy();
});

test('geçersiz girişler açıklamalı Türkçe hata verir', () => {
  assert.throws(() => createFrameSequence(), /2D canvas/);
  assert.throws(() => harness({ urls: [] }), /görsel adresleri/);
  assert.throws(() => harness({ urls: [''] }), /görsel adresleri/);
  assert.throws(() => harness({ maxFrames: 0 }), /maxFrames/);
  assert.throws(() => harness({ concurrency: 1.5 }), /concurrency/);
  assert.throws(() => harness({ preload: -1 }), /preload/);
  assert.throws(() => harness({ maxDecodedBytes: Infinity }), /maxDecodedBytes/);
  assert.throws(() => harness({ loadFrame: null }), /birer işlev/);
  const { sequence } = harness();
  assert.throws(() => sequence.seek(NaN), /sonlu bir sayı/);
  assert.throws(() => sequence.seek('0.5'), /sonlu bir sayı/);
  sequence.destroy();
});

test('varsayılan yükleyici HTTP hatasını decode işleminden önce reddeder', async t => {
  t.mock.method(globalThis, 'fetch', async () => ({ ok: false, status: 404 }));
  await assert.rejects(loadBrowserFrame('/frames/missing.webp'), /HTTP 404/);
});

test('varsayılan yükleyici başlamadan iptal edilen isteği göndermez', async t => {
  const fetchMock = t.mock.method(globalThis, 'fetch', async () => { throw new Error('Çağrılmamalı'); });
  const controller = new AbortController();
  controller.abort();
  await assert.rejects(loadBrowserFrame('/frames/0.webp', { signal: controller.signal }), { name: 'AbortError' });
  assert.equal(fetchMock.mock.callCount(), 0);
});

test('bitmap decode sırasında iptal edilirse açılan bitmap kapanır', async t => {
  const descriptor = Object.getOwnPropertyDescriptor(globalThis, 'createImageBitmap');
  let finish;
  const bitmap = frame(0);
  globalThis.createImageBitmap = () => new Promise(resolve => { finish = resolve; });
  t.after(() => {
    if (descriptor) Object.defineProperty(globalThis, 'createImageBitmap', descriptor);
    else delete globalThis.createImageBitmap;
  });
  t.mock.method(globalThis, 'fetch', async () => ({ ok: true, blob: async () => new Blob(['pixels'], { type: 'image/webp' }) }));
  const controller = new AbortController();
  const loading = loadBrowserFrame('/frames/0.webp', { signal: controller.signal });
  await setImmediate();
  controller.abort();
  finish(bitmap);
  await assert.rejects(loading, { name: 'AbortError' });
  assert.equal(bitmap.closed, 1);
});

test('SVG image fallback blob adresini bırakır; abort görsel kaynağını da temizler', async t => {
  const descriptor = Object.getOwnPropertyDescriptor(globalThis, 'Image');
  const images = [];
  globalThis.Image = class {
    constructor() {
      this.naturalWidth = 240;
      this.naturalHeight = 160;
      images.push(this);
    }
  };
  t.after(() => {
    if (descriptor) Object.defineProperty(globalThis, 'Image', descriptor);
    else delete globalThis.Image;
  });
  t.mock.method(globalThis, 'fetch', async () => ({ ok: true, blob: async () => new Blob(['<svg/>'], { type: 'image/svg+xml' }) }));
  t.mock.method(URL, 'createObjectURL', () => 'blob:frame');
  const revoke = t.mock.method(URL, 'revokeObjectURL', () => {});
  const loading = loadBrowserFrame('/frames/0.svg');
  await setImmediate();
  assert.equal(images[0].src, 'blob:frame');
  images[0].onload();
  const loaded = await loading;
  assert.equal(loaded.width, 240);
  assert.equal(loaded.height, 160);
  assert.equal(revoke.mock.callCount(), 1);
  loaded.close();
  assert.equal(images[0].src, '');

  const controller = new AbortController();
  const cancelled = loadBrowserFrame('/frames/1.svg', { signal: controller.signal });
  await setImmediate();
  controller.abort();
  await assert.rejects(cancelled, { name: 'AbortError' });
  assert.equal(images[1].src, '');
  assert.equal(images[1].onload, null);
  assert.equal(revoke.mock.callCount(), 2);
});
