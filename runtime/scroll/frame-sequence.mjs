function abortError() {
  return new DOMException('Kare yükleme iptal edildi.', 'AbortError');
}

export async function loadBrowserFrame(url, { signal } = {}) {
  if (signal?.aborted) throw abortError();
  const response = await fetch(url, { signal });
  if (!response.ok) throw new Error(`Kare yüklenemedi: HTTP ${response.status}.`);
  const blob = await response.blob();
  if (signal?.aborted) throw abortError();

  if (typeof createImageBitmap === 'function' && blob.type !== 'image/svg+xml') {
    try {
      const bitmap = await createImageBitmap(blob);
      if (signal?.aborted) {
        bitmap.close();
        throw abortError();
      }
      return {
        width: bitmap.width,
        height: bitmap.height,
        image: bitmap,
        close: () => bitmap.close(),
      };
    } catch (error) {
      if (signal?.aborted || error.name === 'AbortError') throw error;
      if (typeof Image !== 'function') throw error;
    }
  }

  if (typeof Image !== 'function') throw new Error('Bu ortam görsel çözümlemeyi desteklemiyor.');
  return new Promise((resolve, reject) => {
    const image = new Image();
    const objectUrl = URL.createObjectURL(blob);
    const cleanup = () => {
      image.onload = null;
      image.onerror = null;
      signal?.removeEventListener('abort', cancel);
      URL.revokeObjectURL(objectUrl);
    };
    const cancel = () => {
      cleanup();
      image.src = '';
      reject(abortError());
    };
    image.onload = () => {
      cleanup();
      resolve({
        width: image.naturalWidth,
        height: image.naturalHeight,
        image,
        close: () => { image.src = ''; },
      });
    };
    image.onerror = () => {
      cleanup();
      image.src = '';
      reject(new Error(`Kare çözümlenemedi: ${url}`));
    };
    signal?.addEventListener('abort', cancel, { once: true });
    image.src = objectUrl;
    if (signal?.aborted) cancel();
  });
}

export function createFrameSequence({
  canvas,
  urls,
  maxFrames = 6,
  maxDecodedBytes = 24_000_000,
  preload = 2,
  concurrency = 2,
  loadFrame = loadBrowserFrame,
  onFrame = () => {},
  onError = () => {},
} = {}) {
  const context = canvas?.getContext?.('2d');
  if (!context?.drawImage) throw new TypeError('Kare dizisi için 2D canvas gerekiyor.');
  if (!Array.isArray(urls) || !urls.length || urls.some(url => typeof url !== 'string' || !url.trim())) {
    throw new TypeError('urls, boş olmayan görsel adresleri içeren bir dizi olmalı.');
  }
  for (const [name, value, minimum] of [['maxFrames', maxFrames, 1], ['preload', preload, 0], ['concurrency', concurrency, 1]]) {
    if (!Number.isInteger(value) || value < minimum) {
      throw new RangeError(`${name}, en az ${minimum} olan bir tam sayı olmalı.`);
    }
  }
  if (!Number.isFinite(maxDecodedBytes) || maxDecodedBytes <= 0) {
    throw new RangeError('maxDecodedBytes, sıfırdan büyük bir sayı olmalı.');
  }
  if ([loadFrame, onFrame, onError].some(callback => typeof callback !== 'function')) {
    throw new TypeError('loadFrame, onFrame ve onError birer işlev olmalı.');
  }

  const sources = [...urls];
  const cache = new Map();
  const active = new Map();
  let queue = [];
  let waiting = [];
  let generation = 0;
  let target = null;
  let displayedFrame = null;
  let decodedBytes = 0;
  let requests = 0;
  let destroyed = false;

  function report(error, index) {
    try {
      onError(error, { index, url: sources[index] });
    } catch {
      // Tüketici callback'i yükleme kuyruğunu kilitlememeli.
    }
  }

  function release(frame, index) {
    try {
      frame?.close?.();
    } catch (error) {
      report(error, index);
    }
  }

  function settle(rendered) {
    const listeners = waiting;
    waiting = [];
    for (const resolve of listeners) resolve(rendered);
  }

  function evict(index) {
    const entry = cache.get(index);
    cache.delete(index);
    decodedBytes -= entry.bytes;
    release(entry.frame, index);
  }

  function remember(index, frame, bytes) {
    if (bytes > maxDecodedBytes) return false;
    while (cache.size >= maxFrames || decodedBytes + bytes > maxDecodedBytes) {
      const candidates = [...cache.keys()].filter(key => key !== target);
      if (!candidates.length) return false;
      const farthest = candidates.reduce((a, b) => Math.abs(a - target) >= Math.abs(b - target) ? a : b);
      evict(farthest);
    }
    cache.set(index, { frame, bytes });
    decodedBytes += bytes;
    return true;
  }

  function draw(index, frame) {
    if (displayedFrame === index) return true;
    const composition = context.globalCompositeOperation;
    try {
      if (canvas.width !== frame.width) canvas.width = frame.width;
      if (canvas.height !== frame.height) canvas.height = frame.height;
      context.globalCompositeOperation = 'copy';
      context.drawImage(frame.image, 0, 0, frame.width, frame.height);
      displayedFrame = index;
    } catch (error) {
      report(error, index);
      if (cache.get(index)?.frame === frame) evict(index);
      return false;
    } finally {
      context.globalCompositeOperation = composition;
    }
    try {
      onFrame({ index, progress: sources.length === 1 ? 0 : index / (sources.length - 1), width: frame.width, height: frame.height });
    } catch (error) {
      report(error, index);
    }
    return true;
  }

  function cancel(job) {
    job.cancelled = true;
    job.controller.abort();
  }

  async function load(index, job) {
    let frame;
    let retained = false;
    try {
      frame = await loadFrame(sources[index], { signal: job.controller.signal });
      if (destroyed || job.cancelled || job.generation !== generation) return;
      const bytes = frame?.width * frame?.height * 4;
      if (!Number.isInteger(frame?.width) || frame.width < 1 || !Number.isInteger(frame?.height) || frame.height < 1 || !Number.isSafeInteger(bytes) || !frame.image) {
        throw new TypeError('Yüklenen karenin görseli ve geçerli piksel boyutları gerekiyor.');
      }
      retained = remember(index, frame, bytes);
      if (index === target) {
        const rendered = draw(index, frame);
        if (index === target && job.generation === generation) settle(rendered);
      }
    } catch (error) {
      if (!destroyed && !job.cancelled && job.generation === generation) {
        report(error, index);
        if (index === target && job.generation === generation) settle(false);
      }
    } finally {
      if (frame && !retained) release(frame, index);
      active.delete(index);
      if (!job.cancelled) queue = queue.filter(queued => queued !== index);
      pump();
    }
  }

  function pump() {
    if (destroyed) return;
    queue = queue.filter(index => !cache.has(index) && index !== displayedFrame);
    while (active.size < concurrency) {
      const next = queue.findIndex(index => !active.has(index));
      if (next === -1) return;
      const [index] = queue.splice(next, 1);
      const job = { controller: new AbortController(), generation, cancelled: false };
      active.set(index, job);
      requests += 1;
      void load(index, job);
    }
  }

  function seek(progress) {
    if (!Number.isFinite(progress)) throw new TypeError('Kaydırma ilerlemesi sonlu bir sayı olmalı.');
    if (destroyed) return Promise.resolve(false);
    const index = Math.round(Math.max(0, Math.min(1, progress)) * (sources.length - 1));
    if (target === index && displayedFrame === index) return Promise.resolve(true);
    if (target === index && waiting.length) return new Promise(resolve => waiting.push(resolve));

    const direction = target === null || index >= target ? 1 : -1;
    settle(false);
    target = index;
    const completion = new Promise(resolve => waiting.push(resolve));
    const desired = [index];
    for (let offset = 1; offset <= preload && desired.length < maxFrames; offset += 1) {
      for (const step of [direction, -direction]) {
        const neighbor = index + offset * step;
        if (neighbor >= 0 && neighbor < sources.length && desired.length < maxFrames) desired.push(neighbor);
      }
    }
    for (const [pendingIndex, job] of active) {
      if (!desired.includes(pendingIndex)) cancel(job);
    }
    queue = desired;
    const cached = cache.get(index);
    if (displayedFrame === index) settle(true);
    else if (cached) {
      const drawnGeneration = generation;
      const rendered = draw(index, cached.frame);
      if (index === target && generation === drawnGeneration) settle(rendered);
    }
    pump();
    return completion;
  }

  function clear() {
    generation += 1;
    target = null;
    displayedFrame = null;
    queue = [];
    settle(false);
    for (const job of active.values()) cancel(job);
    for (const index of cache.keys()) evict(index);
  }

  return {
    seek,
    clear,
    destroy() {
      if (destroyed) return;
      destroyed = true;
      clear();
    },
    get stats() {
      return { cachedFrames: cache.size, decodedBytes, pending: active.size, requests, displayedFrame };
    },
  };
}
