// The Hertzsprung-Russell diagram in the side panel: the main sequence band, the track the chosen
// star has walked so far, and where it is now. Redrawn only when the state changes.
const L10 = Math.log10;
const clamp = (x, a, b) => (x < a ? a : x > b ? b : x);

function starCss(T) {
  const t = clamp(T, 1000, 40000) / 100;
  const r = t <= 66 ? 1 : clamp(1.293 * Math.pow(t - 60, -0.1332), 0, 1);
  const g = t <= 66 ? clamp(0.39 * Math.log(t) - 0.632, 0, 1) : clamp(1.13 * Math.pow(t - 60, -0.0755), 0, 1);
  const b = t >= 66 ? 1 : t <= 19 ? 0 : clamp(0.543 * Math.log(t - 10) - 1.196, 0, 1);
  return `rgb(${Math.round(r * 255)},${Math.round(g * 255)},${Math.round(b * 255)})`;
}

export function createHR(parent) {
  const wrap = document.createElement('div');
  wrap.className = 'sl-hr';
  wrap.style.cssText = 'position:relative;width:100%;aspect-ratio:1.25;border-radius:14px;overflow:hidden;background:rgba(8,14,30,0.85);border:1px solid rgba(160,190,255,0.16);margin:4px 0 10px';
  const cv = document.createElement('canvas');
  cv.style.cssText = 'width:100%;height:100%;display:block';
  wrap.appendChild(cv);
  parent.appendChild(wrap);
  let key = '';
  function draw(S, s, O) {
    const w = wrap.clientWidth || 280; const h = wrap.clientHeight || 224;
    const k = `${w}|${h}|${S.length}|${S[2].T.toFixed(0)}|${s.toFixed(3)}`;
    if (k === key) return;
    key = k;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
    const g = cv.getContext('2d');
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, w, h);
    const px = 34; const py = 22; const pw = w - px - 12; const ph = h - py - 26;
    const X = (T) => px + (L10(40000) - L10(clamp(T, 2500, 40000))) / (L10(40000) - L10(2500)) * pw;
    const Y = (L) => py + (6 - clamp(L10(Math.max(L, 1e-5)), -4.5, 6)) / 10.5 * ph;
    const grad = g.createLinearGradient(px, 0, px + pw, 0);
    grad.addColorStop(0, 'rgba(150,180,255,0.10)'); grad.addColorStop(0.5, 'rgba(255,245,230,0.06)'); grad.addColorStop(1, 'rgba(255,140,90,0.10)');
    g.fillStyle = grad; g.fillRect(px, py, pw, ph);
    g.font = '600 9px Poppins, system-ui, sans-serif'; g.fillStyle = '#8ea0c2';
    for (const T of [30000, 10000, 6000, 3000]) { g.textAlign = 'center'; g.fillText(`${T / 1000}k K`, X(T), h - 10); }
    for (const e of [-4, -2, 0, 2, 4, 6]) { g.textAlign = 'right'; g.fillText(e === 0 ? '1 L☉' : `10${e < 0 ? '⁻' : ''}${'⁰¹²³⁴⁵⁶'[Math.abs(e)]}`, px - 4, Y(Math.pow(10, e)) + 3); }
    g.textAlign = 'center'; g.fillStyle = '#aab8d3'; g.fillText('hot ← surface temperature → cool', px + pw / 2, 13);
    g.strokeStyle = 'rgba(160,190,255,0.22)'; g.lineWidth = 12; g.lineCap = 'round'; g.beginPath();
    let first = true;
    for (let m = 0.1; m <= 40; m *= 1.2) { const L = m < 0.43 ? 0.23 * Math.pow(m, 2.3) : Math.pow(m, 3.5); const T = 5772 * Math.pow(m, 0.505); if (first) { g.moveTo(X(T), Y(L)); first = false; } else g.lineTo(X(T), Y(L)); }
    g.stroke();
    g.fillStyle = 'rgba(200,215,255,0.6)'; g.textAlign = 'left'; g.fillText('main sequence', X(9000) + 8, Y(30) + 20);
    const ok = (T, L) => L > 0 && L < 1e7 && T < 60000 && T > 2000;
    g.strokeStyle = 'rgba(251,191,36,0.9)'; g.lineWidth = 2; g.beginPath(); let started = false;
    for (const x of S) { if (x.a > s) break; if (!ok(x.T, x.L)) continue; if (!started) { g.moveTo(X(x.T), Y(x.L)); started = true; } else g.lineTo(X(x.T), Y(x.L)); }
    if (started && ok(O.T, O.L)) g.lineTo(X(O.T), Y(O.L));
    g.stroke();
    if (ok(O.T, O.L)) {
      const cx = X(O.T); const cy = Y(O.L);
      const rg = g.createRadialGradient(cx, cy, 0, cx, cy, 14); rg.addColorStop(0, starCss(O.T)); rg.addColorStop(1, 'rgba(0,0,0,0)');
      g.fillStyle = rg; g.beginPath(); g.arc(cx, cy, 14, 0, Math.PI * 2); g.fill();
      g.fillStyle = '#fff'; g.beginPath(); g.arc(cx, cy, 3.5, 0, Math.PI * 2); g.fill();
    } else {
      g.fillStyle = '#aab8d3'; g.font = '700 11px Poppins, system-ui, sans-serif'; g.textAlign = 'center';
      g.fillText(O.c.key === 'bh' ? 'no light escapes: off the diagram' : 'off the diagram', px + pw / 2, py + ph / 2);
    }
  }
  return { draw, el: wrap };
}
