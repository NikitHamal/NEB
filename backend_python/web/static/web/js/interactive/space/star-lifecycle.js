import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';

function msColor(mass) {
  if (mass < 0.8) return '#ff9d6f';
  if (mass < 1.4) return '#ffd27a';
  if (mass < 3) return '#fff4d6';
  if (mass < 10) return '#dce8ff';
  return '#aac4ff';
}

function buildStages(mass) {
  const msLife = 10 / Math.pow(mass, 2.5);
  const lifeTxt = msLife >= 1000 ? `${Math.round(msLife / 100) / 10} trillion yrs` : msLife >= 1 ? `${msLife.toFixed(1)} billion yrs` : `${Math.round(msLife * 1000)} million yrs`;
  const stages = [
    { key: 'nebula', name: 'Nebula', color: '#8d7bd4', r: 46, info: 'A cold cloud of hydrogen gas and dust, light-years wide. Gravity slowly pulls clumps of it together — the nursery where stars are born.' },
    { key: 'proto', name: 'Protostar', color: '#ff9d5c', r: 22, info: 'A collapsing clump heats up as gravity squeezes it. When the core hits about 10 million degrees, hydrogen fusion ignites — a star is born.' },
    { key: 'ms', name: 'Main Sequence', color: msColor(mass), r: 13 + Math.min(mass, 12) * 1.6, info: `The long, stable adulthood: hydrogen fuses into helium and the outward energy balances gravity. At ${mass.toFixed(1)} solar masses this lasts about ${lifeTxt}.` },
  ];
  if (mass < 8) {
    stages.push(
      { key: 'giant', name: 'Red Giant', color: '#ff6b4a', r: 52, info: 'Core hydrogen runs out, the core shrinks and heats, and the outer layers swell hugely. Our Sun will reach this stage in about 5 billion years.' },
      { key: 'pneb', name: 'Planetary Nebula', color: '#6fd8c9', r: 44, info: 'The bloated outer layers drift gently away as a glowing shell of gas, leaving the hot bare core behind. (Nothing to do with planets — early astronomers just thought they looked round like planets.)' },
      { key: 'wd', name: 'White Dwarf', color: '#e8f1ff', r: 7, info: 'The leftover core: Earth-sized but half the Sun\u2019s mass. A teaspoon would weigh about five tonnes. It makes no new energy and will cool for billions of years.' }
    );
  } else {
    stages.push(
      { key: 'giant', name: 'Red Supergiant', color: '#ff5436', r: 60, info: 'A monster hundreds of times wider than the Sun, fusing heavier and heavier elements in onion-like shells — until the core turns to iron, which fusion cannot burn.' },
      { key: 'sn', name: 'Supernova', color: '#ffffff', r: 64, info: 'The iron core collapses in under a second and the star detonates, briefly outshining its entire galaxy. Elements heavier than iron — gold, silver, uranium — are forged here.' },
      mass >= 20
        ? { key: 'bh', name: 'Black Hole', color: '#11131c', r: 12, info: 'The crushed core\u2019s gravity is so extreme that not even light escapes. Anything crossing the event horizon is gone forever. Mass above ~20-25 suns ends here.' }
        : { key: 'ns', name: 'Neutron Star', color: '#cfe4ff', r: 5, info: 'A city-sized sphere of almost pure neutrons, spinning up to hundreds of times per second. A teaspoon would weigh a billion tonnes.' }
    );
  }
  return stages;
}

export default function init(stage) {
  const sim = createCanvas2D(stage);

  let mass = 1;
  let stages = buildStages(mass);
  let progress = 0;
  let evolving = false;
  let nodes = [];
  let particles = [];
  let flash = 0;
  let viewMode = '2d';

  const hud = createHud(stage);
  const stageBadge = hud.badge('Stage: Nebula', '#8d7bd4');
  const fateBadge = hud.badge('Fate: White Dwarf', '#e8f1ff');

  function fateName() {
    return stages[stages.length - 1].name;
  }

  function refresh() {
    stages = buildStages(mass);
    progress = 0;
    evolving = false;
    particles = [];
    flash = 0;
    fateBadge.set(`Fate: ${fateName()}`);
    fateBadge.el.style.setProperty('--ix-hud-color', stages[stages.length - 1].key === 'bh' ? '#c4b5fd' : stages[stages.length - 1].color);
  }

  const panel = createPanel(stage, { title: 'Star Builder' });
  panel.select({
    label: 'View',
    options: [
      { value: '2d', label: '2D' },
      { value: '3d', label: '3D' },
    ],
    value: viewMode,
    onChange: (v) => { viewMode = v; },
  });
  panel.slider({
    label: 'Starting mass',
    min: 0.5, max: 30, step: 0.5, value: 1,
    format: (v) => `${v} \u2609 (suns)`,
    onChange: (v) => { mass = v; refresh(); },
  });
  panel.buttonRow([
    { label: 'Evolve!', icon: 'play_arrow', onClick: () => { if (progress >= stages.length - 1) progress = 0; evolving = true; } },
    { label: 'Reset', icon: 'replay', variant: 'ghost', onClick: refresh },
  ]);
  panel.info('Choose a mass and press Evolve. Tap any stage circle on the timeline to read about it. Mass decides everything: small stars die gently, giants explode.');

  function onTap(e) {
    const p = pointerPos(sim.canvas, e);
    for (let i = 0; i < nodes.length; i++) {
      const nd = nodes[i];
      if (Math.hypot(p.x - nd.x, p.y - nd.y) < Math.max(nd.r + 8, 18)) {
        showInfoCard(stage, { title: nd.stage.name, body: nd.stage.info, color: '#6D28D9' });
        return;
      }
    }
  }
  sim.canvas.style.touchAction = 'none';
  sim.canvas.addEventListener('pointerdown', onTap);

  function lerpColor(c1, c2, t) {
    const a = parseInt(c1.slice(1), 16);
    const b = parseInt(c2.slice(1), 16);
    const r = Math.round(((a >> 16) & 255) + (((b >> 16) & 255) - ((a >> 16) & 255)) * t);
    const g = Math.round(((a >> 8) & 255) + (((b >> 8) & 255) - ((a >> 8) & 255)) * t);
    const bl = Math.round((a & 255) + ((b & 255) - (a & 255)) * t);
    return `rgb(${r},${g},${bl})`;
  }

  sim.setUpdate((ctx, dt, w, h) => {
    if (evolving) {
      const prev = Math.floor(progress);
      progress = Math.min(progress + dt / 2.4, stages.length - 1);
      const cur = Math.floor(progress);
      if (cur !== prev && stages[cur] && stages[cur].key === 'sn') {
        flash = 1;
        for (let i = 0; i < 50; i++) {
          const a = Math.random() * Math.PI * 2;
          const s = 40 + Math.random() * 160;
          particles.push({ a, s, t: 0, life: 1.2 + Math.random() * 1.2 });
        }
      }
      if (progress >= stages.length - 1) evolving = false;
    }
    flash = Math.max(0, flash - dt * 0.8);
    for (let i = particles.length - 1; i >= 0; i--) {
      particles[i].t += dt;
      if (particles[i].t > particles[i].life) particles.splice(i, 1);
    }

    ctx.fillStyle = '#0a1322';
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#cdd9ec';
    for (let i = 0; i < 60; i++) {
      ctx.globalAlpha = ((i * 37) % 50) / 100 + 0.15;
      ctx.fillRect(((i * 89) % 100) / 100 * w, ((i * 53) % 100) / 100 * h, 1.3, 1.3);
    }
    ctx.globalAlpha = 1;

    const idx = Math.floor(progress);
    const frac = progress - idx;
    const s0 = stages[idx];
    const s1 = stages[Math.min(idx + 1, stages.length - 1)];
    const radius = (s0.r + (s1.r - s0.r) * frac) * Math.min(w, h) / 420;
    const color = frac < 0.5 ? s0.color : s1.color;
    const starX = w / 2;
    const starY = h * 0.36;
    const is3d = viewMode === '3d';

    const isBH = s0.key === 'bh' || (s1.key === 'bh' && frac > 0.5);
    const curKey = frac < 0.5 ? s0.key : s1.key;

    if (curKey === 'nebula') {
      for (let i = 0; i < 9; i++) {
        const depth = is3d ? ((i % 3) - 1) * radius * 0.12 : 0;
        const bx = starX + Math.cos(i * 2.4) * radius * 0.85 + depth;
        const by = starY + Math.sin(i * 1.7) * radius * (is3d ? 0.38 : 0.55) - depth * 0.25;
        const br = radius * (0.45 + ((i * 29) % 40) / 100);
        const g = ctx.createRadialGradient(bx, by, 2, bx, by, br);
        g.addColorStop(0, 'rgba(141,123,212,0.28)');
        g.addColorStop(1, 'rgba(141,123,212,0)');
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(bx, by, br, 0, Math.PI * 2);
        ctx.fill();
      }
    } else if (isBH) {
      const g = ctx.createRadialGradient(starX, starY, radius, starX, starY, radius * 3);
      g.addColorStop(0, 'rgba(196,181,253,0.5)');
      g.addColorStop(0.4, 'rgba(125,90,220,0.22)');
      g.addColorStop(1, 'rgba(125,90,220,0)');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(starX, starY, radius * 3, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = 'rgba(255,220,150,0.85)';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.ellipse(starX, starY, radius * 2.1, radius * 0.55, -0.3, 0, Math.PI * 2);
      ctx.stroke();
      ctx.fillStyle = '#05060c';
      ctx.beginPath();
      ctx.arc(starX, starY, radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = 'rgba(196,181,253,0.6)';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    } else {
      const g = ctx.createRadialGradient(starX, starY, radius * 0.2, starX, starY, radius * 2.4);
      g.addColorStop(0, color);
      g.addColorStop(0.45, lerpColor(s0.color, '#0a1322', 0.4));
      g.addColorStop(1, 'rgba(10,19,34,0)');
      ctx.globalAlpha = 0.55;
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(starX, starY, radius * 2.4, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
      if (is3d) {
        const sg = ctx.createRadialGradient(starX - radius * 0.35, starY - radius * 0.38, radius * 0.12, starX, starY, radius);
        sg.addColorStop(0, '#ffffff');
        sg.addColorStop(0.18, color);
        sg.addColorStop(1, lerpColor(s0.color, '#050814', 0.55));
        ctx.fillStyle = 'rgba(0,0,0,0.26)';
        ctx.beginPath();
        ctx.ellipse(starX + radius * 0.2, starY + radius * 0.78, radius * 0.9, radius * 0.18, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = sg;
        ctx.beginPath();
        ctx.arc(starX, starY, radius, 0, Math.PI * 2);
        ctx.fill();
      } else {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(starX, starY, radius, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      const d = p.s * p.t;
      ctx.globalAlpha = Math.max(0, 1 - p.t / p.life);
      ctx.fillStyle = i % 3 === 0 ? '#ffd27a' : '#ffffff';
      ctx.beginPath();
      ctx.arc(starX + Math.cos(p.a) * d, starY + Math.sin(p.a) * d, 2.4, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;

    if (flash > 0) {
      ctx.globalAlpha = flash * 0.85;
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, w, h);
      ctx.globalAlpha = 1;
    }

    const tlY = h * 0.78;
    const pad = Math.max(40, w * 0.08);
    nodes = [];
    ctx.strokeStyle = 'rgba(255,255,255,0.2)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(pad, tlY + (is3d ? 8 : 0));
    ctx.lineTo(w - pad, tlY - (is3d ? 8 : 0));
    ctx.stroke();
    ctx.strokeStyle = '#8be9a8';
    ctx.beginPath();
    const progX = pad + (w - pad * 2) * (progress / (stages.length - 1));
    const progY = tlY + (is3d ? 8 - 16 * ((progX - pad) / (w - pad * 2)) : 0);
    ctx.moveTo(pad, tlY + (is3d ? 8 : 0));
    ctx.lineTo(progX, progY);
    ctx.stroke();

    ctx.font = '600 10px Poppins, sans-serif';
    ctx.textAlign = 'center';
    for (let i = 0; i < stages.length; i++) {
      const st = stages[i];
      const x = pad + ((w - pad * 2) * i) / (stages.length - 1);
      const y = tlY + (is3d ? 8 - 16 * (i / (stages.length - 1)) : 0);
      const reached = progress >= i - 0.001;
      const nr = i === idx && evolving ? 11 : 8;
      nodes.push({ x, y, r: nr, stage: st });
      ctx.fillStyle = st.key === 'bh' ? '#2a2440' : st.color;
      ctx.globalAlpha = reached ? 1 : 0.32;
      ctx.beginPath();
      if (is3d) ctx.ellipse(x, y, nr * 1.15, nr * 0.75, 0, 0, Math.PI * 2);
      else ctx.arc(x, y, nr, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = reached ? 0.95 : 0.45;
      ctx.fillStyle = '#e8eefb';
      const words = st.name.split(' ');
      for (let j = 0; j < words.length; j++) {
        ctx.fillText(words[j], x, y + 24 + j * 12);
      }
      ctx.globalAlpha = 1;
    }
    ctx.textAlign = 'left';

    const cur = stages[Math.round(Math.min(progress, stages.length - 1))];
    stageBadge.set(`Stage: ${cur.name}`);
    stageBadge.el.style.setProperty('--ix-hud-color', cur.key === 'bh' ? '#c4b5fd' : cur.color);
  });

  refresh();
  sim.start();

  return {
    dispose() {
      sim.canvas.removeEventListener('pointerdown', onTap);
      panel.dispose();
      hud.dispose();
      sim.dispose();
    },
  };
}
