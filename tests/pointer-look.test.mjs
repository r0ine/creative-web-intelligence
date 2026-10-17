import assert from 'node:assert/strict';
import test from 'node:test';
import { observePointerLook, samplePointerLook } from '../runtime/three/pointer-look.mjs';

test('fare bakışı scroll pozuna küçük ve sınırlı bir katkı verir', () => {
  assert.equal(samplePointerLook(0, 0).yaw, 0);
  assert.ok(samplePointerLook(0, 0).height === 0);
  assert.equal(samplePointerLook(5, -5).yaw, 7 * Math.PI / 180);
  assert.equal(samplePointerLook(5, -5).height, 0.18);
  for (const value of [NaN, Infinity, undefined]) assert.throws(() => samplePointerLook(value, 0), TypeError);
});

test('fare hareketi yumuşar; hareket azaltma ve kapatma dinleyicileri temizler', () => {
  const element = new EventTarget();
  element.getBoundingClientRect = () => ({ left: 10, top: 20, width: 200, height: 100 });
  const fine = new EventTarget();
  fine.matches = true;
  const reduced = new EventTarget();
  reduced.matches = false;
  const document = new EventTarget();
  document.hidden = false;
  const pending = new Map();
  let nextId = 0;
  const view = {
    document,
    matchMedia(query) { return query.includes('hover') ? fine : reduced; },
    requestAnimationFrame(callback) { pending.set(++nextId, callback); return nextId; },
    cancelAnimationFrame(id) { pending.delete(id); },
  };
  const changes = [];
  const look = observePointerLook({ element, onChange: (x, y) => changes.push([x, y]), window: view });
  const move = new Event('pointermove');
  Object.assign(move, { clientX: 210, clientY: 20 });
  element.dispatchEvent(move);
  assert.equal(pending.size, 1);
  for (let frame = 0; frame < 35; frame++) {
    const [id, callback] = pending.entries().next().value ?? [];
    if (!callback) break;
    pending.delete(id);
    callback(frame * 16);
  }
  assert.ok(changes.at(-1)[0] > 0.99);
  assert.ok(changes.at(-1)[1] < -0.99);

  reduced.matches = true;
  reduced.dispatchEvent(new Event('change'));
  for (let frame = 35; frame < 80; frame++) {
    const [id, callback] = pending.entries().next().value ?? [];
    if (!callback) break;
    pending.delete(id);
    callback(frame * 16);
  }
  assert.deepEqual(changes.at(-1), [0, 0]);
  look.destroy();
  reduced.matches = false;
  reduced.dispatchEvent(new Event('change'));
  element.dispatchEvent(move);
  assert.equal(pending.size, 0);
});
