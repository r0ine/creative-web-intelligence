const radians = degrees => degrees * Math.PI / 180;

function easeBetween(start, end, progress) {
  const position = Math.max(0, Math.min(1, (progress - start) / (end - start)));
  return position ** 3 * (position * (position * 6 - 15) + 10);
}

export function sampleLampMotion(progress) {
  if (!Number.isFinite(progress)) throw new TypeError('Sahne ilerlemesi sonlu bir sayı olmalı.');
  const position = Math.max(0, Math.min(1, progress));
  const separation = easeBetween(0.12, 0.38, position) * (1 - easeBetween(0.60, 0.82, position));
  const inspection = easeBetween(0.38, 0.60, position);
  const returnToHero = easeBetween(0.72, 0.94, position);
  const illumination = easeBetween(0.82, 0.94, position);

  return {
    progress: position,
    separation,
    orbit: radians(32 + 66 * inspection - 66 * returnToHero),
    shadeY: 1.48 * separation,
    stemY: 0.30 * separation,
    baseY: 0,
    bulbY: 0.60 * separation,
    targetY: 1.88 + 0.59 * separation,
    cameraRadius: 8.25 + 1.75 * separation,
    cameraHeight: 4.40 - 1.28 * separation,
    lampRotation: 0,
    lightIntensity: illumination,
  };
}
