import assert from 'node:assert/strict';
import test from 'node:test';
import { sampleLampMotion } from '../runtime/three/lamp-motion.mjs';

function pose(progress) {
  const { progress: position, ...motion } = sampleLampMotion(progress);
  return motion;
}

test('başlangıç ve bitişte dinlenme alanları sabit kalır', () => {
  for (const progress of [0.01, 0.04, 0.08, 0.12]) assert.deepEqual(pose(progress), pose(0));
  for (const progress of [0.94, 0.96, 0.98]) assert.deepEqual(pose(progress), pose(1));
  assert.equal(sampleLampMotion(0).lightIntensity, 0);
  assert.equal(sampleLampMotion(1).lightIntensity, 1);
  assert.equal(sampleLampMotion(1).separation, 0);
});

test('giriş aralık dışındaysa sahne sınırda durur; geçersiz sayılar reddedilir', () => {
  assert.deepEqual(sampleLampMotion(-2), sampleLampMotion(0));
  assert.deepEqual(sampleLampMotion(2), sampleLampMotion(1));
  for (const progress of [NaN, Infinity, -Infinity, undefined, '0.5', null]) {
    assert.throws(() => sampleLampMotion(progress), TypeError);
  }
});

test('parçalar ayrılınca duy görünür ve taban masada kalır', () => {
  for (const progress of [0.38, 0.42, 0.5, 0.6]) {
    const motion = sampleLampMotion(progress);
    assert.equal(motion.separation, 1);
    assert.equal(motion.baseY, 0);
    assert.ok(motion.shadeY > motion.bulbY);
    assert.ok(motion.bulbY > motion.stemY);
    assert.ok(2.49 + motion.shadeY > 2.79 + 0.285 + motion.bulbY);
  }
});

test('inceleme kamerası 66 derecelik yayı izler ve başlangıç açısına döner', () => {
  const start = sampleLampMotion(0.38);
  const inspection = sampleLampMotion(0.6);
  const finish = sampleLampMotion(1);
  assert.ok(Math.abs((inspection.orbit - start.orbit) * 180 / Math.PI - 66) < 1e-10);
  assert.ok(inspection.cameraHeight < 2.49 + inspection.shadeY);
  assert.equal(finish.orbit, start.orbit);
});

test('ışık ancak birleşme bittikten sonra açılır', () => {
  for (let step = 0; step <= 82; step++) assert.equal(sampleLampMotion(step / 100).lightIntensity, 0);
  const illuminated = sampleLampMotion(0.89);
  assert.equal(illuminated.separation, 0);
  assert.ok(illuminated.lightIntensity > 0 && illuminated.lightIntensity < 1);
});

test('ileri ve geri kaydırma aynı pozisyonda aynı sahneyi verir', () => {
  const positions = Array.from({ length: 201 }, (_, index) => index / 200);
  const forward = new Map(positions.map(progress => [progress, sampleLampMotion(progress)]));
  for (const progress of positions.reverse()) assert.deepEqual(sampleLampMotion(progress), forward.get(progress));
});

test('tüm koreografi sonlu kalır ve parçalar tanımlı mesafeyi aşmaz', () => {
  for (let step = 0; step <= 1000; step++) {
    const motion = sampleLampMotion(step / 1000);
    assert.ok(Object.values(motion).every(Number.isFinite));
    assert.ok(motion.separation >= 0 && motion.separation <= 1);
    assert.ok(motion.shadeY >= 0 && motion.shadeY <= 1.48);
    assert.ok(motion.lightIntensity >= 0 && motion.lightIntensity <= 1);
    assert.ok(motion.cameraRadius >= 8.25 && motion.cameraRadius <= 10);
  }
});

test('sahne kesimleri arasında konum ve hız sıçraması olmaz', () => {
  const epsilon = 0.00001;
  for (const boundary of [0.12, 0.38, 0.6, 0.72, 0.82, 0.94]) {
    const before = pose(boundary - epsilon);
    const center = pose(boundary);
    const after = pose(boundary + epsilon);
    for (const field of Object.keys(center)) {
      assert.ok(Math.abs(before[field] - after[field]) < 0.001, `${boundary}: ${field}`);
      const leftSpeed = (center[field] - before[field]) / epsilon;
      const rightSpeed = (after[field] - center[field]) / epsilon;
      assert.ok(Math.abs(leftSpeed - rightSpeed) < 0.02, `${boundary}: ${field} hız değişimi`);
    }
  }
});
