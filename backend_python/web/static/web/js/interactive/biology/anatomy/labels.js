import { THREE } from '../../core/engine.js';

const CSS = `
.an-labels{position:absolute;inset:0;pointer-events:none;z-index:3;font-family:Poppins,system-ui,sans-serif;overflow:hidden}
.an-labels svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.an-labels line,.an-labels polyline{stroke:rgba(235,242,255,.75);stroke-width:1.1;fill:none}
.an-labels circle{fill:#fff;stroke:rgba(0,0,0,.45);stroke-width:1}
.an-label{position:absolute;left:0;top:0;pointer-events:auto;cursor:pointer;white-space:nowrap;font-size:12px;font-weight:600;color:#f3f6ff;
  background:rgba(10,14,26,.62);border:1px solid rgba(255,255,255,.14);padding:4px 9px;border-radius:999px;backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);
  transition:background .2s,border-color .2s;transform-origin:left center}
.an-label:hover,.an-label.on{background:rgba(59,130,246,.85);border-color:rgba(147,197,253,.9)}
.an-label i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;vertical-align:0}
@media (max-width:640px){.an-label{font-size:10.5px;padding:3px 7px}}
`;
let styled = false;

export function createAtlasLabels(stage, { onPick } = {}) {
  if (!styled) { const s = document.createElement('style'); s.textContent = CSS; document.head.appendChild(s); styled = true; }
  const root = document.createElement('div');
  root.className = 'an-labels';
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  root.appendChild(svg);
  stage.appendChild(root);
  const items = [];
  const v = new THREE.Vector3();
  let enabled = true;
  let active = null;

  function add(def) {
    const el = document.createElement('div');
    el.className = 'an-label';
    el.innerHTML = `${def.color ? `<i style="background:${def.color}"></i>` : ''}${def.text}`;
    el.addEventListener('click', (e) => { e.stopPropagation(); if (onPick) onPick(def.id); });
    root.appendChild(el);
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
    const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('r', '2.6');
    svg.appendChild(line); svg.appendChild(dot);
    const it = { def, el, line, dot, w: 0 };
    items.push(it);
    return it;
  }

  function hideItem(it) { it.el.style.display = 'none'; it.line.style.display = 'none'; it.dot.style.display = 'none'; }

  function update(camera, width, height, filter) {
    const phone = width < 640;
    const vis = [];
    for (const it of items) {
      if (!enabled || (filter && !filter(it.def)) || (phone && it.def.minor)) { hideItem(it); continue; }
      v.copy(it.def.anchor);
      if (it.def.object) it.def.object.localToWorld(v);
      v.project(camera);
      if (v.z > 1) { hideItem(it); continue; }
      const x = (v.x * 0.5 + 0.5) * width; const y = (-v.y * 0.5 + 0.5) * height;
      if (x < 0 || x > width || y < 0 || y > height) { hideItem(it); continue; }
      if (!it.w) it.w = it.el.offsetWidth || it.def.text.length * 7 + 24;
      vis.push({ it, x, y });
    }
    const margin = phone ? 6 : 14;
    const gap = phone ? 22 : 27;
    for (const side of [0, 1]) {
      const col = vis.filter((o) => (side === 0 ? o.x < width / 2 : o.x >= width / 2)).sort((a, b) => a.y - b.y);
      let last = (phone ? 46 : 40) - gap;
      col.forEach((o) => { o.ly = Math.max(o.y, last + gap); last = o.ly; });
      const over = last - (height - 16);
      if (over > 0) col.forEach((o) => { o.ly -= over; });
      for (let i = 1; i < col.length; i++) if (col[i].ly < col[i - 1].ly + gap) col[i].ly = col[i - 1].ly + gap;
      col.forEach((o) => {
        const { it } = o;
        const lx = side === 0 ? margin : width - margin - it.w;
        const ey = Math.max(phone ? 46 : 40, Math.min(height - 12, o.ly));
        it.el.style.display = '';
        it.el.style.transform = `translate(${lx.toFixed(1)}px,${(ey - 12).toFixed(1)}px)`;
        it.el.classList.toggle('on', active === it.def.id);
        const ax = side === 0 ? lx + it.w : lx;
        const elbow = side === 0 ? Math.min(o.x - 10, ax + 18) : Math.max(o.x + 10, ax - 18);
        it.line.style.display = ''; it.dot.style.display = '';
        it.line.setAttribute('points', `${ax.toFixed(1)},${ey.toFixed(1)} ${elbow.toFixed(1)},${ey.toFixed(1)} ${o.x.toFixed(1)},${o.y.toFixed(1)}`);
        it.dot.setAttribute('cx', o.x.toFixed(1)); it.dot.setAttribute('cy', o.y.toFixed(1));
      });
    }
  }

  return {
    add,
    update,
    set enabled(b) { enabled = b; if (!b) items.forEach(hideItem); },
    get enabled() { return enabled; },
    set active(id) { active = id; },
    dispose() { root.remove(); },
  };
}
