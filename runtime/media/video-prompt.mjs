const scrollBeats = [
  [0, 0.18, 'Hold the complete object in a readable three-quarter view.'],
  [0.18, 0.48, 'Separate its main parts slowly along their assembly axes; keep every part visible.'],
  [0.48, 0.72, 'Use a small camera arc to reveal the inner connection and material detail.'],
  [0.72, 1, 'Reassemble precisely, reveal the final working state, then settle into a still composition.'],
];
const backgroundBeats = [
  [0, 0.25, 'Hold the complete object; establish a still, readable composition.'],
  [0.25, 0.75, 'Let one broad soft light travel gently across the surface; keep the camera and object still.'],
  [0.75, 1, 'Return the light to its starting position and intensity, matching the first frame exactly.'],
];

function requiredText(brief, field) {
  const value = brief[field];
  if (typeof value !== 'string' || !value.trim() || value.length > 2000) {
    throw new TypeError(`${field}: 1–2000 karakter arasında metin gerekiyor.`);
  }
  return value.trim();
}

export function buildVideoPrompts(brief) {
  if (!brief || typeof brief !== 'object' || Array.isArray(brief)) throw new TypeError('Sahne brief’i bir nesne olmalı.');
  const subject = requiredText(brief, 'subject');
  const purpose = requiredText(brief, 'purpose');
  const materials = requiredText(brief, 'materials');
  const lighting = requiredText(brief, 'lighting');
  const palette = requiredText(brief, 'palette');
  const mode = brief.mode ?? 'scroll';
  if (!['scroll', 'background'].includes(mode)) throw new RangeError('mode: scroll veya background olmalı.');
  const duration = brief.durationSeconds ?? 8;
  if (!Number.isFinite(duration) || duration < 2 || duration > 20) throw new RangeError('Süre 2–20 saniye arasında olmalı.');
  const frameCount = brief.frameCount ?? 48;
  if (!Number.isInteger(frameCount) || frameCount < 12 || frameCount > 120) throw new RangeError('Kare sayısı 12–120 arasında olmalı.');
  const beats = brief.beats ?? (mode === 'scroll' ? scrollBeats : backgroundBeats);
  if (!Array.isArray(beats) || beats.length < 2 || beats.length > 8) throw new TypeError('2–8 storyboard adımı gerekiyor.');
  let boundary = 0;
  for (const beat of beats) {
    if (!Array.isArray(beat) || beat.length !== 3 || !Number.isFinite(beat[0]) || !Number.isFinite(beat[1])
      || Math.abs(beat[0] - boundary) > 0.000001 || beat[1] <= beat[0] || beat[1] > 1
      || typeof beat[2] !== 'string' || !beat[2].trim() || beat[2].length > 2000) {
      throw new TypeError('Storyboard, 0–1 aralığını boşluk bırakmadan kapsayan [başlangıç, bitiş, eylem] adımları olmalı.');
    }
    boundary = beat[1];
  }
  if (boundary !== 1) throw new RangeError('Storyboard son adımı 1’de bitmeli.');
  const storyboard = beats.map(([start, end, action]) => ({
    startSeconds: Number((start * duration).toFixed(2)),
    endSeconds: Number((end * duration).toFixed(2)),
    action,
  }));
  const timing = storyboard.map(beat => `${beat.startSeconds}–${beat.endSeconds}s: ${beat.action}`).join('\n');
  const motion = mode === 'scroll'
    ? 'One continuous shot, no cuts. Motion must read when scrubbed both forwards and backwards. The final working state is the ending; do not reset to the opening shot.'
    : 'One continuous seamless loop. First and last frames must match in geometry, light, camera and exposure. No disassembly or narrative reset.';
  const scene = `Subject: ${subject}\nVisual purpose: ${purpose}\nMaterials: ${materials}\nPalette: ${palette}\nLighting: ${lighting}`;
  function shot(aspect, composition) {
    return `Create a silent, ${duration}-second, authored 3D product film for a website.\n\n${scene}\n\nFraming: ${aspect}. ${composition}\n${motion}\n\nShot progression:\n${timing}\n\nKeep the object identity, number of parts and proportions constant. Use physically plausible contact, stable shadows and restrained reflections. No text, logos, UI, HUD, particles, camera shake, rapid zooms, flicker, warping, melting geometry or invented parts. All website text will be real HTML placed over or beside the film.\n\nDesired delivery: ${aspect} video, clean high-quality export, no audio. Duration and resolution must also be set in the generator controls if they are available; this prompt does not enforce technical settings. Inspect the exported clip for temporal errors before using it.`;
  }
  const desktop = shot('16:9', 'Place the object in the right half, leaving the left 40% calm and low-contrast for HTML copy. Keep all moving parts within the safe frame.');
  const mobile = shot('9:16', 'Recompose the shot for portrait; do not crop the landscape result. Keep the full object and every separated part in the central 70%; leave the top quarter calm for HTML copy.');
  const chatgpt = `Aşağıdaki brief için web sitesinde kullanılacak 3D video hazırla. Bu oturumda video üretim aracı varsa brief’i uygula; yoksa video ürettiğini iddia etmeden, video aracına yapıştırabileceğim son promptu ve storyboard’u ver. Model veya hesap erişimi varsayma. Masaüstü ve mobil için ayrı kompozisyon kullan. Referans görsel sağlarsam nesnenin kimliğini koru.\n\nMasaüstü çekimi:\n${desktop}\n\nMobil çekimi:\n${mobile}`;
  return {
    version: 1, mode, durationSeconds: duration, frameCount, storyboard, desktop, mobile, chatgpt,
    delivery: {
      desktopAspect: '16:9', mobileAspect: '9:16',
      playback: mode === 'scroll' ? 'frame-sequence' : 'muted-loop',
      reducedMotion: 'poster', saveData: 'poster',
      frameSelection: 'Math.round(progress * (frameCount - 1))',
      requiresTemporalReview: true,
    },
  };
}
