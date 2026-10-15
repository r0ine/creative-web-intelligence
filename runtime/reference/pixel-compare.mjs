export function comparePixels(reference, candidate, width, height, threshold = 24) {
  if (!Number.isInteger(width) || !Number.isInteger(height) || width < 1 || height < 1) {
    throw new RangeError('Geçerli görüntü ölçüleri gerekli.');
  }

  const length = width * height * 4;
  if (reference.length !== length || candidate.length !== length) {
    throw new RangeError('Görüntülerin ölçüleri aynı olmalı.');
  }
  if (!Number.isFinite(threshold) || threshold < 0 || threshold > 255) {
    throw new RangeError('Eşik 0 ile 255 arasında olmalı.');
  }

  const heatmap = new Uint8ClampedArray(length);
  let totalError = 0;
  let different = 0;
  const pixels = width * height;

  for (let offset = 0; offset < length; offset += 4) {
    let error = 0;
    for (let channel = 0; channel < 3; channel += 1) {
      const source = (reference[offset + channel] * reference[offset + 3]
        + 255 * (255 - reference[offset + 3])) / 255;
      const target = (candidate[offset + channel] * candidate[offset + 3]
        + 255 * (255 - candidate[offset + 3])) / 255;
      error += Math.abs(source - target);
    }
    error /= 3;
    totalError += error;
    if (error > threshold) different += 1;

    const intensity = Math.min(255, Math.round(error * 2.2));
    heatmap[offset] = 255;
    heatmap[offset + 1] = Math.max(16, 236 - intensity);
    heatmap[offset + 2] = Math.max(24, 190 - intensity);
    heatmap[offset + 3] = error > threshold ? Math.max(92, intensity) : 0;
  }

  return {
    meanError: totalError / pixels,
    mismatchPercent: different / pixels * 100,
    differentPixels: different,
    totalPixels: pixels,
    heatmap,
  };
}
