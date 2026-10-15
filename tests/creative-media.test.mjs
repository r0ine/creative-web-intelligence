import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { buildVideoPrompts } from '../runtime/media/video-prompt.mjs';
import { selectCreativeSources } from '../runtime/media/source-selection.mjs';
import { resolveSequenceFiles } from '../runtime/media/sequence-manifest.mjs';

const brief = JSON.parse(await readFile(new URL('../examples/v6/video-brief.json', import.meta.url), 'utf8'));
const catalog = JSON.parse(await readFile(new URL('../data/v6/creative_sources.json', import.meta.url), 'utf8'));

test('scroll prompt preserves the subject and requests reversible motion and portrait recomposition', () => {
  const prompts = buildVideoPrompts(brief);
  assert.ok(prompts.desktop.includes(brief.subject));
  assert.match(prompts.desktop, /forwards and backwards/);
  assert.match(prompts.mobile, /do not crop/);
  assert.equal(prompts.delivery.playback, 'frame-sequence');
  assert.equal(prompts.storyboard.at(-1).endSeconds, brief.durationSeconds);
  assert.equal(prompts.delivery.reducedMotion, 'poster');
  assert.match(prompts.chatgpt, /video ürettiğini iddia etmeden/);
});

test('background prompt asks for a closed light cycle without object disassembly', () => {
  const prompts = buildVideoPrompts({ ...brief, mode: 'background' });
  assert.match(prompts.desktop, /First and last frames must match/);
  assert.doesNotMatch(prompts.desktop, /Separate its main parts/);
  assert.equal(prompts.delivery.playback, 'muted-loop');
});

test('custom shot progression is preserved instead of replaced by the lamp storyboard', () => {
  const prompts = buildVideoPrompts({ ...brief, beats: [[0, .5, 'Reveal the fold.'], [.5, 1, 'Unfold the fabric.']] });
  assert.deepEqual(prompts.storyboard.map(beat => beat.action), ['Reveal the fold.', 'Unfold the fabric.']);
  assert.match(prompts.desktop, /4–8s: Unfold the fabric/);
});

test('gaps, invalid timing and missing creative direction are rejected', () => {
  for (const change of [
    { subject: '' }, { purpose: null }, { durationSeconds: Infinity }, { durationSeconds: 30 },
    { frameCount: 13.5 }, { frameCount: 500 }, { mode: 'webgl' },
    { beats: [[0, .4, 'Hold.'], [.5, 1, 'Finish.']] },
    { beats: [[0, .5, 'Hold.'], [.5, .8, 'Finish.']] },
  ]) assert.throws(() => buildVideoPrompts({ ...brief, ...change }));
});

test('project source selection includes React Bits and official 21st handoff', () => {
  const sources = selectCreativeSources(catalog, { role: 'hero' });
  assert.ok(sources.some(source => source.id === 'react-bits'));
  assert.equal(sources.find(source => source.id === '21st').access, 'official-copy-prompt');
});

test('library source selection excludes restricted and item-level unknown licenses', () => {
  const sources = selectCreativeSources(catalog, { scope: 'library' });
  assert.ok(sources.length > 0);
  assert.ok(sources.every(source => source.libraryRedistribution === 'license-notice'));
  assert.ok(!sources.some(source => ['react-bits', '21st'].includes(source.id)));
});

test('vanilla projects do not receive React components as compatible dependencies', () => {
  assert.deepEqual(selectCreativeSources(catalog, { framework: 'vanilla' }).map(source => source.id), ['cwi-native']);
  assert.deepEqual(selectCreativeSources(catalog, { framework: 'vanilla', role: 'template' }), []);
  assert.throws(() => selectCreativeSources(catalog, { scope: 'unknown' }));
});

function sequenceFixture() {
  const frames = Array.from({ length: 12 }, (_, index) => ({ file: `frames/frame-${index}.webp`, bytes: 100 }));
  const manifest = { version: 1, kind: 'video-frame-sequence', frameCount: 12, frames, poster: { file: 'poster.webp', bytes: 100 } };
  const files = [...frames, manifest.poster].map(record => ({
    name: record.file.split('/').at(-1), webkitRelativePath: `export/${record.file}`, size: record.bytes,
  }));
  return { manifest, files };
}

test('folder manifest resolves ordered local files without consulting a remote URL', () => {
  const { manifest, files } = sequenceFixture();
  const selected = resolveSequenceFiles(manifest, files);
  assert.equal(selected.frames.length, 12);
  assert.equal(selected.frames.at(-1).name, 'frame-11.webp');
  assert.equal(selected.poster.name, 'poster.webp');
});

test('missing, duplicate and changed frames are rejected before replacing the preview', () => {
  const { manifest, files } = sequenceFixture();
  assert.throws(() => resolveSequenceFiles(manifest, files.slice(1)));
  assert.throws(() => resolveSequenceFiles(manifest, [...files, files[0]]));
  assert.throws(() => resolveSequenceFiles(manifest, files.map((file, index) => index === 0 ? { ...file, size: 90 } : file)));
  assert.throws(() => resolveSequenceFiles({ ...manifest, frames: [manifest.frames[0], ...manifest.frames.slice(0, -1)] }, files));
});

test('manifest cannot inject external URLs or traverse outside the selected folder', () => {
  for (const path of ['../poster.webp', 'https://reactbits.dev/frame.webp', '/poster.webp', 'frames//frame.webp']) {
    const { manifest, files } = sequenceFixture();
    manifest.frames[0].file = path;
    assert.throws(() => resolveSequenceFiles(manifest, files));
  }
});
