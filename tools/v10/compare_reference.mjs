#!/usr/bin/env node
// Referans ile yeni siteyi aynı ekran ölçüsünde karşılaştırır; fark haritası ve en farklı bölgeleri yazar.
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { comparePixels } from '../../runtime/reference/pixel-compare.mjs';
import { diffRegions } from '../../runtime/reference/style-metrics.mjs';

const require = createRequire(import.meta.url);
const VIEWPORTS = { desktop: { width: 1440, height: 900 }, mobile: { width: 390, height: 844 } };
const REGION_HINTS = { 0: 'menü ve ilk ekran (hero)', 1: 'ana içerik', 2: 'alt bölümler' };

function usage(message) {
  console.error(`${message}\nKullanım: node tools/v10/compare_reference.mjs <referans.png|adres> <yeni.png|adres> [--viewport desktop|mobile] [--threshold 24] [--out fark.png]`);
  process.exit(2);
}

function parseArgs(argv) {
  const args = { inputs: [], viewport: 'desktop', threshold: 24, out: null };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === '--viewport') args.viewport = argv[++index];
    else if (value === '--threshold') args.threshold = Number(argv[++index]);
    else if (value === '--out') args.out = argv[++index];
    else args.inputs.push(value);
  }
  if (args.inputs.length !== 2) usage('İki girdi gerekli.');
  if (!VIEWPORTS[args.viewport]) usage(`Bilinmeyen ekran: ${args.viewport}`);
  if (!Number.isFinite(args.threshold) || args.threshold < 0 || args.threshold > 255) usage('Eşik 0-255 arasında olmalı.');
  args.out = resolve(args.out ?? 'reference-workspace/compare/diff.png');
  return args;
}

async function imageDataUrl(page, input, viewport) {
  if (/^https?:\/\//i.test(input) || /\.html?$/i.test(input)) {
    const url = /^https?:\/\//i.test(input) ? input : pathToFileURL(resolve(input)).href;
    await page.setViewportSize(viewport);
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60_000 });
    await page.waitForTimeout(800);
    return `data:image/png;base64,${(await page.screenshot()).toString('base64')}`;
  }
  if (!existsSync(input)) usage(`Bulunamadı: ${input}`);
  return `data:image/png;base64,${(await readFile(input)).toString('base64')}`;
}

// Tarayıcıda PNG çözülür; ortak alan RGBA olarak Node'a döner.
function decode([first, second]) {
  const load = source => new Promise((done, fail) => {
    const image = new Image();
    image.onload = () => done(image);
    image.onerror = () => fail(new Error('Görüntü okunamadı.'));
    image.src = source;
  });
  return Promise.all([load(first), load(second)]).then(images => {
    const width = Math.min(...images.map(image => image.naturalWidth));
    const height = Math.min(...images.map(image => image.naturalHeight));
    const pixels = images.map(image => {
      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      const context = canvas.getContext('2d');
      context.drawImage(image, 0, 0);
      const data = context.getImageData(0, 0, width, height).data;
      let binary = '';
      for (let offset = 0; offset < data.length; offset += 0x8000) binary += String.fromCharCode(...data.subarray(offset, offset + 0x8000));
      return btoa(binary);
    });
    return { width, height, sizes: images.map(image => [image.naturalWidth, image.naturalHeight]), pixels };
  });
}

function overlay({ base, heatmap, width, height }) {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const context = canvas.getContext('2d');
  return new Promise(done => {
    const image = new Image();
    image.onload = () => {
      context.drawImage(image, 0, 0);
      const layer = document.createElement('canvas');
      layer.width = width;
      layer.height = height;
      const bytes = Uint8ClampedArray.from(atob(heatmap), char => char.charCodeAt(0));
      layer.getContext('2d').putImageData(new ImageData(bytes, width, height), 0, 0);
      context.drawImage(layer, 0, 0);
      done(canvas.toDataURL('image/png').split(',')[1]);
    };
    image.src = base;
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  let chromium;
  try {
    ({ chromium } = require('playwright'));
  } catch {
    usage('Playwright bulunamadı. npm install playwright && npx playwright install chromium ile kur.');
  }
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    const sources = [];
    for (const input of args.inputs) sources.push(await imageDataUrl(page, input, VIEWPORTS[args.viewport]));
    await page.goto('about:blank');
    const decoded = await page.evaluate(decode, sources);
    const [reference, candidate] = decoded.pixels.map(text => new Uint8ClampedArray(Buffer.from(text, 'base64')));
    const result = comparePixels(reference, candidate, decoded.width, decoded.height, args.threshold);
    const regions = diffRegions(result.heatmap, decoded.width, decoded.height);
    const png = await page.evaluate(overlay, {
      base: sources[1], heatmap: Buffer.from(result.heatmap).toString('base64'), width: decoded.width, height: decoded.height,
    });
    await mkdir(dirname(args.out), { recursive: true });
    await writeFile(args.out, Buffer.from(png, 'base64'));
    const summary = {
      inputs: args.inputs, sizes: decoded.sizes, compared: [decoded.width, decoded.height], threshold: args.threshold,
      meanError: Math.round(result.meanError * 100) / 100, mismatchPercent: Math.round(result.mismatchPercent * 100) / 100,
      regions: regions.map(region => ({ ...region, percent: Math.round(region.percent * 10) / 10, hint: REGION_HINTS[region.row] })),
      diffImage: args.out,
    };
    await writeFile(args.out.replace(/\.png$/i, '.json'), `${JSON.stringify(summary, null, 2)}\n`);
    if (decoded.sizes[0].join('x') !== decoded.sizes[1].join('x')) {
      console.log(`Uyarı: ölçüler farklı (${decoded.sizes.map(size => size.join('x')).join(' / ')}); yalnız ortak ${decoded.width}x${decoded.height} alan karşılaştırıldı.`);
    }
    console.log(`Farklı piksel: %${summary.mismatchPercent} · ortalama hata ${summary.meanError}`);
    for (const region of summary.regions.slice(0, 3)) {
      console.log(`  ${region.label}: %${region.percent} fark (${region.hint})`);
    }
    console.log('Önce en büyük farkı düzelt: yapı → ölçek → hiza → yazı ölçüleri → kırpma → renk → mikro detay.');
    if (args.threshold > 10) console.log(`Zemin tonu gibi ince renk farklarını görmek için --threshold 8 ile tekrar çalıştır.`);
    console.log(`Fark görüntüsü: ${args.out}`);
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error);
  process.exit(1);
});
