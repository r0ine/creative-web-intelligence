const assert = require('node:assert/strict');
const { mkdir } = require('node:fs/promises');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');
const sharp = require('sharp');

const demoUrl = new URL(process.argv[2] ?? 'http://127.0.0.1:22222/examples/v6/mobile-scroll/');
if (!['http:', 'https:'].includes(demoUrl.protocol)) throw new Error('Örnek adresi HTTP veya HTTPS kullanmalı.');
const screenshotDir = process.env.CWI_SCREENSHOT_DIR ? path.resolve(process.env.CWI_SCREENSHOT_DIR) : null;
const chapterTitles = ['Her parçanınbir yeri var.', 'Görünmeyenbağlantı.', 'Ve her şeyyerine oturur.'];
let completed = 0;
let frameCount;

async function waitMode(page, motion, renderer) {
  await page.waitForFunction(expected => {
    const state = document.documentElement.dataset;
    return state.motion === expected.motion && (!expected.renderer || state.renderer === expected.renderer);
  }, { motion, renderer });
}

async function seek(page, progress) {
  await page.evaluate(fraction => {
    const section = document.querySelector('.story');
    const stage = document.querySelector('.stage');
    const bounds = section.getBoundingClientRect();
    const distance = Math.max(0, bounds.height - stage.getBoundingClientRect().height);
    const offset = Number.parseFloat(getComputedStyle(stage).top) || 0;
    const introHeight = document.documentElement.dataset.motion === 'compact'
      ? document.querySelector('.intro').getBoundingClientRect().height : 0;
    window.scrollTo(0, scrollY + bounds.top - offset + introHeight + (distance - introHeight) * fraction);
  }, progress);
  await page.waitForFunction(({ expected, count }) => {
    const renderer = document.documentElement.dataset.renderer;
    const canvas = document.querySelector(renderer === 'webgl' ? '#scene-canvas' : '#sequence-canvas');
    if (canvas.hidden) return false;
    if (renderer === 'sequence') return Number(canvas.dataset.frame) === Math.round(expected * (count - 1));
    return Math.abs(Number(canvas.dataset.progress) - expected) < 0.003;
  }, { expected: progress, count: frameCount });
}

async function assertNoOverflow(page) {
  const dimensions = await page.evaluate(() => ({
    viewport: document.documentElement.clientWidth,
    document: document.documentElement.scrollWidth,
    body: document.body.scrollWidth,
  }));
  assert.ok(dimensions.document <= dimensions.viewport, `Sayfa yatay taşıyor: ${JSON.stringify(dimensions)}`);
  assert.ok(dimensions.body <= dimensions.viewport, `İçerik yatay taşıyor: ${JSON.stringify(dimensions)}`);
}

async function assertPoster(page) {
  await waitMode(page, 'poster', 'poster');
  await page.waitForFunction(() => {
    const poster = document.querySelector('.poster');
    return poster.complete && poster.naturalWidth > 0;
  });
  assert.equal(await page.locator('.poster').isVisible(), true, 'Sabit görüntü görünmeli.');
  for (const canvas of await page.locator('canvas').all()) {
    assert.equal(await canvas.isVisible(), false, 'Hareket kapalıyken canvas görünmemeli.');
  }
  assert.notEqual(await page.locator('.stage').evaluate(stage => getComputedStyle(stage).position), 'sticky', 'Sabit görüntüler doğal akışta kalmalı.');
  assert.deepEqual(await page.locator('.chapter h2').allTextContents(), chapterTitles);
  for (const chapter of await page.locator('.chapter').all()) {
    assert.equal(await chapter.isVisible(), true, 'Bölüm metni görünmeli.');
    assert.equal(await chapter.locator('.static-step').isVisible(), true, 'Bölüm görüntüsü görünmeli.');
  }
  await assertNoOverflow(page);
}

async function snapshot(page, name) {
  if (screenshotDir) await page.screenshot({ path: path.join(screenshotDir, `${name}.png`) });
}

async function imagePixels(page, selector) {
  const image = await page.locator(selector).screenshot();
  return sharp(image).resize(240, 240, { fit: 'fill' }).removeAlpha().raw().toBuffer();
}

function assertImageChanged(before, after, action) {
  assert.equal(before.length, after.length);
  let difference = 0;
  let changed = 0;
  for (let index = 0; index < before.length; index++) {
    const delta = Math.abs(before[index] - after[index]);
    difference += delta;
    if (delta > 8) changed++;
  }
  assert.ok(difference / before.length > 0.3 && changed / before.length > 0.01, `${action}: sahne pikselleri değişmeli.`);
}

async function assertRenderedScene(page) {
  const canvas = page.locator('#scene-canvas');
  await page.waitForFunction(() => Number(document.querySelector('#scene-canvas').dataset.renderCount) > 0);
  const stats = await canvas.evaluate(element => ({ ...element.dataset }));
  assert.ok(Number(stats.drawCalls) > 0 && Number(stats.drawCalls) <= 30, `3D çizim çağrısı bütçesi: ${stats.drawCalls}`);
  assert.ok(Number(stats.triangles) > 1000 && Number(stats.triangles) <= 200_000, `3D üçgen bütçesi: ${stats.triangles}`);
  const rendered = await canvas.screenshot();
  const pixels = await sharp(rendered).stats();
  assert.ok(pixels.channels.slice(0, 3).some(channel => channel.stdev > 15), '3D canvas boş ya da tek renk olmamalı.');
  return stats;
}

function assertLightRequests(requests) {
  assert.deepEqual(requests.three, [], 'Bu cihaz veya tercih için Three.js yüklenmemeli.');
  assert.deepEqual(requests.frames, [], 'Sabit görünümde animasyon karesi yüklenmemeli.');
}

async function scenario(browser, name, options, verify, setup, expectedError, waitUntil = 'networkidle') {
  const context = await browser.newContext(options);
  const page = await context.newPage();
  const errors = [];
  const requests = { frames: [], three: [] };
  page.setDefaultTimeout(20_000);
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => {
    if (message.type() === 'error' && !expectedError?.test(message.text())) errors.push(message.text());
  });
  page.on('request', request => {
    const pathname = new URL(request.url()).pathname;
    if (/\/frames-3d\/[^/]+\/mobile-\d+\.webp$/.test(pathname)) requests.frames.push(pathname);
    if (/\/runtime\/(three|vendor\/three)\//.test(pathname)) requests.three.push(pathname);
  });
  try {
    if (setup) await setup(context, page);
    const response = await page.goto(demoUrl.href, { waitUntil });
    assert.equal(response?.ok(), true, 'Örnek sayfası yüklenemedi.');
    await verify(page, requests);
    await page.waitForLoadState('networkidle');
    assert.deepEqual(errors, [], `${name}: tarayıcı hatası`);
    completed++;
    console.log(`Geçti: ${name} (${requests.frames.length} kare, ${requests.three.length} 3D modül isteği)`);
  } catch (error) {
    await snapshot(page, `failure-${completed + 1}`);
    console.error(`${name}:`, await page.evaluate(() => ({
      ...document.documentElement.dataset,
      progress: document.querySelector('#scene-canvas').dataset.progress,
      frame: document.querySelector('#sequence-canvas').dataset.frame,
      note: document.querySelector('#mode-note').textContent,
    })));
    throw error;
  } finally {
    await context.close();
  }
}

async function main() {
  ({ frameCount } = await import(pathToFileURL(path.join(__dirname, '../../examples/v6/mobile-scroll/sequence-config.mjs'))));
  assert.ok(Number.isInteger(frameCount) && frameCount > 1, 'Sekansta en az iki kare olmalı.');
  if (screenshotDir) await mkdir(screenshotDir, { recursive: true });
  const browser = await chromium.launch({ headless: true, args: ['--enable-unsafe-swiftshader'] });
  try {
    await scenario(browser, 'Masaüstünde gerçek 3D, renk, açı ve boşta render', { viewport: { width: 1440, height: 900 } }, async (page, requests) => {
      await waitMode(page, 'desktop', 'webgl');
      await seek(page, 0);
      const stats = await assertRenderedScene(page);
      await snapshot(page, 'desktop-hero');
      const assembled = await imagePixels(page, '#scene-canvas');
      await seek(page, 0.45);
      const exploded = await imagePixels(page, '#scene-canvas');
      assertImageChanged(assembled, exploded, 'Parçaları ayırma');
      await snapshot(page, 'desktop-exploded');
      await page.locator('.finish[data-finish="forest"]').click();
      await page.waitForFunction(() => document.querySelector('#scene-canvas').dataset.finish === 'forest');
      assert.equal(await page.locator('.finish[data-finish="forest"]').getAttribute('aria-pressed'), 'true');
      const forest = await imagePixels(page, '#scene-canvas');
      assertImageChanged(exploded, forest, 'Yüzey rengini değiştirme');
      await page.locator('#view-angle').focus();
      await page.locator('#view-angle').press('End');
      await page.waitForFunction(() => Number(document.querySelector('#scene-canvas').dataset.viewAngle) === 25);
      assertImageChanged(forest, await imagePixels(page, '#scene-canvas'), 'Bakış açısını değiştirme');
      const renderCount = await page.locator('#scene-canvas').getAttribute('data-render-count');
      await page.waitForTimeout(350);
      assert.equal(await page.locator('#scene-canvas').getAttribute('data-render-count'), renderCount, 'Kaydırma ve kontroller durunca render da durmalı.');
      await seek(page, 1);
      await snapshot(page, 'desktop-lit');
      await seek(page, 0);
      await assertNoOverflow(page);
      assert.ok(requests.three.length > 0, 'Masaüstünde 3D modülleri yüklenmeli.');
      assert.deepEqual(requests.frames, [], 'WebGL çalışırken mobil sekans yüklenmemeli.');
      console.log(`  Sahne: ${stats.drawCalls} çizim çağrısı, ${stats.triangles} üçgen`);
    });

    await scenario(browser, 'Masaüstü ve mobil genişlikler arasında geçiş', { viewport: { width: 1440, height: 900 } }, async (page, requests) => {
      await waitMode(page, 'desktop', 'webgl');
      await seek(page, 0.45);
      const moduleCount = requests.three.length;
      await page.setViewportSize({ width: 390, height: 844 });
      await waitMode(page, 'compact', 'sequence');
      await seek(page, 1);
      assert.equal(await page.locator('#scene-canvas').isVisible(), false);
      assert.equal(await page.locator('.view-control').isVisible(), false);
      await assertNoOverflow(page);
      assert.ok(requests.frames.length > 0, 'Mobil genişliğe geçince sekans yüklenmeli.');
      assert.equal(requests.three.length, moduleCount, 'Mobil geçişi yeni 3D modülü istememeli.');
      await snapshot(page, 'resized-mobile');
      await page.setViewportSize({ width: 1440, height: 900 });
      await waitMode(page, 'desktop', 'webgl');
      await seek(page, 0.45);
      await assertRenderedScene(page);
      assert.equal(await page.locator('#sequence-canvas').isVisible(), false);
      assert.equal(await page.locator('.view-control').isVisible(), true);
    });

    await scenario(browser, 'Mobil sekans, renk, durdurma ve yeniden açma', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }, async (page, requests) => {
      await waitMode(page, 'compact', 'sequence');
      await seek(page, 0);
      await snapshot(page, 'mobile-assembled');
      const assembled = await imagePixels(page, '#sequence-canvas');
      await seek(page, 0.45);
      assertImageChanged(assembled, await imagePixels(page, '#sequence-canvas'), 'Mobil parçaları ayırma');
      await snapshot(page, 'mobile-exploded');
      await seek(page, 1);
      await page.locator('.finish[data-finish="chalk"]').click();
      await page.waitForFunction(() => document.querySelector('#sequence-canvas').dataset.finish === 'chalk');
      await seek(page, 1);
      assert.equal(await page.locator('.finish[data-finish="chalk"]').getAttribute('aria-pressed'), 'true');
      assert.ok(requests.frames.some(url => url.includes('/chalk/')), 'Yeni rengin kareleri yüklenmeli.');
      await snapshot(page, 'mobile-lit');
      await page.locator('#motion-toggle').click();
      await assertPoster(page);
      assert.equal(await page.locator('#motion-toggle').getAttribute('aria-pressed'), 'true');
      const pausedRequests = requests.frames.length;
      await page.locator('.chapter').last().scrollIntoViewIfNeeded();
      await page.waitForLoadState('networkidle');
      assert.equal(requests.frames.length, pausedRequests, 'Durdurulan sekans yeni kare istememeli.');
      await page.locator('#motion-toggle').click();
      await waitMode(page, 'compact', 'sequence');
      assert.equal(await page.locator('#motion-toggle').getAttribute('aria-pressed'), 'false');
      await seek(page, 1);
      await seek(page, 0);
      await assertNoOverflow(page);
      assert.deepEqual(requests.three, [], 'Mobilde Three.js yüklenmemeli.');
    });

    await scenario(browser, 'Canlı hareket tercihi, klavye ve anlatımı atlama', { viewport: { width: 1440, height: 900 } }, async page => {
      await waitMode(page, 'desktop', 'webgl');
      await page.keyboard.press('PageDown');
      await page.waitForFunction(() => scrollY > 100);
      await page.waitForTimeout(350);
      await seek(page, 0.45);
      await page.emulateMedia({ reducedMotion: 'reduce' });
      await assertPoster(page);
      await page.emulateMedia({ reducedMotion: 'no-preference' });
      await waitMode(page, 'desktop', 'webgl');
      await seek(page, 1);
      await page.locator('.skip-link').click();
      await page.waitForFunction(() => location.hash === '#after-story');
      assert.equal(await page.locator('#after-story').evaluate(section => section === document.activeElement), true);
    });

    await scenario(browser, 'Kısa yatay ekran', { viewport: { width: 844, height: 390 }, isMobile: true, hasTouch: true }, async (page, requests) => {
      await assertPoster(page);
      assertLightRequests(requests);
    });

    await scenario(browser, 'Hareket azaltma tercihi', { viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' }, async (page, requests) => {
      await assertPoster(page);
      await page.locator('.chapter').last().scrollIntoViewIfNeeded();
      await page.waitForLoadState('networkidle');
      assertLightRequests(requests);
      await snapshot(page, 'reduced-motion');
    });

    await scenario(browser, 'JavaScript kapalı içerik', { viewport: { width: 390, height: 844 }, javaScriptEnabled: false }, async (page, requests) => {
      await assertPoster(page);
      await page.locator('.chapter').last().scrollIntoViewIfNeeded();
      assertLightRequests(requests);
      await snapshot(page, 'no-javascript');
    });

    await scenario(browser, 'Veri tasarrufu tercihi', { viewport: { width: 1440, height: 900 } }, async (page, requests) => {
      await assertPoster(page);
      await page.locator('.chapter').last().scrollIntoViewIfNeeded();
      await page.waitForLoadState('networkidle');
      assertLightRequests(requests);
    }, context => context.addInitScript(() => {
      const connection = new EventTarget();
      Object.defineProperty(connection, 'saveData', { value: true });
      Object.defineProperty(navigator, 'connection', { configurable: true, value: connection });
    }));

    await scenario(browser, 'WebGL yokken sekansa geçiş', { viewport: { width: 1440, height: 900 } }, async (page, requests) => {
      await waitMode(page, 'desktop', 'sequence');
      await seek(page, 0);
      await seek(page, 1);
      assert.equal(await page.locator('#scene-canvas').isVisible(), false);
      assert.equal(await page.locator('.view-control').isVisible(), false);
      assert.ok(requests.frames.length > 0, 'WebGL açılamazsa hafif sekans yüklenmeli.');
      await assertNoOverflow(page);
    }, context => context.addInitScript(() => {
      const getContext = HTMLCanvasElement.prototype.getContext;
      HTMLCanvasElement.prototype.getContext = function (type, ...args) {
        return /^webgl/.test(type) ? null : getContext.call(this, type, ...args);
      };
    }), /Error creating WebGL context/);

    await scenario(browser, 'Bağlam kaybı olayı simülasyonunda sekansa geçiş', { viewport: { width: 1440, height: 900 } }, async (page, requests) => {
      await waitMode(page, 'desktop', 'webgl');
      await seek(page, 0.45);
      await page.locator('#scene-canvas').evaluate(canvas => canvas.dispatchEvent(new Event('webglcontextlost', { cancelable: true })));
      await waitMode(page, 'desktop', 'sequence');
      await seek(page, 0.45);
      await seek(page, 1);
      assert.ok(requests.frames.length > 0, 'Bağlam kaybı sekansı devreye almalı.');
      assert.equal(await page.locator('#scene-canvas').isVisible(), false);
      await snapshot(page, 'context-fallback');
    });

    let rejectFrames = true;
    await scenario(browser, 'Mobil kare hatasından sonra sabit görünüm ve yeniden deneme', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }, async (page, requests) => {
      await assertPoster(page);
      assert.ok(requests.frames.length > 0, 'Hata senaryosu bir animasyon karesi istemiş olmalı.');
      assert.match(await page.locator('#mode-note').textContent(), /yüklenemedi/);
      assert.equal(await page.locator('#motion-toggle').textContent(), 'Hareketi yeniden dene');
      assert.equal(await page.locator('#motion-toggle').isEnabled(), true);
      await snapshot(page, 'mobile-frame-error');
      rejectFrames = false;
      await page.locator('#motion-toggle').click();
      await waitMode(page, 'compact', 'sequence');
      await seek(page, 0.45);
      await seek(page, 1);
      await seek(page, 0);
      assert.equal(await page.locator('#motion-toggle').getAttribute('aria-pressed'), 'false');
      assert.deepEqual(requests.three, [], 'Mobil hata kurtarma Three.js yüklememeli.');
      await assertNoOverflow(page);
    }, context => context.route('**/frames-3d/*/mobile-*.webp', route => rejectFrames
      ? route.fulfill({ status: 503, contentType: 'image/webp', body: '' })
      : route.continue()), /Failed to load resource: the server responded with a status of 503 \(Service Unavailable\)/);

    let importRequested;
    let releaseImport;
    const importGate = new Promise(resolve => { releaseImport = resolve; });
    await scenario(browser, 'Geciken 3D modülü sırasında hareket azaltma ve yeniden açma', { viewport: { width: 1440, height: 900 } }, async (page, requests) => {
      try {
        await importRequested;
        await page.emulateMedia({ reducedMotion: 'reduce' });
        await assertPoster(page);
        assert.equal(await page.evaluate(() => window.__webglAttempts), 0, 'Bekleyen modül henüz WebGL başlatmamalı.');
        releaseImport();
        await page.waitForLoadState('networkidle');
        await assertPoster(page);
        assert.equal(await page.evaluate(() => window.__webglAttempts), 0, 'Hareket kapandıktan sonra gelen modül WebGL başlatmamalı.');
        assert.ok(requests.three.length > 0, 'Geciktirilen 3D modülü gerçekten istenmiş olmalı.');
        assert.deepEqual(requests.frames, [], 'Hareket azaltmada sekans yüklenmemeli.');
        await page.emulateMedia({ reducedMotion: 'no-preference' });
        await waitMode(page, 'desktop', 'webgl');
        await seek(page, 0.45);
        await assertRenderedScene(page);
        assert.ok(await page.evaluate(() => window.__webglAttempts) > 0, 'Hareket açıldığında WebGL kurulmalı.');
        await assertNoOverflow(page);
      } finally {
        releaseImport();
      }
    }, async (context, page) => {
      importRequested = page.waitForRequest('**/runtime/three/lamp-scene.mjs');
      await context.addInitScript(() => {
        window.__webglAttempts = 0;
        const getContext = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function (type, ...args) {
          if (/^webgl/.test(type)) window.__webglAttempts++;
          return getContext.call(this, type, ...args);
        };
      });
      await context.route('**/runtime/three/lamp-scene.mjs', async route => {
        await importGate;
        await route.continue();
      });
    }, undefined, 'domcontentloaded');
  } finally {
    await browser.close();
  }
  console.log(`${completed} tarayıcı senaryosu geçti.`);
}

main().catch(error => {
  console.error(error.stack ?? error.message);
  process.exitCode = 1;
});
