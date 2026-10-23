/**
 * Indicators (NEB class 10) in 3D: a rack of household solutions on the chemistry bench. Choose red or
 * blue litmus paper, phenolphthalein, methyl orange or universal indicator (or dilute NaOH or HCl) and
 * tap a test tube: the strip dips in or the dropper adds a drop, and the colour changes as the pH says.
 * Every result fills the observation table. NaOH and HCl neutralise a tube drop by drop (each drop is
 * 0.05 mL of 0.1 M into 5 mL), and universal indicator follows the pH through green at 7.
 */
import { INDICATORS, litmusPaper } from '../core/indicators2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { createChemLab, THREE } from '../chemistry/chem3d/stage.js';

const SOL = [
  { name: 'Lemon juice', short: 'Lemon', pH: 2.2, base: 0xfbf3c4 },
  { name: 'Vinegar', short: 'Vinegar', pH: 2.9, base: 0xf6efd9 },
  { name: 'Curd (dahi) water', short: 'Curd', pH: 4.5, base: 0xf8f6ef },
  { name: 'Common salt solution', short: 'Salt', pH: 7.0, base: 0xeef4fb },
  { name: 'Baking soda solution', short: 'Soda', pH: 8.3, base: 0xeef4fb },
  { name: 'Soap solution', short: 'Soap', pH: 10.0, base: 0xf1f1f4 },
  { name: 'Milk of magnesia', short: 'Mg(OH)₂', pH: 10.5, base: 0xf8fafc },
  { name: 'Lime water', short: 'Lime w.', pH: 12.4, base: 0xf1f7fd },
];
const REAG = [
  { id: 'red', label: 'Red litmus' }, { id: 'blue', label: 'Blue litmus' }, { id: 'phenolphthalein', label: 'Phenolphthalein' },
  { id: 'methylorange', label: 'Methyl orange' }, { id: 'universal', label: 'Universal' }, { id: 'naoh', label: 'NaOH (dil.)' }, { id: 'hcl', label: 'HCl (dil.)' },
];
const KW = 1e-14; const COLS = ['red', 'blue', 'phenolphthalein', 'methylorange', 'universal'];
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

export default function init(stage) {
  const L = createChemLab(stage, { title: 'Indicators', aim: 'Acids, bases and indicators', target: [0, 0.7, 0], camera: [0.2, 2.6, 4.4], minDistance: 1.8, maxDistance: 9 });
  if (!L) return null;
  const { engine, world, controls } = L;
  const hud = createHud(stage);
  const badge = hud.badge('Choose an indicator, then tap a test tube', '#2563eb');

  const state = SOL.map((s) => ({ c: excess(s.pH), ind: null, res: {}, paper: null, paperC: null }));
  let current = 'red';
  const wood = new THREE.MeshStandardMaterial({ color: 0x9a6b3e, roughness: 0.7 });
  const rack = new THREE.Group(); world.add(rack);
  const top = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.06, 0.45), wood); top.position.y = 0.62; rack.add(top);
  const shelf = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.06, 0.45), wood); shelf.position.y = 0.05; rack.add(shelf);
  for (const x of [-1.77, 1.77]) { const side = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.66, 0.45), wood); side.position.set(x, 0.33, 0); rack.add(side); }
  rack.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  const glass = new THREE.MeshPhysicalMaterial({ color: 0xeaf6ff, roughness: 0.04, transparent: true, opacity: 0.28, clearcoat: 1, depthWrite: false, side: THREE.DoubleSide });
  const tubes = SOL.map((s, i) => {
    const g = new THREE.Group(); g.position.set(-1.54 + i * 0.44, 0.08, 0); rack.add(g);
    const prof = []; for (let k = 0; k <= 8; k++) { const a = k / 8 * Math.PI / 2; prof.push(new THREE.Vector2(Math.sin(a) * 0.085, 0.085 - Math.cos(a) * 0.085)); } prof.push(new THREE.Vector2(0.085, 1.05), new THREE.Vector2(0.095, 1.07));
    const tube = new THREE.Mesh(new THREE.LatheGeometry(prof, 28), glass); tube.renderOrder = 5; g.add(tube);
    const liqMat = new THREE.MeshPhysicalMaterial({ color: s.base, roughness: 0.05, transparent: true, opacity: 0.6, clearcoat: 0.5, depthWrite: false });
    const liq = new THREE.Mesh(new THREE.CylinderGeometry(0.078, 0.078, 0.42, 24), liqMat); liq.position.y = 0.25; liq.renderOrder = 4; g.add(liq);
    const paper = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.6, 0.004), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9 })); paper.position.set(0.02, 0.62, 0); paper.visible = false; g.add(paper);
    const c = document.createElement('canvas'); c.width = 128; c.height = 48; const x = c.getContext('2d'); x.fillStyle = '#ffffff'; x.fillRect(0, 0, 128, 48); x.fillStyle = '#0f172a'; x.font = '700 22px Poppins, system-ui, sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(s.short, 64, 25);
    const tag = new THREE.Mesh(new THREE.PlaneGeometry(0.38, 0.14), new THREE.MeshStandardMaterial({ map: Object.assign(new THREE.CanvasTexture(c), { colorSpace: THREE.SRGBColorSpace }), roughness: 0.8 })); tag.position.set(0, 0.7, 0.235); g.add(tag);
    L.tappable(g, () => apply(current, i));
    return { g, liq, liqMat, paper };
  });
  const dropper = new THREE.Group();
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.07, 16, 12), new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.6 })); bulb.scale.y = 1.4; bulb.position.y = 0.42;
  const pipe = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.01, 0.6, 12), glass); pipe.position.y = 0.05; dropper.add(bulb, pipe); dropper.visible = false; world.add(dropper);
  const drop = new THREE.Mesh(new THREE.SphereGeometry(0.022, 12, 8), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.85 })); drop.visible = false; world.add(drop);

  const panel = createPanel(stage, { title: 'Indicator tests' });
  panel.chips({ label: 'Test with', options: REAG.map((r) => ({ value: r.id, label: r.label })), value: current, onChange: (v) => { current = v; } });
  panel.button({ label: 'Wash all the tubes', icon: 'water', variant: 'ghost', onClick: wash });
  const table = document.createElement('div');
  table.style.cssText = 'display:grid;grid-template-columns:1.3fr repeat(5,1fr);gap:3px 6px;font:600 11px Poppins,system-ui,sans-serif;color:#cbd5e1;padding:8px 10px;border-radius:12px;background:rgba(255,255,255,0.04);flex-shrink:0;align-items:center';
  panel.body.appendChild(table);
  const verdict = panel.readout({ label: 'Last test', value: '—' });
  panel.info('Acids turn blue litmus red; bases turn red litmus blue. Phenolphthalein is colourless in acid and pink in base; methyl orange is red in acid and yellow in base. Universal indicator shows the whole pH scale. Acid + base → salt + water.');

  function excess(pH) { return Math.pow(10, -pH) - Math.pow(10, pH - 14); }
  function pHof(c) { const hh = (c + Math.sqrt(c * c + 4 * KW)) / 2; return -Math.log10(hh); }
  function tubeColor(i) { const st = state[i]; const p = pHof(st.c); if (!st.ind) return [SOL[i].base, 0.6]; const I = INDICATORS[st.ind]; const a = I.alpha(p); return a < 0.05 ? [SOL[i].base, 0.6] : [new THREE.Color(I.color(p)).getHex(), Math.max(0.6, a)]; }
  function wash() { SOL.forEach((s, i) => { state[i].c = excess(s.pH); state[i].ind = null; state[i].paper = null; tubes[i].paper.visible = false; }); render(); }
  function render() {
    tubes.forEach((t, i) => { const [c, a] = tubeColor(i); t.liqMat.color.setHex(c); t.liqMat.opacity = a; const st = state[i]; if (st.paper) { t.paper.visible = true; t.paper.material.color.set(st.paperC); } });
    table.innerHTML = '<b style="color:#94a3b8">Solution</b><b style="color:#94a3b8">Red lit.</b><b style="color:#94a3b8">Blue lit.</b><b style="color:#94a3b8">Phen.</b><b style="color:#94a3b8">M.O.</b><b style="color:#94a3b8">pH</b>' + SOL.map((s, i) => `<span>${s.short}</span>${COLS.map((c) => { const r = state[i].res[c]; if (!r) return '<span style="color:#475569">·</span>'; return c === 'universal' ? `<span>${fmt(r.pH, 1)}</span>` : `<span><i style="display:inline-block;width:12px;height:12px;border-radius:3px;background:${r.color};border:1px solid rgba(255,255,255,0.25)"></i></span>`; }).join('')}`).join('');
  }
  let anim = null;
  function apply(id, i) {
    const st = state[i]; const p = pHof(st.c); const name = SOL[i].name; const item = REAG.find((r) => r.id === id);
    if (id === 'red' || id === 'blue') {
      st.paper = id; st.paperC = litmusPaper(id, p); st.res[id] = { color: st.paperC };
      const changed = (id === 'red' && p > 8) || (id === 'blue' && p < 5);
      verdict.set(`${item.label} in ${name}: ${changed ? (id === 'red' ? 'turns blue → base' : 'turns red → acid') : 'no change'}`);
      tubes[i].paper.material.color.set(id === 'red' ? '#e8596e' : '#4c6ef5'); tubes[i].paper.visible = true;
      anim = { kind: 'paper', i, t: 0 };
    } else {
      anim = { kind: 'drop', i, t: 0, id };
      if (id === 'naoh' || id === 'hcl') {
        st.c += (id === 'naoh' ? -1 : 1) * 0.1 * 0.05 / 5 * 4;
        const np = pHof(st.c);
        verdict.set(`${id === 'naoh' ? 'Base' : 'Acid'} added to ${name}: pH is now ${fmt(np, 1)}${Math.abs(np - 7) < 0.6 ? ': neutral! acid + base → salt + water' : ''}`);
        if (st.paper) st.paperC = litmusPaper(st.paper, np);
      } else {
        st.ind = id; const I = INDICATORS[id];
        st.res[id] = { color: I.alpha(p) < 0.05 ? '#ffffff' : I.color(p), pH: p };
        verdict.set(`${I.label} in ${name}: ${id === 'phenolphthalein' ? (p > 8.2 ? 'pink → base' : 'colourless → acid or neutral') : id === 'methylorange' ? (p < 3.1 ? 'red → acid' : p > 4.4 ? 'yellow → neutral or base' : 'orange') : `pH ${fmt(p, 0)} → ${p < 6.5 ? 'acid' : p > 7.5 ? 'base' : 'neutral'}`}`);
      }
    }
    badge.set(verdict.el.querySelector('.ix-readout-value') ? verdict.el.querySelector('.ix-readout-value').textContent : 'Tested');
  }
  render();

  const v3 = new THREE.Vector3();
  engine.setUpdate((dt) => {
    controls.update(dt);
    dropper.visible = false; drop.visible = false;
    if (anim) {
      anim.t += dt; const t = tubes[anim.i];
      t.g.getWorldPosition(v3); world.worldToLocal(v3);
      if (anim.kind === 'paper') { const k = Math.min(1, anim.t / 0.5); t.paper.position.y = 1.2 - 0.6 * k * k; if (anim.t > 0.6) { render(); anim = null; } }
      else {
        dropper.visible = true; dropper.position.set(v3.x, 1.55, v3.z);
        if (anim.t > 0.4) { drop.visible = anim.t < 0.9; drop.position.set(v3.x, 1.3 - (anim.t - 0.4) * 1.8, v3.z); }
        if (anim.t > 0.9 && !anim.done) { anim.done = true; render(); }
        if (anim.t > 1.3) anim = null;
      }
    }
  });
  engine.start();

  stage.__indicators = { apply, state: () => state.map((s) => pHof(s.c)) };
  return { dispose() { panel.dispose(); hud.dispose(); L.dispose(); } };
}
