// The metre bridge (a Wheatstone bridge with a 100 cm wire). The student pulls plugs from a
// resistance box to choose R, closes the key, and touches the jockey to the wire to hunt for the
// null point, where the galvanometer needle does not move; then interchanges R and the unknown
// coil and balances again, which cancels the end resistances of the wire. The galvanometer is
// driven by the actual circuit, solved by nodal analysis each time the jockey touches, with the
// wire's end resistances, the cell's resistance and the galvanometer's own. Sliding the pressed
// jockey along the wire, or leaving the key in, is caught.
import { THREE } from '../../engine.js';
import { MAT, mesh, clamp, canvasTexture } from '../../bio-handson/kit.js';
import { M as KIT } from '../../lab3d-kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, screenDist } from '../hud.js';
import { bindingPost, lead, galvanometer, resistanceBox, plugKey, cell, solve, postTop, brass } from '../circuit.js';

const BY = 0.8;
const E = 2.0; const RS = 10; const RG = 60; const RHO = 0.02; const FOM = 1e-5;
const ALPHA = 0.4; const BETA = 0.6;
const WIRE_Y = 0.16; const WIRE_Z = 0.25;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
const xOf = (l) => -5 + l / 10;

function scaleTex() {
  return canvasTexture('ho-mb-scale', 8192, 160, (g, w, h) => {
    g.fillStyle = '#f6edd2'; g.fillRect(0, 0, w, h); g.fillStyle = '#111827';
    const x = (mm) => 40 + (w - 80) * mm / 1000;
    for (let mm = 0; mm <= 1000; mm++) { const cm = mm % 10 === 0; const five = mm % 50 === 0; const len = five ? 70 : cm ? 52 : 26; g.fillRect(Math.round(x(mm) - (cm ? 1.6 : 0.9)), 0, cm ? 3.2 : 1.8, len); if (cm) { g.font = `700 ${five ? 40 : 30}px system-ui, sans-serif`; g.textAlign = 'center'; g.fillText(String(mm / 10), x(mm), 118); } }
  }, { anisotropy: 16 });
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const X = Math.round((2 + Math.random() * 6) * 100) / 100;
  const COIL_L = 50.0; const rhoTrue = 4.9e-7; const dmm = Math.round(Math.sqrt(4 * rhoTrue * COIL_L / 100 / (Math.PI * X)) * 1e3 * 1000) / 1000;

  // ---- board ----
  const board = mesh(new THREE.BoxGeometry(11.2, 0.1, 1.6), KIT.wood('teak'), [0, 0.05, 0.05]); world.add(board);
  const scale = new THREE.Mesh(new THREE.PlaneGeometry(10.08, 0.2), new THREE.MeshStandardMaterial({ map: scaleTex(), roughness: 0.6 }));
  scale.rotation.x = -Math.PI / 2; scale.position.set(0, 0.102, WIRE_Z + 0.13); world.add(scale);
  const copper = new THREE.MeshStandardMaterial({ color: 0xc8794a, metalness: 1, roughness: 0.3 });
  const strip = (x0, x1, z0, z1) => world.add(mesh(new THREE.BoxGeometry(x1 - x0, 0.03, z1 - z0), copper, [(x0 + x1) / 2, 0.115, (z0 + z1) / 2]));
  strip(-5.4, -2.0, -0.45, -0.25); strip(-5.4, -4.98, -0.45, WIRE_Z + 0.06); strip(-1.2, 1.2, -0.45, -0.25); strip(2.0, 5.4, -0.45, -0.25); strip(4.98, 5.4, -0.45, WIRE_Z + 0.06);
  const wire = mesh(new THREE.CylinderGeometry(0.008, 0.008, 10, 8), new THREE.MeshStandardMaterial({ color: 0xbfc5cc, metalness: 1, roughness: 0.3 }), [0, WIRE_Y, WIRE_Z]); wire.rotation.z = Math.PI / 2; world.add(wire);
  const post = (x, z) => { const p = bindingPost(); p.position.set(x, 0.13, z); world.add(p); return p; };
  const P = { lb: post(-5.15, -0.35), r1: post(-2.25, -0.35), m1: post(-0.95, -0.35), mg: post(0, -0.35), m2: post(0.95, -0.35), r2: post(2.25, -0.35), rb: post(5.15, -0.35) };

  // ---- components ----
  const box = resistanceBox(); box.group.position.set(-1.6, 0, -1.45); world.add(box.group);
  const coil = new THREE.Group(); world.add(coil);
  coil.add(mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.32, 24), MAT.gloss(0x7c2d12), [0, 0.2, 0]));
  for (let i = 0; i < 14; i++) coil.add(mesh(new THREE.TorusGeometry(0.17, 0.008, 6, 28), copper, [0, 0.07 + i * 0.019, 0]).rotateX(Math.PI / 2));
  coil.add(mesh(new THREE.BoxGeometry(0.7, 0.04, 0.4), MAT.gloss(0x111827), [0, 0.02, 0]));
  const coilPosts = [-0.26, 0.26].map((x) => { const p = bindingPost(); p.scale.setScalar(0.8); p.position.set(x, 0.04, 0.1); coil.add(p); return p; });
  const tagX = mesh(new THREE.PlaneGeometry(0.22, 0.1), new THREE.MeshBasicMaterial({ map: canvasTexture('ho-mb-x', 96, 44, (c, w, h) => { c.fillStyle = '#fef3c7'; c.fillRect(0, 0, w, h); c.fillStyle = '#111827'; c.font = '800 30px system-ui, sans-serif'; c.textAlign = 'center'; c.fillText('X', w / 2, 32); }) }), [0, 0.38, 0.17]); coil.add(tagX);
  coil.position.set(1.6, 0, -1.35);
  const galvo = galvanometer(); galvo.group.position.set(0, 0, 1.75); galvo.group.scale.setScalar(1.5); world.add(galvo.group);
  const key = plugKey(); key.group.position.set(3.2, 0, -1.6); world.add(key.group);
  const bat = cell('2 V'); bat.group.position.set(4.5, 0, -1.65); world.add(bat.group);
  const jockey = new THREE.Group(); world.add(jockey);
  jockey.add(mesh(new THREE.CylinderGeometry(0.035, 0.03, 0.55, 14), MAT.gloss(0x111827), [0, 0.42, 0]));
  jockey.add(mesh(new THREE.ConeGeometry(0.03, 0.12, 4), brass(), [0, 0.09, 0]).rotateX(Math.PI));
  jockey.add(mesh(new THREE.SphereGeometry(0.05, 14, 10), MAT.gloss(0x111827), [0, 0.72, 0]));

  // ---- leads ----
  const tmpA = new THREE.Vector3(); const tmpB = new THREE.Vector3();
  const L = {};
  function wireUp() {
    const left = st.swapped ? coilPosts : box.posts; const right = st.swapped ? box.posts : coilPosts;
    const set = (k, a, b, col) => { postTop(a, world, tmpA); postTop(b, world, tmpB); if (L[k]) L[k].set(tmpA, tmpB); else L[k] = lead(world, tmpA, tmpB, col); };
    set('r1', left[0], P.r1, 0xb91c1c); set('r2', left[1], P.m1, 0xb91c1c);
    set('x1', right[0], P.m2, 0x1d4ed8); set('x2', right[1], P.r2, 0x1d4ed8);
    set('g1', galvo.posts[0], P.mg, 0x111827);
    set('k1', P.rb, bat.posts[1], 0xb91c1c); set('k2', bat.posts[0], key.posts[1], 0x111827); set('k3', key.posts[0], P.lb, 0x111827);
    jockeyLead();
  }
  function jockeyLead() { postTop(galvo.posts[1], world, tmpA); tmpB.copy(jockey.position); tmpB.y += 0.66; if (L.j) L.j.set(tmpA, tmpB); else L.j = lead(world, tmpA, tmpB, 0x166534, { sag: 0.15 }); }

  const st = { swapped: false, l: 50, pressed: false, lastDiv: 0, lastL: null, sets: [], cur: [], scraped: false, keyT: 0, warnedKey: false };
  const jy = { y: 0.4, v: 0 };
  function setJockey(l) { st.l = clamp(Math.round(l * 10) / 10, 0.5, 99.5); jockey.position.x = xOf(st.l); jockey.position.z = WIRE_Z; jockeyLead(); }

  function galvoCurrent(l) {
    const Rl = st.swapped ? X : box.total(); const Rr = st.swapped ? box.total() : X;
    if (!key.closed || Rl <= 0) return 0;
    const RAJ = RHO * (l + ALPHA); const RJC = RHO * (100 - l + BETA);
    const gA = 1 / RS, g1 = 1 / Rl, g2 = 1 / Rr, gW1 = 1 / RAJ, gW2 = 1 / RJC, gG = 1 / RG;
    const A = [[gA + g1 + gW1, -g1, -gW1], [-g1, g1 + g2 + gG, -gG], [-gW1, -gG, gW1 + gG + gW2]];
    const [, VB, VJ] = solve(A, [E * gA, 0, 0]);
    return (VB - VJ) / RG;
  }

  const lChip = hud.chip('ho-chip-read'); lChip.dx = 14; lChip.dy = -38;
  const rChip = hud.chip(); rChip.dx = -50; rChip.dy = -70;
  const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0); const hit = new THREE.Vector3();
  function wireX() { plane.constant = -(BY + WIRE_Y); if (!ctx.input.ptr.ray.intersectPlane(plane, hit)) return null; return hit.x; }
  const jockeyHandler = {
    down(p) {
      const x = wireX(); if (x === null) return false;
      if (Math.abs(hit.z - WIRE_Z) > 0.55 && screenDist(ctx, jockey, p, 0.4) > 60) return false;
      setJockey((x + 5) * 10); st.pressed = true; st.pressL = st.l; sfx.play('click');
      if (!key.closed) ctx.say('Nothing moves: the key is out, so no current flows. Insert the plug key.', 'hint', 2400);
      return true;
    },
    move() { if (!st.pressed) return; const x = wireX(); if (x === null) return; setJockey((x + 5) * 10); if (Math.abs(st.l - st.pressL) > 1.5 && !st.scraped) { st.scraped = true; ctx.mistake('Lift the jockey before moving it. Dragging it along the wire while pressed scrapes the wire and spoils its uniform resistance.', 2); } },
    up() { if (st.pressed) { st.lastDiv = galvo.divisions; st.lastL = st.l; } st.pressed = false; },
    cancel() { st.pressed = false; },
  };

  const SHOT_ALL = shot({ pos: [0, 4.6, 7.4], target: [0, 0.1, -0.2], fit: 11.8 });
  const SHOT_BOX = shot({ pos: [-0.6, 1.9, 1.4], target: [-1.2, 0.3, -1.3], fit: 3.2 });
  const SHOT_KEY = shot({ pos: [3.6, 1.6, 0.6], target: [3.6, 0.2, -1.5], fit: 2.4 });
  const SHOT_BAL = shot({ pos: [0, 2.9, 3.9], target: [0, 0.15, 0.7], fit: 6.4 });

  function balanceStep(n) {
    return {
      title: n === 0 ? 'Find the balance point' : 'Balance again',
      text: 'Touch the <b>jockey</b> to the wire (press and hold), watch the needle, lift it, and try again further along. Where the needle <b>does not move at all</b>, record the balance length.',
      hint: 'If the needle kicks one way at one end and the other way at the other end, the null point lies between. Halve the gap each time.', shot: SHOT_BAL,
      enter() { st.scraped = false; st.lastL = null; hud.actions([{ id: 'rec', label: 'Record balance length', primary: true, disabled: true, onClick: record }]); },
      exit() { hud.actions([]); },
      skip() { const l = bisect(); setJockey(l); st.lastL = st.l; st.lastDiv = galvoCurrent(st.l) / FOM; st.cur.push({ R: box.total(), l: st.l, swapped: st.swapped }); },
      update() { if (st.lastL !== null) hud.enable('rec', true); },
      handler: jockeyHandler,
    };
  }
  function bisect() { let a = 0.5, b = 99.5; const f = (l) => galvoCurrent(l); for (let i = 0; i < 50; i++) { const m = (a + b) / 2; if (f(a) * f(m) <= 0) b = m; else a = m; } return (a + b) / 2; }
  function record() {
    if (st.lastL === null) return;
    const div = galvoCurrent(st.lastL) / FOM;
    if (Math.abs(div) > 0.6) { ctx.mistake(`Not balanced: at ${st.lastL.toFixed(1)} cm the needle kicks ${Math.abs(div).toFixed(1)} divisions ${div > 0 ? 'right' : 'left'}.`, 3); return; }
    const l = st.lastL;
    if (l < 30 || l > 70) ctx.say('Balanced — but a null point near the middle of the wire is more sensitive. Choose R closer to X next time.', 'hint', 3600);
    st.cur.push({ R: box.total(), l, swapped: st.swapped });
    ui.observe(`${st.swapped ? 'X | R' : 'R | X'}  R = ${box.total()} Ω`, `l = <b>${l.toFixed(1)} cm</b>`);
    ctx.next(`Balance at l = ${l.toFixed(1)} cm.`);
  }

  const steps = [];
  const IDX = {};
  IDX.r = steps.length;
  steps.push({
    title: 'Choose R on the resistance box', text: 'Pull <b>plugs</b> out of the resistance box (tap them) to put resistance in the left gap. A value close to the unknown gives a null point near the middle.', hint: 'Every plug pulled adds its coil. Try a few ohms.', shot: SHOT_BOX,
    enter() { hud.actions([{ id: 'ok', label: 'R chosen', primary: true, disabled: box.total() <= 0, onClick: () => { ui.observe('R', `${box.total()} Ω`); ctx.next(`R = ${box.total()} Ω in the left gap.`); } }]); },
    exit() { hud.actions([]); rChip.show(false); },
    skip() { if (box.total() <= 0) { box.toggle(3); } },
    handler: { down(p) {
      for (let i = 0; i < box.plugs.length; i++) if (screenDist(ctx, box.plugs[i].plug, p, 0.08) < (p.touch ? 30 : 22)) { box.toggle(i, anim); sfx.play('click'); hud.enable('ok', box.total() > 0); rChip.at.set(box.group.position.x, BY + 0.7, box.group.position.z); rChip.set(`R = <b>${box.total()} Ω</b>`).show(true); return true; }
      return false;
    } },
  });
  steps.push({
    title: 'Close the key', text: 'Insert the <b>plug key</b> (tap it) to let current flow through the wire.', shot: SHOT_KEY,
    skip() { key.set(true); },
    handler: { down(p) { if (screenDist(ctx, key.group, p, 0.12) > 70) return false; key.set(true, anim); sfx.play('click'); anim.wait(0.6, () => ctx.next('Current flows through the bridge wire.')); return true; } },
  });
  IDX.bal1 = steps.length; steps.push(balanceStep(0));
  steps.push({
    title: 'Interchange R and X', text: 'Swap the resistance box and the unknown coil between the gaps (tap <b>Interchange</b>). Balancing again cancels the resistance at the ends of the wire.', hideBelt: true, shot: SHOT_ALL,
    enter() { hud.actions([{ id: 'sw', label: 'Interchange', primary: true, onClick: () => { hud.actions([]); swap(() => ctx.next('Interchanged: X now in the left gap.')); } }]); },
    exit() { hud.actions([]); },
    skip() { swapNow(); },
  });
  IDX.bal2 = steps.length; steps.push(balanceStep(1));
  steps.push({
    title: 'Open the key', text: 'Take the <b>plug key</b> out between readings so the wire does not warm up and change its resistance.', shot: SHOT_KEY,
    enter() { st.keyT = 0; },
    skip() { key.set(false); },
    handler: { down(p) { if (screenDist(ctx, key.group, p, 0.12) > 70) return false; key.set(false, anim); sfx.play('click'); st.sets.push(st.cur.splice(0)); anim.wait(0.5, () => ctx.next('Key out.')); return true; } },
  });
  steps.push({
    title: 'Another R?', text: 'Repeat with a <b>different R</b>, or work out X.', hideBelt: true, shot: SHOT_ALL,
    enter() { hud.actions([{ id: 'again', label: 'Another R', onClick: () => { hud.actions([]); if (st.swapped) swapNow(); ctx.goTo(IDX.r); } }, { id: 'calc', label: 'Calculate X', primary: true, onClick: () => { hud.actions([]); ctx.next(); } }]); },
    exit() { hud.actions([]); },
    skip() { if (st.cur.length) st.sets.push(st.cur.splice(0)); },
  });
  steps.push({
    title: 'Calculate X and the resistivity', text: 'R/X = l/(100 − l) for each balance (and X/R after interchanging). Then ρ = X π r² / L for the coil.', hideBelt: true, shot: SHOT_ALL,
    enter() {
      const all = st.sets.flat();
      const xs = all.map((s) => (s.swapped ? s.R * s.l / (100 - s.l) : s.R * (100 - s.l) / s.l));
      const Xm = xs.reduce((a, b) => a + b, 0) / Math.max(1, xs.length); st.Xm = Xm;
      all.forEach((s, i) => ui.observe(`X (${s.swapped ? 'interchanged' : 'direct'}, R = ${s.R} Ω)`, `${xs[i].toFixed(3)} Ω`));
      const r = dmm / 2 / 1000; const rho = Xm * Math.PI * r * r / (COIL_L / 100); st.rho = rho;
      const opts = [[rho, 'X π r² / L'], [Xm * Math.PI * (dmm / 1000) ** 2 / (COIL_L / 100), 'X π d² / L'], [Xm * (COIL_L / 100) / (Math.PI * r * r), 'X L / π r²']].map(([v, w]) => ({ label: `${v.toExponential(2)} Ω m  (${w})`, value: v })).sort(() => Math.random() - 0.5);
      anim.wait(0.8, () => ui.choose(ctx.stage.clientWidth / 2, 50, `Mean X = ${Xm.toFixed(3)} Ω. Coil: L = ${COIL_L.toFixed(1)} cm, d = ${dmm.toFixed(3)} mm (screw gauge). Resistivity ρ =`, opts, (v) => {
        if (Math.abs(v - rho) / rho > 1e-6) ctx.mistake('R = ρL/A with A = π r² (r is half the diameter), so ρ = X π r² / L.', 3);
        ui.observe('ρ', `<b>${rho.toExponential(2)} Ω m</b>`); ctx.next(`X = ${Xm.toFixed(2)} Ω, ρ = ${rho.toExponential(2)} Ω m: constantan (manganin and constantan are about 4.4–4.9 × 10⁻⁷ Ω m).`, 1.2);
      }));
    },
    exit() { ui.clearChooser(); },
  });

  function swapNow() { st.swapped = !st.swapped; const a = box.group.position.clone(); box.group.position.copy(coil.position).setY(0); coil.position.copy(a); box.group.position.x = st.swapped ? 1.6 : -1.6; coil.position.x = st.swapped ? -1.6 : 1.6; wireUp(); }
  function swap(done) {
    const a0 = box.group.position.clone(); const b0 = coil.position.clone();
    const a1 = new THREE.Vector3(st.swapped ? -1.6 : 1.6, 0, a0.z); const b1 = new THREE.Vector3(st.swapped ? 1.6 : -1.6, 0, b0.z);
    st.swapped = !st.swapped;
    anim.add(1.2, (k) => { box.group.position.lerpVectors(a0, a1, k); box.group.position.y = Math.sin(k * Math.PI) * 0.5; coil.position.lerpVectors(b0, b1, k); coil.position.y = Math.sin(k * Math.PI) * 0.35; wireUp(); }, { done: () => { sfx.play('place'); wireUp(); done && done(); } });
  }

  setJockey(50); jockey.position.y = 0.4; wireUp();
  ctx.debug = { st, X, box, key, galvoCurrent, bisect, setJockey };
  return {
    tools: [], steps,
    update(dt) {
      const target = st.pressed ? WIRE_Y - 0.005 : 0.42;
      for (let n = Math.max(1, Math.ceil(dt / 0.008)), h = dt / n, i = 0; i < n; i++) { jy.v += ((target - jy.y) * 260 - jy.v * 24) * h; jy.y += jy.v * h; }
      if (st.pressed && jy.y < WIRE_Y) { jy.y = WIRE_Y; jy.v = 0; }
      jockey.position.y = jy.y - 0.04; if (st.pressed) jockeyLead();
      const touching = st.pressed && jy.y < WIRE_Y + 0.02;
      galvo.setDivisions(touching ? galvoCurrent(st.l) / FOM : 0);
      galvo.update(dt);
      if (key.closed) { st.keyT += dt; if (st.keyT > 150 && !st.warnedKey) { st.warnedKey = true; ctx.say('The key has been in for a while: current warms the wire. Take it out between readings.', 'hint', 3000); } } else st.keyT = 0;
      lChip.at.set(jockey.position.x, BY + jockey.position.y + 0.8, jockey.position.z); lChip.set(`l = <b>${st.l.toFixed(1)}</b> cm`).show(ctx.step && ctx.step.handler === jockeyHandler);
      hud.update();
    },
    result() {
      const err = ((st.Xm || 0) - X) / X * 100;
      return { title: 'Metre bridge', rows: [['Your X', `${(st.Xm || 0).toFixed(3)} Ω`], ['True X', `${X.toFixed(3)} Ω`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(2)} %`], ['Resistivity', `${(st.rho || 0).toExponential(2)} Ω m`]],
        conclusion: 'At balance no current flows through the galvanometer, so R/X equals the ratio of the two wire lengths. Interchanging R and X and averaging cancels the end resistances where the wire meets the copper strips.' };
    },
    dispose() { hud.dispose(); },
  };
}
