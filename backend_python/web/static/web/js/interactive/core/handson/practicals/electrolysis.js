// Electrolysis of copper sulphate with copper electrodes: Faraday's first law. The student cleans
// and weighs the cathode on a digital balance, sets a steady current with the rheostat (watching
// the ammeter), runs the cell for a timed interval (the clock can be run forward), then washes,
// dries and reweighs it. Copper deposits as a salmon-pink film whose mass follows m = (M/2F)·I·t;
// the electrochemical equivalent Z = Δm/(It) is compared with 63.55/(2 × 96485).
import { THREE } from '../../engine.js';
import { MAT, mesh, clamp, canvasTexture } from '../../bio-handson/kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits, screenDist } from '../hud.js';
import { lead, dialMeter, plugKey, cell, postTop, rheostat } from '../circuit.js';

const BY = 0.8; const F = 96485; const MCU = 63.55;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const m0 = Math.round((8 + Math.random() * 3) * 10000) / 10000;
  const st = { t: 0, running: false, mass: null, w0: null, w1: null, on: false, Ilog: 0, dep: 0, weighed: 0, speed: 1 };

  const beaker = new THREE.Group(); beaker.position.set(0, 0, 0); world.add(beaker);
  const prof = [[0.001, 0], [0.7, 0], [0.72, 0.03], [0.72, 1.3], [0.76, 1.35]].map(([r, y]) => new THREE.Vector2(r, y));
  beaker.add(mesh(new THREE.LatheGeometry(prof, 48), MAT.glass(), null, { cast: false, receive: false }));
  const sol = mesh(new THREE.CylinderGeometry(0.69, 0.69, 1.0, 40), MAT.liquid(0x2f86d6, 0.5), [0, 0.53, 0], { cast: false }); sol.renderOrder = 3; beaker.add(sol);
  const copper = (c) => new THREE.MeshStandardMaterial({ color: c, metalness: 0.9, roughness: 0.38 });
  const anode = mesh(new THREE.BoxGeometry(0.02, 1.25, 0.36), copper(0xb87333), [-0.38, 0.9, 0]); beaker.add(anode);
  const cathMat = copper(0xc58a5a); const cathode = mesh(new THREE.BoxGeometry(0.02, 1.25, 0.36), cathMat, [0.38, 0.9, 0]); beaker.add(cathode);
  const bar = mesh(new THREE.BoxGeometry(1.1, 0.06, 0.12), MAT.matte(0x111827), [0, 1.5, 0]); beaker.add(bar);
  const ions = new THREE.Group(); beaker.add(ions);
  const ionMat = new THREE.MeshBasicMaterial({ color: 0x9fd2ff, transparent: true, opacity: 0.8, depthWrite: false });
  const ionGeo = new THREE.SphereGeometry(0.018, 8, 6); const ionList = [];
  for (let i = 0; i < 40; i++) { const m = new THREE.Mesh(ionGeo, ionMat); m.position.set(-0.3 + Math.random() * 0.6, 0.15 + Math.random() * 0.8, -0.25 + Math.random() * 0.5); ions.add(m); ionList.push(m); }
  const bat = cell('6 V'); bat.group.position.set(-2.6, 0, -0.9); world.add(bat.group);
  const key = plugKey(); key.group.position.set(-1.7, 0, -0.9); world.add(key.group);
  const rh = rheostat(20); rh.group.position.set(0, 0, -1.6); rh.group.scale.setScalar(0.85); world.add(rh.group); rh.set(0.7);
  const am = dialMeter('A', 1, 'A', 0.02); am.group.position.set(2.1, 0, -0.6); am.group.scale.setScalar(1.2); world.add(am.group);
  const tA = new THREE.Vector3(); const tB = new THREE.Vector3();
  const link = (a, b, col) => { postTop(a, world, tA); postTop(b, world, tB); lead(world, tA, tB, col); };
  link(bat.posts[1], key.posts[0], 0xb91c1c); link(key.posts[1], rh.posts[0], 0xb91c1c); link(rh.posts[2], am.posts[1], 0xb91c1c);
  anode.updateMatrixWorld(); cathode.updateMatrixWorld();
  const ap = new THREE.Vector3(-0.38, 1.55, 0); const cp = new THREE.Vector3(0.38, 1.55, 0);
  postTop(am.posts[0], world, tA); lead(world, tA, ap, 0xb91c1c); postTop(bat.posts[0], world, tA); lead(world, tA, cp, 0x111827);
  // digital balance
  const bal = new THREE.Group(); bal.position.set(2.4, 0, 0.9); world.add(bal);
  bal.add(mesh(new THREE.BoxGeometry(0.9, 0.18, 0.8), MAT.gloss(0xe5e7eb), [0, 0.09, 0]));
  bal.add(mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.03, 32), MAT.steel(), [0, 0.2, -0.05]));
  const lcdC = document.createElement('canvas'); lcdC.width = 256; lcdC.height = 64; const lcdT = new THREE.CanvasTexture(lcdC);
  const lcd = mesh(new THREE.PlaneGeometry(0.5, 0.125), new THREE.MeshBasicMaterial({ map: lcdT }), [0, 0.12, 0.401]); bal.add(lcd);
  function showMass(m) { const g = lcdC.getContext('2d'); g.fillStyle = '#b9c9a8'; g.fillRect(0, 0, 256, 64); g.fillStyle = '#1b2414'; g.font = '700 40px ui-monospace, monospace'; g.textAlign = 'right'; g.fillText(m === null ? '0.0000 g' : `${m.toFixed(4)} g`, 246, 46); lcdT.needsUpdate = true; }
  showMass(null);
  const clockChip = hud.chip(); clockChip.at.set(0, BY + 1.9, 0);

  const current = () => (key.closed && st.on ? 6 / (2.2 + rh.ohms + 2.0) : 0);
  const cathodeMass = () => m0 + st.dep;
  function moveCathode(to, done) { const from = cathode.position.clone(); const toL = beaker.worldToLocal(to.clone()); anim.add(0.9, (k) => { cathode.position.lerpVectors(from, toL, k); cathode.position.y += Math.sin(k * Math.PI) * 0.5; }, { done }); }
  const home = new THREE.Vector3(0.38, 0.9, 0);

  const SHOT = shot({ pos: [0.2, 2.8, 4.6], target: [0.1, 0.7, -0.1], fit: 6.2 });
  const steps = [
    {
      title: 'Weigh the clean cathode', text: 'The cathode has been cleaned with sandpaper, washed and dried. Tap it to put it on the <b>balance</b>, read the mass, then tap it again to put it back in the cell.', hideBelt: true, shot: SHOT,
      skip() { st.w0 = m0; },
      handler: { down(p) {
        if (!hits(ctx, cathode, p, 60, 0.3)) return false;
        if (!st.weighed) { st.weighed = 1; const to = bal.position.clone().add(new THREE.Vector3(0, 0.25 + 0.62, -0.05)); world.localToWorld(to); moveCathode(to, () => { cathode.rotation.z = 0; showMass(cathodeMass()); sfx.play('place'); st.w0 = cathodeMass(); ui.observe('Cathode before', `${st.w0.toFixed(4)} g`); }); }
        else if (st.weighed === 1 && st.w0) { st.weighed = 2; moveCathode(beaker.localToWorld(home.clone()), () => { showMass(null); ctx.next('Weighed and back in the cell, facing the anode.'); }); }
        return true;
      } },
    },
    {
      title: 'Set a steady current', text: 'Insert the <b>key</b> (tap it) and slide the <b>rheostat</b> until the ammeter reads about <b>0.5 A</b>. Then start the clock.', hint: 'Lower rheostat resistance gives more current.', hideBelt: true, shot: SHOT,
      enter() { hud.actions([{ id: 'go', label: 'Start the clock', primary: true, onClick: () => {
        if (!key.closed) { ctx.say('Insert the key first.', 'hint', 1600); return; }
        const I = current(); if (I < 0.35 || I > 0.7) { ctx.say(`The current is ${I.toFixed(2)} A; aim for about 0.5 A.`, 'hint', 2400); return; }
        hud.actions([]); ctx.next(`Current ${I.toFixed(2)} A. Clock running.`);
      } }]); },
      exit() { hud.actions([]); },
      skip() { key.set(true); st.on = true; rh.set(0.3); },
      handler: { down(p) {
        if (screenDist(ctx, key.group, p, 0.12) < 60) { key.set(!key.closed, anim); st.on = key.closed; sfx.play('click'); return true; }
        if (screenDist(ctx, rh.slider.children[0], p) < 60) { this.d = { x: p.x, f: rh.fraction }; return true; }
        return false;
      }, move(p) { if (this.d) { rh.set(this.d.f + (p.x - this.d.x) / (ctx.stage.clientWidth * 0.3)); sfx.play('knob'); } }, up() { this.d = null; } },
    },
    {
      title: 'Run for 30 minutes', text: 'Keep the current steady. Run the clock forward (×120) and watch copper plate onto the cathode. Stop at <b>30 minutes</b>.', hideBelt: true, shot: SHOT,
      enter() { st.running = true; hud.actions([{ id: 'ff', label: 'Run ×120', primary: true, onClick: () => { st.speed = st.speed === 1 ? 120 : 1; hud.relabel('ff', st.speed === 1 ? 'Run ×120' : 'Normal speed'); } }, { id: 'stop', label: 'Stop at 30 min', onClick: () => {
        if (st.t < 1790) { ctx.say(`Only ${(st.t / 60).toFixed(1)} minutes so far.`, 'hint', 1600); return; }
        st.running = false; key.set(false, anim); st.on = false; hud.actions([]); ctx.next(`Switched off after ${(st.t / 60).toFixed(1)} min at a mean ${(st.Ilog / st.t).toFixed(3)} A.`);
      } }]); },
      exit() { hud.actions([]); },
      skip() { const I = current() || 0.5; st.t = 1800; st.Ilog = I * 1800; st.dep = MCU / (2 * F) * I * 1800; st.running = false; },
    },
    {
      title: 'Wash, dry and reweigh', text: 'Tap the cathode: it is rinsed, dried in warm air and weighed again.', hideBelt: true, shot: SHOT,
      skip() { st.w1 = cathodeMass(); },
      handler: { down(p) {
        if (!hits(ctx, cathode, p, 60, 0.3) || st.w1) return false;
        const to = bal.position.clone().add(new THREE.Vector3(0, 0.87, -0.05)); world.localToWorld(to);
        moveCathode(to, () => { showMass(cathodeMass()); sfx.play('place'); st.w1 = cathodeMass(); ui.observe('Cathode after', `${st.w1.toFixed(4)} g`); anim.wait(0.8, () => ctx.next(`Gain ${(st.w1 - st.w0).toFixed(4)} g of copper.`)); });
        return true;
      } },
    },
    {
      title: 'Electrochemical equivalent', text: 'Z = Δm / (I t), against Faraday\'s M/(nF) for Cu²⁺ + 2e⁻ → Cu.', hideBelt: true, shot: SHOT,
      enter() {
        const dm = st.w1 - st.w0; const I = st.Ilog / Math.max(1, st.t); const Z = dm / (I * st.t); st.Z = Z;
        const opts = [[Z, 'Δm / (I t)'], [dm * I / st.t, 'Δm I / t'], [dm / (I * st.t / 60), 'Δm / (I × minutes)']].map(([v, w]) => ({ label: `${(v * 1e4).toFixed(3)} × 10⁻⁴ g/C  (${w})`, value: v })).sort(() => Math.random() - 0.5);
        anim.wait(0.7, () => ui.choose(ctx.stage.clientWidth / 2, 50, `Δm = ${dm.toFixed(4)} g, I = ${I.toFixed(3)} A, t = ${st.t.toFixed(0)} s. Z =`, opts, (v) => {
          if (Math.abs(v - Z) > 1e-12) ctx.mistake('m = Z I t, with t in seconds, so Z = Δm / (I t).', 3);
          ui.observe('Z', `<b>${(Z * 1e4).toFixed(3)} × 10⁻⁴ g/C</b>`); ctx.next(`Z = ${(Z * 1e4).toFixed(3)} × 10⁻⁴ g/C; Faraday: 63.55/(2 × 96485) = ${(MCU / (2 * F) * 1e4).toFixed(3)} × 10⁻⁴.`, 1.2);
        }));
      },
      exit() { ui.clearChooser(); },
    },
  ];
  ctx.debug = { st, current, key, rh };
  return {
    tools: [], steps,
    update(dt, t) {
      const I = current(); am.set(I); am.update(dt);
      if (st.running) {
        const sdt = dt * st.speed; st.t += sdt; st.Ilog += I * sdt; st.dep += MCU / (2 * F) * I * sdt;
        const k = clamp(st.dep / 0.4, 0, 1); cathMat.color.setRGB(0.77 + 0.15 * k, 0.54 - 0.05 * k, 0.35 - 0.04 * k); anode.scale.x = 1 - 0.3 * k;
        sol.material.opacity = 0.5;
        clockChip.set(`⏱ <b>${Math.floor(st.t / 60)}:${String(Math.floor(st.t % 60)).padStart(2, '0')}</b> min`).show(true);
      } else clockChip.show(false);
      if (I > 0) for (const m of ionList) { m.position.x += dt * 0.12 * (I / 0.5); if (m.position.x > 0.34) m.position.x = -0.32; }
      hud.update();
    },
    result() {
      const zt = MCU / (2 * F); const err = ((st.Z || 0) - zt) / zt * 100;
      return { title: 'Electrolysis of CuSO₄', rows: [['Δm', `${((st.w1 || 0) - (st.w0 || 0)).toFixed(4)} g`], ['Your Z', `${((st.Z || 0) * 1e4).toFixed(3)} × 10⁻⁴ g/C`], ['Faraday', `${(zt * 1e4).toFixed(3)} × 10⁻⁴ g/C`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`]],
        conclusion: 'The mass deposited is proportional to the charge passed (Faraday\'s first law); each copper ion needs two electrons, so 2F of charge plates one mole, 63.55 g.' };
    },
    dispose() { hud.dispose(); lcdT.dispose(); },
  };
}
