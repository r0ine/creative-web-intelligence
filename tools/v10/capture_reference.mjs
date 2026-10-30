#!/usr/bin/env node
// Referansı gerçek tarayıcıda açar: ekran görüntüleri, alan ağırlıklı palet, tipografi, kontrast, animasyon ve ağ özeti.
import { mkdir, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { areaPalette, contrastFindings } from '../../runtime/reference/style-metrics.mjs';

const require = createRequire(import.meta.url);
const VIEWPORTS = {
  desktop: { viewport: { width: 1440, height: 900 } },
  mobile: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true },
};

function usage(message) {
  console.error(`${message}\nKullanım: node tools/v10/capture_reference.mjs <adres|html-dosyası> [--out klasör] [--workspace mirror-çalışma-alanı]`);
  process.exit(2);
}

function parseArgs(argv) {
  const args = { target: null, out: null };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === '--out') args.out = argv[++index];
    else if (value === '--workspace') args.workspace = argv[++index];
    else if (!args.target) args.target = value;
    else usage(`Fazla argüman: ${value}`);
  }
  if (args.workspace && !args.target) {
    const capture = JSON.parse(readFileSync(resolve(args.workspace, 'capture.json'), 'utf8'));
    args.target = resolve(args.workspace, 'site', capture.entry);
  }
  if (!args.target) usage('Adres veya dosya gerekli.');
  args.out = resolve(args.out ?? (args.workspace ? resolve(args.workspace, 'live') : 'reference-workspace/live'));
  return args;
}

export function targetUrl(target) {
  if (/^https?:\/\//i.test(target)) return target;
  const path = resolve(target);
  if (!existsSync(path)) usage(`Bulunamadı: ${target}`);
  return pathToFileURL(path).href;
}

function loadPlaywright() {
  try {
    return require('playwright');
  } catch {
    usage('Playwright bulunamadı. npm install playwright && npx playwright install chromium ile kur.');
  }
}

function axeSource() {
  try {
    return readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
  } catch {
    return null;
  }
}

// Tarayıcı içinde çalışır; yalnız görünür öğeleri örnekler.
function sampleStyles() {
  const transparent = value => !value || value === 'transparent' || /rgba\([^)]*,\s*0\)$/.test(value) || /\/\s*0\)$/.test(value);
  const backgroundOf = element => {
    for (let node = element; node; node = node.parentElement) {
      const value = getComputedStyle(node).backgroundColor;
      if (!transparent(value)) return value;
    }
    return 'rgb(255, 255, 255)';
  };
  const viewportArea = innerWidth * Math.max(innerHeight, document.documentElement.scrollHeight);
  const backgrounds = [{ color: backgroundOf(document.body), area: viewportArea }];
  const texts = [];
  const fonts = new Map();
  const elements = [...document.body.querySelectorAll('*')].slice(0, 5000);
  for (const element of elements) {
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    if (style.visibility === 'hidden' || style.display === 'none' || rect.width < 1 || rect.height < 1) continue;
    if (!transparent(style.backgroundColor)) backgrounds.push({ color: style.backgroundColor, area: rect.width * rect.height });
    const ownText = [...element.childNodes].filter(node => node.nodeType === 3).map(node => node.textContent.trim()).join(' ');
    if (!ownText) continue;
    const family = style.fontFamily.split(',')[0].replace(/["']/g, '').trim();
    const size = Number.parseFloat(style.fontSize);
    const key = `${family}|${element.tagName.toLowerCase()}`;
    const entry = fonts.get(key) ?? { family, tag: element.tagName.toLowerCase(), sizes: new Set(), weight: style.fontWeight, count: 0 };
    entry.sizes.add(Math.round(size));
    entry.count += 1;
    fonts.set(key, entry);
    if (texts.length < 1500) {
      texts.push({ color: style.color, background: backgroundOf(element), fontSize: size, fontWeight: style.fontWeight,
        tag: element.tagName.toLowerCase(), text: ownText.slice(0, 60) });
    }
  }
  const animations = document.getAnimations().map(animation => {
    const timing = animation.effect?.getTiming?.() ?? {};
    return { type: animation.constructor.name, name: animation.animationName ?? animation.transitionProperty ?? '',
      duration: timing.duration, easing: timing.easing, iterations: timing.iterations };
  });
  return {
    title: document.title,
    lang: document.documentElement.lang || null,
    scrollHeight: document.documentElement.scrollHeight,
    backgrounds,
    texts,
    fonts: [...fonts.values()].map(entry => ({ ...entry, sizes: [...entry.sizes].sort((a, b) => a - b) }))
      .sort((a, b) => b.count - a.count).slice(0, 20),
    loadedFonts: [...document.fonts].filter(face => face.status === 'loaded').map(face => face.family.replace(/["']/g, '')),
    animations: animations.slice(0, 60),
    media: { canvas: document.querySelectorAll('canvas').length, video: document.querySelectorAll('video').length,
      images: document.images.length, svg: document.querySelectorAll('svg').length },
  };
}

async function captureViewport(browser, url, name, options, out, axe) {
  const context = await browser.newContext(options);
  const page = await context.newPage();
  const network = [];
  page.on('requestfinished', async request => {
    const sizes = await request.sizes().catch(() => null);
    network.push({ url: request.url().slice(0, 300), type: request.resourceType(), bytes: sizes?.responseBodySize ?? 0 });
  });
  const errors = [];
  page.on('pageerror', error => errors.push(String(error.message).slice(0, 200)));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60_000 }).catch(async error => {
    errors.push(`Yükleme: ${error.message.split('\n')[0]}`);
  });
  await page.waitForTimeout(800);
  await page.screenshot({ path: resolve(out, `${name}.png`) });
  await page.screenshot({ path: resolve(out, `${name}-full.png`), fullPage: true }).catch(() => {});
  const sample = await page.evaluate(sampleStyles);
  let accessibility = null;
  if (axe) {
    await page.addScriptTag({ content: axe });
    accessibility = await page.evaluate(async () => {
      const result = await window.axe.run(document, { resultTypes: ['violations'] });
      return result.violations.map(v => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length }));
    });
  }
  await context.close();
  const byType = {};
  for (const item of network) {
    const bucket = byType[item.type] ??= { count: 0, bytes: 0 };
    bucket.count += 1;
    bucket.bytes += item.bytes;
  }
  return {
    ...sample,
    backgrounds: undefined,
    texts: undefined,
    palette: areaPalette(sample.backgrounds),
    contrast: contrastFindings(sample.texts).slice(0, 25),
    accessibility,
    network: { byType, scripts: network.filter(item => item.type === 'script').map(item => item.url) },
    errors,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const url = targetUrl(args.target);
  const { chromium } = loadPlaywright();
  await mkdir(args.out, { recursive: true });
  const axe = axeSource();
  const browser = await chromium.launch();
  const result = { version: '10.0', url, capturedAt: new Date().toISOString(), axe: Boolean(axe), viewports: {} };
  try {
    for (const [name, options] of Object.entries(VIEWPORTS)) {
      result.viewports[name] = await captureViewport(browser, url, name, options, args.out, axe);
    }
    const reduced = await browser.newContext({ ...VIEWPORTS.desktop, reducedMotion: 'reduce' });
    const page = await reduced.newPage();
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60_000 }).catch(() => {});
    result.reducedMotionAnimations = await page.evaluate(() => document.getAnimations().length);
    await page.screenshot({ path: resolve(args.out, 'desktop-reduced-motion.png') });
    await reduced.close();
  } finally {
    await browser.close();
  }
  await writeFile(resolve(args.out, 'live.json'), `${JSON.stringify(result, null, 2)}\n`);
  for (const [name, view] of Object.entries(result.viewports)) {
    const plan = view.palette.plan;
    console.log(`${name}: ${view.palette.colors.slice(0, 4).map(c => `${c.hex} %${Math.round(c.share * 100)}`).join(', ')}`);
    console.log(`  alan planı: nötr %${Math.round(plan.neutral * 100)} · destek %${Math.round(plan.support * 100)} · vurgu %${Math.round(plan.accent * 100)}`);
    console.log(`  fontlar: ${[...new Set(view.fonts.map(f => f.family))].slice(0, 4).join(', ')} · animasyon: ${view.animations.length} · kontrast bulgusu: ${view.contrast.length}`);
    if (view.accessibility) console.log(`  axe: ${view.accessibility.length} ihlal türü`);
    if (view.errors.length) console.log(`  hata: ${view.errors[0]}`);
  }
  console.log(`Hareket azaltma tercihinde animasyon sayısı: ${result.reducedMotionAnimations}`);
  if (!axe) console.log('axe-core kurulu değil; statik erişilebilirlik denetimi analyze_reference.py içinde. Ayrıntılı tarama için: npm install axe-core');
  console.log(`Çıktı: ${args.out}`);
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch(error => {
    console.error(error);
    process.exit(1);
  });
}
