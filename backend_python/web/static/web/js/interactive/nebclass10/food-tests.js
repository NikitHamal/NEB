/**
 * Food tests (NEB class 10) in 3D: ten food extracts in a rack standing in a water bath on the
 * chemistry bench. Choose iodine, Benedict's or Biuret reagent and tap a tube: iodine turns blue-black
 * with starch, Biuret turns violet with protein, and Benedict's only changes when the bath is boiling:
 * blue, green, yellow, orange or brick red with a settling precipitate, depending on how much reducing
 * sugar there is. Table sugar (sucrose) is a sugar but not a reducing one, so it stays blue.
 */
import { mixHex } from '../core/tubes2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { createChemLab, THREE } from '../chemistry/chem3d/stage.js';

const FOODS = [
  { name: 'Boiled rice', short: 'Rice', s: 0.9, r: 0.02, p: 0.15, base: '#f8f5ec' },
  { name: 'Potato', short: 'Potato', s: 0.85, r: 0.08, p: 0.1, base: '#f6f0dc' },
  { name: 'Bread', short: 'Bread', s: 0.75, r: 0.18, p: 0.3, base: '#f3ead6' },
  { name: 'Ripe banana', short: 'Banana', s: 0.12, r: 0.8, p: 0.05, base: '#f8f1cf' },
  { name: 'Milk', short: 'Milk', s: 0, r: 0.5, p: 0.6, base: '#fbfbf7' },
  { name: 'Egg white', short: 'Egg w.', s: 0, r: 0.02, p: 0.95, base: '#f4f6ee' },
  { name: 'Soybean', short: 'Soybean', s: 0.1, r: 0.05, p: 0.85, base: '#f3eedb' },
  { name: 'Groundnut', short: 'G.nut', s: 0.1, r: 0.05, p: 0.7, base: '#f1e9d6' },
  { name: 'Table sugar (sucrose)', short: 'Sucrose', s: 0, r: 0, p: 0, base: '#f5f8fc' },
  { name: 'Glucose', short: 'Glucose', s: 0, r: 1, p: 0, base: '#f5f8fc' },
];
const REAG = [{ id: 'iodine', label: 'Iodine' }, { id: 'benedict', label: "Benedict's" }, { id: 'biuret', label: 'Biuret' }];
const BEN = ['#3b82f6', '#4caf50', '#d9c13a', '#e8742a', '#b5401f'];
const clamp = (x, a, b) => (x < a ? a : x > b ? b : x);
const benColor = (x) => { const f = clamp(x, 0, 1) * 4; const i = Math.min(3, Math.floor(f)); return mixHex(BEN[i], BEN[i + 1], f - i); };
const benName = (x) => (x < 0.12 ? 'stays blue' : x < 0.35 ? 'green (a trace)' : x < 0.6 ? 'yellow (some)' : x < 0.85 ? 'orange (a lot)' : 'brick red (very much)');

export default function init(stage) {
  const L = createChemLab(stage, { title: 'Food tests', aim: 'Testing foods for starch, sugar and protein', target: [0, 0.7, 0], camera: [0.2, 2.5, 4.8], minDistance: 1.8, maxDistance: 9 });
  if (!L) return null;
  const { engine, world, controls } = L;
  const hud = createHud(stage);
  const badge = hud.badge('Choose a reagent, then tap a food tube', '#2563eb');

  const st = FOODS.map(() => ({ reag: null, heat: 0, res: {} }));
  let current = 'iodine'; let bathOn = false; let bathT = 25;
  const steel = new THREE.MeshStandardMaterial({ color: 0xc0c6cf, metalness: 0.8, roughness: 0.35 });
  const tank = new THREE.Group(); world.add(tank);
  const TW = 4.7; const TD = 0.8; const TH = 0.5;
  for (const [x, z, w, d] of [[0, -TD / 2, TW, 0.03], [0, TD / 2, TW, 0.03], [-TW / 2, 0, 0.03, TD], [TW / 2, 0, 0.03, TD]]) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, TH, d), steel); m.position.set(x, TH / 2, z); tank.add(m); }
  const water = new THREE.Mesh(new THREE.BoxGeometry(TW - 0.04, TH * 0.75, TD - 0.04), new THREE.MeshPhysicalMaterial({ color: 0x9fd3f7, roughness: 0.05, transparent: true, opacity: 0.35, clearcoat: 0.5, depthWrite: false }));
  water.position.y = TH * 0.375; water.renderOrder = 3; tank.add(water);
  const heater = new THREE.Mesh(new THREE.BoxGeometry(TW, 0.06, TD), new THREE.MeshStandardMaterial({ color: 0x1f2937, emissive: 0x000000 })); heater.position.y = 0.03; tank.add(heater);
  const glass = new THREE.MeshPhysicalMaterial({ color: 0xeaf6ff, roughness: 0.04, transparent: true, opacity: 0.28, clearcoat: 1, depthWrite: false, side: THREE.DoubleSide });
  const tubes = FOODS.map((f, i) => {
    const g = new THREE.Group(); g.position.set(-2.07 + i * 0.46, 0.1, 0); world.add(g);
    const prof = []; for (let k = 0; k <= 8; k++) { const a = k / 8 * Math.PI / 2; prof.push(new THREE.Vector2(Math.sin(a) * 0.085, 0.085 - Math.cos(a) * 0.085)); } prof.push(new THREE.Vector2(0.085, 1.05), new THREE.Vector2(0.095, 1.07));
    const tube = new THREE.Mesh(new THREE.LatheGeometry(prof, 28), glass); tube.renderOrder = 5; g.add(tube);
    const liqMat = new THREE.MeshPhysicalMaterial({ color: new THREE.Color(f.base), roughness: 0.05, transparent: true, opacity: 0.6, clearcoat: 0.5, depthWrite: false });
    const liq = new THREE.Mesh(new THREE.CylinderGeometry(0.078, 0.078, 0.42, 24), liqMat); liq.position.y = 0.25; liq.renderOrder = 4; g.add(liq);
    const ppt = new THREE.Mesh(new THREE.CylinderGeometry(0.076, 0.076, 1, 24), new THREE.MeshStandardMaterial({ color: 0xb5401f, roughness: 0.9 })); ppt.visible = false; g.add(ppt);
    const c = document.createElement('canvas'); c.width = 128; c.height = 48; const x = c.getContext('2d'); x.fillStyle = '#ffffff'; x.fillRect(0, 0, 128, 48); x.fillStyle = '#0f172a'; x.font = '700 20px Poppins, system-ui, sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(f.short, 64, 25);
    const tag = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.15), new THREE.MeshStandardMaterial({ map: Object.assign(new THREE.CanvasTexture(c), { colorSpace: THREE.SRGBColorSpace }), roughness: 0.8 })); tag.position.set(0, 1.2, 0.0); g.add(tag);
    L.tappable(g, () => apply(current, i));
    return { g, liq, liqMat, ppt };
  });
  const rackTop = new THREE.Mesh(new THREE.BoxGeometry(TW, 0.05, 0.3), new THREE.MeshStandardMaterial({ color: 0x9a6b3e, roughness: 0.7 })); rackTop.position.y = 0.72; world.add(rackTop);
  const puffs = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.22, depthWrite: false }), 40);
  puffs.count = 0; puffs.renderOrder = 7; world.add(puffs);
  const P = Array.from({ length: 40 }, () => ({ a: 99 }));
  const dropper = new THREE.Group();
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.07, 16, 12), new THREE.MeshStandardMaterial({ color: 0x1f2937 })); bulb.scale.y = 1.4; bulb.position.y = 0.42;
  dropper.add(bulb, new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.01, 0.6, 12), glass)); dropper.visible = false; world.add(dropper);

  const panel = createPanel(stage, { title: 'Food tests' });
  panel.chips({ label: 'Reagent', options: REAG.map((r) => ({ value: r.id, label: r.label })), value: current, onChange: (v) => { current = v; } });
  const bathTg = panel.toggle({ label: 'Water bath (boiling)', value: false, onChange: (v) => { bathOn = v; } });
  panel.button({ label: 'Wash all the tubes', icon: 'water', variant: 'ghost', onClick: wash });
  const table = document.createElement('div');
  table.style.cssText = 'display:grid;grid-template-columns:1.2fr repeat(3,1fr);gap:3px 8px;font:600 11px Poppins,system-ui,sans-serif;color:#cbd5e1;padding:8px 10px;border-radius:12px;background:rgba(255,255,255,0.04);flex-shrink:0;align-items:center';
  panel.body.appendChild(table);
  const last = panel.readout({ label: 'Last result', value: '—' });
  panel.info("Iodine: yellow-brown → blue-black means starch. Benedict's: heat for 2–3 minutes; green → yellow → orange → brick red means more and more reducing sugar. Biuret: blue → violet means protein. Always compare with a control.");

  function colorOf(i) {
    const f = FOODS[i]; const s = st[i];
    if (s.reag === 'iodine') return [mixHex('#c8892b', '#1b2240', clamp((f.s - 0.05) * 1.4, 0, 1)), 0.85];
    if (s.reag === 'biuret') return [mixHex('#7da2e8', '#7d3fbf', clamp((f.p - 0.08) * 1.3, 0, 1)), 0.75];
    if (s.reag === 'benedict') return [benColor(f.r * s.heat), 0.8];
    return [f.base, 0.6];
  }
  function render() {
    tubes.forEach((t, i) => { const [c, a] = colorOf(i); t.liqMat.color.set(c); t.liqMat.opacity = a; const x = FOODS[i].r * st[i].heat; t.ppt.visible = st[i].reag === 'benedict' && x > 0.3; if (t.ppt.visible) { const h = 0.02 + 0.08 * st[i].heat; t.ppt.scale.y = h; t.ppt.position.y = 0.04 + h / 2; t.ppt.material.color.set(benColor(FOODS[i].r)); } });
    const cell = (r) => (r ? `<span><i style="display:inline-block;width:11px;height:11px;border-radius:3px;vertical-align:-2px;background:${r.c};border:1px solid rgba(255,255,255,0.25)"></i> ${r.v}</span>` : '<span style="color:#475569">·</span>');
    table.innerHTML = '<b style="color:#94a3b8">Food</b><b style="color:#94a3b8">Starch</b><b style="color:#94a3b8">Sugar</b><b style="color:#94a3b8">Protein</b>' + FOODS.map((f, i) => `<span>${f.short}</span>${cell(st[i].res.iodine)}${cell(st[i].res.benedict)}${cell(st[i].res.biuret)}`).join('');
  }
  function wash() { FOODS.forEach((f, i) => { st[i].reag = null; st[i].heat = 0; }); render(); }
  let anim = null;
  function apply(id, i) {
    const f = FOODS[i];
    if (st[i].reag && st[i].reag !== id) { badge.set('Use a clean tube for each test: wash the tubes first'); return; }
    st[i].reag = id; st[i].heat = 0; anim = { i, t: 0 };
    const [c] = colorOf(i);
    if (id === 'iodine') { const pos = f.s > 0.15; st[i].res.iodine = { c, v: pos ? '+' : '−' }; last.set(`${f.name} + iodine: ${pos ? 'blue-black → starch present' : 'stays yellow-brown → no starch'}`); }
    else if (id === 'biuret') { const pos = f.p > 0.2; st[i].res.biuret = { c, v: pos ? '+' : '−' }; last.set(`${f.name} + Biuret: ${pos ? 'violet → protein present' : 'stays blue → no protein'}`); }
    else last.set(`Benedict's added to ${f.name}. It stays blue until you heat it in the water bath.`);
    badge.set(last.el.querySelector('.ix-readout-value') ? last.el.querySelector('.ix-readout-value').textContent : 'Tested');
  }
  render();

  const m4 = new THREE.Matrix4(); const q = new THREE.Quaternion(); const sc = new THREE.Vector3(); const v3 = new THREE.Vector3();
  engine.setUpdate((dt, time) => {
    controls.update(dt);
    bathT += ((bathOn ? 100 : 25) - bathT) * (1 - Math.exp(-dt * 0.8));
    heater.material.emissive.setHex(0xff3b0a).multiplyScalar(bathOn ? 0.5 : 0);
    let changed = false;
    for (let i = 0; i < FOODS.length; i++) {
      if (st[i].reag === 'benedict' && bathT > 70 && st[i].heat < 1) {
        st[i].heat = Math.min(1, st[i].heat + dt / 5); changed = true;
        if (st[i].heat >= 1) { const x = FOODS[i].r; st[i].res.benedict = { c: benColor(x), v: x > 0.12 ? '+' : '−' }; last.set(`${FOODS[i].name} + Benedict's, heated: ${benName(x)}${FOODS[i].short === 'Sucrose' ? ': sucrose is not a reducing sugar' : ''}`); }
      }
    }
    if (changed || anim) render();
    let n = 0;
    for (const p of P) {
      if (p.a > 1 && bathT > 90 && Math.random() < dt * 10) { p.a = 0; p.x = (Math.random() - 0.5) * TW * 0.9; p.z = (Math.random() - 0.5) * TD * 0.6; }
      if (p.a > 1) continue;
      p.a += dt * 0.6;
      m4.compose(v3.set(p.x + Math.sin(time + p.x * 5) * 0.05, TH * 0.75 + p.a * 1.4, p.z), q, sc.setScalar(0.04 + p.a * 0.16)); puffs.setMatrixAt(n++, m4);
    }
    puffs.count = n; puffs.instanceMatrix.needsUpdate = true;
    dropper.visible = false;
    if (anim) { anim.t += dt; tubes[anim.i].g.getWorldPosition(v3); world.worldToLocal(v3); dropper.visible = anim.t < 0.9; dropper.position.set(v3.x, 1.65, v3.z); if (anim.t > 0.9) anim = null; }
    void bathTg;
  });
  engine.start();

  stage.__food = { apply, bath: (v) => { bathOn = v; bathTg.set(v); }, state: () => st.map((s) => ({ reag: s.reag, heat: s.heat })) };
  return { dispose() { panel.dispose(); hud.dispose(); L.dispose(); } };
}
