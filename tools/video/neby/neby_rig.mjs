// Neby rig server: the product's own avatar geometry (neby-avatar.js), driven by the film.
//
//   node neby_rig.mjs <neby-avatar.js>
//   stdin, one JSON per line: {"keys": [[expressionId, weight], ...], "t": ms, "blink": 0..1,
//                              "look": [x, y], "body": "#rrggbb"|null, "eyes": "#rrggbb"|null}
//   stdout, one line per request: the SVG Neby draws for that blended pose.
//
// Unlike the interactive player (timer-driven steps), every input here is continuous, so a
// film can animate Neby with eased, overlapping crossfades and no jumps.
import fs from 'node:fs';
import readline from 'node:readline';
import vm from 'node:vm';

const src = fs.readFileSync(process.argv[2], 'utf8')
  .replace('window.NebyAvatar = {', 'window.NebyAvatar = { engine: AvatarProceduralEngine,');

class El {
  constructor() { this.children = []; this.style = {}; this.classList = { add() {}, contains: () => false }; }
  setAttribute() {} append() {} addEventListener() {}
}
const document = {
  readyState: 'complete', createElementNS: () => new El(), querySelectorAll: () => [], addEventListener() {},
};
const window = { document, addEventListener() {}, requestAnimationFrame() {}, performance: { now: () => 0 } };
window.window = window;
const ctx = { window, document, performance: window.performance, setTimeout() {}, clearTimeout() {},
  requestAnimationFrame() {}, console, Math, Object, Array, Number, String, Symbol, JSON, Map, Set };
vm.createContext(ctx);
vm.runInContext(src, ctx);
const engine = ctx.window.NebyAvatar.engine;
const DATA = ctx.window.NebyAvatar.data;
const surface = DATA.avatar.surface;
const FIELDS = engine.expressionFields;
// Saccade-style eye motions jump by design; the film uses smooth drifts instead.
const EYE_SMOOTH = { microSaccades: 'wander', dart: 'lookAround', shake: 'focusPulse' };

function blend(keys, t) {
  const total = keys.reduce((s, [, w]) => s + w, 0) || 1;
  const out = {};
  const base = DATA.expressions[keys[0][0]];
  FIELDS.forEach(f => { out[f] = 0; });
  let bx = 0, by = 0, ex = 0, ey = 0;
  for (const [id, w0] of keys) {
    const w = w0 / total;
    const e = { ...DATA.expressions[id] };
    e.eyeMotion = EYE_SMOOTH[e.eyeMotion] || e.eyeMotion;
    const amb = e.bodyMotion && e.bodyMotion !== 'none' ? engine.applyAmbientBodyMotion(e, t, 1) : e;
    FIELDS.forEach(f => { out[f] += (amb[f] || 0) * w; });
    const bo = engine.ambientBodyOffset(e, t, 1);
    const eo = engine.ambientEyeOffset(e, t, 1);
    bx += bo.x * w; by += bo.y * w; ex += eo.x * w; ey += eo.y * w;
  }
  const dominant = keys.reduce((a, b) => (b[1] > a[1] ? b : a))[0];
  const d = DATA.expressions[dominant];
  return { expr: { ...base, ...out, eyeMotion: 'none', bodyMotion: 'none', mouth: d.mouth, effect: 'none' },
           body: { x: bx, y: by }, eye: { x: ex, y: ey } };
}

function svg(req) {
  const { expr, body, eye } = blend(req.keys, req.t || 0);
  const [lx, ly] = req.look || [0, 0];
  expr.headY = (expr.headY || 0) + lx * 18;
  expr.headX = (expr.headX || 0) - ly * 14;
  expr.positionXLeft = (expr.positionXLeft || 0) + lx * 4;
  expr.positionXRight = (expr.positionXRight || 0) + lx * 4;
  const pose = engine.poseFromExpression(expr);
  const g = engine.renderAvatar(pose, surface, req.blink == null ? 1 : req.blink,
    { includeWire: false, bodyNodes: DATA.avatar.bodyNodes, eyeOffset: eye });
  const bodyC = req.body || DATA.avatar.colors.body;
  const eyeC = req.eyes || DATA.avatar.colors.eyes;
  const paths = (list, fill) => (list || []).map(p => `<path d="${p}" fill="${fill}"/>`).join('');
  const decals = (g.decals || []).map(d => `<path d="${d.path}" fill="${d.fill}" opacity="${d.opacity ?? 1}"/>`).join('');
  const eyes = (g.leftVisible ? `<path d="${g.leftPath}" fill="${eyeC}"/>` : '') +
               (g.rightVisible ? `<path d="${g.rightPath}" fill="${eyeC}"/>` : '');
  const mouth = g.mouthVisible && g.mouthPath
    ? `<path d="${g.mouthPath}" fill="none" stroke="${eyeC}" stroke-width="${(2.8 * (expr.mouthScale || 1)).toFixed(1)}" stroke-linecap="round"/>` : '';
  const bbox = d => {
    const n = (d || '').match(/-?\d+(?:\.\d+)?/g) || [];
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (let i = 0; i + 1 < n.length; i += 2) {
      const x = +n[i], y = +n[i + 1];
      x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y);
    }
    return { x0, y0, x1, y1, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2 };
  };
  let props = '';
  if (req.jamara > 0 && g.headPath) {
    const hb = bbox(g.headPath);
    const s = req.jamara;
    const bx = hb.cx - (hb.x1 - hb.x0) * 0.16, by = hb.y0 + 10;
    const sway = Math.sin((req.t || 0) / 1000 * 2.2) * 3;
    let blades = '';
    for (let i = 0; i < 9; i++) {
      const a = (-0.62 + i * 0.155);
      const len = (34 + (i % 3) * 9) * s;
      const tx = bx + Math.sin(a) * len + sway * (len / 40), ty = by - Math.cos(a) * len;
      const col = ['#d9e64a', '#b8d43a', '#e8ef7a'][i % 3];
      blades += `<path d="M${bx - 2} ${by} Q${bx + Math.sin(a) * len * 0.5} ${by - Math.cos(a) * len * 0.6} ${tx} ${ty} Q${bx + Math.sin(a) * len * 0.5 + 3} ${by - Math.cos(a) * len * 0.55} ${bx + 2} ${by} Z" fill="${col}"/>`;
    }
    props += `<g>${blades}<rect x="${bx - 7}" y="${by - 4}" width="14" height="6" rx="3" fill="#e0313b"/></g>`;
  }
  if (req.tika > 0 && g.leftVisible && g.rightVisible) {
    const l = bbox(g.leftPath), r = bbox(g.rightPath);
    const k = req.tika;
    const cx = (l.cx + r.cx) / 2, top = Math.min(l.y0, r.y0);
    const h = 26 * k, w = 13 * k;
    const cy = top - 14 - h / 2;
    props += `<ellipse cx="${cx}" cy="${cy}" rx="${w / 2}" ry="${h / 2}" fill="#e0313b"/>` +
      [[-3, -5], [3, -1], [-1, 4], [4, 7], [-4, 2]].map(([dx, dy]) => `<ellipse cx="${cx + dx * k}" cy="${cy + dy * k}" rx="${1.6 * k}" ry="${1.1 * k}" fill="#fff6e8"/>`).join('');
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-150 -150 300 300"><defs><clipPath id="h"><path d="${g.headPath}"/></clipPath></defs>` +
    `<g transform="translate(${body.x} ${body.y})">${paths(g.backPaths, bodyC)}<path d="${g.headPath}" fill="${bodyC}"/>${decals}` +
    `<g clip-path="url(#h)">${eyes}</g>${mouth}${paths(g.frontPaths, bodyC)}${props}</g></svg>`;
}

const rl = readline.createInterface({ input: process.stdin });
rl.on('line', line => {
  let out;
  try { out = svg(JSON.parse(line)); } catch (e) { out = 'ERR ' + e.message; }
  process.stdout.write(out.replace(/\n/g, ' ') + '\n');
});
