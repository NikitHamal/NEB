import { createStage } from './engine/stage.js';
import { show } from './engine/dom.js';
import { SCENES } from './scenes/index.js';

async function boot() {
  const params = new URLSearchParams(location.search);
  const spec = await (await fetch('/spec/launch.spec.json')).json();
  const S = await createStage(spec, params);

  const runtime = spec.timeline.map((entry) => {
    const scene = SCENES[entry.id];
    if (!scene) throw new Error(`no scene implementation for timeline id "${entry.id}" (available: ${Object.keys(SCENES).join(', ')})`);
    const from = entry.from * S.bd;
    const to = entry.to * S.bd;
    const root = S.mk('div', { class: 'scene', 'data-scene': entry.id });
    S.layers.scenes.append(root);
    const inst = scene.build(S, spec.scenes?.[entry.id] ?? {}, { ...entry, start: from, end: to }, root);
    return { entry, inst, root, from, to, pre: inst.pre ?? 0, post: inst.post ?? 0 };
  });

  if (window.NebArt) window.NebArt.scan(S.layers.scenes);

  const seek = (t) => {
    for (const r of runtime) {
      const on = t >= r.from - r.pre && t < r.to + r.post;
      show(r.root, on);
      if (on) r.inst.update(t - r.from, t);
    }
    S.frame(t);
    return true;
  };
  window.__seek = seek;
  window.__label = (text) => {
    let badge = document.getElementById('debug-label');
    if (!badge) {
      badge = S.mk('div', { id: 'debug-label', style: 'position:absolute;right:16px;bottom:16px;z-index:99;padding:8px 16px;border-radius:999px;background:rgba(0,0,0,.72);color:#fff;font:600 28px Poppins' });
      document.getElementById('stage').append(badge);
    }
    badge.textContent = text;
  };
  window.__info = { aspect: S.aspect, width: S.W, height: S.H, fps: spec.meta.fps, duration: spec.meta.duration, beat: S.bd };
  seek(0);
}

window.__ready = boot().then(() => true);
