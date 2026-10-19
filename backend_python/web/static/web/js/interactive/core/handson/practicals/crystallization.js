// Water of crystallization of blue vitriol by heating to constant mass. The student tares the
// balance and weighs the crucible and lid, spoons in hydrated copper sulphate and weighs again,
// then heats it on a pipe-clay triangle, cools it in the desiccator and weighs, as many times as it
// takes for two weighings to agree. The salt loses its water at a rate that falls as the last,
// most tightly held molecule remains; strong heating at the end decomposes CuSO₄ to black CuO and
// SO₃; a hot crucible weighs light (convection) and one cooled in the open air takes water back.
// x in CuSO₄·xH₂O comes from the student's own weighings.
import { THREE } from '../../engine.js';
import { MAT, mesh } from '../../bio-handson/kit.js';
import { reagentBottle } from '../../bio-handson/props.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits } from '../hud.js';
import { bunsen } from '../burner.js';
import { balance } from '../thermo.js';

const BY = 0.8; const M_CUSO4 = 159.61; const M_H2O = 18.015; const M_CUO = 79.55;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
const V2 = (x, y) => new THREE.Vector2(x, y);

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const ROOM = 25;
  world.add(mesh(new THREE.BoxGeometry(6, 0.02, 2.6), MAT.matte(0x2f3640), [0, 0.01, 0]));
  const bal = balance(); bal.group.scale.setScalar(1.6); bal.group.position.set(-2.1, 0, 0.2); world.add(bal.group); bal.set(1.83);
  const PAN = new THREE.Vector3(-2.1, 0.385, 0.072);
  const porcelain = new THREE.MeshPhysicalMaterial({ color: 0xf6f4ef, roughness: 0.3, clearcoat: 0.7, side: THREE.DoubleSide });
  const cru = new THREE.Group(); world.add(cru);
  cru.add(mesh(new THREE.LatheGeometry([V2(0.001, 0), V2(0.16, 0), V2(0.2, 0.02), V2(0.3, 0.42), V2(0.32, 0.44)], 36), porcelain));
  const saltMat = new THREE.MeshStandardMaterial({ color: 0x2f6fd0, roughness: 0.85 });
  const salt = mesh(new THREE.CylinderGeometry(1, 1, 1, 30), saltMat, null); salt.visible = false; cru.add(salt);
  const lid = mesh(new THREE.SphereGeometry(0.4, 30, 8, 0, Math.PI * 2, 0, 0.6), porcelain, [0.07, 0.36, 0]); cru.add(lid); lid.scale.set(0.85, 0.5, 0.85); lid.rotation.z = -0.12;
  const glowMat = new THREE.MeshBasicMaterial({ color: 0xff5a1a, transparent: true, opacity: 0, depthWrite: false }); const glow = mesh(new THREE.SphereGeometry(0.21, 20, 10), glowMat, [0, 0.08, 0], { cast: false }); cru.add(glow);
  const tri = new THREE.Group(); tri.position.set(0.3, 0, 0); world.add(tri);
  for (let i = 0; i < 3; i++) { const a = i * Math.PI * 2 / 3; const leg = mesh(new THREE.CylinderGeometry(0.025, 0.025, 1.45, 8), MAT.matte(0x2d3436), [Math.cos(a) * 0.36, 0.7, Math.sin(a) * 0.36]); leg.rotation.set(Math.sin(a) * 0.12, 0, -Math.cos(a) * 0.12); tri.add(leg); }
  tri.add(mesh(new THREE.TorusGeometry(0.42, 0.025, 8, 36), MAT.matte(0x2d3436), [0, 1.42, 0]).rotateX(Math.PI / 2));
  for (let i = 0; i < 3; i++) { const a = i * Math.PI * 2 / 3 + Math.PI / 6; const b = mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.62, 10), MAT.matte(0xf1ece0), [Math.cos(a) * 0.17, 1.45, Math.sin(a) * 0.17]); b.rotation.set(0, -a, Math.PI / 2); tri.add(b); }
  const burner = bunsen(ctx.quality); burner.group.position.set(0.3, 0, 0); burner.group.rotation.y = Math.PI / 2; world.add(burner.group);
  const desic = new THREE.Group(); desic.position.set(2.1, 0, 0); world.add(desic);
  desic.add(mesh(new THREE.LatheGeometry([V2(0.001, 0), V2(0.45, 0), V2(0.62, 0.3), V2(0.62, 0.95), V2(0.66, 1.0)], 40), MAT.glass(), null, { cast: false }));
  desic.add(mesh(new THREE.CylinderGeometry(0.5, 0.45, 0.25, 30), MAT.matte(0x2f6fbd), [0, 0.13, 0]));
  desic.add(mesh(new THREE.CylinderGeometry(0.58, 0.58, 0.02, 30), MAT.matte(0xe8e2d0), [0, 0.42, 0]));
  const dlid = mesh(new THREE.SphereGeometry(0.68, 30, 10, 0, Math.PI * 2, 0, 0.9), MAT.glass(), [0, 0.85, 0], { cast: false }); dlid.scale.set(1, 0.5, 1); desic.add(dlid);
  const jar = reagentBottle('CuSO₄·5H₂O', 0x2f6fd0, 'crystals'); jar.position.set(-1.1, 0, 0.85); world.add(jar);
  const SPOTS = { bench: new THREE.Vector3(-1.1, 0.02, -0.3), pan: PAN, tri: new THREE.Vector3(0.3, 1.35, 0), desic: new THREE.Vector3(2.1, 0.45, 0) };

  const st = { at: 'bench', tared: false, m: { cru: null, hyd: null }, hyd: 0, f: 0, decomp: 0, T: ROOM, heat: 0, weighings: [], open: 0, readV: null, cycles: 0 };
  const CRU = 21.48 + Math.round(Math.random() * 300) / 100;
  const mass = () => CRU + st.hyd * (M_CUSO4 / (M_CUSO4 + 5 * M_H2O)) * (1 - st.decomp * (1 - M_CUO / M_CUSO4)) + st.hyd * (5 * M_H2O / (M_CUSO4 + 5 * M_H2O)) * (1 - st.f);
  const col = new THREE.Color(); const blue = new THREE.Color(0x2f6fd0); const white = new THREE.Color(0xf0f1ec); const black = new THREE.Color(0x232020);
  function look() {
    const h = Math.min(0.22, 0.03 + st.hyd * 0.045); salt.visible = st.hyd > 0; salt.scale.set(0.16 + h * 0.45, h, 0.16 + h * 0.45); salt.position.y = 0.02 + h / 2;
    col.copy(blue).lerp(white, Math.min(1, st.f * 1.05)).lerp(black, st.decomp); saltMat.color.copy(col);
  }
  function move(to, done) {
    const from = cru.position.clone(); const target = SPOTS[to]; st.at = 'moving';
    anim.add(0.9, (k) => { cru.position.lerpVectors(from, target, k); cru.position.y += Math.sin(k * Math.PI) * 0.6; }, { done: () => { st.at = to; sfx.play('place'); bal.set(1.83 + (to === 'pan' ? mass() : 0)); if (done) done(); } });
  }
  cru.position.copy(SPOTS.bench);

  function physics(dt) {
    const onFlame = st.at === 'tri' && burner.lit && st.heat > 0;
    const Tt = onFlame ? (st.heat > 1 ? 650 : 320) : ROOM; st.T += (Tt - st.T) * (1 - Math.exp(-dt / (st.at === 'desic' ? 9 : 7)));
    if (st.T > 110 && st.hyd > 0) { const rate = (st.T > 400 ? 0.4 : 0.16) * (st.f < 0.8 ? 1 : 0.3); st.f = Math.min(1, st.f + rate * (1 - st.f + 0.02) * dt); }
    if (st.T > 560 && st.f > 0.97) st.decomp = Math.min(1, st.decomp + 0.012 * dt);
    if (st.at === 'bench' && st.T < 60 && st.f > 0.5) { st.open += dt; st.f = Math.max(0.8, st.f - 0.0015 * dt); }
    glowMat.opacity = Math.max(0, (st.T - 480) / 400) * 0.6;
    if (st.at === 'pan') { const drift = st.T > 40 ? -0.0011 * (st.T - ROOM) : 0; bal.set(1.83 + mass() + drift); }
    look();
  }
  const balChip = hud.chip('ho-chip-read'); balChip.dx = -40; balChip.dy = -60;

  const SHOT_ALL = shot({ pos: [0, 2.6, 4.6], target: [0, 0.8, 0], fit: 5.6, fitH: 2.6 });
  const SHOT_BAL = shot({ pos: [-1.8, 1.9, 2.4], target: [-1.8, 0.4, 0.2], fit: 2.6, fitH: 1.6 });

  function record(label, cb) {
    if (st.at !== 'pan') { ctx.say('Put the crucible on the balance first (tap the balance).', 'hint', 1800); return; }
    if (!bal.settled) { ctx.say('Wait for the reading to settle.', 'hint', 1400); return; }
    if (!st.tared) { ctx.mistake('The balance read 1.83 g with nothing on it. Take the crucible off, press TARE, and weigh again.', 3); return; }
    if (st.T > 40) { ctx.mistake('You weighed it while still hot: rising warm air makes the pan read light, and it drifts. Cool it in the desiccator first.', 3); }
    const v = bal.reading; ui.observe(label, `<b>${v.toFixed(2)} g</b>`); sfx.play('ok'); cb(v);
  }
  const panHandler = (extra) => ({ down(p) {
    if (hits(ctx, bal.tareBtn, p, 30)) { if (st.at === 'pan') { ctx.mistake('Never tare with the crucible on the pan: you would be weighing nothing. Tare the empty pan.', 3); return true; } bal.tare(); st.tared = true; sfx.play('click'); return true; }
    if (extra && extra(p)) return true;
    if (st.at === 'moving') return true;
    if (hits(ctx, bal.group, p, 60, 0.3) && st.at !== 'pan') { move('pan'); return true; }
    if (hits(ctx, tri, p, 70, 1.3) && st.at !== 'tri') { if (st.hyd <= 0) { ctx.say('Weigh the empty crucible first, then add the salt.', 'hint', 1800); return true; } move('tri'); return true; }
    if (hits(ctx, desic, p, 80, 0.5) && st.at !== 'desic') { move('desic'); return true; }
    if (hits(ctx, cru, p, 50, 0.1) && st.at === 'pan') { move('bench'); return true; }
    return false;
  } });

  const steps = [
    {
      title: 'Weigh the empty crucible', text: 'Press <b>TARE</b> with the pan empty, then tap the <b>balance</b> to put the clean, dry crucible and lid on it. Record the mass.', shot: SHOT_BAL, hideBelt: true,
      enter() { hud.actions([{ id: 'rec', label: 'Record mass', primary: true, onClick: () => record('Crucible + lid', (v) => { st.m.cru = v; hud.actions([]); ctx.next(null, 0.3); }) }]); },
      exit() { hud.actions([]); },
      skip() { st.tared = true; bal.tare(); cru.position.copy(SPOTS.pan); st.at = 'pan'; bal.set(1.83 + mass()); st.m.cru = Math.round(CRU * 100) / 100; },
      handler: panHandler(),
    },
    {
      title: 'Add the blue crystals', text: 'With the crucible on the pan, tap the <b>CuSO₄·5H₂O</b> jar to spoon in crystals, a spatula-full at a time, until you have <b>about 2–3 g</b>. Record the mass.', hint: 'Too little and the mass of water is hard to measure; too much and it takes a long time to dry right through.', shot: SHOT_BAL, hideBelt: true,
      enter() { hud.actions([{ id: 'rec', label: 'Record mass', primary: true, onClick: () => {
        if (st.hyd < 1.5) { ctx.say('Add a little more: about 2–3 g.', 'hint', 1800); return; }
        if (st.hyd > 3.6) ctx.say('That is rather a lot; it will need longer heating.', 'hint', 2400);
        record('Crucible + hydrate', (v) => { st.m.hyd = v; hud.actions([]); ctx.next(null, 0.3); });
      } }]); },
      exit() { hud.actions([]); },
      skip() { st.hyd = 2.5 + Math.round(Math.random() * 40) / 100; st.m.hyd = Math.round(mass() * 100) / 100; },
      handler: panHandler((p) => { if (!hits(ctx, jar, p, 50, 0.3)) return false; if (st.at !== 'pan') { ctx.say('Put the crucible on the balance first.', 'hint', 1600); return true; } st.hyd += 0.35 + Math.random() * 0.3; sfx.play('drop'); return true; }),
    },
    {
      title: 'Heat, cool, weigh — to constant mass', text: 'Tap the <b>tripod</b> to put the crucible on the pipe-clay triangle and heat it (lid slightly open): <b>gently</b> first. Then cool it in the <b>desiccator</b> and weigh it. Repeat until two weighings agree within 0.01 g.', hint: 'Strong heating at the end decomposes CuSO₄ to black CuO. Cool in the desiccator, not on the bench, or the white powder takes water back from the air.', shot: SHOT_ALL, hideBelt: true,
      enter() { bar(); },
      exit() { hud.actions([]); burner.setGas(0); },
      skip() { st.f = 1; st.T = ROOM; st.at = 'pan'; cru.position.copy(SPOTS.pan); const v = Math.round(mass() * 100) / 100; st.weighings = [v + 0.03, v, v]; },
      handler: panHandler(),
    },
    {
      title: 'Calculate x', text: 'Mass of water lost, and the mole ratio of water to CuSO₄.', shot: SHOT_ALL, hideBelt: true,
      enter() {
        const m3 = st.weighings[st.weighings.length - 1]; const anh = m3 - st.m.cru; const water = st.m.hyd - m3;
        const x = (water / M_H2O) / (anh / M_CUSO4); st.x = x; st.water = water; st.anh = anh;
        const opts = [[x, 'n(H₂O) ÷ n(CuSO₄)'], [water / anh, 'mass of water ÷ mass of CuSO₄'], [(water / M_H2O) / ((st.m.hyd - st.m.cru) / M_CUSO4), 'divided by the hydrate'], [anh / M_CUSO4 / (water / M_H2O), 'n(CuSO₄) ÷ n(H₂O)']].map(([v, w]) => ({ label: `x = ${v.toFixed(2)}  (${w})`, value: w })).sort(() => Math.random() - 0.5);
        ui.observe('Water lost', `${water.toFixed(2)} g`); ui.observe('Anhydrous CuSO₄', `${anh.toFixed(2)} g`);
        anim.wait(0.8, () => ui.choose(ctx.stage.clientWidth / 2, 40, `Water ${water.toFixed(2)} g (M 18.0), CuSO₄ ${anh.toFixed(2)} g (M 159.6). x =`, opts, (v) => {
          if (v !== 'n(H₂O) ÷ n(CuSO₄)') ctx.mistake('x is a mole ratio: (mass of water ÷ 18.0) ÷ (mass of anhydrous CuSO₄ ÷ 159.6).', 3);
          ui.observe('x', `<b>${x.toFixed(2)}</b> ≈ ${Math.round(x)}`); ctx.next(`CuSO₄·${Math.round(x)}H₂O.`, 1.2);
        }));
      },
      exit() { ui.clearChooser(); },
    },
  ];
  function bar() {
    hud.actions([
      { id: 'gentle', label: 'Heat gently', onClick: () => setHeat(1) }, { id: 'strong', label: 'Heat strongly', onClick: () => setHeat(2) }, { id: 'off', label: 'Burner off', onClick: () => setHeat(0) },
      { id: 'rec', label: `Weigh (${st.weighings.length})`, primary: true, onClick: () => record(`Weighing ${st.weighings.length + 1}`, (v) => {
        st.weighings.push(v); hud.relabel('rec', `Weigh (${st.weighings.length})`);
        const n = st.weighings.length; if (n >= 2 && Math.abs(st.weighings[n - 1] - st.weighings[n - 2]) <= 0.01) {
          if (st.f < 0.97) ctx.mistake('Two weighings agree, but the salt still has water in it: blue patches remain. Each heating must be long enough to change the mass.', 2);
          if (st.decomp > 0.05) ctx.say('The powder has turned grey-black in places: CuO. Your mass is too low.', 'hint', 3000);
          hud.actions([]); ctx.next('Constant mass.', 0.8);
        } else if (n >= 2) ctx.say(`Changed by ${(st.weighings[n - 2] - st.weighings[n - 1]).toFixed(2)} g since last time: heat, cool and weigh again.`, 'info', 2600);
      }) },
    ]);
  }
  function setHeat(h) {
    if (h > 0 && st.at !== 'tri') { ctx.say('Put the crucible on the triangle first (tap the tripod).', 'hint', 1800); return; }
    st.heat = h; if (h > 0) { burner.setGas(1); burner.light(); burner.setAir(h > 1 ? 1 : 0.55); sfx.play('whoosh'); } else burner.setGas(0);
    if (h === 2 && st.f < 0.5) ctx.say('Strong heating so early makes the crystals spit out of the crucible. Start gently.', 'hint', 2600);
  }

  ctx.debug = { st, mass, move, setHeat };
  return {
    tools: [], steps,
    update(dt, t) {
      physics(dt); bal.update(dt); burner.update(dt, t);
      bal.display.getWorldPosition(balChip.at); balChip.set(`<b>${bal.shown.toFixed(2)}</b> g`); balChip.show(true);
      if (st.at === 'tri' && st.heat > 0 && st.f < 0.97 && Math.random() < dt * 4) { const p = cru.position.clone(); p.y += 0.5; ctx.fx.burst(p.add(new THREE.Vector3(0, BY, 0)), 0xffffff, 1, 0.06, p.y - 0.2); }
      hud.update();
    },
    result() {
      const err = ((st.x || 0) - 5) / 5 * 100;
      return {
        title: 'Water of crystallization',
        rows: [['Crucible', `${(st.m.cru || 0).toFixed(2)} g`], ['+ hydrate', `${(st.m.hyd || 0).toFixed(2)} g`], ['Weighings', st.weighings.map((w) => w.toFixed(2)).join(', ')], ['Water lost', `${(st.water || 0).toFixed(2)} g`], ['x', `${(st.x || 0).toFixed(2)}`], ['Formula', 'CuSO₄·5H₂O'], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`]],
        conclusion: `Heating to constant mass drives off all the water: x ≈ ${(st.x || 0).toFixed(1)}, so the crystals are CuSO₄·5H₂O. A result below 5 means water was left (stopped too soon, or the powder took water back while cooling in air); above 5 means CuSO₄ itself decomposed (strong heating) or crystals spat out.`,
      };
    },
    dispose() { hud.dispose(); },
  };
}
