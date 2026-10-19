// A digital stopwatch for timing by hand: start and stop on the student's own reflexes (the big
// button, or the space bar), shown large on the stage. Also a small least-squares graph panel.
function el(tag, cls, html) { const n = document.createElement(tag); if (cls) n.className = cls; if (html !== undefined) n.innerHTML = html; return n; }

export function createStopwatch(hud, { onStart, onStop } = {}) {
  const box = el('div', 'ho-watch', '<div class="ho-watch-face"><span class="ho-watch-t">0.00</span><small>s</small></div><div class="ho-watch-sub"></div><div class="ho-watch-btns"><button type="button" class="ho-watch-go">Start</button><button type="button" class="ho-watch-reset">Reset</button></div>');
  hud.root.appendChild(box);
  const face = box.querySelector('.ho-watch-t'); const sub = box.querySelector('.ho-watch-sub');
  const go = box.querySelector('.ho-watch-go'); const reset = box.querySelector('.ho-watch-reset');
  let running = false; let t = 0; let enabled = false; let shown = '';
  function press() {
    if (!enabled) return;
    if (!running) { running = true; t = 0; go.textContent = 'Stop'; go.classList.add('stop'); onStart && onStart(); }
    else { running = false; go.textContent = 'Start'; go.classList.remove('stop'); onStop && onStop(t); }
  }
  go.addEventListener('click', (e) => { e.stopPropagation(); press(); });
  reset.addEventListener('click', (e) => { e.stopPropagation(); if (running) return; t = 0; face.textContent = '0.00'; });
  const key = (e) => { if (enabled && e.code === 'Space' && !e.repeat && !/INPUT|TEXTAREA|BUTTON/.test(document.activeElement && document.activeElement.tagName)) { e.preventDefault(); press(); } };
  window.addEventListener('keydown', key);
  return {
    get running() { return running; }, get time() { return t; },
    show(on) { enabled = on; box.classList.toggle('show', on); if (!on && running) { running = false; go.textContent = 'Start'; go.classList.remove('stop'); } },
    sub(html) { if (html !== shown) { sub.innerHTML = html; shown = html; } },
    update(dt) { if (!running) return; t += dt; face.textContent = t.toFixed(2); },
    reset() { running = false; t = 0; face.textContent = '0.00'; go.textContent = 'Start'; go.classList.remove('stop'); },
    press,
    dispose() { window.removeEventListener('keydown', key); box.remove(); },
  };
}

/** Least squares y = a + b x. */
export function fitLine(pts) {
  const n = pts.length; let sx = 0, sy = 0, sxx = 0, sxy = 0;
  pts.forEach(([x, y]) => { sx += x; sy += y; sxx += x * x; sxy += x * y; });
  const b = (n * sxy - sx * sy) / Math.max(1e-12, n * sxx - sx * sx); const a = (sy - b * sx) / n;
  return { a, b };
}

/** A graph panel on the stage: points, a fitted line through the origin region, axis labels. */
export function createGraph(hud, { title, xLabel, yLabel }) {
  const box = el('div', 'ho-graph', `<b>${title}</b><canvas width="520" height="360"></canvas>`);
  hud.root.appendChild(box);
  const cv = box.querySelector('canvas'); const g = cv.getContext('2d');
  return {
    el: box,
    show(on) { box.classList.toggle('on', on); },
    draw(pts, fit, { xMax, yMax, yMin = 0 } = {}) {
      const W = cv.width; const H = cv.height; const L = 62; const B = 48; const R = 18; const T = 16;
      const xm = xMax || Math.max(...pts.map((p) => p[0])) * 1.15; const ym = yMax || Math.max(...pts.map((p) => p[1])) * 1.15;
      const X = (x) => L + (W - L - R) * x / xm; const Y = (y) => H - B - (H - B - T) * (y - yMin) / (ym - yMin);
      g.fillStyle = '#fffef8'; g.fillRect(0, 0, W, H);
      g.strokeStyle = 'rgba(14,116,144,.12)'; g.lineWidth = 1;
      for (let i = 0; i <= 10; i++) { g.beginPath(); g.moveTo(X(xm * i / 10), T); g.lineTo(X(xm * i / 10), H - B); g.stroke(); g.beginPath(); g.moveTo(L, Y(yMin + (ym - yMin) * i / 10)); g.lineTo(W - R, Y(yMin + (ym - yMin) * i / 10)); g.stroke(); }
      g.strokeStyle = '#0f172a'; g.lineWidth = 1.6; g.beginPath(); g.moveTo(L, T); g.lineTo(L, H - B); g.lineTo(W - R, H - B); g.stroke();
      g.fillStyle = '#334155'; g.font = '600 13px system-ui, sans-serif'; g.textAlign = 'center';
      for (let i = 0; i <= 5; i++) { g.fillText((xm * i / 5).toFixed(xm < 10 ? 1 : 0), X(xm * i / 5), H - B + 18); }
      g.textAlign = 'right'; for (let i = 0; i <= 5; i++) { const v = yMin + (ym - yMin) * i / 5; g.fillText(v.toFixed(ym - yMin < 10 ? (ym < 10 ? 2 : 1) : 0), L - 8, Y(v) + 4); }
      g.textAlign = 'center'; g.font = '700 14px system-ui, sans-serif'; g.fillText(xLabel, (L + W - R) / 2, H - 8);
      g.save(); g.translate(16, (T + H - B) / 2); g.rotate(-Math.PI / 2); g.fillText(yLabel, 0, 0); g.restore();
      if (fit) { g.strokeStyle = '#2563eb'; g.lineWidth = 2; g.beginPath(); g.moveTo(X(0), Y(fit.a)); g.lineTo(X(xm), Y(fit.a + fit.b * xm)); g.stroke(); }
      pts.forEach(([x, y, c]) => { g.strokeStyle = c || '#dc2626'; g.lineWidth = 2; g.beginPath(); g.moveTo(X(x) - 6, Y(y)); g.lineTo(X(x) + 6, Y(y)); g.moveTo(X(x), Y(y) - 6); g.lineTo(X(x), Y(y) + 6); g.stroke(); });
    },
    dispose() { box.remove(); },
  };
}
