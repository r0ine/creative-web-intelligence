const assert = require('node:assert/strict');
const { mkdir } = require('node:fs/promises');
const path = require('node:path');
const { chromium } = require('playwright');

const studioUrl = process.argv[2] ?? 'http://127.0.0.1:22222/examples/v6/media-studio/';
const videoFixture = process.argv[3];
const sequenceFixture = process.argv[4];
const screenshotDir = process.env.CWI_SCREENSHOT_DIR;

async function seek(page, progress, count) {
  await page.evaluate(fraction => {
    const section = document.querySelector('#preview');
    const stage = document.querySelector('.preview-stage');
    const bounds = section.getBoundingClientRect();
    scrollTo(0, scrollY + bounds.top + (bounds.height - stage.getBoundingClientRect().height) * fraction);
  }, progress);
  await page.waitForFunction(expected => Number(document.querySelector('canvas').dataset.frame) === expected,
    Math.round(progress * (count - 1)));
}

async function noOverflow(page) {
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'Yatay taşma olmamalı.');
}

async function main() {
  if (!videoFixture || !sequenceFixture) throw new Error('Kullanım: node tools/v6/check_media_studio.cjs URL test-video.mp4 dönüştürülen-klasör');
  if (screenshotDir) await mkdir(screenshotDir, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  let passed = 0;
  try {
    async function scenario(name, options, verify) {
      const context = await browser.newContext(options);
      const page = await context.newPage();
      const faults = [];
      page.on('pageerror', error => faults.push(error.message));
      page.on('response', response => { if (response.status() >= 400) faults.push(`${response.status()} ${response.url()}`); });
      try {
        await verify(page);
        await noOverflow(page);
        assert.deepEqual(faults, [], 'Tarayıcı hatasız çalışmalı.');
        passed += 1;
        console.log(`GEÇTİ ${name}`);
      } finally { await context.close(); }
    }

    await scenario('Kaynak filtreleri ve yeniden dağıtım kapsamı', { viewport: { width: 1440, height: 1000 } }, async page => {
      await page.goto(studioUrl);
      await page.waitForFunction(() => document.querySelectorAll('.source-entry').length === 7);
      assert.ok(await page.getByRole('heading', { name: 'React Bits', exact: true }).isVisible());
      await page.locator('#source-scope').selectOption('library');
      assert.equal(await page.getByRole('heading', { name: 'React Bits', exact: true }).count(), 0);
      assert.equal(await page.getByRole('heading', { name: '21st.dev', exact: true }).count(), 0);
      await page.locator('#source-scope').selectOption('project');
      await page.locator('#source-framework').selectOption('vanilla');
      assert.equal(await page.locator('.source-entry').count(), 1);
      await page.locator('#source-role').selectOption('template');
      assert.match(await page.locator('#source-list').textContent(), /kaynak yok/);
    });

    await scenario('Promptun nesneye ve kullanım moduna göre değişmesi', { viewport: { width: 1440, height: 1000 } }, async page => {
      await page.goto(studioUrl);
      assert.equal(await page.locator('#video-prompt').inputValue(), '');
      assert.equal(await page.locator('#copy-prompt').isDisabled(), true);
      await page.locator('[name="subject"]').fill('A folded linen sculpture on a stone plinth');
      await page.locator('[name="mode"]').selectOption('background');
      await page.getByRole('button', { name: 'Video promptunu hazırla' }).click();
      const prompt = await page.locator('#video-prompt').inputValue();
      assert.match(prompt, /folded linen/);
      assert.match(prompt, /First and last frames must match/);
      assert.match(prompt, /Recompose the shot for portrait/);
      assert.doesNotMatch(prompt, /Separate its main parts/);
      assert.equal(await page.locator('#copy-prompt').isEnabled(), true);
      const downloadPromise = page.waitForEvent('download');
      await page.getByRole('button', { name: 'Brief’i indir' }).click();
      assert.equal((await downloadPromise).suggestedFilename(), 'video-brief.json');
    });

    await scenario('Lamba karelerinin ileri ve geri kaydırılması', { viewport: { width: 1440, height: 1000 } }, async page => {
      await page.goto(studioUrl);
      await seek(page, .7, 48);
      await seek(page, .2, 48);
      if (screenshotDir) await page.screenshot({ path: path.join(screenshotDir, 'desktop-sequence.png') });
      await page.getByRole('button', { name: 'Hareketi durdur', exact: true }).click();
      assert.equal(await page.locator('#sequence-canvas').isVisible(), false);
      assert.equal(await page.locator('#poster').isVisible(), true);
      assert.equal(await page.locator('#frame-progress').isDisabled(), true);
      await page.getByRole('button', { name: 'Hareketi sürdür', exact: true }).click();
      await page.waitForFunction(() => !document.querySelector('#sequence-canvas').hidden);
    });

    await scenario('Yerel kare klasörü, ilk/son kare ve yeniden seçim', { viewport: { width: 1280, height: 900 } }, async page => {
      await page.goto(studioUrl);
      await page.locator('#sequence-files').setInputFiles(sequenceFixture);
      await page.waitForFunction(() => document.querySelector('#media-status').textContent.includes('yerel kare yüklendi'));
      const { frameCount } = require(path.join(path.resolve(sequenceFixture), 'manifest.json'));
      await seek(page, .99, frameCount);
      await seek(page, 0, frameCount);
      await page.getByRole('button', { name: 'Lamba örneğine dön' }).click();
      await seek(page, .6, 48);
    });

    await scenario('Yerel video arka planı, poster, durdurma ve tekrar oynatma', { viewport: { width: 1440, height: 1000 } }, async page => {
      await page.goto(studioUrl);
      await page.locator('#video-file').setInputFiles(videoFixture);
      await page.waitForFunction(() => document.querySelector('#preview').dataset.mode === 'background');
      await page.locator('#preview').scrollIntoViewIfNeeded();
      await page.waitForFunction(() => document.querySelector('#preview').dataset.videoState === 'playing');
      const initialTime = await page.locator('video').evaluate(video => video.currentTime);
      await page.waitForFunction(before => document.querySelector('video').currentTime !== before, initialTime);
      assert.deepEqual(await page.locator('video').evaluate(video => ({ muted: video.muted, loop: video.loop, playsInline: video.playsInline })),
        { muted: true, loop: true, playsInline: true });
      await page.getByRole('button', { name: 'Hareketi durdur', exact: true }).click();
      await page.waitForFunction(() => document.querySelector('#preview').dataset.videoState === 'poster');
      assert.equal(await page.locator('video').getAttribute('src'), null);
      assert.equal(await page.locator('#poster').isVisible(), true);
      await page.getByRole('button', { name: 'Hareketi sürdür', exact: true }).click();
      await page.waitForFunction(() => document.querySelector('#preview').dataset.videoState === 'playing');
      await page.locator('h1').scrollIntoViewIfNeeded();
      await page.waitForFunction(() => document.querySelector('#preview').dataset.videoState === 'idle');
      assert.equal(await page.locator('video').evaluate(video => video.paused), true);
      await page.locator('#preview').scrollIntoViewIfNeeded();
      await page.waitForFunction(() => document.querySelector('#preview').dataset.videoState === 'playing');
      await page.emulateMedia({ reducedMotion: 'reduce' });
      await page.waitForFunction(() => document.querySelector('#preview').dataset.videoState === 'poster');
      assert.equal(await page.locator('video').getAttribute('src'), null);
    });

    await scenario('Geçersiz video ve eksik manifest mevcut sahneyi korur', { viewport: { width: 1280, height: 900 } }, async page => {
      await page.goto(studioUrl);
      await page.locator('#video-file').setInputFiles({ name: 'broken.mp4', mimeType: 'video/mp4', buffer: Buffer.from('broken video') });
      await page.waitForFunction(() => document.querySelector('#media-status').textContent.includes('çözümlenemedi'));
      assert.equal(await page.locator('#preview').getAttribute('data-mode'), 'sequence');
      await page.locator('#sequence-files').evaluate(input => {
        const transfer = new DataTransfer();
        transfer.items.add(new File(['{}'], 'manifest.json', { type: 'application/json' }));
        input.files = transfer.files;
        input.dispatchEvent(new Event('change', { bubbles: true }));
      });
      await page.waitForFunction(() => document.querySelector('#media-status').textContent.includes('manifest gerekiyor'));
      await seek(page, .7, 48);
    });

    await scenario('Mobil ekran, klavyeyle kare kontrolü ve canlı hareket tercihi', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }, async page => {
      await page.goto(studioUrl);
      await seek(page, .4, 48);
      await page.locator('#frame-progress').focus();
      await page.keyboard.press('ArrowRight');
      await page.waitForFunction(() => Number(document.querySelector('canvas').dataset.frame) === 19);
      if (screenshotDir) await page.screenshot({ path: path.join(screenshotDir, 'mobile-sequence.png') });
      await page.emulateMedia({ reducedMotion: 'reduce' });
      await page.waitForFunction(() => document.querySelector('#preview').dataset.static === 'true');
      assert.equal(await page.locator('#sequence-canvas').isVisible(), false);
      assert.equal(await page.locator('#poster').isVisible(), true);
      assert.equal(await page.locator('#frame-progress').isDisabled(), true);
      assert.notEqual(await page.locator('.preview-stage').evaluate(stage => getComputedStyle(stage).position), 'sticky');
      await page.emulateMedia({ reducedMotion: 'no-preference' });
      await page.locator('#preview').scrollIntoViewIfNeeded();
      await page.waitForFunction(() => !document.querySelector('#sequence-canvas').hidden);
    });

    await scenario('Save-Data ile kare isteklerinin kapatılması', { viewport: { width: 390, height: 844 } }, async page => {
      const frameRequests = [];
      await page.addInitScript(() => Object.defineProperty(navigator, 'connection', { value: { saveData: true, addEventListener() {}, removeEventListener() {} } }));
      page.on('request', request => { if (/mobile-\d+\.webp/.test(request.url())) frameRequests.push(request.url()); });
      await page.goto(studioUrl);
      await page.locator('#preview').scrollIntoViewIfNeeded();
      assert.equal(await page.locator('#poster').isVisible(), true);
      assert.equal(await page.locator('#sequence-canvas').isVisible(), false);
      assert.deepEqual(frameRequests, []);
    });

    await scenario('JavaScript kapalıyken içerik ve poster', { viewport: { width: 390, height: 844 }, javaScriptEnabled: false }, async page => {
      await page.goto(studioUrl);
      assert.equal(await page.getByRole('heading', { name: 'Hareketin malzemesi.' }).isVisible(), true);
      await page.locator('#preview').scrollIntoViewIfNeeded();
      assert.equal(await page.locator('#poster').isVisible(), true);
    });
  } finally { await browser.close(); }
  console.log(`${passed} medya atölyesi tarayıcı senaryosu geçti.`);
}

main().catch(error => { console.error(error); process.exitCode = 1; });
