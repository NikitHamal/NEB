/**
 * Concave mirror (NEB class 10) — move the object along the principal axis and watch the image
 * from beyond C to inside F, with the ray diagram traced exactly. Jump to the six textbook
 * positions, switch to a distant object (parallel rays meet at F) to find f the school-lab way,
 * and record u and v readings: each row computes f = uv/(u + v) from the student's own numbers.
 */
import { createKit, T, fmt, background, grid } from '../core/kit2d.js';
import { createOptics, describe } from '../core/optics2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

export default function init(stage) {
  const k = createKit(stage, { label: 'A concave mirror on a principal axis with an object and its ray diagram' });
  const hud = createHud(stage);
  const badge = hud.badge('Drag the object along the axis', T.blue);
  const op = createOptics(k, { kind: 'concave-mirror', f: 15, u: 45, h: 6, span: 70, regions: true });
  const rows = [];

  const panel = createPanel(stage, { title: 'Concave mirror' });
  const fS = panel.slider({ label: 'Focal length f', min: 6, max: 25, step: 1, value: 15, format: (v) => `${v} cm (R = ${2 * v} cm)`, onChange: (v) => { op.state.f = v; k.invalidate(); } });
  const uS = panel.slider({ label: 'Object distance u', min: 2, max: 68, step: 1, value: 45, format: (v) => `${v} cm`, onChange: (v) => { op.state.u = v; k.invalidate(); } });
  const pos = panel.chips({
    label: 'Put the object…',
    options: [{ value: 'far', label: 'Far away' }, { value: 'bc', label: 'Beyond C' }, { value: 'c', label: 'At C' }, { value: 'cf', label: 'Between C and F' }, { value: 'f', label: 'At F' }, { value: 'fp', label: 'Between F and P' }],
    value: 'bc',
    onChange: (v) => {
      const f = op.state.f;
      op.state.mode = v === 'far' ? 'parallel' : 'principal';
      op.state.u = { far: 66, bc: Math.min(66, Math.round(3 * f)), c: 2 * f, cf: Math.round(1.5 * f), f, fp: Math.round(0.5 * f) }[v];
      uS.set(op.state.u); k.invalidate();
    },
  });
  const st = panel.stats([{ key: 'u', label: 'u' }, { key: 'v', label: 'v' }, { key: 'm', label: 'm = −v/u' }, { key: 'nat', label: 'Image' }]);
  panel.button({ label: 'Record this reading', icon: 'edit_note', onClick: record });
  const table = document.createElement('div');
  table.className = 'k2-table';
  panel.body.appendChild(table);
  panel.info('Mirror formula 1/f = 1/u + 1/v (distances from the pole P, real-is-positive). Record readings at several positions: every row should give the same f.');
  op.state.onChange = () => { fS.set(op.state.f); uS.set(op.state.u); pos.set(''); };

  function record() {
    const r = op.result, s = op.state;
    if (s.mode === 'parallel') { rows.unshift({ u: '∞', v: fmt(s.f, 1), f: fmt(s.f, 1) }); }
    else if (r.inf || !r.real) { badge.set('Only a real image can be caught on a screen: move the object beyond F'); return; }
    else rows.unshift({ u: fmt(s.u, 0), v: fmt(r.v, 1), f: fmt(s.u * r.v / (s.u + r.v), 1) });
    if (rows.length > 6) rows.pop();
    table.innerHTML = '<div class="k2-tr k2-th"><span>u / cm</span><span>v / cm</span><span>f = uv/(u+v)</span></div>' + rows.map((x) => `<div class="k2-tr"><span>${x.u}</span><span>${x.v}</span><span>${x.f}</span></div>`).join('');
  }

  k.onResize((w, h) => { op.state.span = k.small ? 50 : 70; op.layout(0, 0, w, h); });

  k.frame((ctx, dt, w, h) => {
    background(k, ctx, w, h);
    grid(ctx, 0, 0, w, h, 24, T.grid);
    const r = op.draw(ctx, dt);
    const s = op.state;
    st.u.set(s.mode === 'parallel' ? '∞' : `${fmt(s.u, 0)} cm`);
    st.v.set(s.mode === 'parallel' ? `${fmt(s.f, 0)} cm (at F)` : r.inf ? '∞' : `${fmt(r.v, 1)} cm`);
    st.m.set(s.mode === 'parallel' || r.inf ? '—' : fmt(r.m, 2));
    st.nat.set(s.mode === 'parallel' ? 'Point image at F' : describe(r).replace('At infinity (no image)', 'At infinity'));
    badge.set(s.mode === 'parallel' ? `Rays from a distant object meet at F: f = ${s.f} cm` : `u = ${fmt(s.u, 0)} cm → ${describe(r)}`);
    k.animate(op.moving);
  });

  k.debug = { op: () => op.debug(), state: () => op.state, result: () => op.result, rows: () => rows, record };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
