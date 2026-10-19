// Resonance column: strike a tuning fork, hold it over a glass tube and move the water level by
// raising or lowering the reservoir until the air column booms. The loudness follows a resonance
// curve centred where the column plus its end correction is an odd number of quarter waves,
// L + e = (2n - 1) lambda / 4, with e = 0.3 d. The student finds the first and second resonances
// by ear (a real synthesised tone, with a meter for when the sound is off), then v = 2 f (l2 - l1)
// and e = (l2 - 3 l1) / 2, with v at the room's temperature: 331.5 + 0.6 T m/s.
import { THREE } from '../../engine.js';
import { MAT, mesh, clamp, canvasTexture } from '../../bio-handson/kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, screenDist } from '../hud.js';

const BY = 0.8;
const TOP = 7.4; const LEN = 7.0; const R = 0.2; const D_CM = 4.0;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

function scaleTex() {
  return canvasTexture('ho-res-scale', 128, 4096, (g, w, h) => {
    g.fillStyle = '#f2e3b8'; g.fillRect(0, 0, w, h); g.fillStyle = '#1f2937';
    for (let mm = 0; mm <= 700; mm += 2) { const y = 20 + (h - 40) * mm / 700; const cm = mm % 10 === 0; const five = mm % 50 === 0; g.fillRect(0, Math.round(y), five ? 60 : cm ? 42 : 22, cm ? 3 : 1.6); if (cm && (mm / 10) % 5 === 0) { g.font = '700 30px system-ui, sans-serif'; g.textBaseline = 'middle'; g.fillText(String(mm / 10), 66, y); } }
  });
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const forks = [384, 426.6, 480, 512];
  const f = forks[Math.floor(Math.random() * forks.length)];
  const T = 18 + Math.round(Math.random() * 12);
  const v = 331.5 + 0.6 * T; const lambda = v / f * 100; const e = 0.3 * D_CM;
  const L1 = lambda / 4 - e; const L2 = 3 * lambda / 4 - e;

  const stand = new THREE.Group(); world.add(stand);
  stand.add(mesh(new THREE.BoxGeometry(1.2, 0.08, 1.0), MAT.matte(0x2b3138), [0, 0.04, 0]));
  stand.add(mesh(new THREE.CylinderGeometry(0.05, 0.05, 8.2, 14), MAT.steel(), [-0.6, 4.1, -0.25]));
  [2.2, 6.6].forEach((y) => { stand.add(mesh(new THREE.BoxGeometry(0.7, 0.08, 0.12), MAT.steel(), [-0.3, y, -0.12])); });
  const glass = mesh(new THREE.CylinderGeometry(R, R, LEN, 32, 1, true), MAT.glass(), [0, TOP - LEN / 2, 0], { cast: false }); glass.renderOrder = 5; world.add(glass);
  const rim = mesh(new THREE.TorusGeometry(R, 0.012, 6, 32), MAT.glassEdge(), [0, TOP, 0]); rim.rotation.x = Math.PI / 2; world.add(rim);
  const rule = mesh(new THREE.BoxGeometry(0.16, LEN, 0.02), new THREE.MeshStandardMaterial({ map: scaleTex(), roughness: 0.6 }), [R + 0.13, TOP - LEN / 2 - 0.02, 0.06]); world.add(rule);
  const waterMat = MAT.liquid(0x9cc9e8, 0.55);
  const water = mesh(new THREE.CylinderGeometry(R - 0.01, R - 0.01, 1, 32), waterMat, null, { cast: false }); water.renderOrder = 3; world.add(water);
  const surf = mesh(new THREE.CircleGeometry(R - 0.01, 32), MAT.liquid(0xc5e3f5, 0.8), null, { cast: false }); surf.rotation.x = -Math.PI / 2; world.add(surf);
  const res = new THREE.Group(); world.add(res);
  res.add(mesh(new THREE.CylinderGeometry(0.42, 0.42, 1.0, 28, 1, true), MAT.glass(), [0, 0, 0], { cast: false }));
  const resWater = mesh(new THREE.CylinderGeometry(0.41, 0.41, 0.7, 28), waterMat, [0, -0.12, 0], { cast: false }); res.add(resWater);
  res.add(mesh(new THREE.BoxGeometry(0.2, 0.14, 0.2), MAT.matte(0x30363d), [-0.5, 0, 0]));
  res.position.set(1.4, 2.0, 0.2);
  const hose = mesh(new THREE.BufferGeometry(), MAT.gloss(0x9a3412)); world.add(hose);

  // the fork, with prongs that blur while ringing
  const fork = new THREE.Group(); fork.position.set(0, TOP + 0.35, 0.05); world.add(fork);
  const steel = MAT.steel();
  fork.add(mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.9, 12), steel, [0, 0.9, 0]));
  const prongs = [-1, 1].map((sg) => { const p = mesh(new THREE.BoxGeometry(0.06, 0.95, 0.07), steel, [sg * 0.12, -0.05, 0]); fork.add(p); return p; });
  fork.add(mesh(new THREE.TorusGeometry(0.12, 0.035, 8, 20, Math.PI), steel, [0, 0.42, 0]).rotateZ(Math.PI));
  const label = mesh(new THREE.PlaneGeometry(0.3, 0.12), new THREE.MeshBasicMaterial({ map: canvasTexture(`ho-fork-${f}`, 128, 48, (c, w, h) => { c.fillStyle = '#e5e7eb'; c.fillRect(0, 0, w, h); c.fillStyle = '#111827'; c.font = '800 28px system-ui, sans-serif'; c.textAlign = 'center'; c.fillText(`${f} Hz`, w / 2, 34); }) }), [0, 1.0, 0.04]); fork.add(label);
  const pad = new THREE.Group(); pad.position.set(-1.3, 0, 0.6); world.add(pad);
  pad.add(mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.12, 24), MAT.matte(0x1f2937), [0, 0.06, 0]));
  // standing wave: a soft envelope inside the column, brightest at the antinodes
  const waveTex = canvasTexture('ho-res-wave', 64, 512, (g, w, h) => { for (let y = 0; y < h; y++) { const a = Math.abs(Math.cos(Math.PI * y / h * 3)); g.fillStyle = `rgba(96,165,250,${0.55 * a})`; g.fillRect(0, y, w, 1); } });
  const wave = new THREE.Mesh(new THREE.CylinderGeometry(R - 0.02, R - 0.02, 1, 24, 1, true), new THREE.MeshBasicMaterial({ map: waveTex, transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide }));
  wave.renderOrder = 4; world.add(wave);

  const st = { level: 4.0, amp: 0, struck: 0, picked: [], audio: null, loud: 0 };
  const lenCm = () => (TOP - st.level) * 10;
  function layout() {
    const h = Math.max(0.01, st.level - (TOP - LEN));
    water.scale.y = h; water.position.y = TOP - LEN + h / 2; surf.position.y = st.level;
    res.position.y = st.level - 0.12;
    const a = new THREE.Vector3(0, TOP - LEN + 0.05, 0); const b = res.position.clone().add(new THREE.Vector3(0, -0.5, 0));
    const curve = new THREE.CatmullRomCurve3([a, a.clone().add(new THREE.Vector3(0.1, -0.6, 0.15)), b.clone().add(new THREE.Vector3(-0.2, -0.8, 0.1)), b]);
    hose.geometry.dispose(); hose.geometry = new THREE.TubeGeometry(curve, 30, 0.035, 8);
    const L = lenCm() / 100 * 10; wave.scale.y = Math.max(0.01, L); wave.position.y = TOP - L / 2;
  }
  function response(lcm) {
    const w = 0.55;
    const r1 = 1 / (1 + ((lcm - L1) / w) ** 2); const r2 = 0.8 / (1 + ((lcm - L2) / (w * 1.3)) ** 2);
    return Math.max(r1, r2);
  }
  function strike() {
    st.struck = 1; sfx.play('click');
    if (!sfx.muted) {
      if (!st.audio) {
        const AC = window.AudioContext || window.webkitAudioContext; if (AC) {
          const c = new AC(); const o = c.createOscillator(); const o2 = c.createOscillator(); const g = c.createGain();
          o.frequency.value = f; o2.frequency.value = f * 2.01; const g2 = c.createGain(); g2.gain.value = 0.04;
          o.connect(g); o2.connect(g2); g2.connect(g); g.connect(c.destination); g.gain.value = 0; o.start(); o2.start();
          st.audio = { c, g };
        }
      }
      if (st.audio && st.audio.c.state === 'suspended') st.audio.c.resume();
    }
  }
  const meter = hud.chip('ho-meter'); meter.dx = 18; meter.dy = -30;

  const SHOT = shot({ pos: [1.4, TOP - 0.6, 6.4], target: [0.35, TOP - 1.9, 0], fitH: 6.6, fit: 3.8 });
  const resHandler = {
    down(p) {
      if (screenDist(ctx, pad, p, 0.1) < 60 || screenDist(ctx, fork, p, 0.5) < 70) { strike(); return true; }
      if (screenDist(ctx, res, p) > (p.touch ? 120 : 90) && !ctx.input.pick([res])) return false;
      this.d = { y: p.y, l: st.level }; return true;
    },
    move(p) { if (!this.d) return; st.level = clamp(this.d.l - (p.y - this.d.y) / (ctx.stage.clientHeight / 5.6), TOP - LEN + 0.6, TOP - 0.6); layout(); },
    up() { this.d = null; },
  };
  function recordStep(n) {
    return {
      title: n === 1 ? 'Find the first resonance' : 'Find the second resonance',
      text: n === 1 ? 'Strike the fork on the <b>rubber pad</b> (tap it), then raise or lower the <b>reservoir</b> (drag it) to move the water. Starting with the water high, lower it slowly until the column <b>booms loudest</b>, then record the length of air.' : 'Lower the water further, about three times as far, to the <b>second resonance</b>: fainter, but just as sharp. Strike the fork again when it fades.',
      hint: 'Sweep through the loud spot both ways and settle where it peaks. Turn the sound on to hear it; the meter shows it too.', shot: SHOT,
      enter() {
        if (n === 1) { st.level = TOP - 0.9; layout(); }
        hud.actions([
          { id: 'snd', label: sfx.muted ? 'Sound on' : 'Sound off', onClick: () => { sfx.setMuted(!sfx.muted); hud.relabel('snd', sfx.muted ? 'Sound on' : 'Sound off'); if (!sfx.muted) strike(); } },
          { id: 'rec', label: `Record l${n}`, primary: true, onClick: () => {
            const l = Math.round(lenCm() * 10) / 10; const r = response(l);
            if (st.struck < 0.05) { ctx.say('Strike the fork first.', 'hint', 1600); return; }
            if (r < 0.75) { ctx.mistake(`At ${l.toFixed(1)} cm the column is not at its loudest. Move the water slowly through the boom and stop at the peak.`, 3); return; }
            if (n === 2 && l < (st.picked[0] || 0) + 10) { ctx.mistake('That is the first resonance again. The second is about three times as long.', 2); return; }
            st.picked[n - 1] = l; ui.observe(`l${n}`, `<b>${l.toFixed(1)} cm</b>`); hud.actions([]);
            ctx.next(n === 1 ? `l₁ = ${l.toFixed(1)} cm: a quarter wavelength, less the end correction.` : `l₂ = ${l.toFixed(1)} cm: three quarter wavelengths, less the same end correction.`);
          } },
        ]);
      },
      exit() { hud.actions([]); },
      skip() { st.picked[n - 1] = Math.round((n === 1 ? L1 : L2) * 10) / 10; st.level = TOP - st.picked[n - 1] / 10; layout(); },
      handler: resHandler,
    };
  }
  const steps = [
    {
      title: 'The apparatus', text: `A ${f} Hz tuning fork, a glass resonance tube (inner diameter ${D_CM.toFixed(1)} cm) joined by rubber tubing to a water reservoir, and a metre scale. Room temperature: <b>${T} °C</b>.`, hideBelt: true, shot: SHOT,
      enter() { hud.actions([{ id: 'go', label: 'Start', primary: true, onClick: () => { hud.actions([]); ctx.next(); } }]); },
      exit() { hud.actions([]); },
    },
    recordStep(1), recordStep(2),
    {
      title: 'Speed of sound and end correction', text: 'l₂ − l₁ is exactly half a wavelength, so the end correction cancels.', hideBelt: true, shot: SHOT,
      enter() {
        const [l1, l2] = st.picked; const vm = 2 * f * (l2 - l1) / 100; st.v = vm; st.e = (l2 - 3 * l1) / 2;
        const opts = [[vm, '2f(l₂ − l₁)'], [4 * f * l1 / 100, '4 f l₁'], [f * (l2 - l1) / 100, 'f(l₂ − l₁)']].map(([x, w]) => ({ label: `${x.toFixed(1)} m/s  (${w})`, value: x })).sort(() => Math.random() - 0.5);
        anim.wait(0.7, () => ui.choose(ctx.stage.clientWidth / 2, 50, `l₁ = ${l1.toFixed(1)} cm, l₂ = ${l2.toFixed(1)} cm, f = ${f} Hz. Speed of sound?`, opts, (x) => {
          if (Math.abs(x - vm) > 1e-6) ctx.mistake('l₂ − l₁ = λ/2, so v = fλ = 2f(l₂ − l₁). 4fl₁ ignores the end correction.', 3);
          ui.observe('v', `<b>${vm.toFixed(1)} m/s</b>`); ui.observe('End correction e', `${st.e.toFixed(2)} cm (0.3d = ${e.toFixed(2)} cm)`);
          ctx.next(`v = ${vm.toFixed(1)} m/s at ${T} °C; e = (l₂ − 3l₁)/2 = ${st.e.toFixed(2)} cm.`, 1.2);
        }));
      },
      exit() { ui.clearChooser(); },
    },
  ];

  layout();
  ctx.debug = { st, L1, L2, f, v, layout, response };
  return {
    tools: [], steps,
    update(dt, t) {
      st.struck *= Math.exp(-dt / 7);
      const r = response(lenCm());
      st.amp += ((st.struck * (0.08 + 0.92 * r)) - st.amp) * (1 - Math.exp(-dt * 8));
      const a = st.struck * 0.012 * Math.sin(t * 90);
      prongs[0].position.x = -0.12 - a; prongs[1].position.x = 0.12 + a;
      wave.material.opacity = Math.min(0.85, st.amp * 1.1 * r);
      if (st.audio) st.audio.g.gain.setTargetAtTime(sfx.muted ? 0 : st.amp * 0.22, st.audio.c.currentTime, 0.03);
      meter.at.set(R + 0.3, BY + TOP - 0.3, 0);
      const bars = Math.round(st.amp * 12);
      meter.set(`<span class="ho-bars">${'▮'.repeat(bars)}<i>${'▮'.repeat(12 - bars)}</i></span> <b>${lenCm().toFixed(1)}</b> cm`).show(true);
      hud.update();
    },
    result() {
      const err = ((st.v || 0) - v) / v * 100;
      return { title: 'Resonance column', rows: [['l₁, l₂', `${(st.picked[0] || 0).toFixed(1)} cm, ${(st.picked[1] || 0).toFixed(1)} cm`], ['Your v', `${(st.v || 0).toFixed(1)} m/s`], [`v at ${T} °C`, `${v.toFixed(1)} m/s`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`], ['End correction', `${(st.e || 0).toFixed(2)} cm`]],
        conclusion: 'The closed air column resonates when it holds an odd number of quarter waves. The antinode sits a little above the open end (the end correction, about 0.3 times the diameter), which is why the difference of two resonances, exactly half a wavelength, gives the speed of sound without needing to know it.' };
    },
    dispose() { hud.dispose(); if (st.audio) { try { st.audio.c.close(); } catch (er) { /* closed */ } } },
  };
}
