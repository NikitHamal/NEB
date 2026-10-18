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
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-150 -150 300 300"><defs><clipPath id="h"><path d="${g.headPath}"/></clipPath></defs>` +
    `<g transform="translate(${body.x} ${body.y})">${paths(g.backPaths, bodyC)}<path d="${g.headPath}" fill="${bodyC}"/>${decals}` +
    `<g clip-path="url(#h)">${eyes}</g>${mouth}${paths(g.frontPaths, bodyC)}</g></svg>`;
}

const rl = readline.createInterface({ input: process.stdin });
rl.on('line', line => {
  let out;
  try { out = svg(JSON.parse(line)); } catch (e) { out = 'ERR ' + e.message; }
  process.stdout.write(out.replace(/\n/g, ' ') + '\n');
});
