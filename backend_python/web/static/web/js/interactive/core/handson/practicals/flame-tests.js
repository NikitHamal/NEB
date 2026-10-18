// Flame tests with a nichrome wire. The student lights a Bunsen burner and opens its air hole,
// cleans the wire (dip in concentrated HCl, heat, repeat until the flame shows nothing), then
// tests three unknown salts: dip in acid, touch the salt, hold the loop in the hottest part of the
// flame and name the ion from the colour, a cobalt-blue glass or the line spectrum in a hand
// spectroscope. The wire carries what it touched: sodium from fingers masks potassium, and a wire
// not cleaned between samples shows both. Colours come from each metal's real emission lines.
import { THREE } from '../../engine.js';
import { watchGlass } from '../../bio-handson/props.js';
import { MAT, mesh, clamp, canvasTexture, SpringV3 } from '../../bio-handson/kit.js';
import { sfx, noise, tone } from '../../bio-handson/sound.js';
import { bunsen } from '../burner.js';
import { LINES, emissionColour, glowColour, drawSpectrum } from '../flame.js';
import { createHud, hits, screenDist } from '../hud.js';

sfx.register('hiss', () => noise(0.9, { freq: 5200, q: 0.6, gain: 0.05 }));
sfx.register('whoosh', () => { noise(0.5, { freq: 300, q: 0.7, gain: 0.25, type: 'lowpass', sweep: 3 }); tone(90, 0.4, { gain: 0.06, slide: 1.6 }); });
sfx.register('sizzle', () => noise(0.35, { freq: 6500, q: 1.5, gain: 0.08, sweep: 0.6 }));

const BY = 0.8;
const ROW_Z = 0.45;
const SENS = { Na: 4, K: 0.9, Li: 1.4, Ca: 1, Sr: 1.2, Ba: 0.9, Cu: 0.85 };
const CANDIDATES = ['Na', 'K', 'Li', 'Ca', 'Sr', 'Ba', 'Cu'];
const shot = (o) => Object.assign({}, o, { pos: [o.pos[0], o.pos[1] + BY, o.pos[2]], target: [o.target[0], o.target[1] + BY, o.target[2]] });

function tagTex(text, sub) {
  return canvasTexture(`ho-tag:${text}:${sub}`, 256, 128, (g, w, h) => {
    g.fillStyle = '#fffdf5'; g.fillRect(0, 0, w, h); g.fillStyle = '#0f766e'; g.fillRect(0, 0, w, 14);
    g.fillStyle = '#111827'; g.font = '800 46px system-ui, sans-serif'; g.textAlign = 'center'; g.fillText(text, w / 2, 70);
    g.font = '600 22px system-ui, sans-serif'; g.fillStyle = '#475569'; g.fillText(sub, w / 2, 104);
  });
}

export function create(ctx) {
  const { world, anim, ui } = ctx;
  const hud = createHud(ctx);
  const pool = CANDIDATES.slice().sort(() => Math.random() - 0.5);
  if (!pool.slice(0, 3).includes('K') && Math.random() < 0.5) pool[2] = 'K';
  const unknowns = pool.slice(0, 3);
  const names = ['A', 'B', 'C'];

  const burner = bunsen(ctx.quality); burner.group.position.set(-0.2, 0, ROW_Z); world.add(burner.group);
  const acidGlass = watchGlass(0xf1f7ef, 0.55); acidGlass.position.set(-1.45, 0.02, ROW_Z); world.add(acidGlass);
  const glasses = unknowns.map((ion, i) => {
    const wg = watchGlass(null); wg.position.set(0.75 + i * 0.6, 0.02, ROW_Z); world.add(wg);
    const salt = mesh(new THREE.SphereGeometry(0.12, 18, 8, 0, Math.PI * 2, 0, Math.PI / 2), MAT.matte(ion === 'Cu' ? 0x5eead4 : 0xf8fafc), [0, 0.012, 0]);
    salt.scale.set(1, 0.32, 1); wg.add(salt);
    return wg;
  });
  [[acidGlass, 'HCl', 'conc.'], ...glasses.map((g, i) => [g, names[i], 'unknown'])].forEach(([g, t, s]) => {
    const tag = mesh(new THREE.PlaneGeometry(0.26, 0.13), new THREE.MeshStandardMaterial({ map: tagTex(t, s), roughness: 0.8 }), [0, 0.006, 0.52]);
    tag.rotation.x = -Math.PI / 2 + 0.25; g.add(tag);
  });
  const tray = mesh(new THREE.BoxGeometry(4.6, 0.02, 1.0), MAT.matte(0x2f3640), [0.05, 0.01, ROW_Z]); world.add(tray);

  // ---- the wire: a glass rod handle with a nichrome loop ----
  const wire = new THREE.Group(); world.add(wire);
  const nichrome = new THREE.MeshStandardMaterial({ color: 0x9ca3af, metalness: 0.9, roughness: 0.35, emissive: 0x000000 });
  const loop = mesh(new THREE.TorusGeometry(0.03, 0.006, 6, 18), nichrome); loop.rotation.y = Math.PI / 2; wire.add(loop);
  const wDir = new THREE.Vector3(0.55, 0.8, 0.25).normalize();
  const w1 = mesh(new THREE.CylinderGeometry(0.005, 0.005, 0.55, 6), nichrome); w1.position.copy(wDir).multiplyScalar(0.3); w1.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), wDir); wire.add(w1);
  const rodMat = new THREE.MeshPhysicalMaterial({ color: 0xe0f2fe, roughness: 0.08, transparent: true, opacity: 0.55, clearcoat: 1 });
  const rod = mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.3, 12), rodMat, null, { cast: false }); rod.position.copy(wDir).multiplyScalar(0.57 + 0.65); rod.quaternion.copy(w1.quaternion); wire.add(rod);
  const salted = mesh(new THREE.SphereGeometry(0.022, 10, 8), MAT.matte(0xf8fafc), [0, 0, 0]); salted.visible = false; wire.add(salted);
  const tipSpring = new SpringV3(260, 0.9); const REST = new THREE.Vector3(-0.9, 0.95, ROW_Z); tipSpring.snap(REST); wire.position.copy(REST);

  const st = { T: 25, load: { Na: 0.55 }, acid: 0, peak: 0, cleanT: 0, dips: 0, cobalt: false, spec: false, hot: false, gasT: 0, inAcid: false, inSample: -1, current: -1, seen: 0, identified: [] };
  const col = new THREE.Color(); const glow = new THREE.Color(); const mixE = {};
  const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -ROW_Z); const hit = new THREE.Vector3(); const tmp = new THREE.Vector3();
  let dragging = false;

  const cobaltDiv = document.createElement('div'); cobaltDiv.className = 'ho-cobalt'; hud.root.appendChild(cobaltDiv);
  const specBox = document.createElement('div'); specBox.className = 'ho-spec'; specBox.innerHTML = '<b>Hand spectroscope</b><canvas width="360" height="96"></canvas>';
  hud.root.appendChild(specBox); const specCanvas = specBox.querySelector('canvas'); let specT = 0;

  function emissionNow() {
    let total = 0;
    for (const k in st.load) { const a = st.load[k]; mixE[k] = st.hot ? a * SENS[k] * evapRate() * 2.2 : 0; total += mixE[k]; }
    return total;
  }
  function evapRate() { return st.T < 620 ? 0 : (0.22 + 0.9 * st.acid) * Math.min(1, (st.T - 620) / 450); }
  function dirty() { let s = 0; for (const k in st.load) s += st.load[k] * SENS[k]; return s; }

  function wireHandler(extraDown) {
    return {
      down(p) {
        if (extraDown && extraDown(p)) return true;
        if (screenDist(ctx, wire, p) < (p.touch ? 90 : 70) || ctx.input.pick([rod, loop])) { dragging = true; return true; }
        return false;
      },
      move() {
        if (!dragging || !ctx.input.ptr.ray.intersectPlane(plane, hit)) return;
        world.worldToLocal(hit);
        hit.x = clamp(hit.x, -2.1, 2.4); hit.y = clamp(hit.y, 0.03, 2.9); hit.z = ROW_Z;
        tipSpring.target.copy(hit);
      },
      up() { dragging = false; },
      cancel() { dragging = false; },
    };
  }
  function nearGlass(g) { return Math.abs(wire.position.x - g.position.x) < 0.3 && wire.position.y < 0.1; }

  function onDipAcid() {
    if (st.inAcid) return; st.inAcid = true; st.dips += 1;
    if (st.T > 300) { sfx.play('sizzle'); ctx.fx.burst(world.localToWorld(tmp.copy(wire.position)), 0xffffff, 8, 0.2, BY); }
    st.acid = 1; for (const k in st.load) st.load[k] *= 0.6;
    salted.visible = false; st.T = Math.min(st.T, 120);
  }
  function onDipSample(i) {
    if (st.inSample === i) return; st.inSample = i;
    const ion = unknowns[i];
    let other = 0; for (const k in st.load) if (k !== ion) other += st.load[k] * SENS[k];
    if (other > 0.25) ctx.mistake('The wire was not clean: whatever is on it now goes into this sample too. Clean it in acid and the flame first.', 3);
    if (st.T > 300) ctx.say('Let the hot wire cool for a moment, or the salt spits.', 'hint', 1800);
    st.load[ion] = (st.load[ion] || 0) + (st.acid > 0.3 ? 1 : 0.35);
    if (st.acid <= 0.3) ctx.say('Little salt sticks to a dry wire: moisten it with the acid first.', 'hint', 2600);
    salted.visible = true; salted.material.color.setHex(ion === 'Cu' ? 0x5eead4 : 0xf8fafc); sfx.play('place');
  }

  function tickWire(dt) {
    tipSpring.step(dt); wire.position.copy(tipSpring.v);
    const tilt = clamp(tipSpring.vel.x * 0.08, -0.3, 0.3); wire.rotation.z = -tilt;
    // dips
    st.inAcid = st.inAcid && nearGlass(acidGlass);
    if (nearGlass(acidGlass)) onDipAcid();
    let inS = -1; glasses.forEach((g, i) => { if (nearGlass(g)) inS = i; });
    if (inS >= 0) onDipSample(inS); else st.inSample = -1;
    // heating
    burner.group.localToWorld(tmp.set(0, 0, 0)); world.worldToLocal(tmp);
    const dx = Math.abs(wire.position.x - tmp.x); const y = wire.position.y - burner.top;
    const on = burner.lit && burner.gas > 0;
    const inFlame = on && dx < 0.12 && y > 0.02 && y < (burner.air > 0.5 ? 0.85 : 1.4);
    const hotZone = inFlame && Math.abs(wire.position.y - burner.hotY()) < 0.16 && burner.air > 0.5;
    const Tt = inFlame ? (hotZone ? 1150 : burner.air > 0.5 ? 820 : 640) : 25;
    st.T += (Tt - st.T) * (1 - Math.exp(-dt * (Tt > st.T ? 2.2 : 0.9)));
    st.hot = inFlame;
    if (inFlame && st.acid > 0) st.acid = Math.max(0, st.acid - dt * 0.35);
    const r = evapRate();
    if (inFlame && r > 0) { for (const k in st.load) { st.load[k] *= Math.exp(-r * dt); if (st.load[k] < 1e-3) delete st.load[k]; } if (salted.visible && r > 0.2) salted.visible = false; }
    glowColour(st.T, glow); nichrome.emissive.copy(glow);
    const e = emissionNow();
    const b = emissionColour(mixE, col, { cobalt: st.cobalt });
    const k = Math.min(1, e) * (b > 0 ? 1 : 0);
    burner.setEmission(col, inFlame ? k : 0);
    st.emission = inFlame ? e : 0;
  }

  // ---- steps ----
  const SHOT_BENCH = shot({ pos: [0.2, 2.2, 4.6], target: [0.1, 0.9, ROW_Z], fit: 4.8, fitH: 2.6 });
  const SHOT_FLAME = shot({ pos: [-0.1, 1.9, 3.0], target: [-0.2, 1.45, ROW_Z], fit: 2.2, fitH: 2.0 });
  const steps = [];
  steps.push({
    title: 'Light the Bunsen burner', text: 'Turn on the <b>gas tap</b> (tap its lever), then tap the <b>top of the burner</b> to light it. Then turn the <b>brass collar</b> (drag or tap it) to open the air hole.', hint: 'Gas, flame, then air: a yellow luminous flame turns into a roaring blue one as the air hole opens.', shot: SHOT_BENCH,
    skip() { burner.setGas(1); burner.light(); burner.setAir(1); },
    update(dt) {
      if (burner.gas > 0 && !burner.lit) { st.gasT += dt; if (st.gasT > 7 && !this.warned) { this.warned = true; ctx.mistake('Gas is escaping unlit. Light it straight away, or turn the tap off.', 2); } }
      if (burner.lit && burner.air > 0.8 && !this.done) { this.done = true; ctx.next('A non-luminous blue flame: hot, clean and colourless, so a metal\'s colour shows true.'); }
    },
    handler: { down(p) {
      if (hits(ctx, burner.tap, p, 50, 0.3)) { burner.setGas(burner.gas > 0 ? 0 : 1); sfx.play(burner.gas ? 'hiss' : 'click'); return true; }
      if (screenDist(ctx, burner.collar, p) < (p.touch ? 50 : 36)) { this.coll = { x: p.x, a: burner.air }; return true; }
      if (screenDist(ctx, burner.group, p, burner.top) < 70) {
        if (burner.gas <= 0) { ctx.say('No gas yet — open the tap first.', 'hint', 1800); return true; }
        if (!burner.lit) { burner.light(); sfx.play('whoosh'); ctx.say(burner.air < 0.3 ? 'Lit: a luminous yellow flame (air hole closed). Now open the air hole.' : 'Lit.', 'info', 2600); }
        return true;
      }
      return false;
    }, move(p) { if (this.coll) { burner.setAir(this.coll.a + (p.x - this.coll.x) * 0.006); } }, up(p) { if (this.coll && p.moved < 6) burner.setAir(burner.air > 0.5 ? 0 : 1); this.coll = null; } },
  });

  function cleanStep(first) {
    return {
      title: first ? 'Clean the wire' : 'Clean the wire again', text: `Drag the wire into the <b>conc. HCl</b>, then hold the loop in the <b>flame</b>, just above the blue inner cone. Repeat until the flame stays <b>colourless</b>.${first ? ' (A new wire carries sodium from fingers: watch for yellow.)' : ''}`,
      hint: 'Dip, heat, dip, heat. Acid turns the residue into volatile chlorides that burn off quickly.', shot: SHOT_BENCH,
      enter() { st.cleanT = 0; st.dips = 0; },
      skip() { st.load = {}; st.acid = 0; },
      update(dt) {
        tickWire(dt);
        const clean = dirty() < 0.05;
        if (st.hot && st.T > 900 && clean && st.dips > 0) st.cleanT += dt; else if (!clean) st.cleanT = 0;
        ctx.progress(clamp(1 - dirty() / 1.5));
        if (st.cleanT > 1.0 && !this.done) { this.done = true; anim.wait(0.6, () => ctx.next('Clean: the wire glows orange and the flame stays blue.')); }
      },
      exit() { this.done = false; },
      handler: wireHandler(),
    };
  }
  function testStep(i) {
    return {
      title: `Test sample ${names[i]}`, text: `Moisten the clean loop in the acid, touch it to <b>salt ${names[i]}</b>, then hold it in the <b>hottest part of the flame</b>. Name the ion from the colour — use the <b>cobalt glass</b> or the <b>spectroscope</b> if you need to.`,
      hint: 'Sodium\'s yellow can hide other colours; cobalt-blue glass absorbs it.', shot: SHOT_BENCH,
      enter() {
        st.current = i; st.seen = 0;
        hud.actions([
          { id: 'co', label: 'Cobalt glass', onClick: () => { st.cobalt = !st.cobalt; cobaltDiv.classList.toggle('on', st.cobalt); hud.relabel('co', st.cobalt ? 'Cobalt glass ✓' : 'Cobalt glass'); } },
          { id: 'sp', label: 'Spectroscope', onClick: () => { st.spec = !st.spec; specBox.classList.toggle('on', st.spec); hud.relabel('sp', st.spec ? 'Spectroscope ✓' : 'Spectroscope'); } },
          { id: 'id', label: 'Name the ion', primary: true, disabled: true, onClick: () => identify(i) },
        ]);
      },
      exit() { hud.actions([]); ui.clearChooser(); st.cobalt = false; cobaltDiv.classList.remove('on'); },
      skip() { st.load = { [unknowns[i]]: 0.02 }; st.identified[i] = unknowns[i]; ui.observe(`Salt ${names[i]}`, `${LINES[unknowns[i]].colour} → ${LINES[unknowns[i]].ion}`); },
      update(dt) {
        tickWire(dt);
        if ((st.load[unknowns[i]] || 0) > 0 && st.emission > 0.35) { st.seen += dt; if (st.seen > 0.8) hud.enable('id', true); }
        if (st.seen > 0.8 && !this.focused) { this.focused = true; ctx.rig.go(SHOT_FLAME, 1.2); }
      },
      handler: wireHandler(),
    };
  }
  function identify(i) {
    ui.choose(ctx.stage.clientWidth / 2, 60, `Salt ${names[i]} — which ion gives this flame?`, CANDIDATES.map((k) => ({ label: `${LINES[k].ion}  ${LINES[k].name}`, value: k })), (k) => {
      if (k !== unknowns[i]) {
        const hint = k === 'Na' && unknowns[i] === 'K' ? ' Look through the cobalt glass: the yellow was sodium contamination.' : '';
        ctx.mistake(`Not ${LINES[k].name.toLowerCase()} — that would be ${LINES[k].colour}.${hint}`, 4); return;
      }
      st.identified[i] = k; ui.observe(`Salt ${names[i]}`, `${LINES[k].colour} → <b>${LINES[k].ion}</b>`);
      ctx.next(`${LINES[k].name}: ${LINES[k].colour}. The electrons of ${LINES[k].ion} fall back from excited levels and give out light of fixed wavelengths.`, 1.4);
    });
  }

  steps.push(cleanStep(true));
  unknowns.forEach((u, i) => { steps.push(testStep(i)); if (i < unknowns.length - 1) steps.push(cleanStep(false)); });
  steps.push({
    title: 'Turn off the gas', text: 'Put the wire down and turn the <b>gas tap</b> off.', shot: SHOT_BENCH,
    enter() { tipSpring.target.copy(REST); },
    update(dt) { tickWire(dt); },
    handler: { down(p) { if (!hits(ctx, burner.tap, p, 50, 0.3)) return false; burner.setGas(0); sfx.play('click'); ctx.next('Gas off.'); return true; } },
  });

  ctx.debug = { st, burner, tipSpring, unknowns, wire };
  return {
    tools: [], steps,
    update(dt, t) {
      burner.update(dt, t);
      if (st.spec && (specT -= dt) <= 0) { specT = 0.1; const m = {}; for (const k in mixE) m[k] = mixE[k] * (st.cobalt ? 0.6 : 1); drawSpectrum(specCanvas, st.hot ? m : {}, st.T > 500 ? (st.T - 500) / 700 : 0); }
      hud.update();
    },
    result() {
      return {
        title: 'Flame tests',
        rows: unknowns.map((u, i) => [`Salt ${names[i]}`, `${LINES[u].ion} (${LINES[u].colour})`]),
        conclusion: 'Each metal ion gives a characteristic flame colour because its electrons, excited by the heat, fall back between fixed energy levels and emit light of fixed wavelengths (ΔE = hc/λ) — a line spectrum, not a rainbow.',
      };
    },
    dispose() { hud.dispose(); },
  };
}
