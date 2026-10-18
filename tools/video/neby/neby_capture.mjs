// Run the product's own Neby avatar (backend_python/web/static/web/js/neby-avatar.js)
// under a tiny fake DOM and a virtual clock, and dump the SVG it draws at every frame.
//
//   node neby_capture.mjs <neby-avatar.js> <out.json> <fps> <clip>=<animation>:<seconds>[:react1@t,react2@t] ...
//
// Each clip mounts a fresh avatar playing <animation> and records <seconds> of frames.
import fs from 'node:fs';
import vm from 'node:vm';

const [, , src, out, fpsArg, ...clipArgs] = process.argv;
const fps = Number(fpsArg || 60);
const code = fs.readFileSync(src, 'utf8');

const esc = s => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

class El {
  constructor(tag) {
    this.tagName = tag;
    this.attrs = {};
    this.children = [];
    this.parent = null;
    this.style = {};
    this._classes = new Set();
    this.classList = {
      add: (...c) => c.forEach(x => this._classes.add(x)),
      remove: (...c) => c.forEach(x => this._classes.delete(x)),
      contains: c => this._classes.has(c),
      toggle: c => (this._classes.has(c) ? this._classes.delete(c) : this._classes.add(c)),
    };
  }
  set id(v) { this.attrs.id = v; }
  get id() { return this.attrs.id; }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; }
  removeAttribute(k) { delete this.attrs[k]; }
  append(...kids) { if (this._raw && this.tagName === 'div') this._raw = ''; kids.forEach(k => { k.parent = this; this.children.push(k); }); }
  appendChild(k) { this.append(k); return k; }
  remove() { if (this.parent) { this.parent.children = this.parent.children.filter(c => c !== this); this.parent = null; } }
  get lastElementChild() { return this.children[this.children.length - 1] || null; }
  get firstElementChild() { return this.children[0] || null; }
  set innerHTML(v) { this.children.forEach(c => (c.parent = null)); this.children = []; this._raw = String(v || ''); }
  get innerHTML() { return (this._raw || '') + this.children.map(c => c.serialize()).join(''); }
  addEventListener() {}
  removeEventListener() {}
  getBoundingClientRect() { return { left: 0, top: 0, width: 300, height: 300, right: 300, bottom: 300 }; }
  querySelector() { return null; }
  querySelectorAll() { return []; }
  closest() { return null; }
  serialize() {
    if (this.style.display === 'none') return '';
    const cls = this._classes.size ? ` class="${esc([...this._classes].join(' '))}"` : '';
    const a = Object.entries(this.attrs).filter(([k]) => k !== 'class').map(([k, v]) => ` ${k}="${esc(v)}"`).join('');
    const extra = this.tagName === 'svg' ? ' xmlns="http://www.w3.org/2000/svg"' : '';
    const op = this.style.opacity != null && this.style.opacity !== '' ? ` opacity="${esc(this.style.opacity)}"` : '';
    const tf = this.style.transform ? '' : '';
    return `<${this.tagName}${extra}${cls}${a}${op}${tf}>${this._raw || ''}${this.children.map(c => c.serialize()).join('')}</${this.tagName}>`;
  }
}

function makeWorld() {
  let now = 0;
  let timerId = 0;
  const timers = new Map();
  let rafs = [];
  let seed = 1234567;
  const rand = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };
  const document = {
    readyState: 'complete',
    createElementNS: (_ns, tag) => new El(tag),
    createElement: tag => new El(tag),
    querySelectorAll: () => [],
    querySelector: () => null,
    getElementById: () => null,
    addEventListener() {},
    body: null,
  };
  const MathR = Object.create(Math);
  MathR.random = rand;
  const window = {
    document,
    innerWidth: 1920, innerHeight: 1080,
    addEventListener() {}, removeEventListener() {},
    requestAnimationFrame: cb => { rafs.push(cb); return rafs.length; },
    cancelAnimationFrame: () => {},
    setTimeout: (cb, ms) => { const id = ++timerId; timers.set(id, { at: now + (ms || 0), cb }); return id; },
    clearTimeout: id => timers.delete(id),
    performance: { now: () => now },
  };
  const ctx = {
    window, document, performance: window.performance,
    requestAnimationFrame: window.requestAnimationFrame, cancelAnimationFrame: window.cancelAnimationFrame,
    setTimeout: window.setTimeout, clearTimeout: window.clearTimeout,
    Math: MathR, console, Object, Array, Number, String, Symbol, JSON, Map, Set, Boolean, Infinity, NaN,
    parseInt, parseFloat, isNaN, isFinite, Date: { now: () => now },
  };
  window.window = window;
  vm.createContext(ctx);
  vm.runInContext(code, ctx);
  const advance = ms => {
    const target = now + ms;
    for (;;) {
      let next = null;
      for (const [id, t] of timers) if (t.at <= target && (!next || t.at < next[1].at)) next = [id, t];
      if (!next) break;
      now = Math.max(now, next[1].at);
      timers.delete(next[0]);
      next[1].cb();
    }
    now = target;
    const cbs = rafs;
    rafs = [];
    cbs.forEach(cb => cb(now));
  };
  return { ctx, advance, now: () => now };
}

const result = { fps, clips: {} };
for (const arg of clipArgs) {
  const [name, spec] = arg.split('=');
  const [anim, secs, reacts] = spec.split(':');
  const w = makeWorld();
  const container = new El('div');
  const inst = w.ctx.window.NebyAvatar.mount(container, { animation: anim, hero: false, interactive: false });
  const plan = (reacts || '').split(',').filter(Boolean).map(r => { const [k, t] = r.split('@'); return { k, t: Number(t), done: false }; });
  const frames = [];
  const n = Math.round(Number(secs) * fps);
  for (let i = 0; i < n; i++) {
    const t = i / fps;
    for (const p of plan) if (!p.done && t >= p.t) {
      p.done = true;
      if (p.k.startsWith('look')) { const [, x, y] = p.k.split('|'); inst.setLookAt(Number(x), Number(y)); }
      else inst.react(p.k);
    }
    w.advance(1000 / fps);
    frames.push(container.innerHTML);
  }
  result.clips[name] = frames;
  process.stderr.write(`${name}: ${anim} ${frames.length} frames\n`);
}
fs.writeFileSync(out, JSON.stringify(result));
