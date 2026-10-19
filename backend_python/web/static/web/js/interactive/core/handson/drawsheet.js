// A sheet of drawing paper on the stage, for constructions done by hand after a measurement:
// lines from a point at given angles, points the student drags along them or anywhere, a scale
// in centimetres, and a ruler/protractor readout. Coordinates are in centimetres, y up, origin O.
function el(tag, cls, html) { const n = document.createElement(tag); if (cls) n.className = cls; if (html !== undefined) n.innerHTML = html; return n; }

export function createDrawSheet(hud, { title = 'Drawing sheet', widthCm = 16, heightCm = 13, origin = [8, 4] } = {}) {
  const box = el('div', 'ho-sheet', `<b>${title}</b><canvas width="640" height="520"></canvas><div class="ho-sheet-read"></div>`);
  hud.root.appendChild(box);
  const cv = box.querySelector('canvas'); const g = cv.getContext('2d'); const out = box.querySelector('.ho-sheet-read');
  const PX = cv.width / widthCm;
  const toPx = (x, y) => [(origin[0] + x) * PX, cv.height - (origin[1] + y) * PX];
  const toCm = (px, py) => [px / PX - origin[0], (cv.height - py) / PX - origin[1]];
  const lines = []; const handles = []; const segs = [];
  let drag = null; let onChange = null;
  function draw() {
    g.fillStyle = '#fffef8'; g.fillRect(0, 0, cv.width, cv.height);
    g.strokeStyle = 'rgba(14,116,144,.10)'; g.lineWidth = 1;
    for (let x = 0; x <= widthCm; x += 0.5) { g.beginPath(); g.moveTo(x * PX, 0); g.lineTo(x * PX, cv.height); g.stroke(); }
    for (let y = 0; y <= heightCm; y += 0.5) { g.beginPath(); g.moveTo(0, cv.height - y * PX); g.lineTo(cv.width, cv.height - y * PX); g.stroke(); }
    for (const l of lines) {
      const [x0, y0] = toPx(0, 0); const [x1, y1] = toPx(Math.cos(l.a) * 30, Math.sin(l.a) * 30);
      g.strokeStyle = l.color || '#334155'; g.lineWidth = 1.6; g.setLineDash(l.dash ? [6, 5] : []); g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke(); g.setLineDash([]);
      if (l.label) { const [lx, ly] = toPx(Math.cos(l.a) * (l.labelAt || 5.5), Math.sin(l.a) * (l.labelAt || 5.5)); g.fillStyle = l.color || '#334155'; g.font = '700 18px system-ui, sans-serif'; g.fillText(l.label, lx + 8, ly - 6); }
    }
    for (const s of segs) {
      const [x0, y0] = toPx(s.a[0], s.a[1]); const [x1, y1] = toPx(s.b[0], s.b[1]);
      g.strokeStyle = s.color || '#2563eb'; g.lineWidth = s.width || 2.4; g.setLineDash(s.dash ? [7, 6] : []); g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke(); g.setLineDash([]);
    }
    const [ox, oy] = toPx(0, 0); g.fillStyle = '#111827'; g.beginPath(); g.arc(ox, oy, 4, 0, Math.PI * 2); g.fill(); g.font = '700 16px system-ui, sans-serif'; g.fillText('O', ox - 18, oy + 16);
    for (const h of handles) {
      if (!h.visible) continue;
      const [x, y] = toPx(h.x, h.y);
      g.fillStyle = h.color || '#dc2626'; g.globalAlpha = 0.18; g.beginPath(); g.arc(x, y, 16, 0, Math.PI * 2); g.fill(); g.globalAlpha = 1;
      g.beginPath(); g.arc(x, y, 6, 0, Math.PI * 2); g.fill();
      if (h.label) { g.font = '800 17px system-ui, sans-serif'; g.fillText(h.label, x + 10, y - 10); }
    }
  }
  function pointer(e) { const r = cv.getBoundingClientRect(); return toCm((e.clientX - r.left) * cv.width / r.width, (e.clientY - r.top) * cv.height / r.height); }
  cv.addEventListener('pointerdown', (e) => {
    e.stopPropagation(); const [x, y] = pointer(e); let best = null; let bd = 1.2;
    for (const h of handles) { if (!h.visible || h.locked) continue; const d = Math.hypot(h.x - x, h.y - y); if (d < bd) { bd = d; best = h; } }
    if (!best) return; drag = best; cv.setPointerCapture(e.pointerId); move(e);
  });
  function move(e) {
    if (!drag) return; e.stopPropagation(); let [x, y] = pointer(e);
    if (drag.along !== undefined) { const t = Math.max(0, x * Math.cos(drag.along) + y * Math.sin(drag.along)); x = t * Math.cos(drag.along); y = t * Math.sin(drag.along); }
    drag.x = Math.round(x * 20) / 20; drag.y = Math.round(y * 20) / 20; if (drag.along !== undefined) { const t = Math.round(Math.hypot(x, y) * 20) / 20; drag.x = t * Math.cos(drag.along); drag.y = t * Math.sin(drag.along); }
    draw(); onChange && onChange(drag);
  }
  cv.addEventListener('pointermove', move);
  cv.addEventListener('pointerup', (e) => { if (drag) { e.stopPropagation(); const d = drag; drag = null; onChange && onChange(d, true); } });
  ['pointerdown', 'pointermove', 'pointerup', 'wheel', 'touchstart'].forEach((t) => box.addEventListener(t, (e) => e.stopPropagation()));
  return {
    show(on) { box.classList.toggle('on', on); if (on) draw(); },
    line(a, opts = {}) { lines.push(Object.assign({ a }, opts)); draw(); },
    seg(a, b, opts = {}) { const s = Object.assign({ a, b }, opts); segs.push(s); draw(); return s; },
    handle(opts) { const h = Object.assign({ x: 0, y: 0, visible: true }, opts); handles.push(h); draw(); return h; },
    clear() { lines.length = 0; handles.length = 0; segs.length = 0; draw(); },
    redraw: draw,
    onChange(fn) { onChange = fn; },
    read(html) { out.innerHTML = html; },
    dispose() { box.remove(); },
  };
}
