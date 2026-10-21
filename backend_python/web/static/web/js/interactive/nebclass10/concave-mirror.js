/**
 * Concave mirror (NEB class 10), in 3D on the optics bench. Move the candle along the rail and watch the
 * image from beyond C to inside F, with the principal rays traced exactly. Jump to the textbook
 * positions and record u and v readings: each row computes f = uv/(u + v) from the student's own
 * numbers, which should agree.
 */
import { describe } from '../core/optics2d.js';
import { createOpticsBench } from '../physics/optics-bench.js';

const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

export default function init(stage) {
  const rows = [];
  const { handle } = createOpticsBench(stage, {
    title: 'Concave mirror', aim: 'Images formed by a concave mirror', kinds: ['concave-mirror'], kind: 'concave-mirror', f: 15, u: 45, fMax: 25, screen: false,
    hint: (r) => `u = ${fmt(stage.__cm ? stage.__cm.u() : 0, 0)} cm → ${describe(r)}`,
    extend(api) {
      const { panel, badge } = api;
      panel.chips({
        label: 'Put the candle…',
        options: [{ value: 'bc', label: 'Beyond C' }, { value: 'c', label: 'At C' }, { value: 'cf', label: 'Between C and F' }, { value: 'f', label: 'At F' }, { value: 'fp', label: 'Between F and P' }],
        value: '',
        onChange: (v) => { const f = api.f; api.setU({ bc: Math.min(50, Math.round(2.8 * f)), c: 2 * f, cf: Math.round(1.5 * f), f, fp: Math.round(0.5 * f) }[v]); },
      });
      panel.button({ label: 'Record this reading', icon: 'edit_note', onClick: record });
      const table = document.createElement('div');
      table.style.cssText = 'display:grid;grid-template-columns:repeat(3,1fr);gap:3px 10px;font:600 12px Poppins,system-ui,sans-serif;color:#cbd5e1;padding:8px 10px;border-radius:12px;background:rgba(255,255,255,0.04);flex-shrink:0';
      panel.body.appendChild(table);
      panel.info('Mirror formula 1/f = 1/u + 1/v (distances from the pole P, real-is-positive). Record readings at several positions: every row should give the same f.');
      function record() {
        const r = api.result(); const u = api.u;
        if (r.inf || !r.real) { badge.set('Only a real image can be caught on a screen: move the candle beyond F'); return; }
        rows.unshift({ u: fmt(u, 0), v: fmt(r.v, 1), f: fmt(u * r.v / (u + r.v), 1) });
        if (rows.length > 6) rows.pop();
        table.innerHTML = '<b style="color:#94a3b8;font-size:11px">u / cm</b><b style="color:#94a3b8;font-size:11px">v / cm</b><b style="color:#94a3b8;font-size:11px">f = uv/(u+v)</b>' + rows.map((x) => `<span>${x.u}</span><span>${x.v}</span><span>${x.f}</span>`).join('');
      }
      stage.__cm = { u: () => api.u, record, rows: () => rows };
    },
  });
  return handle;
}
