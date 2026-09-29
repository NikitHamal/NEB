import test from 'node:test';
import assert from 'node:assert/strict';
import { encodeArgs, frameTimes, videoFilter } from '../pipeline/render.mjs';

test('one sample per frame lands exactly on the frame time', () => {
  const { frames, at } = frameTimes({ from: 0, to: 15, fps: 60, samples: 1, shutter: 0.5, duration: 15 });
  assert.equal(frames, 900);
  assert.equal(at(60, 0), 1);
});

test('sub-frame samples straddle the frame time inside the shutter window', () => {
  const { at } = frameTimes({ from: 0, to: 15, fps: 60, samples: 3, shutter: 0.5, duration: 15 });
  const [a, b, c] = [0, 1, 2].map((k) => at(60, k));
  assert.ok(a < b && b < c);
  assert.ok(Math.abs(b - 1) < 1e-9);
  assert.ok(c - a <= 0.5 / 60 + 1e-9);
});

test('samples never leave the film', () => {
  const { at } = frameTimes({ from: 0, to: 15, fps: 60, samples: 3, shutter: 0.5, duration: 15 });
  assert.ok(at(0, 0) >= 0);
  assert.ok(at(899, 2) < 15);
});

test('the filter chain averages sub-frames only when supersampling', () => {
  assert.doesNotMatch(videoFilter({ samples: 1, fps: 60, grain: 0 }), /tmix/);
  const chain = videoFilter({ samples: 3, fps: 60, grain: 1.5 });
  assert.match(chain, /tmix=frames=3/);
  assert.match(chain, /select='eq\(mod\(n\\,3\)\\,2\)'/);
  assert.match(chain, /noise=alls=1.5/);
  assert.match(chain, /out_color_matrix=bt709/);
});

test('encode arguments tag colour, set the frame rate and stay web friendly', () => {
  const args = encodeArgs({ fps: 60, samples: 3, grain: 0, crf: 15, preset: 'slow', out: 'x.mp4' }).join(' ');
  assert.match(args, /-framerate 180/);
  assert.match(args, /-r 60/);
  assert.match(args, /-colorspace bt709/);
  assert.match(args, /-pix_fmt yuv420p/);
  assert.match(args, /-movflags \+faststart/);
});
