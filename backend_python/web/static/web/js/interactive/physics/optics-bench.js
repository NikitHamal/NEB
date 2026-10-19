/**
 * Optics bench — a ray-traced bench for convex and concave lenses and mirrors. Drag the object's
 * tip to move it and change its height, drag F to change the focal length, and on a lens bench
 * slide the screen until the real image is sharp. The three principal rays are traced exactly
 * (paraxial), so they meet where 1/f = 1/u + 1/v says the image is.
 */
import { createKit, T, fmt, background, grid } from '../core/kit2d.js';
import { createOptics, describe, KINDS } from '../core/optics2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

export default function init(stage) {
  const k = createKit(stage, { label: 'An optics bench with an object, a lens or mirror, and ray diagrams' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the object, F, or the screen', T.blue);
  const op = createOptics(k, { kind: 'convex-lens', f: 20, u: 45, h: 8, screen: true, span: 100 });

  const panel = createPanel(stage, { title: 'Optics bench' });
  panel.chips({ label: 'Element', options: Object.keys(KINDS).map((key) => ({ value: key, label: KINDS[key].label })), value: 'convex-lens', onChange: (v) => { op.setKind(v); relayout(); } });
  const fS = panel.slider({ label: 'Focal length |f|', min: 5, max: 40, step: 1, value: 20, format: (v) => `${v} cm`, onChange: (v) => { op.state.f = v; k.invalidate(); } });
  const uS = panel.slider({ label: 'Object distance u', min: 2, max: 98, step: 1, value: 45, format: (v) => `${v} cm`, onChange: (v) => { op.state.u = v; k.invalidate(); } });
  panel.chips({ label: 'Rays', options: [{ value: 'principal', label: 'Principal rays' }, { value: 'parallel', label: 'Parallel beam' }], value: 'principal', onChange: (v) => { op.state.mode = v; k.invalidate(); } });
  const st = panel.stats([{ key: 'u', label: 'u' }, { key: 'v', label: 'v' }, { key: 'm', label: 'm = −v/u' }, { key: 'f', label: 'f (signed)' }]);
  const nature = panel.readout({ label: 'Image', value: '—' });
  const check = panel.readout({ label: '1/u + 1/v', value: '—' });
  panel.info('Real-is-positive: u, v and f are positive for real objects, real images and converging elements; a negative v means a virtual image. Put the object inside F of a convex lens to make a magnifying glass.');
  op.state.onChange = () => { fS.set(op.state.f); uS.set(op.state.u); };

  function relayout() { op.state.span = k.small ? 60 : 100; op.state.u = Math.min(op.state.u, op.state.span - 2); op.layout(0, 0, k.w, k.h); k.invalidate(); }
  k.onResize(() => relayout());

  k.frame((ctx, dt, w, h) => {
    background(k, ctx, w, h);
    grid(ctx, 0, 0, w, h, 24, T.grid);
    const r = op.draw(ctx, dt);
    const s = op.state;
    st.u.set(`${fmt(s.u, 0)} cm`);
    st.v.set(r.inf ? '∞' : `${fmt(r.v, 1)} cm`);
    st.m.set(r.inf ? '∞' : fmt(r.m, 2));
    st.f.set(`${fmt(r.F, 0)} cm`);
    check.set(r.inf ? `1/u = 1/f → v = ∞` : `${fmt(1 / s.u, 3)} + ${fmt(1 / r.v, 3)} = ${fmt(1 / s.u + 1 / r.v, 3)} = 1/${fmt(r.F, 1)}`);
    nature.set(s.mode === 'parallel' ? `Parallel rays meet at F (${fmt(Math.abs(r.F), 0)} cm)` : describe(r));
    badge.set(s.screen !== null && KINDS[s.kind].lens && r.real && !r.inf ? (s.blur < 0.4 ? `Sharp image on the screen at v = ${fmt(r.v, 1)} cm` : 'Slide the screen to sharpen the image') : describe(r));
    k.animate(op.moving);
  });

  k.debug = { op: () => op.debug(), state: () => op.state, result: () => op.result };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
