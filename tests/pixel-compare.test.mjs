import assert from 'node:assert/strict';
import test from 'node:test';
import { comparePixels } from '../runtime/reference/pixel-compare.mjs';

test('aynı görüntüde fark ve ısı haritası yok', () => {
  const pixels = new Uint8ClampedArray([30, 60, 90, 255, 10, 20, 30, 255]);
  const comparison = comparePixels(pixels, pixels, 2, 1);
  assert.equal(comparison.meanError, 0);
  assert.equal(comparison.mismatchPercent, 0);
  assert.equal(comparison.heatmap[3], 0);
});

test('eşik aşılınca değişen piksel oranı hesaplanır', () => {
  const reference = new Uint8ClampedArray([0, 0, 0, 255, 255, 255, 255, 255]);
  const candidate = new Uint8ClampedArray([100, 100, 100, 255, 255, 255, 255, 255]);
  const comparison = comparePixels(reference, candidate, 2, 1, 24);
  assert.equal(comparison.meanError, 50);
  assert.equal(comparison.mismatchPercent, 50);
  assert.ok(comparison.heatmap[3] > 0);
  assert.equal(comparison.heatmap[7], 0);
});

test('saydam pikseller beyaz zeminde karşılaştırılır', () => {
  const transparent = new Uint8ClampedArray([0, 0, 0, 0]);
  const white = new Uint8ClampedArray([255, 255, 255, 255]);
  assert.equal(comparePixels(transparent, white, 1, 1).meanError, 0);
});

test('uyumsuz ölçü ve eşik reddedilir', () => {
  const pixel = new Uint8ClampedArray(4);
  assert.throws(() => comparePixels(pixel, pixel, 2, 1), RangeError);
  assert.throws(() => comparePixels(pixel, pixel, 1, 1, 256), RangeError);
});
