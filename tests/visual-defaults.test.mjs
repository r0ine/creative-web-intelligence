import assert from 'node:assert/strict';
import test from 'node:test';
import { inspectVisualDefaults } from '../tools/v7/audit_visual_defaults.mjs';

test('işlevsel ve sakin yüzey gereksiz bulgu üretmez', () => {
  const css = ':root { background: #f4f1eb; } .upload { background: #e8e4dc; border-radius: 20px; padding: 24px; }';
  assert.deepEqual(inspectVisualDefaults(css), []);
});

test('tekrarlanan kutular ve koyu çizgi yoğunluğu görünür', () => {
  const css = ':root { background: #101815; } .a { border: 1px solid; background: #222; padding: 20px; } .b { border: 1px solid; background: #222; padding: 20px; } .c { border: 1px solid; background: #222; padding: 20px; } .d { border-top: 1px solid; } .e { border-bottom: 1px solid; }';
  const codes = inspectVisualDefaults(css).map(finding => finding.code);
  assert.ok(codes.includes('repeated-boxes'));
  assert.ok(codes.includes('dark-hairlines'));
});

test('otomatik hareket kalıpları işaretlenir', () => {
  const css = '.a { opacity: 0; transform: translateY(30px); transition: all .5s; } .b { opacity: 0; transform: translateY(30px); animation: float 4s infinite; }';
  const codes = inspectVisualDefaults(css).map(finding => finding.code);
  assert.ok(codes.includes('repeated-fade-up'));
  assert.ok(codes.includes('transition-all'));
  assert.ok(codes.includes('infinite-motion'));
});
