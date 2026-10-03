import test from 'node:test';
import assert from 'node:assert/strict';
import { loadSpec } from '../lib/spec.mjs';
import { SR, midi } from '../audio/dsp.mjs';
import { compose } from '../audio/score.mjs';

test('midi note 69 is concert A', () => {
  assert.equal(midi(69), 440);
  assert.ok(Math.abs(midi(81) - 880) < 1e-9);
});

test('the score fills the film exactly, stays finite and leaves headroom', () => {
  const spec = loadSpec();
  const { L, R, kickTimes } = compose(spec);
  assert.equal(L.length, spec.meta.duration * SR);
  assert.equal(R.length, L.length);
  let peak = 0;
  for (let i = 0; i < L.length; i += 1) {
    assert.ok(Number.isFinite(L[i]) && Number.isFinite(R[i]));
    peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
  }
  assert.ok(peak <= 0.71 && peak > 0.3, `peak ${peak}`);
  assert.ok(kickTimes.length >= 26, `kicks ${kickTimes.length}`);
});

test('the film fades out to silence at the very end', () => {
  const { L } = compose(loadSpec());
  assert.ok(Math.abs(L[L.length - 1]) < 1e-3);
});
