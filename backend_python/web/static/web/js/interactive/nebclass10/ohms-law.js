/**
 * Ohm's law (NEB class 10) in 3D — the school practical on the physics bench: a 6 V battery, a plug
 * key, a slide-wire rheostat, an ammeter in series and a voltmeter across the resistor (or two
 * resistors in series or parallel, or a torch bulb). Slide the rheostat, read the analogue meters
 * (their needles settle like real ones), record readings and build the I–V graph: its slope is 1/R.
 * The bulb's filament heats up and glows, so its graph bends — Ohm's law needs a steady temperature.
 */
import { createPanel, createHud } from '../core/sim-ui.js';
import { dialMeter, plugKey, rheostat, cell, lead } from '../core/handson/circuit.js';
import { canvasCard } from '../space/space3d/kit.js';
import { createChemLab, THREE } from '../chemistry/chem3d/stage.js';

const E = 6; const RINT = 0.4; const RH = 20;
const NETS = [{ value: 'single', label: 'R₁ only' }, { value: 'series', label: 'R₁ + R₂ series' }, { value: 'parallel', label: 'R₁ ∥ R₂ parallel' }, { value: 'bulb', label: 'Torch bulb' }];
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

function resistor() {
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.09, 0.34, 8, 20), new THREE.MeshStandardMaterial({ color: 0xd9c4a0, roughness: 0.6 })); body.rotation.z = Math.PI / 2; g.add(body);
  [-0.12, -0.04, 0.04, 0.13].forEach((x, i) => { const b = new THREE.Mesh(new THREE.CylinderGeometry(0.097, 0.097, 0.04, 20), new THREE.MeshStandardMaterial({ color: [0x7c4a1e, 0x111827, 0x111827, 0xc9a14a][i], metalness: i === 3 ? 0.8 : 0 })); b.rotation.z = Math.PI / 2; b.position.x = x; g.add(b); });
  const legs = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.9, 8), new THREE.MeshStandardMaterial({ color: 0xc0c6cf, metalness: 0.9 })); legs.rotation.z = Math.PI / 2; g.add(legs);
  g.position.y = 0.2;
  return g;
}

export default function init(stage) {
  const S = createChemLab(stage, { title: "Ohm's law", aim: 'Verify Ohm\'s law and find a resistance', subject: 'physics', target: [0.3, 0.3, 0], camera: [0.6, 4.4, 5.4], minDistance: 2.5, maxDistance: 12 });
  if (!S) return null;
  const { engine, world, controls } = S;
  const hud = createHud(stage);
  const badge = hud.badge('Insert the key, then slide the rheostat', '#2563eb');

  let net = 'single'; let R1 = 10; let R2 = 15; let keyIn = false; let slide = 0.9;
  let I = 0; let V = 0; let aFull = 1; let aLc = 0.02;
  const pts = [];

  const board = new THREE.Mesh(new THREE.BoxGeometry(7.4, 0.1, 4.4), new THREE.MeshStandardMaterial({ color: 0xc8a06a, roughness: 0.65 })); board.position.y = 0.05; board.receiveShadow = true; world.add(board);
  const bat = cell('6 V'); bat.group.position.set(-2.8, 0.1, -1.3); bat.group.scale.setScalar(1.3); world.add(bat.group);
  const key = plugKey(); key.group.position.set(-1.2, 0.1, -1.5); key.group.scale.setScalar(1.4); world.add(key.group);
  const rh = rheostat(RH); rh.group.position.set(1.5, 0.1, -1.4); world.add(rh.group);
  const am1 = dialMeter('A', 1, 'A', 0.2); const am3 = dialMeter('A', 3, 'A', 0.5);
  [am1, am3].forEach((m) => { m.group.position.set(-2.6, 0.1, 0.9); m.group.scale.setScalar(1.15); world.add(m.group); });
  const vm = dialMeter('V', 6, 'V', 1); vm.group.position.set(0.4, 0.1, 1.5); vm.group.scale.setScalar(1.15); world.add(vm.group);
  const ra = resistor(); const rb = resistor(); world.add(ra, rb);
  const bulb = new THREE.Group(); world.add(bulb);
  const holder = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 0.18, 20), new THREE.MeshStandardMaterial({ color: 0x9aa3ad, metalness: 0.8, roughness: 0.3 })); holder.position.y = 0.19; bulb.add(holder);
  const glassB = new THREE.Mesh(new THREE.SphereGeometry(0.16, 24, 16), new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.02, transparent: true, opacity: 0.3, clearcoat: 0.5, depthWrite: false })); glassB.position.y = 0.42; bulb.add(glassB);
  const fil = new THREE.Mesh(new THREE.TorusGeometry(0.04, 0.008, 6, 16, Math.PI), new THREE.MeshStandardMaterial({ color: 0x555555, emissive: 0x000000 })); fil.position.y = 0.42; bulb.add(fil);
  const glow = new THREE.PointLight(0xffb057, 0, 4, 2); glow.position.y = 0.42; bulb.add(glow);
  const leads = [];
  const P = (x, z, y = 0.3) => new THREE.Vector3(x, y, z);

  const panel = createPanel(stage, { title: "Ohm's law practical" });
  panel.chips({ label: 'What is being tested', options: NETS, value: 'single', onChange: (v) => { net = v; pts.length = 0; layout(); render(); } });
  panel.chips({ label: 'R₁', options: [5, 10, 15, 20].map((r) => ({ value: String(r), label: `${r} Ω` })), value: '10', onChange: (v) => { R1 = +v; pts.length = 0; render(); } });
  panel.chips({ label: 'R₂', options: [5, 10, 15, 20].map((r) => ({ value: String(r), label: `${r} Ω` })), value: '15', onChange: (v) => { R2 = +v; pts.length = 0; render(); } });
  const keyT = panel.toggle({ label: 'Key inserted', value: false, onChange: (v) => { keyIn = v; key.set(v); } });
  const slS = panel.slider({ label: 'Rheostat in circuit', min: 0, max: 100, step: 1, value: 90, format: (v) => `${fmt(RH * v / 100, 1)} Ω`, onChange: (v) => { slide = v / 100; } });
  panel.buttonRow([{ label: 'Record', icon: 'add_chart', onClick: record }, { label: 'Clear', icon: 'restart_alt', variant: 'ghost', onClick: () => { pts.length = 0; render(); } }]);
  const graph = canvasCard(panel.body, 1.4);
  const st = panel.stats([{ key: 'R', label: 'Expected R' }, { key: 'slope', label: 'Slope of I–V' }, { key: 'fit', label: 'R = 1/slope' }, { key: 'n', label: 'Readings' }]);
  const table = document.createElement('div');
  table.style.cssText = 'display:grid;grid-template-columns:repeat(3,1fr);gap:3px 10px;font:600 12px Poppins,system-ui,sans-serif;color:#cbd5e1;padding:8px 10px;border-radius:12px;background:rgba(255,255,255,0.04);flex-shrink:0';
  panel.body.appendChild(table);
  panel.info('Read each meter to its least count (ammeter 0.02 A on the 1 A scale, voltmeter 0.1 V). Take five or six readings spread across the range; the best straight line through the origin has slope 1/R.');
  S.tappable(key.group, () => { keyIn = !keyIn; keyT.set(keyIn); key.set(keyIn); });

  function netR(i) {
    if (net === 'single') return R1;
    if (net === 'series') return R1 + R2;
    if (net === 'parallel') return R1 * R2 / (R1 + R2);
    return 4 * (1 + 2.2 * Math.sqrt(i * i * 6));
  }
  function solve() {
    const Rr = RH * slide;
    aFull = E / (RINT + netR(net === 'bulb' ? 0.4 : 0)) > 1 ? 3 : 1; aLc = aFull === 1 ? 0.02 : 0.05;
    if (!keyIn) { I = 0; V = 0; return; }
    I = E / (Rr + netR(0) + RINT);
    for (let it = 0; it < 30; it++) I = 0.5 * I + 0.5 * E / (Rr + netR(I) + RINT);
    V = I * netR(I);
  }
  function layout() {
    ra.visible = net !== 'bulb'; rb.visible = net === 'series' || net === 'parallel'; bulb.visible = net === 'bulb';
    if (net === 'parallel') { ra.position.set(0.4, 0.2, -0.1); rb.position.set(0.4, 0.2, 0.45); } else { ra.position.set(net === 'series' ? -0.1 : 0.4, 0.2, 0.2); rb.position.set(0.9, 0.2, 0.2); }
    bulb.position.set(0.4, 0.05, 0.2);
    leads.forEach((l) => world.remove(l.mesh)); leads.length = 0;
    const L = (a, b, c) => leads.push(lead(world, a, b, c));
    const rl = net === 'series' ? -0.55 : net === 'parallel' ? -0.05 : -0.05; const rr = net === 'series' ? 1.35 : 0.85;
    L(P(-2.6, -1.3, 0.8), P(-1.5, -1.5, 0.35), 0xd32f2f);
    L(P(-0.9, -1.5, 0.35), P(0.6, -1.5, 0.6), 0xd32f2f);
    L(P(2.4, -1.45, 0.6), P(rr, 0.2, 0.3), 0xd32f2f);
    L(P(rl, 0.2, 0.3), P(-2.3, 0.8, 0.6), 0x111827);
    L(P(-2.9, 0.8, 0.6), P(-3.0, -1.3, 0.8), 0x111827);
    L(P(rl, 0.2, 0.3), P(0.15, 1.3, 0.6), 0x1d4ed8); L(P(rr, 0.2, 0.3), P(0.7, 1.3, 0.6), 0x1d4ed8);
    if (net === 'parallel') { L(P(rl, 0.2, 0.3), P(rl, 0.45, 0.3), 0x6b7280); L(P(rr, 0.2, 0.3), P(rr, 0.45, 0.3), 0x6b7280); }
  }
  layout();
  function record() {
    if (!keyIn) { badge.set('Insert the key first: no current flows'); return; }
    solve();
    const a = Math.round(I / aLc) * aLc; const vv = Math.round(V / 0.1) * 0.1;
    if (pts.some((p) => Math.abs(p.v - vv) < 0.05)) { badge.set('You already have that reading: move the rheostat'); return; }
    pts.push({ v: vv, i: a }); pts.sort((p, q) => p.v - q.v); render();
  }
  function fitSlope() { let sxy = 0; let sxx = 0; for (const p of pts) { sxy += p.v * p.i; sxx += p.v * p.v; } return sxx > 0 ? sxy / sxx : 0; }
  function render() {
    table.innerHTML = pts.length ? '<b style="color:#94a3b8">V / volt</b><b style="color:#94a3b8">I / A</b><b style="color:#94a3b8">V/I / Ω</b>' + pts.map((p) => `<span>${fmt(p.v, 1)}</span><span>${fmt(p.i, 2)}</span><span>${p.i > 0 ? fmt(p.v / p.i, 1) : '—'}</span>`).join('') : '';
    const { g, w, h } = graph.ctx();
    const ix = 34; const iy = 20; const iw = w - 44; const ih = h - 40;
    const X = (v) => ix + v / 6 * iw; const Y = (i) => iy + ih - i / aFull * ih;
    g.font = '700 11px Poppins, system-ui, sans-serif'; g.fillStyle = '#e8eefb'; g.textAlign = 'left'; g.fillText('I–V graph (your readings)', 10, 13);
    g.strokeStyle = 'rgba(160,190,255,0.18)'; g.strokeRect(ix, iy, iw, ih);
    const s = fitSlope();
    if (pts.length > 1) { g.strokeStyle = '#60a5fa'; g.lineWidth = 1.5; g.beginPath(); g.moveTo(X(0), Y(0)); g.lineTo(X(6), Y(6 * s)); g.stroke(); }
    pts.forEach((p) => { g.fillStyle = '#fbbf24'; g.beginPath(); g.arc(X(p.v), Y(p.i), 4, 0, Math.PI * 2); g.fill(); });
    g.font = '600 9px Poppins, system-ui, sans-serif'; g.fillStyle = '#8ea0c2'; g.textAlign = 'center'; g.fillText('V / volt', ix + iw / 2, h - 5); g.textAlign = 'right'; g.fillText(`${aFull} A`, ix - 4, iy + 8); g.fillText('0', ix - 4, iy + ih);
    st.n.set(String(pts.length)); st.slope.set(pts.length > 1 ? `${fmt(s, 4)} A/V` : '—'); st.fit.set(pts.length > 1 && s > 0 ? `${fmt(1 / s, 2)} Ω` : '—');
  }
  render();

  engine.setUpdate((dt) => {
    controls.update(dt);
    solve();
    rh.set(slide);
    am1.group.visible = aFull === 1; am3.group.visible = aFull === 3;
    const am = aFull === 1 ? am1 : am3;
    am.set(I); vm.set(V); am1.update(dt); am3.update(dt); vm.update(dt);
    const P2 = I * V;
    fil.material.emissive.setHex(0xffa040).multiplyScalar(net === 'bulb' ? Math.min(3, P2 * 1.2) : 0); glow.intensity = net === 'bulb' ? P2 * 3 : 0;
    st.R.set(net === 'bulb' ? `${fmt(netR(I), 1)} Ω (hot)` : `${fmt(netR(0), 2)} Ω`);
    badge.set(!keyIn ? 'Insert the key, then slide the rheostat' : net === 'bulb' ? `The filament is at ${fmt(netR(I), 1)} Ω now: it rises as it heats, so the I–V line bends` : `${fmt(V, 2)} V ÷ ${fmt(I, 3)} A = ${fmt(V / Math.max(I, 1e-6), 2)} Ω: record a few readings`);
  });
  engine.start();

  stage.__ohm = { key: (v) => { keyIn = v; keyT.set(v); key.set(v); }, slide: (v) => { slide = v; slS.set(Math.round(v * 100)); }, record, pts: () => pts.slice() };
  return { dispose() { panel.dispose(); hud.dispose(); S.dispose(); } };
}
