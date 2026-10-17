import assert from 'node:assert/strict';
import test from 'node:test';
import { buildExperiencePlan } from '../runtime/media/experience-plan.mjs';

const videoBrief = {
  subject: 'A ceramic lamp with a brass stem',
  purpose: 'Show its material while the 3D subject remains interactive',
  materials: 'Matte ceramic and brushed brass',
  lighting: 'Soft side light, stable shadows',
  palette: 'Ivory, clay and brass',
};

test('video istenmediğinde prompt oluşmaz ve temel iş tamamlanır', () => {
  const plan = buildExperiencePlan({ goal: 'Ürün sayfası', pointer: 'camera-look', video: { requested: false } });
  assert.equal(plan.video.status, 'not-requested');
  assert.equal(plan.video.prompt, undefined);
  assert.match(plan.finish, /video beklemeden/);
  assert.match(plan.interaction.desktop, /Scroll ana sahne pozunu/);
});

test('açık video isteği prompt üretir; fare gerçek 3D sahnede kalır', () => {
  const plan = buildExperiencePlan({
    goal: 'Ürün sayfası', pointer: 'camera-look',
    video: { requested: true, mode: 'background', brief: videoBrief },
  });
  assert.equal(plan.video.status, 'prompt-ready');
  assert.match(plan.video.prompt, /Masaüstü çekimi/);
  assert.match(plan.video.integration, /gerçek 3D sahnede/);
  assert.equal(plan.questions.length, 0);
});

test('eksik video brief’i temeli durdurmaz, sonuç değiştiren soruyu üretir', () => {
  const plan = buildExperiencePlan({
    goal: 'Ürün sayfası', video: { requested: true, mode: 'scroll', brief: { subject: 'Lamba' } },
  });
  assert.equal(plan.video.status, 'brief-needed');
  assert.equal(plan.video.prompt, undefined);
  assert.ok(plan.questions.some(question => question.includes('materials')));
  assert.ok(plan.questions.some(question => question.includes('ayrı bir 3D nesne')));
  assert.equal(plan.base.length, 3);
});

test('video biçimi belirsizse temel plan sürer ve seçim sorulur', () => {
  const plan = buildExperiencePlan({ goal: 'Ürün sayfası', video: { requested: true, brief: videoBrief } });
  assert.equal(plan.video.status, 'brief-needed');
  assert.equal(plan.video.prompt, undefined);
  assert.equal(plan.video.integration, undefined);
  assert.ok(plan.questions.some(question => question.includes('arka plan')));
});

test('belirsiz video veya geçersiz etkileşim gizlice açılmaz', () => {
  for (const video of [null, { requested: 'yes' }, { requested: true, mode: 'other' }]) {
    assert.throws(() => buildExperiencePlan({ goal: 'Sayfa', video }));
  }
  assert.throws(() => buildExperiencePlan({ goal: 42 }), TypeError);
  assert.throws(() => buildExperiencePlan({ goal: 'Sayfa', pointer: 'spin' }), RangeError);
});
