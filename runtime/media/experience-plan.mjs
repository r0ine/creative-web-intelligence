import { buildVideoPrompts } from './video-prompt.mjs';

const videoFields = ['subject', 'purpose', 'materials', 'lighting', 'palette'];

export function buildExperiencePlan(brief) {
  if (!brief || typeof brief !== 'object' || Array.isArray(brief)) throw new TypeError('Deneyim brief’i bir nesne olmalı.');
  if (typeof brief.goal !== 'string') throw new TypeError('goal: kısa ve açık bir amaç gerekli.');
  const goal = brief.goal.trim();
  if (!goal || goal.length > 2000) throw new TypeError('goal: kısa ve açık bir amaç gerekli.');
  const pointer = brief.pointer ?? 'camera-look';
  if (!['camera-look', 'none'].includes(pointer)) throw new RangeError('pointer: camera-look veya none olmalı.');
  const video = Object.hasOwn(brief, 'video') ? brief.video : { requested: false };
  if (!video || typeof video !== 'object' || Array.isArray(video) || typeof video.requested !== 'boolean') {
    throw new TypeError('video.requested açıkça true veya false olmalı.');
  }

  const questions = [];
  const videoPlan = { requested: video.requested, status: video.requested ? 'brief-needed' : 'not-requested' };
  if (video.requested) {
    if (video.mode !== undefined && !['background', 'scroll'].includes(video.mode)) {
      throw new RangeError('video.mode: background veya scroll olmalı.');
    }
    if (video.mode === undefined) questions.push('Video sakin bir arka plan mı, yoksa scroll ile ilerleyen bir sekans mı olacak?');
    else videoPlan.mode = video.mode;
    const missing = videoFields.filter(field => typeof video.brief?.[field] !== 'string' || !video.brief[field].trim());
    if (missing.length) {
      questions.push(`Video çekimi için şu bilgiler gerekli: ${missing.join(', ')}.`);
    } else if (video.mode) {
      const prompts = buildVideoPrompts({ ...video.brief, mode: video.mode });
      videoPlan.status = 'prompt-ready';
      videoPlan.prompt = prompts.chatgpt;
      videoPlan.delivery = prompts.delivery;
    }
    if (video.mode) {
      videoPlan.integration = video.mode === 'background'
        ? 'Video bağımsız arka plan katmanıdır; fareyle dönen nesne gerçek 3D sahnede kalır.'
        : 'Video kareleri scroll ile ilerler; video görüntüsünün kamerası fareyle serbestçe dönmez.';
    }
    if (video.mode === 'scroll' && pointer === 'camera-look') {
      questions.push('Fareyle dönecek ayrı bir 3D nesne var mı? Yoksa video üzerinde yalnız hafif katman hareketi mi istiyorsun?');
    }
  }

  return {
    version: 8,
    goal,
    base: [
      'Tek başlangıç referansı ve kısa görsel prototip ile tasarım yönünü doğrula.',
      'İçerik, tipografi, gezinme, mobil düzen ve etkileşimi video dosyası olmadan tamamla.',
      'Sahnenin anlamını HTML metinde koru; poster, reduced-motion ve veri tasarrufu görünümünü bitir.',
    ],
    interaction: pointer === 'camera-look'
      ? {
          desktop: 'Scroll ana sahne pozunu yönetir; fare yalnız sınırlı kamera ofseti ekler.',
          mobile: 'Fare ofseti yoktur; scroll ve hafif sekans veya statik poster kullanılır.',
          owner: 'Aynı kamera dönüşümünü iki ayrı animasyon motoruna verme.',
        }
      : { desktop: 'Fare ile kamera hareketi yok.', mobile: 'Scroll veya statik görünüm.', owner: 'Tek hareket sahibi kullan.' },
    video: videoPlan,
    questions,
    finish: video.requested
      ? 'Temel siteyi bekletmeden teslim edilebilir durumda tut. Kullanıcı video dosyasını sağlarsa kalite kontrolü, dönüştürme ve entegrasyonu tamamla.'
      : 'Temel siteyi video beklemeden bitir ve mobil/erişilebilirlik kontrolünden geçir.',
  };
}
