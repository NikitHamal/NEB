// Specific heat capacity of a solid by the method of mixtures. The student tares the balance and
// weighs the copper calorimeter with its stirrer, pours in water (held press = pouring) and weighs
// again, weighs the metal, hangs it in the steam heater over a lit burner and waits for it to
// reach steam temperature, reads θ₂ and the water's θ₁, carries the hot metal across (it cools in
// the air while carried), stirs and catches the peak θ. Heat flows by the real exchange equations
// (stirring speeds mixing, the jacket leaks slowly), and c is computed from the student's readings.
import { THREE } from '../../engine.js';
import { MAT, mesh, canvasTexture } from '../../bio-handson/kit.js';
import { tripodWithGauze } from '../../lab3d-kit.js';
import { sfx } from '../../bio-handson/sound.js';
import { createHud, hits, screenDist } from '../hud.js';
import { beaker } from '../glass.js';
import { bunsen } from '../burner.js';
import { thermometer, thermoReader, calorimeter, balance, steamPuffs } from '../thermo.js';

const BY = 0.8; const CW = 4.18; const CC = 0.385;
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });
const METALS = { Al: { name: 'Aluminium', c: 0.900, rho: 2.70, color: 0xd5d9de }, Fe: { name: 'Iron', c: 0.450, rho: 7.87, color: 0x7d8288 }, Cu: { name: 'Copper', c: 0.385, rho: 8.96, color: 0xc77b4a } };

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const key = ['Al', 'Fe', 'Cu'][Math.floor(Math.random() * 3)]; const MET = METALS[key];
  const mS = Math.round(Math.PI * 1.25 * 1.25 * 6 * MET.rho * 100) / 100 + Math.round(Math.random() * 300) / 100;
  const mC = Math.round((88 + Math.random() * 12) * 100) / 100; const ROOM = Math.round((21 + Math.random() * 5) * 10) / 10;
  const TB = Math.round((98.6 + Math.random() * 1.2) * 10) / 10; const PAPER = 3.47;

  const bal = balance(); bal.group.position.set(-2.9, 0, 0.35); bal.group.scale.setScalar(1.6); world.add(bal.group); bal.set(PAPER);
  const cal = calorimeter(); cal.group.position.set(-0.8, 0, 0); world.add(cal.group);
  const th1 = thermometer({ min: 0, max: 50, div: 0.2, len: 2.5 }); th1.group.position.set(-0.12, 0.12, 0.05); cal.group.add(th1.group); cal.lid.visible = false; th1.set(ROOM, true);
  const rd1 = thermoReader(ctx, th1);
  const bk = beaker(0, 0xd6ebf7); bk.group.scale.setScalar(1.3); bk.group.position.set(-0.2, 0, 1.2); world.add(bk.group); const BKS = 1.3 ** 3; bk.setVolume(380 / BKS);
  const metal = new THREE.Group(); metal.position.set(0.75, 0, 1.1); world.add(metal);
  metal.add(mesh(new THREE.CylinderGeometry(0.125, 0.125, 0.6, 28), new THREE.MeshStandardMaterial({ color: MET.color, metalness: 1, roughness: 0.35 }), [0, 0.3, 0]));
  metal.add(mesh(new THREE.TorusGeometry(0.04, 0.008, 6, 12), MAT.steel(), [0, 0.64, 0]));
  const thread = mesh(new THREE.CylinderGeometry(0.004, 0.004, 1, 5), MAT.matte(0xf5f0e1), [0, 1.18, 0], { cast: false }); thread.visible = false; metal.add(thread);
  const tri = tripodWithGauze(); tri.position.set(1.9, 0, 0); world.add(tri);
  const burner = bunsen(ctx.quality); burner.group.position.set(1.9, 0, 0); burner.group.rotation.y = Math.PI / 2; world.add(burner.group); burner.setAir(0.85);
  const copper = new THREE.MeshStandardMaterial({ color: 0xc8794a, metalness: 1, roughness: 0.35 });
  const heater = new THREE.Group(); heater.position.set(1.9, 1.47, 0); world.add(heater);
  heater.add(mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.7, 32), copper, [0, 0.35, 0]));
  heater.add(mesh(new THREE.CylinderGeometry(0.3, 0.3, 1.15, 32), MAT.steel(), [0, 1.27, 0]));
  heater.add(mesh(new THREE.CylinderGeometry(0.17, 0.15, 0.12, 20), MAT.matte(0x9a6b3e), [0, 1.9, 0]));
  const outlet = mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.4, 10), MAT.steel(), [0.42, 0.95, 0]); outlet.rotation.z = Math.PI / 2 - 0.4; heater.add(outlet);
  const th2 = thermometer({ min: -10, max: 110, div: 1, len: 2.4 }); th2.group.position.set(0.08, 0.9, 0.0); heater.add(th2.group); th2.set(ROOM, true);
  const rd2 = thermoReader(ctx, th2);
  const steam = steamPuffs(world, 26);

  const balChip = hud.chip('ho-chip-read'); balChip.dx = -40; balChip.dy = -60; balChip.show(true);
  const st = { tared: false, mCup: null, mCupW: null, mMetal: null, water: 0, pouring: false, lit: false, Th: ROOM, Ts: ROOM, Tw: ROOM, inHeater: false, inCal: false, carry: false, carryT: 0, stir: 0, peak: ROOM, t1: null, t2: null, t: null, readV: null, onPan: null, spilled: 0 };
  const Cs = () => mS * MET.c; const Cw = () => (st.water + st.spilled * 0) * CW + mC * CC;

  // ---- weighing ----
  const PAN = new THREE.Vector3();
  function putOnPan(what) {
    PAN.set(-2.9, 0.384, 0.222);
    if (what === 'cup') { const from = cal.cup.position.clone(); const to = PAN.clone().sub(cal.group.position); anim.add(0.9, (k) => { cal.cup.position.lerpVectors(from, to, k); cal.cup.position.y += Math.sin(k * Math.PI) * 0.6; }, { done: () => { sfx.play('place'); bal.set(PAPER * !st.tared + mC + st.water); } }); }
    else { const from = metal.position.clone(); anim.add(0.9, (k) => { metal.position.lerpVectors(from, PAN, k); metal.position.y += Math.sin(k * Math.PI) * 0.6; }, { done: () => { sfx.play('place'); bal.set(PAPER * !st.tared + mS); } }); }
    st.onPan = what; if (what === 'cup') th1.group.visible = false;
  }
  function takeOff(done) {
    const what = st.onPan; st.onPan = null; bal.set(st.tared ? 0 : PAPER);
    if (what === 'cup') { const from = cal.cup.position.clone(); anim.add(0.9, (k) => { cal.cup.position.lerpVectors(from, new THREE.Vector3(0, 0, 0), k); cal.cup.position.y += Math.sin(k * Math.PI) * 0.6; }, { done: () => { th1.group.visible = true; if (done) done(); } }); }
    else if (what === 'metal') { const from = metal.position.clone(); anim.add(0.9, (k) => { metal.position.lerpVectors(from, new THREE.Vector3(0.75, 0, 1.1), k); metal.position.y += Math.sin(k * Math.PI) * 0.6; }, { done }); }
    else if (done) done();
  }
  function weighStep(title, text, what, keyName, label) {
    return {
      title, text, hint: 'Press TARE with the pan empty so it reads 0.00 g; then put the object on, wait for the reading to settle and record it.', shot: SHOT_BAL, hideBelt: true,
      enter() { anim.wait(0.4, () => ctx.rig.go(SHOT_BAL, 0.6)); hud.actions([{ id: 'rec', label: 'Record mass', primary: true, onClick: () => {
        if (st.onPan !== what) { ctx.say('Put it on the pan first (tap it).', 'hint', 1800); return; }
        if (!bal.settled) { ctx.say('Wait for the display to settle.', 'hint', 1500); return; }
        if (!st.tared) { ctx.mistake(`The balance read ${PAPER.toFixed(2)} g before anything was on it (a scrap of paper). Take it off, press TARE, and weigh again.`, 3); takeOff(); return; }
        st[keyName] = bal.reading; ui.observe(label, `<b>${bal.reading.toFixed(2)} g</b>`); hud.actions([]); takeOff(() => ctx.next(null, 0.3));
      } }]); },
      exit() { hud.actions([]); },
      skip() { st.tared = true; bal.tare(); st[keyName] = what === 'cup' ? Math.round((mC + st.water) * 100) / 100 : mS; },
      handler: { down(p) {
        if (hits(ctx, bal.tareBtn, p, 30)) { bal.tare(); st.tared = st.onPan === null; sfx.play('click'); if (st.onPan) ctx.mistake('You tared with the object on the pan: the balance now reads 0 for it. Take it off and tare an empty pan.', 3); return true; }
        if (st.onPan) return false;
        if (what === 'cup' && hits(ctx, cal.cup, p, 60, 0.5)) { putOnPan('cup'); return true; }
        if (what === 'metal' && hits(ctx, metal, p, 60, 0.3)) { putOnPan('metal'); return true; }
        return false;
      } },
    };
  }

  // ---- pouring water ----
  const stream = mesh(new THREE.CylinderGeometry(0.018, 0.012, 1, 8), MAT.liquid(0xd6ebf7, 0.7), null, { cast: false }); stream.visible = false; world.add(stream);
  const BK_HOME = new THREE.Vector3(-0.2, 0, 1.2); const BK_POUR = new THREE.Vector3(-0.55, 1.3, 0.05);
  function pourStart() { if (st.pouring) return; st.pouring = true; anim.add(0.6, (k) => { bk.group.position.lerpVectors(BK_HOME, BK_POUR, k); bk.group.rotation.z = 1.9 * k; }, { id: 'bk' }); }
  function pourStop() { if (!st.pouring) return; st.pouring = false; stream.visible = false; const from = bk.group.position.clone(); const r0 = bk.group.rotation.z; anim.add(0.6, (k) => { bk.group.position.lerpVectors(from, BK_HOME, k); bk.group.rotation.z = r0 * (1 - k); }, { id: 'bk' }); }
  function pourUpdate(dt) {
    if (!st.pouring || anim.busy('bk')) return;
    const flow = 32 * dt; const left = bk.volume * BKS; if (left <= 1) { pourStop(); return; }
    const f = Math.min(flow, left); bk.setVolume((left - f) / BKS); st.water += f; cal.setWater(st.water);
    const top = cal.waterTop(st.water) + 0; const lipY = BK_POUR.y + 0.85; stream.visible = true; stream.scale.y = lipY - top; stream.position.set(-0.8 + 0.05, (lipY + top) / 2, 0.05);
    if (Math.random() < dt * 4) sfx.play('pour');
  }

  // ---- heating, carrying, mixing ----
  const tmp = new THREE.Vector3();
  function physics(dt) {
    const heating = burner.lit;
    const target = heating ? TB + 6 : ROOM;
    st.Th += (target - st.Th) * (1 - Math.exp(-dt / (heating ? 18 : 120))); if (st.Th > TB) st.Th = TB;
    if (st.inHeater) st.Ts += (st.Th - st.Ts) * (1 - Math.exp(-dt / 14));
    else if (st.carry) st.Ts -= (st.Ts - ROOM) * dt / 600;
    if (st.inCal) {
      const K = (st.stir > 0 ? 1 / 5 : 1 / 22) * (Cs() * Cw()) / (Cs() + Cw());
      const q = K * (st.Ts - st.Tw) * dt; st.Ts -= q / Cs(); st.Tw += q / Cw();
      st.Tw -= (st.Tw - ROOM) * dt / 1800;
    }
    st.stir = Math.max(0, st.stir - dt);
    th1.set(st.Tw); th2.set(heating || st.Th > ROOM + 1 ? st.Th : ROOM);
    th1.update(dt, st.stir > 0 ? 1.2 : 3.5); th2.update(dt, 3);
    st.peak = Math.max(st.peak, th1.reading);
    if (st.Th >= TB - 0.05) { outlet.getWorldPosition(tmp); tmp.x += 0.2; tmp.y += 0.08; world.worldToLocal(tmp); steam.emit(tmp, 7, dt, 0.04, 0.5); }
    steam.update(dt);
  }
  const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -0.05); const hit = new THREE.Vector3();
  function hang() {
    st.inHeater = true; metal.position.set(1.9, 1.47 + 1.0, 0); thread.visible = true; thread.scale.y = 0.6; thread.position.y = 0.95; metal.visible = false; sfx.play('place');
  }

  // ---- reading a thermometer ----
  function readStep(which) {
    const th = which === 1 ? th1 : th2; const rd = which === 1 ? rd1 : rd2;
    return (cb) => {
      st.readV = null;
      const at = new THREE.Vector3(); th.group.getWorldPosition(at); world.worldToLocal(at); const y = at.y + th.yOf(th.reading);
      ctx.rig.go(shot({ pos: [at.x + 0.1, y + 0.02, at.z + 0.6], target: [at.x, y, at.z], fov: 22, limits: { yaw: 0.3, pitch: 0.2, zMin: 0.6, zMax: 1.5 } }), 1.0);
      hud.actions([{ id: 'rec', label: 'Record', primary: true, disabled: true, onClick: () => { rd.hide(); hud.actions([]); cb(st.readV, st.readTruth); } }]);
      readHandler = { down() { const v = rd.tap(); if (v === null) return false; st.readV = v; st.readTruth = th.reading; hud.relabel('rec', `Record ${v.toFixed(1)} °C`); hud.enable('rec', true); sfx.play('click'); return true; } };
    };
  }
  let readHandler = null;
  const checkTemp = (v, truth, half) => { if (Math.abs(v - truth) > half + 0.06) { ctx.mistake(`The mercury stands at ${truth.toFixed(1)} °C, not ${v.toFixed(1)} °C. Read the top of the column with your eye level with it.`, 3); return false; } return true; };

  const SHOT_ALL = shot({ pos: [-0.2, 3.3, 6.2], target: [-0.2, 1.1, 0.2], fit: 6.4, fitH: 3.4 });
  const SHOT_BAL = shot({ pos: [-2.4, 2.3, 3.2], target: [-1.9, 0.5, 0.2], fit: 3.4, fitH: 2.2 });
  const SHOT_CAL = shot({ pos: [-0.6, 2.6, 3.0], target: [-0.6, 1.0, 0.3], fit: 2.6, fitH: 2.8 });
  const SHOT_HEAT = shot({ pos: [1.4, 2.6, 4.4], target: [1.6, 1.8, 0], fit: 2.8, fitH: 3.8 });
  const SHOT_MIX = shot({ pos: [0.6, 2.8, 4.4], target: [0.5, 1.4, 0], fit: 3.8, fitH: 3.0 });

  const steps = [
    weighStep('Weigh the calorimeter', 'Tare the balance (tap <b>TARE</b>), then tap the <b>copper calorimeter</b> (with its stirrer) to put it on the pan, and record its mass.', 'cup', 'mCup', 'Calorimeter + stirrer'),
    {
      title: 'Add water', text: 'Press and <b>hold</b> on the <b>beaker</b> to pour water into the calorimeter; let go to stop. About half full: enough to cover the metal, not so much that it splashes out.', hint: 'Between about 150 and 250 mL.', shot: SHOT_CAL, hideBelt: true,
      enter() { hud.actions([{ id: 'ok', label: 'Enough water', primary: true, onClick: () => {
        if (st.water < 140) { ctx.say('Not enough to cover the metal yet.', 'hint', 1800); return; }
        if (st.water > 280) ctx.mistake('Too full: when the metal goes in, water will splash over the rim and the mass of water you measured is no longer in the calorimeter. And the more water, the smaller the rise you have to read.', 2);
        hud.actions([]); ctx.next(null, 0.3);
      } }]); },
      exit() { hud.actions([]); pourStop(); },
      skip() { st.water = 200; cal.setWater(200); bk.setVolume(180 / BKS); },
      update(dt) { pourUpdate(dt); },
      handler: { down(p) { if (!hits(ctx, bk.group, p, 60, 0.4)) return false; pourStart(); return true; }, up() { pourStop(); }, cancel() { pourStop(); } },
    },
    weighStep('Weigh calorimeter + water', 'Weigh the calorimeter again, now with the water. The difference is the mass of water.', 'cup', 'mCupW', 'Calorimeter + water'),
    weighStep('Weigh the metal', 'Tap the <b>metal cylinder</b> to put it on the pan, and record its mass.', 'metal', 'mMetal', 'Metal'),
    {
      title: 'Heat the metal in steam', text: 'Tap the metal to hang it inside the <b>steam heater</b>, then tap the <b>burner</b> to light it. Wait until steam comes out steadily and the heater thermometer stops rising — the metal needs several minutes to reach the steam\'s temperature.', hint: 'The thermometer in the heater reads the steam. Give the metal time after it steadies.', shot: SHOT_HEAT, hideBelt: true,
      enter() { st.readyT = 0; },
      update(dt) { if (st.Th >= TB - 0.05 && st.inHeater) st.readyT += dt; if (st.readyT > 12 && !st.saidReady) { st.saidReady = true; hud.actions([{ id: 'rd', label: 'Read θ₂', primary: true, onClick: () => readStep(2)((v, truth) => { if (!checkTemp(v, truth, 0.5)) { ctx.rig.go(SHOT_HEAT, 0.8); st.saidReady = false; readHandler = null; return; } st.t2 = v; ui.observe('θ₂ (steam)', `<b>${v.toFixed(1)} °C</b>`); ctx.next(null, 0.3); }) }]); } },
      exit() { hud.actions([]); readHandler = null; },
      skip() { hang(); burner.setGas(1); burner.light(); st.Th = TB; st.Ts = TB; th2.set(TB, true); st.t2 = TB; },
      handler: { down(p) {
        if (readHandler) return readHandler.down(p);
        if (!st.inHeater && hits(ctx, metal, p, 60, 0.3)) { hang(); return true; }
        if (!burner.lit && hits(ctx, burner.group, p, 70, 0.6)) { burner.setGas(1); burner.light(); sfx.play('whoosh'); return true; }
        return false;
      } },
    },
    {
      title: 'Read θ₁', text: 'Stir the water gently (tap the <b>stirrer</b>), then read the calorimeter thermometer.', shot: SHOT_CAL, hideBelt: true,
      enter() { readHandler = null; hud.actions([{ id: 'rd', label: 'Read θ₁', primary: true, onClick: go1 }]); function go1() { readStep(1)((v, truth) => { if (!checkTemp(v, truth, 0.1)) { ctx.rig.go(SHOT_CAL, 0.8); hud.actions([{ id: 'rd', label: 'Read θ₁', primary: true, onClick: go1 }]); readHandler = null; return; } st.t1 = v; ui.observe('θ₁ (water)', `<b>${v.toFixed(1)} °C</b>`); ctx.next(null, 0.3); }); } },
      exit() { hud.actions([]); readHandler = null; },
      skip() { st.t1 = Math.round(ROOM * 10) / 10; },
      handler: { down(p) { if (readHandler) return readHandler.down(p); if (hits(ctx, cal.stirrer, p, 50, 0.9)) { stirOnce(); return true; } return false; } },
    },
    {
      title: 'Transfer quickly and stir', text: 'Drag the hot metal <b>out of the heater</b> and drop it into the calorimeter — <b>quickly</b>, every second in the air loses heat — close the lid and stir (tap the stirrer, or hold <b>Stir</b>). Watch the thermometer rise and catch its <b>highest</b> reading.', hint: 'Keep stirring. When the column stops rising and starts to creep down, the peak has passed: read the highest value.', shot: SHOT_MIX, hideBelt: true,
      enter() { st.carryT = 0; },
      exit() { hud.actions([]); readHandler = null; },
      skip() { st.inHeater = false; st.inCal = true; cal.lid.visible = true; metal.visible = true; metal.position.set(cal.group.position.x + 0.1, 0.06, 0); const T = (Cs() * st.Ts + Cw() * st.Tw) / (Cs() + Cw()); st.Ts = st.Tw = T; th1.set(T, true); st.peak = T; st.t = Math.round(T * 10) / 10; },
      update(dt) { if (st.carry) st.carryT += dt; },
      handler: {
        down(p) {
          if (readHandler) return readHandler.down(p);
          if (st.inCal) { if (hits(ctx, cal.stirrer, p, 60, 0.9)) { stirOnce(); return true; } return false; }
          if (st.inHeater && hits(ctx, heater, p, 80, 1.3)) { st.inHeater = false; st.carry = true; metal.visible = true; thread.visible = true; sfx.play('pick'); return true; }
          return false;
        },
        move() { if (!st.carry) return; if (!ctx.input.ptr.ray.intersectPlane(plane, hit)) return; world.worldToLocal(hit); metal.position.set(hit.x, Math.max(1.3, hit.y - 0.3), 0); },
        up() {
          if (!st.carry) return;
          if (Math.abs(metal.position.x - cal.group.position.x) < 0.45) {
            st.carry = false; st.inCal = true; thread.visible = false; const y0 = metal.position.y; anim.add(0.4, (k) => { metal.position.set(cal.group.position.x + 0.1, y0 + (0.06 - y0) * k, 0); }, { done: () => { sfx.play('drop'); cal.lid.visible = true; } });
            if (st.carryT > 6) ctx.mistake(`That took ${st.carryT.toFixed(0)} s: the metal was cooling all the while. Carry it straight across.`, 2);
            hud.actions([{ id: 'stir', label: 'Stir', onClick: stirOnce }, { id: 'rd', label: 'Read θ (peak)', primary: true, onClick: readPeak }]);
          }
        },
        cancel() {},
      },
    },
    {
      title: 'Specific heat of the metal', text: 'Heat lost by the metal = heat gained by the water and the calorimeter.', shot: SHOT_ALL, hideBelt: true,
      enter() {
        const mw = st.mCupW - st.mCup; st.mw = mw; const dW = st.t - st.t1; const dS = st.t2 - st.t;
        const c = (mw * CW + st.mCup * CC) * dW / (st.mMetal * dS); st.c = c;
        const opts = [[c, 'with the calorimeter'], [(mw * CW) * dW / (st.mMetal * dS), 'water only'], [(mw * CW + st.mCup * CC) * dS / (st.mMetal * dW), 'temperature changes swapped'], [(mw * CW + st.mCup * CC) * dW / (st.mMetal * (st.t2 - st.t1)), 'using θ₂ − θ₁']]
          .map(([v, w]) => ({ label: `${v.toFixed(3)} J g⁻¹ °C⁻¹  (${w})`, value: w })).sort(() => Math.random() - 0.5);
        ui.observe('Water', `${mw.toFixed(2)} g`);
        anim.wait(0.8, () => ui.choose(ctx.stage.clientWidth / 2, 40, `m_w = ${mw.toFixed(2)} g, m_c = ${st.mCup.toFixed(2)} g, m_s = ${st.mMetal.toFixed(2)} g, θ₁ = ${st.t1.toFixed(1)}, θ₂ = ${st.t2.toFixed(1)}, θ = ${st.t.toFixed(1)} °C. c_s =`, opts, (v) => {
          if (v !== 'with the calorimeter') ctx.mistake('c_s = (m_w c_w + m_c c_c)(θ − θ₁) / m_s(θ₂ − θ): the copper calorimeter warms up too, and the metal cools from θ₂ to θ.', 3);
          ui.observe('c (metal)', `<b>${c.toFixed(3)} J g⁻¹ °C⁻¹</b>`);
          anim.wait(0.6, () => ui.choose(ctx.stage.clientWidth / 2, 40, 'Which metal is it? (Al 0.900, Fe 0.450, Cu 0.385)', Object.keys(METALS).map((k) => ({ label: METALS[k].name, value: k })), (m) => {
            const best = Object.keys(METALS).reduce((a, k) => (Math.abs(METALS[k].c - c) < Math.abs(METALS[a].c - c) ? k : a), 'Al');
            if (m !== best) ctx.mistake(`${c.toFixed(3)} is closest to ${METALS[best].name.toLowerCase()} (${METALS[best].c}).`, 2);
            ctx.next(`${METALS[best].name}.`, 1.2);
          }));
        }));
      },
      exit() { ui.clearChooser(); },
    },
  ];
  function stirOnce() { st.stir = 2.5; sfx.play('glass'); anim.add(0.5, (k) => { cal.stirrer.position.y = Math.sin(k * Math.PI) * 0.35; }, { id: 'stir' }); }
  function readPeak() {
    readStep(1)((v, truth) => {
      if (!checkTemp(v, truth, 0.1)) { ctx.rig.go(SHOT_MIX, 0.8); hud.actions([{ id: 'stir', label: 'Stir', onClick: stirOnce }, { id: 'rd', label: 'Read θ (peak)', primary: true, onClick: readPeak }]); readHandler = null; return; }
      const eq = (Cs() * st.Ts + Cw() * st.Tw) / (Cs() + Cw());
      if (st.peak - v > 0.25 && st.Ts - st.Tw < 0.5) ctx.mistake(`The column has already fallen from its highest, ${st.peak.toFixed(1)} °C. The mixture temperature is the peak reading.`, 3);
      else if (st.Ts - st.Tw > 1 && eq - v > 0.3) { ctx.say('Still rising: keep stirring and wait for the highest reading.', 'hint', 2200); ctx.rig.go(SHOT_MIX, 0.8); hud.actions([{ id: 'stir', label: 'Stir', onClick: stirOnce }, { id: 'rd', label: 'Read θ (peak)', primary: true, onClick: readPeak }]); readHandler = null; return; }
      st.t = v; ui.observe('θ (mixture)', `<b>${v.toFixed(1)} °C</b>`); ctx.next(null, 0.3);
    });
  }

  ctx.debug = { st, key, mS, TB, ROOM, Cs, Cw };
  return {
    tools: [], steps,
    update(dt, t) { physics(dt); bal.update(dt); bal.display.getWorldPosition(balChip.at); balChip.set(`<b>${bal.shown.toFixed(2)}</b> g`); balChip.show(ctx.stepIndex >= 0 && ctx.stepIndex <= 3); burner.update(dt, t); hud.update(); },
    result() {
      const c = st.c || 0; const err = (c - MET.c) / MET.c * 100;
      return {
        title: `Specific heat: ${MET.name.toLowerCase()}`,
        rows: [['m_c, m_w, m_s', `${(st.mCup || 0).toFixed(2)}, ${(st.mw || 0).toFixed(2)}, ${(st.mMetal || 0).toFixed(2)} g`], ['θ₁, θ₂, θ', `${(st.t1 || 0).toFixed(1)}, ${(st.t2 || 0).toFixed(1)}, ${(st.t || 0).toFixed(1)} °C`], ['Your c', `${c.toFixed(3)} J g⁻¹ °C⁻¹`], [`${MET.name} (tables)`, `${MET.c.toFixed(3)} J g⁻¹ °C⁻¹`], ['Error', `${err >= 0 ? '+' : ''}${err.toFixed(1)} %`]],
        conclusion: `Heat lost by the ${MET.name.toLowerCase()} = heat gained by water and calorimeter. The rise was only ${((st.t || 0) - (st.t1 || 0)).toFixed(1)} °C, so 0.1 °C on the thermometer is about ${(10 / Math.max(0.1, (st.t || 0) - (st.t1 || 0))).toFixed(1)} % of the result. Heat lost while carrying the metal and from the calorimeter makes θ low and c low; quick transfer, a lid, lagging and stirring keep these small.`,
      };
    },
    dispose() { hud.dispose(); steam.dispose(); },
  };
}
