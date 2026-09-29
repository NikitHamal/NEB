import { el } from './dom.js';
import { makeBackground } from './bg.js';
import { makeAmbient } from './ambient.js';
import { makeFx } from './fx.js';
import { makeChrome } from './chrome.js';
import { smoothstep } from './math.js';

async function loadFonts() {
  const loads = [400, 500, 600, 700, 800, 900].map((w) => document.fonts.load(`${w} 64px Poppins`, 'Aa नमस्ते'));
  loads.push(document.fonts.load("64px 'Material Symbols Outlined'", 'menu_book'));
  await Promise.all(loads);
  await document.fonts.ready;
}

const fetchText = async (url) => {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`cannot load ${url} (${res.status})`);
  return res.text();
};

const loadImage = (url) =>
  new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => img.decode().then(() => resolve(img), () => resolve(img));
    img.onerror = () => reject(new Error(`cannot load image ${url}`));
    img.src = url;
  });

export async function createStage(spec, params) {
  const aspect = params.get('aspect') ?? '16:9';
  const size = spec.meta.aspects[aspect];
  if (!size) throw new Error(`unknown aspect "${aspect}"`);
  const [W, H] = size;
  const root = document.getElementById('stage');
  root.style.width = `${W}px`;
  root.style.height = `${H}px`;
  await loadFonts();

  const bd = 60 / spec.meta.bpm;
  const palette = Object.fromEntries(Object.entries(spec.palette).map(([k, v]) => [k, v.hex]));
  const cues = (spec.cues ?? []).map((c) => ({ ...c, t: c.beat * bd, dur: (c.beats ?? 0) * bd }));
  const portrait = H > W;

  const S = {
    spec, W, H, cx: W / 2, cy: H / 2, aspect, portrait, square: H === W,
    u: Math.min(W / 1920, H / 1080),
    bd, palette, cues, mk: el,
    c: (name) => palette[name] ?? name,
    env(t, kinds, tau = 0.2) {
      let m = 0;
      for (const cue of cues) {
        if (t < cue.t || !kinds.includes(cue.kind)) continue;
        m = Math.max(m, Math.exp(-(t - cue.t) / tau));
      }
      return m;
    },
    pulse(t, { tau = 0.14 } = {}) {
      const since = (t / bd - Math.floor(t / bd)) * bd;
      return Math.exp(-since / tau);
    },
    header: portrait ? { pad: 48, top: 70, logoH: 50, word: 40 } : { pad: 72, top: 62, logoH: 58, word: 44 },
    assets: {},
    layers: {},
    capture: (id) => S.assets.captures?.[id] ?? null,
  };

  S.layers.world = el('div', { class: 'layer world' });
  root.append(S.layers.world);
  for (const name of ['bg', 'ambient', 'scenes', 'chrome']) {
    S.layers[name] = el('div', { class: `layer ${name}` });
    S.layers.world.append(S.layers[name]);
  }
  S.layers.fx = el('div', { class: 'layer fx' });
  root.append(S.layers.fx);
  S.bg = makeBackground(S);
  S.ambient = makeAmbient(S);
  S.layers.bg.append(S.bg.canvas);
  S.layers.ambient.append(S.ambient.canvas);
  S.fx = makeFx(S, S.layers);

  S.assets.logoSvg = await fetchText('/site/img/n-logo-master.svg');
  S.assets.captures = {};
  try {
    const manifest = JSON.parse(await fetchText('/assets/captures/manifest.json'));
    await Promise.all((manifest.items ?? []).map(async (item) => {
      S.assets.captures[item.id] = await loadImage(`/assets/captures/${item.file}`);
    }));
  } catch {
    S.assets.captures = {};
  }

  S.chrome = makeChrome(S);

  const ambientFrom = (spec.timeline[1]?.from ?? 4) * bd;
  S.frame = (t) => {
    S.bg.draw(t);
    S.ambient.draw(t, smoothstep(ambientFrom - 0.02, ambientFrom + 0.25, t));
    S.fx.apply(t);
    S.chrome?.update(t);
  };
  return S;
}
