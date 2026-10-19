// Potentiometer: comparing the e.m.f.s of two cells. A 2 V driver cell, a rheostat and a key send a
// steady current along a 100 cm wire, so the potential falls uniformly along it. A two-way key puts
// a Leclanché cell (1.45 V) or a Daniell cell (1.08 V) in the galvanometer branch; the jockey finds
// the length where the wire's fall of potential exactly balances the cell, so no current flows and
// the cell's full e.m.f. is measured. E1/E2 = l1/l2. The galvanometer current comes from solving the
// branch: (E_cell − V(l)) / (r_cell + R_g), with V(l) from the driver circuit.
import { THREE } from '../../engine.js';
import { MAT, mesh, clamp, canvasTexture } from '../../bio-handson/kit.js';
import { M as KIT } from '../../lab3d-kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, screenDist } from '../hud.js';
import { bindingPost, lead, galvanometer, plugKey, cell, postTop, rheostat, brass } from '../circuit.js';

const BY = 0.8; const RHO = 0.04; const ED = 2.0; const RD = 0.3; const RG = 60; const FOM = 1e-5;
const CELLS = [{ name: 'Leclanché', E: 1.45, r: 1.2 }, { name: 'Daniell', E: 1.08, r: 2.0 }];
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
  const st = { which: -1, l: 50, pressed: false, lastL: null, res: [], scraped: false };

  world.add(mesh(new THREE.BoxGeometry(11.2, 0.1, 1.6), KIT.wood('teak'), [0, 0.05, 0.05]));
  const sc = new THREE.Mesh(new THREE.PlaneGeometry(10.08, 0.2), new THREE.MeshStandardMaterial({ map: scaleTex(), roughness: 0.6 })); sc.rotation.x = -Math.PI / 2; sc.position.set(0, 0.102, WIRE_Z + 0.13); world.add(sc);
  const copper = new THREE.MeshStandardMaterial({ color: 0xc8794a, metalness: 1, roughness: 0.3 });
  [[-5.4, -4.98], [4.98, 5.4]].forEach(([a, b]) => world.add(mesh(new THREE.BoxGeometry(b - a, 0.03, 0.7), copper, [(a + b) / 2, 0.115, -0.05])));
  world.add(mesh(new THREE.CylinderGeometry(0.008, 0.008, 10, 8), new THREE.MeshStandardMaterial({ color: 0xbfc5cc, metalness: 1, roughness: 0.3 }), [0, WIRE_Y, WIRE_Z]).rotateZ(Math.PI / 2));
  const post = (x, z) => { const p = bindingPost(); p.position.set(x, 0.13, z); world.add(p); return p; };
  const PA = post(-5.15, -0.3); const PB = post(5.15, -0.3);
  const driver = cell('2 V'); driver.group.position.set(-1.6, 0, -1.7); world.add(driver.group);
  const key = plugKey(); key.group.position.set(-3.2, 0, -1.6); world.add(key.group);
  const rh = rheostat(20); rh.group.position.set(1.8, 0, -1.7); rh.group.scale.setScalar(0.8); world.add(rh.group); rh.set(0.15);
  const c1 = cell('1.45 V'); c1.group.position.set(-3.6, 0, 1.6); world.add(c1.group);
  const c2 = cell('1.08 V'); c2.group.position.set(-2.4, 0, 1.6); world.add(c2.group);
  const two = new THREE.Group(); two.position.set(-1.0, 0, 1.6); world.add(two);
  two.add(mesh(new THREE.BoxGeometry(0.7, 0.06, 0.4), MAT.gloss(0x111827), [0, 0.03, 0]));
  const sockets = [-0.18, 0.18].map((x) => { two.add(mesh(new THREE.BoxGeometry(0.12, 0.05, 0.12), brass(), [x, 0.085, 0])); return x; });
  const plug = new THREE.Group(); plug.position.set(0, 0.16, 0.26); two.add(plug);
  plug.add(mesh(new THREE.CylinderGeometry(0.028, 0.02, 0.1, 12), brass(), [0, -0.04, 0])); plug.add(mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.1, 14), MAT.gloss(0x111827), [0, 0.05, 0]));
  const galvo = galvanometer(); galvo.group.position.set(1.2, 0, 1.7); galvo.group.scale.setScalar(1.4); world.add(galvo.group);
  const jockey = new THREE.Group(); world.add(jockey);
  jockey.add(mesh(new THREE.CylinderGeometry(0.035, 0.03, 0.55, 14), MAT.gloss(0x111827), [0, 0.42, 0]));
  jockey.add(mesh(new THREE.ConeGeometry(0.03, 0.12, 4), brass(), [0, 0.09, 0]).rotateX(Math.PI));
  const tA = new THREE.Vector3(); const tB = new THREE.Vector3();
  const link = (a, b, col) => { postTop(a, world, tA); postTop(b, world, tB); lead(world, tA, tB, col); };
  link(driver.posts[1], key.posts[1], 0xb91c1c); link(key.posts[0], PA, 0xb91c1c); link(PB, rh.posts[1], 0x111827); link(rh.posts[2], driver.posts[0], 0x111827);
  link(c1.posts[1], PA, 0xb91c1c); link(c2.posts[1], PA, 0xb91c1c);
  let jl = null; const jy = { y: 0.42, v: 0 };
  function jLead() { postTop(galvo.posts[1], world, tA); tB.copy(jockey.position); tB.y += 0.66; if (jl) jl.set(tA, tB); else jl = lead(world, tA, tB, 0x166534, { sag: 0.15 }); }
  link(galvo.posts[0], c2.posts[0], 0x1d4ed8);

  const wireR = RHO * 100;
  const current = () => (key.closed ? ED / (RD + rh.ohms + wireR) : 0);
  function galvo_I(l) {
    if (st.which < 0) return 0;
    const c = CELLS[st.which]; const V = current() * RHO * l;
    return (c.E - V) / (c.r + RG + RHO * l);
  }
  function setJ(l) { st.l = clamp(Math.round(l * 10) / 10, 0.5, 99.5); jockey.position.set(xOf(st.l), jockey.position.y, WIRE_Z); jLead(); }
  const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0); const hit = new THREE.Vector3();
  const wx = () => { plane.constant = -(BY + WIRE_Y); return ctx.input.ptr.ray.intersectPlane(plane, hit) ? hit.x : null; };
  const jockeyHandler = {
    down(p) {
      if (screenDist(ctx, rh.slider.children[0], p) < 50) { this.rh = { x: p.x, f: rh.fraction }; return true; }
      const x = wx(); if (x === null || (Math.abs(hit.z - WIRE_Z) > 0.55 && screenDist(ctx, jockey, p, 0.4) > 60)) return false;
      setJ((x + 5) * 10); st.pressed = true; st.pressL = st.l; sfx.play('click');
      if (st.which < 0) ctx.say('Insert the two-way key to put a cell in the circuit.', 'hint', 2000);
      return true;
    },
    move(p) {
      if (this.rh) { rh.set(this.rh.f + (p.x - this.rh.x) / (ctx.stage.clientWidth * 0.3)); return; }
      if (!st.pressed) return; const x = wx(); if (x === null) return; setJ((x + 5) * 10);
      if (Math.abs(st.l - st.pressL) > 1.5 && !st.scraped) { st.scraped = true; ctx.mistake('Lift the jockey before moving it; dragging it scrapes the wire.', 2); }
    },
    up() { this.rh = null; if (st.pressed) st.lastL = st.l; st.pressed = false; },
  };
  function selectCell(i) {
    st.which = i; const from = plug.position.clone(); const to = new THREE.Vector3(sockets[i], 0.12, 0);
    anim.add(0.45, (k) => { plug.position.lerpVectors(from, to, k); plug.position.y += Math.sin(k * Math.PI) * 0.12; }); sfx.play('click');
  }
  function balanceStep(i) {
    return {
      title: `Balance the ${CELLS[i].name} cell`, text: `Put the plug in the <b>${i === 0 ? 'left' : 'right'}</b> socket of the two-way key (tap it) to connect the ${CELLS[i].name} cell, then press the <b>jockey</b> on the wire and move it until the galvanometer shows <b>no deflection</b>. Record the balancing length.`,
      hint: 'If the needle kicks the same way at both ends, the driver current is too small: slide the rheostat to reduce its resistance.', shot: SHOT, hideBelt: true,
      enter() { st.lastL = null; st.scraped = false; hud.actions([{ id: 'rec', label: `Record l${i + 1}`, primary: true, onClick: () => record(i) }]); },
      exit() { hud.actions([]); },
      skip() { rh.set(0); selectCell(i); const l = CELLS[i].E / (current() * RHO); st.res[i] = Math.round(l * 10) / 10; },
      handler: Object.assign({}, jockeyHandler, {
        down(p) { if (screenDist(ctx, two, p, 0.1) < 60) { selectCell(i); return true; } return jockeyHandler.down.call(this, p); },
      }),
    };
  }
  function record(i) {
    if (st.which !== i) { ctx.say(`Plug in the ${CELLS[i].name} cell first.`, 'hint', 1800); return; }
    if (st.lastL === null) { ctx.say('Touch the jockey to the wire first.', 'hint', 1600); return; }
    const div = galvo_I(st.lastL) / FOM;
    if (Math.abs(div) > 0.6) { ctx.mistake(`Not balanced: at ${st.lastL.toFixed(1)} cm the needle kicks ${Math.abs(div).toFixed(1)} divisions.`, 3); return; }
    st.res[i] = st.lastL; ui.observe(`l${i + 1} (${CELLS[i].name})`, `<b>${st.lastL.toFixed(1)} cm</b>`); hud.actions([]); ctx.next(`l${i + 1} = ${st.lastL.toFixed(1)} cm.`);
  }
  const SHOT = shot({ pos: [0, 3.6, 5.6], target: [0, 0.3, 0.3], fit: 11.4 });
  const steps = [
    {
      title: 'Close the driver circuit', text: 'Insert the <b>plug key</b> in the driver circuit (tap it). The 2 V cell sends a steady current along the wire; set the <b>rheostat</b> so the whole wire drops a little more than the bigger e.m.f.', shot: SHOT, hideBelt: true,
      skip() { key.set(true); },
      handler: { down(p) { if (screenDist(ctx, key.group, p, 0.12) > 70) return false; key.set(true, anim); sfx.play('click'); anim.wait(0.6, () => ctx.next(`Current ${(current() * 1000).toFixed(0)} mA: a fall of ${(current() * RHO * 100).toFixed(2)} V along the wire.`)); return true; } },
    },
    balanceStep(0), balanceStep(1),
    {
      title: 'Compare the e.m.f.s', text: 'At balance no current flows in the cell, so the wire measures its full e.m.f.: E ∝ l.', hideBelt: true, shot: SHOT,
      enter() {
        const [l1, l2] = st.res; const r = l1 / l2; st.ratio = r;
        anim.wait(0.7, () => ui.choose(ctx.stage.clientWidth / 2, 50, `l₁ = ${l1.toFixed(1)} cm, l₂ = ${l2.toFixed(1)} cm. E₁/E₂ =`, [{ label: `${r.toFixed(3)}  (l₁/l₂)`, value: 1 }, { label: `${(l2 / l1).toFixed(3)}  (l₂/l₁)`, value: 0 }, { label: `${((l1 * l1) / (l2 * l2)).toFixed(3)}  (l₁²/l₂²)`, value: 2 }].sort(() => Math.random() - 0.5), (v) => {
          if (v !== 1) ctx.mistake('V ∝ l along a uniform wire, so E₁/E₂ = l₁/l₂.', 3);
          ui.observe('E₁/E₂', `<b>${r.toFixed(3)}</b>`); ctx.next(`E₁/E₂ = ${r.toFixed(3)} (true ${(CELLS[0].E / CELLS[1].E).toFixed(3)}).`, 1.2);
        }));
      },
      exit() { ui.clearChooser(); },
    },
  ];
  setJ(50); jockey.position.y = 0.42;
  ctx.debug = { st, current, galvo_I, setJ, selectCell, key, rh };
  return {
    tools: [], steps,
    update(dt) {
      const target = st.pressed ? WIRE_Y - 0.005 : 0.42;
      for (let n = Math.max(1, Math.ceil(dt / 0.008)), h = dt / n, i = 0; i < n; i++) { jy.v += ((target - jy.y) * 260 - jy.v * 24) * h; jy.y += jy.v * h; }
      if (st.pressed && jy.y < WIRE_Y) { jy.y = WIRE_Y; jy.v = 0; }
      jockey.position.y = jy.y - 0.04; if (st.pressed) jLead();
      galvo.setDivisions(st.pressed && jy.y < WIRE_Y + 0.02 ? galvo_I(st.l) / FOM : 0); galvo.update(dt);
      hud.update();
    },
    result() {
      const t = CELLS[0].E / CELLS[1].E; const err = ((st.ratio || 0) - t) / t * 100;
      return { title: 'Potentiometer', rows: [['l₁ (Leclanché)', `${(st.res[0] || 0).toFixed(1)} cm`], ['l₂ (Daniell)', `${(st.res[1] || 0).toFixed(1)} cm`], ['Your E₁/E₂', (st.ratio || 0).toFixed(3)], ['True E₁/E₂', t.toFixed(3)], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`]],
        conclusion: 'At the balance point the cell drives no current, so there is no drop across its internal resistance: a potentiometer measures true e.m.f., which a voltmeter (drawing current) cannot.' };
    },
    dispose() { hud.dispose(); },
  };
}
