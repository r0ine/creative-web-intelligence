import test from 'node:test';
import assert from 'node:assert/strict';
import {
  areaPalette, contrastFindings, contrastRatio, diffRegions, parseColor, toHex,
} from '../runtime/reference/style-metrics.mjs';

test('hesaplanmış renk biçimleri okunur', () => {
  assert.deepEqual(parseColor('rgb(244, 241, 234)'), { r: 244, g: 241, b: 234, a: 1 });
  assert.deepEqual(parseColor('rgba(0, 0, 0, 0)'), { r: 0, g: 0, b: 0, a: 0 });
  assert.deepEqual(parseColor('rgb(10 20 30 / 50%)'), { r: 10, g: 20, b: 30, a: 0.5 });
  assert.equal(parseColor('oklch(0.7 0.1 40)'), null);
  assert.equal(toHex({ r: 194, g: 65, b: 12 }), '#c2410c');
});

test('kontrast oranı WCAG formülüyle hesaplanır', () => {
  assert.equal(Math.round(contrastRatio(parseColor('rgb(0,0,0)'), parseColor('rgb(255,255,255)'))), 21);
  assert.equal(contrastRatio(parseColor('rgb(119,119,119)'), parseColor('rgb(119,119,119)')), 1);
});

test('palet alan payına göre sıralanır ve alan planı çıkarılır', () => {
  const { colors, plan } = areaPalette([
    { color: 'rgb(244, 241, 234)', area: 800 },
    { color: 'rgb(194, 65, 12)', area: 50 },
    { color: 'rgb(120, 140, 110)', area: 150 },
    { color: 'rgba(0, 0, 0, 0)', area: 5000 },
  ]);
  assert.equal(colors[0].hex, '#f4f1ea');
  assert.equal(colors.length, 3);
  assert.equal(Math.round(plan.neutral * 100), 80);
  assert.equal(Math.round(plan.support * 100), 15);
  assert.equal(Math.round(plan.accent * 100), 5);
});

test('büyük metin için kontrast eşiği 3:1, normal metin için 4.5:1', () => {
  const grey = { color: 'rgb(130, 130, 130)', background: 'rgb(255, 255, 255)', fontWeight: 400 };
  assert.equal(contrastFindings([{ ...grey, fontSize: 16 }]).length, 1);
  assert.equal(contrastFindings([{ ...grey, fontSize: 32 }]).length, 0);
  assert.equal(contrastFindings([{ ...grey, fontSize: 20, fontWeight: 700 }]).length, 0);
  assert.equal(contrastFindings([{ color: 'oklch(1 0 0)', background: 'rgb(0,0,0)', fontSize: 16 }]).length, 0);
});

test('fark bölgeleri en farklı bölgeden başlayarak sıralanır', () => {
  const width = 6;
  const height = 6;
  const heatmap = new Uint8ClampedArray(width * height * 4);
  for (let y = 0; y < 2; y += 1) {
    for (let x = 2; x < 4; x += 1) heatmap[(y * width + x) * 4 + 3] = 255;
  }
  const regions = diffRegions(heatmap, width, height);
  assert.equal(regions[0].label, 'üst orta');
  assert.equal(regions[0].percent, 100);
  assert.equal(regions.at(-1).percent, 0);
  assert.throws(() => diffRegions(heatmap, 5, 6), RangeError);
});
