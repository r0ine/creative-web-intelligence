const assert = require('node:assert/strict');
const { createHash } = require('node:crypto');
const { mkdir, readFile, rename, writeFile } = require('node:fs/promises');
const path = require('node:path');
const { chromium } = require('playwright');
const sharp = require('sharp');

const baseUrl = new URL(process.argv[2] ?? 'http://127.0.0.1:22222/examples/v6/mobile-scroll/');
assert.ok(['http:', 'https:'].includes(baseUrl.protocol), 'Örnek adresi HTTP veya HTTPS kullanmalı.');
assert.ok(['127.0.0.1', 'localhost', '[::1]'].includes(baseUrl.hostname), 'Kareler yerel önizleme sunucusundan üretilmeli.');
const renderUrl = new URL(baseUrl.pathname === '/' ? '/examples/v6/mobile-scroll/render.html' : 'render.html', baseUrl);
const outputDir = path.resolve(__dirname, '../../examples/v6/mobile-scroll/frames-3d');
const size = 720;
const sourcePaths = ['runtime/three/lamp-scene.mjs', 'runtime/three/lamp-motion.mjs', 'examples/v6/mobile-scroll/sequence-config.mjs'];

async function sourceHashes() {
  const hashes = {};
  for (const sourcePath of sourcePaths) {
    const contents = await readFile(path.resolve(__dirname, '../..', sourcePath));
    hashes[sourcePath] = createHash('sha256').update(contents).digest('hex');
  }
  return hashes;
}

async function saveAsset(filePath, contents) {
  const pendingPath = `${filePath}.pending`;
  await writeFile(pendingPath, contents);
  await rename(pendingPath, filePath);
}

async function captureFrame(page, finish, name, progress, errors, captures) {
  const sceneStats = await page.evaluate(pose => window.renderFrame(pose), { finish, progress });
  assert.deepEqual(errors, [], 'Sahne oluşturulurken tarayıcı hatası alındı.');
  const screenshot = await page.locator('canvas').screenshot({ type: 'png', animations: 'disabled' });
  const metadata = await sharp(screenshot).metadata();
  assert.equal(metadata.width, size, 'Kare genişliği beklenenden farklı.');
  assert.equal(metadata.height, size, 'Kare yüksekliği beklenenden farklı.');

  const pixels = await sharp(screenshot).removeAlpha().stats();
  const hasScene = pixels.channels.some(channel => channel.max - channel.min > 24 && channel.stdev > 2);
  assert.ok(hasScene, `${finish}/${name}: canvas boş veya tek renk görünüyor.`);

  const contents = await sharp(screenshot).webp({ quality: 82, effort: 4 }).toBuffer();
  const file = `${finish}/${name}.webp`;
  captures.push({ file, contents });
  return {
    file,
    progress,
    width: size,
    height: size,
    bytes: contents.length,
    sha256: createHash('sha256').update(contents).digest('hex'),
    sceneStats,
  };
}

async function main() {
  const { frameCount, finishes } = await import('../../examples/v6/mobile-scroll/sequence-config.mjs');
  const initialHashes = await sourceHashes();
  const browser = await chromium.launch({
    headless: true,
    args: ['--enable-unsafe-swiftshader'],
  });
  const errors = [];
  try {
    const context = await browser.newContext({
      viewport: { width: size, height: size },
      deviceScaleFactor: 1,
      reducedMotion: 'no-preference',
    });
    const page = await context.newPage();
    for (const sourcePath of sourcePaths) {
      const servedSource = await context.request.get(new URL(sourcePath, new URL('../../../', renderUrl)).href);
      assert.ok(servedSource.ok(), `${sourcePath}: sahne kaynağı sunucudan okunamadı.`);
      const servedHash = createHash('sha256').update(await servedSource.body()).digest('hex');
      assert.equal(servedHash, initialHashes[sourcePath], `${sourcePath}: sunucu başka bir kaynak sürümü kullanıyor.`);
    }
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => {
      if (message.type() === 'error') errors.push(message.text());
    });
    const response = await page.goto(renderUrl.href, { waitUntil: 'networkidle' });
    assert.equal(response?.ok(), true, 'Kare üretim sayfası yüklenemedi.');
    await page.waitForFunction(() => window.ready === true || window.renderError, null, { timeout: 30_000 });
    assert.equal(await page.evaluate(() => window.renderError), null, 'WebGL sahnesi hazırlanamadı.');
    assert.deepEqual(errors, [], 'WebGL sahnesi yüklenirken hata alındı.');

    const variants = {};
    const captures = [];
    for (const finish of finishes) {
      await mkdir(path.join(outputDir, finish), { recursive: true });
      const frames = [];
      for (let index = 0; index < frameCount; index++) {
        frames.push(await captureFrame(page, finish, `mobile-${index}`, index / (frameCount - 1), errors, captures));
      }
      assert.ok(new Set(frames.map(frame => frame.sha256)).size >= 6, `${finish}: sahne kaydırma ilerledikçe değişmiyor.`);
      const stills = [];
      for (const [name, progress] of [['poster', 0.98], ['step-0', 0.05], ['step-1', 0.45], ['step-2', 0.98]]) {
        stills.push(await captureFrame(page, finish, name, progress, errors, captures));
      }
      assert.equal(stills[0].sha256, stills[3].sha256, `${finish}: aynı poz farklı görüntü üretiyor.`);
      const totalBytes = [...frames, ...stills].reduce((sum, frame) => sum + frame.bytes, 0);
      variants[finish] = { frameCount, stillCount: stills.length, totalBytes, frames, stills };
      console.log(`${finish}: ${frameCount} mobil kare, ${stills.length} sabit görsel, ${totalBytes} bayt.`);
    }
    assert.deepEqual(errors, [], 'Kare üretimi sırasında tarayıcı hatası alındı.');
    assert.equal(new Set(Object.values(variants).map(variant => variant.stills[0].sha256)).size, finishes.length, 'Renk seçenekleri aynı görüntüyü üretiyor.');
    assert.deepEqual(await sourceHashes(), initialHashes, 'Sahne kaynakları üretim sırasında değişti; kareleri yeniden üretin.');
    const manifest = {
      schemaVersion: 1,
      source: {
        type: 'procedural-webgl-capture',
        module: 'runtime/three/lamp-scene.mjs',
        motion: 'runtime/three/lamp-motion.mjs',
        sha256: initialHashes,
        capturePage: 'examples/v6/mobile-scroll/render.html',
        generator: 'tools/v6/render_lamp_fallbacks.cjs',
        description: 'Masaüstü örneğinde kullanılan üç boyutlu lamba sahnesinin tarayıcı görüntüleri.',
      },
      capture: {
        browser: `Chromium ${browser.version()}`,
        viewport: { width: size, height: size },
        devicePixelRatio: 1,
        format: 'webp',
        quality: 82,
        progress: 'index / (frameCount - 1)',
        checks: ['source-hashes', 'canvas-dimensions', 'pixel-range', 'distinct-poses', 'repeatable-pose', 'distinct-finishes', 'browser-errors'],
      },
      totalFiles: finishes.length * (frameCount + 4),
      totalBytes: Object.values(variants).reduce((sum, variant) => sum + variant.totalBytes, 0),
      variants,
    };
    for (const { file, contents } of captures) await saveAsset(path.join(outputDir, file), contents);
    await saveAsset(path.join(outputDir, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);
    console.log(`Toplam ${manifest.totalFiles} WebP, ${manifest.totalBytes} bayt. Kaynak kaydı: ${path.join(outputDir, 'manifest.json')}`);
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error.stack ?? error.message);
  process.exitCode = 1;
});
