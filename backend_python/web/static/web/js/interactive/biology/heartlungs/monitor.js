const g = (x, m, s) => Math.exp(-((x - m) * (x - m)) / (2 * s * s));

export function ecg(ph) {
  return 0.12 * g(ph, 0.09, 0.022) - 0.09 * g(ph, 0.165, 0.007) + 1.0 * g(ph, 0.18, 0.008) - 0.24 * g(ph, 0.197, 0.008) + 0.28 * g(ph, 0.43, 0.045);
}

export function cardiac(ph) {
  const atria = g(ph, 0.13, 0.04);
  let vent = 0;
  if (ph > 0.19 && ph < 0.6) {
    const up = Math.min(1, (ph - 0.19) / 0.1);
    const down = ph > 0.44 ? Math.max(0, 1 - (ph - 0.44) / 0.14) : 1;
    vent = Math.min(up, down);
    vent = vent * vent * (3 - 2 * vent);
  }
  const ejecting = ph > 0.21 && ph < 0.5 ? Math.sin((ph - 0.21) / 0.29 * Math.PI) : 0;
  return { atria, vent, ejecting };
}

export function createMonitor(parent) {
  const wrap = document.createElement('div');
  wrap.style.cssText = 'position:relative;margin:4px 0 10px;border-radius:12px;overflow:hidden;background:#04110c;border:1px solid rgba(80,255,170,.18);box-shadow:inset 0 0 24px rgba(0,0,0,.6)';
  const c = document.createElement('canvas');
  c.style.cssText = 'display:block;width:100%;height:92px';
  wrap.appendChild(c);
  const tag = document.createElement('div');
  tag.style.cssText = 'position:absolute;left:10px;top:6px;font:600 10.5px Poppins,system-ui;color:#5dffb0;letter-spacing:.06em;opacity:.85';
  tag.textContent = 'ECG · LEAD II';
  const bpm = document.createElement('div');
  bpm.style.cssText = 'position:absolute;right:10px;top:4px;font:700 18px Poppins,system-ui;color:#5dffb0;text-shadow:0 0 8px rgba(93,255,176,.6)';
  wrap.appendChild(tag); wrap.appendChild(bpm);
  parent.appendChild(wrap);
  const ctx = c.getContext('2d');
  let W = 0; let H = 0; let dpr = 1;
  let x = 0;
  let lastY = null;
  function size() {
    dpr = Math.min(2, window.devicePixelRatio || 1);
    const w = c.clientWidth || 260; const h = 92;
    if (w * dpr !== W) {
      W = Math.round(w * dpr); H = Math.round(h * dpr); c.width = W; c.height = H;
      ctx.fillStyle = '#04110c'; ctx.fillRect(0, 0, W, H);
      grid();
      x = 0; lastY = null;
    }
  }
  function grid() {
    ctx.strokeStyle = 'rgba(80,255,170,0.07)'; ctx.lineWidth = 1;
    for (let gx = 0; gx < W; gx += 12 * dpr) { ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, H); ctx.stroke(); }
    for (let gy = 0; gy < H; gy += 12 * dpr) { ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(W, gy); ctx.stroke(); }
  }
  return {
    push(dt, phase, hr) {
      size();
      bpm.textContent = `♥ ${Math.round(hr)}`;
      const speed = 70 * dpr;
      const dx = speed * dt;
      const y = H * 0.68 - ecg(phase) * H * 0.5;
      ctx.fillStyle = '#04110c';
      ctx.fillRect(x, 0, Math.ceil(dx) + 10 * dpr, H);
      ctx.save(); ctx.beginPath(); ctx.rect(x, 0, Math.ceil(dx) + 10 * dpr, H); ctx.clip(); grid(); ctx.restore();
      ctx.strokeStyle = '#5dffb0'; ctx.lineWidth = 1.8 * dpr; ctx.shadowColor = 'rgba(93,255,176,0.7)'; ctx.shadowBlur = 6 * dpr;
      ctx.beginPath(); ctx.moveTo(x, lastY ?? y); ctx.lineTo(x + dx, y); ctx.stroke();
      ctx.shadowBlur = 0;
      lastY = y;
      x += dx;
      if (x > W) { x = 0; lastY = null; }
    },
    el: wrap,
  };
}

export function createHeartSound() {
  let ac = null;
  let on = false;
  function thump(freq, dur, gain) {
    if (!ac) return;
    const o = ac.createOscillator(); const gn = ac.createGain(); const f = ac.createBiquadFilter();
    o.type = 'sine'; o.frequency.setValueAtTime(freq, ac.currentTime); o.frequency.exponentialRampToValueAtTime(freq * 0.55, ac.currentTime + dur);
    f.type = 'lowpass'; f.frequency.value = 180;
    gn.gain.setValueAtTime(0.0001, ac.currentTime); gn.gain.exponentialRampToValueAtTime(gain, ac.currentTime + 0.012); gn.gain.exponentialRampToValueAtTime(0.0001, ac.currentTime + dur);
    o.connect(f); f.connect(gn); gn.connect(ac.destination);
    o.start(); o.stop(ac.currentTime + dur + 0.02);
  }
  return {
    set on(v) { on = v; if (v && !ac) { try { ac = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { ac = null; } } if (ac && v && ac.state === 'suspended') ac.resume(); },
    get on() { return on; },
    lub() { if (on) thump(62, 0.16, 0.5); },
    dub() { if (on) thump(88, 0.11, 0.35); },
    dispose() { if (ac) ac.close(); },
  };
}
