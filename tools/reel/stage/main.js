'use strict';
// Runtime: preload, then window.__seek(t) poses every scene for time t and resolves once images are decoded.
const NEBY_USED = [
  ['classic', ['wave', 'hop', 'think', 'talk', 'success', 'celebrate', 'blink', 'idle']],
  ...LOOKS.map(([look, state]) => [look, [state]]),
];
const world = document.getElementById('world');
const flashEl = document.getElementById('flash');
const grain = document.getElementById('grain');
const gctx = grain.getContext('2d');
const gimg = gctx.createImageData(grain.width, grain.height);

function drawGrain(frame) {
  const r = rng(frame * 7919 + 13);
  const d = gimg.data;
  for (let i = 0; i < d.length; i += 4) {
    const v = (r() * 255) | 0;
    d[i] = d[i + 1] = d[i + 2] = v;
    d[i + 3] = 255;
  }
  gctx.putImageData(gimg, 0, 0);
}
grain.style.width = '1080px';
grain.style.height = '1920px';

window.__ready = (async () => {
  const jobs = [];
  for (const [look, states] of NEBY_USED) for (const s of states) jobs.push(loadImage(`neby/${look}/${s}`, `${ROOT}img/neby/${look}/${s}.png`));
  await Promise.all(jobs);
  await Promise.all([400, 500, 600, 700, 800, 900].map((w) => document.fonts.load(`${w} 64px Poppins`)));
  await document.fonts.load('24px MS', 'search');
  await document.fonts.ready;
  const imgs = [...document.querySelectorAll('img')];
  await Promise.all(imgs.map((i) => (i.complete ? Promise.resolve() : new Promise((r) => { i.onload = i.onerror = r; }))));
  return { duration: DURATION, fps: FPS, cues: CUES.length };
})();

window.__seek = async (t) => {
  for (const s of scenes) {
    const on = t >= s.a && t < s.b;
    s.root.style.visibility = on ? 'visible' : 'hidden';
    if (on) s.update(t);
  }
  const sh = shake(t, SHAKES);
  world.style.transform = `translate(${sh.x.toFixed(2)}px,${sh.y.toFixed(2)}px) rotate(${sh.r.toFixed(3)}deg)`;
  let f = 0;
  for (const [t0, a] of FLASHES) {
    const d = t - t0;
    if (d >= 0 && d < 0.4) f = Math.max(f, a * Math.exp(-d * 12));
  }
  flashEl.style.opacity = f.toFixed(3);
  drawGrain(Math.round(t * FPS));
  const pending = [];
  for (const s of scenes) {
    if (!(t >= s.a && t < s.b)) continue;
    for (const im of s.root.querySelectorAll('img')) if (im.getAttribute('src')) pending.push(im.decode().catch(() => {}));
  }
  await Promise.all(pending);
  return true;
};
window.__cues = () => CUES.slice().sort((a, b) => a.t - b.t);
