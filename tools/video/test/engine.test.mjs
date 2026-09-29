import test from 'node:test';
import assert from 'node:assert/strict';
import * as E from '../stage/engine/ease.js';
import { keys, seg } from '../stage/engine/tl.js';
import { rng } from '../stage/engine/rng.js';
import { makeNoise } from '../stage/engine/noise.js';
import { mixHex, parseHex } from '../stage/engine/color.js';
import { clamp, lerp, remap } from '../stage/engine/math.js';

const NAMED = ['linear', 'inQuad', 'outQuad', 'inOutQuad', 'inCubic', 'outCubic', 'inOutCubic', 'inQuart', 'outQuart', 'inOutQuart', 'inQuint', 'outQuint', 'inOutQuint', 'inExpo', 'outExpo', 'inOutExpo', 'inCirc', 'outCirc', 'inOutCirc', 'inBack', 'outBack', 'inOutBack', 'outElastic', 'outBounce', 'smooth', 'swift', 'punch'];

for (const name of NAMED) {
  test(`${name} maps 0 to 0 and 1 to 1`, () => {
    assert.ok(Math.abs(E[name](0)) < 1e-9, `${name}(0)`);
    assert.ok(Math.abs(E[name](1) - 1) < 1e-9, `${name}(1)`);
  });
}

test('outExpo never decreases', () => {
  let last = -1;
  for (let i = 0; i <= 100; i += 1) {
    const v = E.outExpo(i / 100);
    assert.ok(v >= last);
    last = v;
  }
});

test('bezier(0,0,1,1) is the identity', () => {
  const f = E.bezier(0, 0, 1, 1);
  for (const x of [0.1, 0.35, 0.5, 0.9]) assert.ok(Math.abs(f(x) - x) < 1e-4);
});

test('an under-damped spring overshoots then settles on 1', () => {
  const f = E.spring(0.4, 14);
  const samples = Array.from({ length: 200 }, (_, i) => f(i / 199));
  assert.ok(Math.max(...samples) > 1.05);
  assert.equal(f(1), 1);
  assert.ok(Math.abs(f(0.95) - 1) < 0.02);
});

test('seg clamps outside its window and eases inside it', () => {
  assert.equal(seg(-1, 0, 1), 0);
  assert.equal(seg(2, 0, 1), 1);
  assert.equal(seg(0.5, 0, 1), 0.5);
  assert.equal(seg(0.5, 0, 0), 1);
});

test('keys interpolates between frames and holds the ends', () => {
  const frames = [[0, 0], [1, 10], [2, 0]];
  assert.equal(keys(-1, frames), 0);
  assert.equal(keys(0.5, frames), 5);
  assert.equal(keys(1.5, frames), 5);
  assert.equal(keys(9, frames), 0);
});

test('the seeded rng is deterministic and stays in range', () => {
  const a = rng(42);
  const b = rng(42);
  for (let i = 0; i < 50; i += 1) {
    const v = a();
    assert.equal(v, b());
    assert.ok(v >= 0 && v < 1);
  }
  assert.notEqual(rng('a')(), rng('b')());
});

test('noise is deterministic and bounded', () => {
  const one = makeNoise(3);
  const two = makeNoise(3);
  for (let i = 0; i < 40; i += 1) {
    const v = one.noise2(i * 0.37, i * 0.11);
    assert.equal(v, two.noise2(i * 0.37, i * 0.11));
    assert.ok(Math.abs(v) <= 1.05);
  }
});

test('colour helpers parse and mix', () => {
  assert.deepEqual(parseHex('#004AC6'), [0, 74, 198]);
  assert.equal(mixHex('#000000', '#FFFFFF', 0.5), '#808080');
});

test('math helpers', () => {
  assert.equal(clamp(5, 0, 1), 1);
  assert.equal(lerp(0, 10, 0.25), 2.5);
  assert.equal(remap(5, 0, 10, 100, 200), 150);
});
