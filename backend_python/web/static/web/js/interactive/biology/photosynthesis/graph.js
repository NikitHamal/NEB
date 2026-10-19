// Live rate trace for the panel: bubbles per minute over the last two simulated minutes.
export function createRateGraph(panelBody, opts = {}) {
  const wrap = document.createElement('div');
  wrap.className = 'ix-ctrl-row';
  wrap.style.cssText = 'display:block;padding:6px 0 2px';
  const title = document.createElement('div');
  title.className = 'ix-ctrl-label';
  title.textContent = opts.title || 'Rate (bubbles per minute)';
  title.style.marginBottom = '4px';
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'width:100%;height:118px;display:block;border-radius:10px;background:rgba(6,14,26,0.65);border:1px solid rgba(148,163,184,0.18)';
  wrap.appendChild(title); wrap.appendChild(canvas);
  panelBody.appendChild(wrap);
  const g = canvas.getContext('2d');
  const span = opts.span || 120;
  const max = opts.max || 60;
  const pts = [];
  const marks = [];
  let t = 0; let acc = 0;
  let dpr = 1; let W = 0; let H = 0;

  function fit() {
    dpr = Math.min(2, window.devicePixelRatio || 1);
    const w = Math.max(10, canvas.clientWidth); const h = Math.max(10, canvas.clientHeight);
    if (w * dpr !== W || h * dpr !== H) { W = w * dpr; H = h * dpr; canvas.width = W; canvas.height = H; }
  }

  function draw() {
    fit();
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    const w = W / dpr; const h = H / dpr;
    const L = 30; const R = 8; const T = 8; const B = 18;
    g.clearRect(0, 0, w, h);
    g.font = '10px Poppins, system-ui, sans-serif';
    g.fillStyle = 'rgba(203,213,225,0.7)'; g.strokeStyle = 'rgba(148,163,184,0.16)'; g.lineWidth = 1;
    for (let k = 0; k <= 3; k++) {
      const y = T + (h - T - B) * (1 - k / 3);
      g.beginPath(); g.moveTo(L, y); g.lineTo(w - R, y); g.stroke();
      g.fillText(String(Math.round((max * k) / 3)), 4, y + 3);
    }
    g.fillText(`last ${Math.round(span / 60)} min`, L, h - 4);
    const x = (tt) => L + ((tt - (t - span)) / span) * (w - L - R);
    const y = (v) => T + (h - T - B) * (1 - Math.min(1, v / max));
    marks.forEach((m) => {
      if (m.t < t - span) return;
      g.strokeStyle = m.color; g.globalAlpha = 0.55; g.setLineDash([3, 3]);
      g.beginPath(); g.moveTo(x(m.t), T); g.lineTo(x(m.t), h - B); g.stroke();
      g.setLineDash([]); g.globalAlpha = 1;
    });
    if (pts.length > 1) {
      const grad = g.createLinearGradient(0, T, 0, h - B);
      grad.addColorStop(0, 'rgba(132,204,22,0.35)'); grad.addColorStop(1, 'rgba(132,204,22,0)');
      g.beginPath(); g.moveTo(x(pts[0].t), h - B);
      pts.forEach((p) => g.lineTo(x(p.t), y(p.v)));
      g.lineTo(x(pts[pts.length - 1].t), h - B); g.closePath(); g.fillStyle = grad; g.fill();
      g.beginPath();
      pts.forEach((p, i) => { if (i) g.lineTo(x(p.t), y(p.v)); else g.moveTo(x(p.t), y(p.v)); });
      g.strokeStyle = '#a3e635'; g.lineWidth = 2; g.stroke();
      const last = pts[pts.length - 1];
      g.fillStyle = '#ecfccb'; g.beginPath(); g.arc(x(last.t), y(last.v), 3, 0, Math.PI * 2); g.fill();
    }
  }

  return {
    push(dt, value) {
      t += dt; acc += dt;
      if (acc >= 0.5) { acc = 0; pts.push({ t, v: value }); while (pts.length && pts[0].t < t - span - 1) pts.shift(); draw(); }
    },
    mark(color) { marks.push({ t, color }); while (marks.length > 12) marks.shift(); },
    redraw: draw,
    dispose() { wrap.remove(); },
  };
}
