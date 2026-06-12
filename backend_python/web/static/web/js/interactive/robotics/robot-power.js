import { createCanvas2D } from '../core/canvas2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

export default function init(stage) {
  const sim = createCanvas2D(stage);
  const panel = createPanel(stage, { title: 'Circuit Lab' });
  const hud = createHud(stage);
  const stateBadge = hud.badge('Circuit OPEN', '#94a3b8');

  let voltage = 4.5;
  let closed = false;
  let fanAngle = 0;
  let flow = 0;
  const dots = [];
  for (let i = 0; i < 26; i++) dots.push(i / 26);

  const speedReadout = panel.readout({ label: 'Motor speed', value: '0 RPM' });
  panel.slider({
    label: 'Battery voltage', min: 1.5, max: 9, step: 0.5, value: voltage,
    format: (v) => v.toFixed(1) + ' V',
    onChange: (v) => { voltage = v; },
  });
  panel.toggle({
    label: 'Switch closed', value: false,
    onChange: (v) => {
      closed = v;
      stateBadge.set(closed ? 'Circuit CLOSED — current flows!' : 'Circuit OPEN');
      stateBadge.el.style.setProperty('--ix-hud-color', closed ? '#35d07f' : '#94a3b8');
    },
  });
  panel.info('Electricity needs a complete loop. Close the switch to let current flow from the battery, through the motor, and back again.');

  function layout(w, h) {
    const m = Math.min(w, h) * 0.12;
    return {
      left: m, right: w - m,
      top: m + 10, bottom: h - m,
      batX: m, motX: w - m,
      midY: (m + 10 + h - m) / 2,
    };
  }

  function drawWirePath(ctx, L) {
    ctx.beginPath();
    ctx.moveTo(L.left, L.midY - 40);
    ctx.lineTo(L.left, L.top);
    ctx.lineTo(L.right, L.top);
    ctx.lineTo(L.right, L.midY - 56);
    ctx.moveTo(L.right, L.midY + 56);
    ctx.lineTo(L.right, L.bottom);
    ctx.lineTo(L.left, L.bottom);
    ctx.lineTo(L.left, L.midY + 40);
    ctx.stroke();
  }

  function pointOnLoop(t, L) {
    const segs = [];
    function add(x1, y1, x2, y2) { segs.push({ x1, y1, x2, y2, len: Math.hypot(x2 - x1, y2 - y1) }); }
    add(L.left, L.midY - 40, L.left, L.top);
    add(L.left, L.top, L.right, L.top);
    add(L.right, L.top, L.right, L.midY - 56);
    add(L.right, L.midY + 56, L.right, L.bottom);
    add(L.right, L.bottom, L.left, L.bottom);
    add(L.left, L.bottom, L.left, L.midY + 40);
    const total = segs.reduce((a, s) => a + s.len, 0);
    let d = t * total;
    for (const s of segs) {
      if (d <= s.len) {
        const p = d / s.len;
        return { x: s.x1 + (s.x2 - s.x1) * p, y: s.y1 + (s.y2 - s.y1) * p };
      }
      d -= s.len;
    }
    return { x: segs[0].x1, y: segs[0].y1 };
  }

  sim.setUpdate((ctx, dt, w, h) => {
    const targetFlow = closed ? voltage / 9 : 0;
    flow += (targetFlow - flow) * Math.min(dt * 5, 1);
    const rpm = Math.round(flow * 9 * 60);
    speedReadout.set(rpm + ' RPM');
    fanAngle += flow * dt * 14;

    ctx.clearRect(0, 0, w, h);
    const L = layout(w, h);

    ctx.lineWidth = 4;
    ctx.strokeStyle = closed ? '#5e8fdb' : '#3d5273';
    ctx.lineCap = 'round';
    drawWirePath(ctx, L);

    const swX = (L.left + L.right) / 2;
    ctx.beginPath();
    ctx.arc(swX - 26, L.top, 5, 0, Math.PI * 2);
    ctx.arc(swX + 26, L.top, 5, 0, Math.PI * 2);
    ctx.fillStyle = '#9ec1ff';
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(swX - 26, L.top);
    if (closed) ctx.lineTo(swX + 26, L.top);
    else ctx.lineTo(swX + 14, L.top - 30);
    ctx.strokeStyle = '#9ec1ff';
    ctx.lineWidth = 5;
    ctx.stroke();
    ctx.fillStyle = '#c7d4ea';
    ctx.font = '600 13px Poppins, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('switch', swX, L.top - 38);

    const bw = 56, bh = 88;
    ctx.fillStyle = '#1e3354';
    ctx.strokeStyle = '#5e8fdb';
    ctx.lineWidth = 3;
    roundRect(ctx, L.batX - bw / 2, L.midY - bh / 2, bw, bh, 10);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#f5b942';
    ctx.fillRect(L.batX - 12, L.midY - bh / 2 - 10, 24, 10);
    ctx.fillStyle = '#e8eefb';
    ctx.font = '700 15px Poppins, sans-serif';
    ctx.fillText(voltage.toFixed(1) + 'V', L.batX, L.midY + 5);
    ctx.font = '600 12px Poppins, sans-serif';
    ctx.fillStyle = '#c7d4ea';
    ctx.fillText('battery', L.batX, L.midY + bh / 2 + 22);
    ctx.fillText('+', L.batX - 38, L.midY - 28);
    ctx.fillText('−', L.batX - 38, L.midY + 34);

    const mr = 46;
    ctx.beginPath();
    ctx.arc(L.motX, L.midY, mr, 0, Math.PI * 2);
    ctx.fillStyle = '#1e3354';
    ctx.fill();
    ctx.strokeStyle = closed && flow > 0.02 ? '#35d07f' : '#5e8fdb';
    ctx.stroke();
    ctx.save();
    ctx.translate(L.motX, L.midY);
    ctx.rotate(fanAngle);
    ctx.fillStyle = '#7fe9ff';
    for (let i = 0; i < 3; i++) {
      ctx.rotate((Math.PI * 2) / 3);
      ctx.beginPath();
      ctx.ellipse(0, -22, 9, 20, 0, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.beginPath();
    ctx.arc(0, 0, 7, 0, Math.PI * 2);
    ctx.fillStyle = '#f5b942';
    ctx.fill();
    ctx.restore();
    ctx.fillStyle = '#c7d4ea';
    ctx.font = '600 12px Poppins, sans-serif';
    ctx.fillText('motor + fan', L.motX, L.midY + mr + 22);

    if (flow > 0.01) {
      ctx.fillStyle = '#ffd76a';
      for (let i = 0; i < dots.length; i++) {
        dots[i] = (dots[i] + flow * dt * 0.55) % 1;
        const p = pointOnLoop(dots[i], L);
        ctx.beginPath();
        ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    ctx.fillStyle = 'rgba(199,212,234,0.75)';
    ctx.font = '500 12px Poppins, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(closed ? 'Current is flowing around the loop →' : 'The loop is broken — no current can flow.', 16, h - 14);
  });

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x, y, w, h, r);
    else ctx.rect(x, y, w, h);
  }

  sim.start();

  return {
    dispose() {
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
