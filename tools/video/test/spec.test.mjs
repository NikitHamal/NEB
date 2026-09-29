import test from 'node:test';
import assert from 'node:assert/strict';
import { CUE_KINDS, aspectSize, cueTimes, derive, loadSpec, validateSpec } from '../lib/spec.mjs';

const fresh = () => structuredClone(loadSpec());

test('the shipped spec is valid', () => {
  assert.deepEqual(validateSpec(loadSpec()), []);
});

test('15 seconds at 128 BPM is 32 beats and 900 frames', () => {
  const d = derive(loadSpec());
  assert.equal(d.totalBeats, 32);
  assert.equal(d.totalFrames, 900);
  assert.equal(d.beatSeconds, 0.46875);
});

test('a gap in the timeline is rejected', () => {
  const spec = fresh();
  spec.timeline[2].from += 1;
  assert.match(validateSpec(spec).join('\n'), /starts at beat/);
});

test('a timeline that stops short of the duration is rejected', () => {
  const spec = fresh();
  spec.timeline.at(-1).to -= 1;
  assert.match(validateSpec(spec).join('\n'), /timeline ends at beat/);
});

test('unknown cue kinds are rejected', () => {
  const spec = fresh();
  spec.cues.push({ beat: 1, kind: 'kazoo' });
  assert.match(validateSpec(spec).join('\n'), /unknown kind "kazoo"/);
});

test('cues outside the film are rejected', () => {
  const spec = fresh();
  spec.cues.push({ beat: 99, kind: 'pop' });
  assert.match(validateSpec(spec).join('\n'), /outside/);
});

test('malformed palette hex is rejected', () => {
  const spec = fresh();
  spec.palette.blue.hex = 'blue';
  assert.match(validateSpec(spec).join('\n'), /palette\.blue\.hex/);
});

test('cue times follow the BPM', () => {
  const spec = fresh();
  spec.meta.bpm = 120;
  spec.cues = [{ beat: 4, kind: 'boom' }, { beat: 2, kind: 'riser', beats: 2 }];
  const [boom, riser] = cueTimes(spec);
  assert.equal(boom.t, 2);
  assert.equal(riser.dur, 1);
});

test('every cue kind used by the spec is a known kind', () => {
  for (const cue of loadSpec().cues) assert.ok(CUE_KINDS.includes(cue.kind), cue.kind);
});

test('aspect sizes resolve and unknown aspects throw', () => {
  assert.deepEqual(aspectSize(loadSpec(), '16:9'), { width: 1920, height: 1080 });
  assert.throws(() => aspectSize(loadSpec(), '4:3'), /unknown aspect/);
});
