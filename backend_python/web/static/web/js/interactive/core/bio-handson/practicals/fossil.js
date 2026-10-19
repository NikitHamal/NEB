// Fossils as evidence of evolution. A tray of museum casts — a trilobite, a Devonian fish, a leaf of
// Glossopteris, a saligram (an ammonite from the Kali Gandaki, sacred in Nepal) and a cast of
// Archaeopteryx. The student studies each with a hand lens, names it, places it in its period on
// the geological time scale by its age, and draws the conclusions: older rocks hold simpler life,
// connecting links join groups, and marine fossils high in the Himalaya show it rose from the sea.
import { THREE } from '../../engine.js';
import { createLens } from '../lens.js';
import { enamelTray, ask, sheet, chipDrop, tag } from '../bench.js';
import { mesh, MAT, canvasTexture, rng, wet } from '../kit.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const PERIODS = [['Cambrian', 541], ['Ordovician', 485], ['Silurian', 444], ['Devonian', 419], ['Carboniferous', 359], ['Permian', 299], ['Triassic', 252], ['Jurassic', 201], ['Cretaceous', 145], ['Paleogene', 66], ['Neogene', 23], ['Quaternary', 2.6]];
const FOSSILS = [
  { id: 'trilobite', name: 'Trilobite', period: 'Cambrian', age: '≈ 520 million years', fact: 'Trilobite: a marine arthropod with a body in three lobes (axial and two pleural) and many segments; among the first animals with hard parts and eyes.' },
  { id: 'fish', name: 'Fossil fish', period: 'Devonian', age: '≈ 390 million years', fact: 'A bony fish of the Devonian, the “Age of Fishes”: backbone, fin rays and scales preserved as an impression.' },
  { id: 'glosso', name: 'Glossopteris leaf', period: 'Permian', age: '≈ 270 million years', fact: 'Glossopteris: a seed fern with tongue-shaped leaves and net veins. Found in India, Africa, South America, Antarctica and Australia — evidence they were once joined as Gondwana.' },
  { id: 'saligram', name: 'Saligram (ammonite)', period: 'Jurassic', age: '≈ 150 million years', fact: 'Saligram: an ammonite, a coiled marine cephalopod, in a black nodule from the Kali Gandaki. The chambered shell shows septa meeting the wall in wavy sutures. Sea animals high in the Himalaya: the mountains were the floor of the Tethys Sea.' },
  { id: 'archae', name: 'Archaeopteryx', period: 'Jurassic', age: '≈ 150 million years', fact: 'Archaeopteryx: feathers and wings like a bird, but teeth, clawed fingers and a long bony tail like a reptile — a connecting link between reptiles and birds.' },
];

function slabTex(id) {
  return canvasTexture(`fossil:${id}`, 512, 512, (g, w, h) => {
    const R = rng(id.length * 13);
    g.fillStyle = id === 'archae' ? '#d9c9a3' : id === 'glosso' ? '#6b6258' : '#bfb39b'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 2500; i++) { g.fillStyle = `rgba(${R() < 0.5 ? '255,255,255' : '0,0,0'},${R() * 0.08})`; g.fillRect(R() * w, R() * h, 2 + R() * 4, 2 + R() * 4); }
    g.strokeStyle = 'rgba(60,45,30,0.75)'; g.fillStyle = 'rgba(80,60,40,0.35)'; g.lineCap = 'round';
    if (id === 'fish') {
      g.lineWidth = 6; g.beginPath(); g.moveTo(90, 260); g.quadraticCurveTo(260, 230, 420, 255); g.stroke();
      g.beginPath(); g.ellipse(250, 255, 170, 62, -0.05, 0, Math.PI * 2); g.fill();
      g.lineWidth = 2.4; for (let x = 120; x < 400; x += 12) { g.beginPath(); g.moveTo(x, 210); g.lineTo(x + 4, 300); g.stroke(); }
      g.beginPath(); g.moveTo(420, 255); g.lineTo(480, 200); g.lineTo(470, 255); g.lineTo(482, 315); g.closePath(); g.fill(); g.stroke();
      g.beginPath(); g.arc(110, 245, 10, 0, 6.28); g.stroke();
      for (const [x, y, a] of [[250, 195, -1], [300, 320, 1], [190, 315, 1]]) { g.beginPath(); for (let k = 0; k < 6; k++) { g.moveTo(x, y); g.lineTo(x + k * 6 - 15, y + a * 40); } g.stroke(); }
    } else if (id === 'glosso') {
      g.strokeStyle = 'rgba(30,25,20,0.85)'; g.fillStyle = 'rgba(40,35,28,0.5)'; g.lineWidth = 4;
      g.beginPath(); g.moveTo(256, 470); g.bezierCurveTo(120, 380, 130, 120, 256, 40); g.bezierCurveTo(382, 120, 392, 380, 256, 470); g.fill(); g.stroke();
      g.lineWidth = 5; g.beginPath(); g.moveTo(256, 470); g.lineTo(256, 60); g.stroke();
      g.lineWidth = 1.2; for (let y = 80; y < 450; y += 9) for (const s of [-1, 1]) { g.beginPath(); g.moveTo(256, y); g.quadraticCurveTo(256 + s * 50, y - 20, 256 + s * (100 - Math.abs(y - 260) * 0.25), y - 50); g.stroke(); }
    } else if (id === 'archae') {
      g.strokeStyle = 'rgba(90,60,35,0.9)'; g.lineWidth = 7;
      g.beginPath(); g.moveTo(140, 330); g.quadraticCurveTo(200, 260, 260, 270); g.stroke();
      g.beginPath(); g.arc(120, 340, 26, 0, 6.28); g.stroke(); g.lineWidth = 3; for (let k = 0; k < 6; k++) { g.beginPath(); g.moveTo(98 + k * 7, 355); g.lineTo(98 + k * 7, 364); g.stroke(); }
      g.lineWidth = 6; g.beginPath(); g.moveTo(260, 270); g.lineTo(420, 300); g.stroke();
      for (let k = 0; k < 18; k++) { g.lineWidth = 2; g.beginPath(); g.moveTo(270 + k * 9, 272 + k * 1.6); g.lineTo(290 + k * 10, 330 + k * 2); g.stroke(); }
      g.lineWidth = 5; g.beginPath(); g.moveTo(230, 270); g.lineTo(190, 160); g.lineTo(120, 110); g.stroke();
      for (let k = 0; k < 16; k++) { g.lineWidth = 2.2; g.beginPath(); g.moveTo(200 - k * 5, 160 - k * 4); g.lineTo(260 - k * 2, 60 + k * 4); g.stroke(); }
      for (const [x, y] of [[120, 110], [110, 120], [128, 102]]) { g.lineWidth = 3; g.beginPath(); g.moveTo(x, y); g.lineTo(x - 20, y - 8); g.stroke(); }
      g.lineWidth = 5; g.beginPath(); g.moveTo(330, 290); g.lineTo(350, 380); g.lineTo(390, 420); g.stroke(); g.beginPath(); g.moveTo(300, 285); g.lineTo(300, 390); g.lineTo(340, 430); g.stroke();
    }
  });
}

function trilobite() {
  const g = new THREE.Group(); const m = wet(0x6b5d4a, { roughness: 0.75, clearcoat: 0.15 });
  g.add(mesh(new THREE.BoxGeometry(0.8, 0.08, 0.6), MAT.matte(0x9c8f78), [0, 0.04, 0]));
  const ceph = mesh(new THREE.SphereGeometry(0.17, 18, 10, 0, Math.PI * 2, 0, Math.PI / 2), m, [0, 0.08, -0.14]); ceph.scale.set(1.2, 0.35, 0.7); g.add(ceph);
  for (let i = 0; i < 9; i++) { const z = -0.05 + i * 0.032; const w = 0.19 - i * 0.008; [-1, 0, 1].forEach((s) => { const seg = mesh(new THREE.CapsuleGeometry ? new THREE.CapsuleGeometry(0.012, s ? w * 0.6 : 0.05, 3, 6) : new THREE.CylinderGeometry(0.012, 0.012, 0.08, 6), m, [s * (w * 0.55), 0.09, z]); seg.rotation.z = Math.PI / 2; g.add(seg); }); }
  const py = mesh(new THREE.SphereGeometry(0.1, 14, 8, 0, Math.PI * 2, 0, Math.PI / 2), m, [0, 0.08, 0.27]); py.scale.set(1, 0.3, 0.7); g.add(py);
  [-1, 1].forEach((s) => g.add(mesh(new THREE.SphereGeometry(0.02, 8, 6), MAT.gloss(0x2b2118), [s * 0.08, 0.12, -0.16])));
  return g;
}
function ammonite() {
  const g = new THREE.Group(); const stone = wet(0x1f1d1b, { roughness: 0.35, clearcoat: 0.6 });
  const pts = []; for (let i = 0; i <= 160; i++) { const a = i / 160 * Math.PI * 2 * 3.2; const r = 0.03 * Math.exp(a * 0.13); pts.push(new THREE.Vector3(Math.cos(a) * r, 0, Math.sin(a) * r)); }
  const geo = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 220, 0.05, 10, false);
  const p = geo.attributes.position; const v = new THREE.Vector3(); for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); const s = Math.hypot(v.x, v.z); const k = Math.min(1, s / 0.34); p.setXYZ(i, v.x, v.y * (0.4 + 0.9 * k), v.z); } geo.computeVertexNormals();
  const coil = mesh(geo, stone); coil.scale.set(1.15, 1, 1.15); coil.position.y = 0.09; g.add(coil);
  for (let i = 0; i < 26; i++) { const a = 5.2 + i * 0.6; const r = 0.03 * Math.exp(a * 0.13) * 1.15; g.add(mesh(new THREE.TorusGeometry(0.05 * (0.4 + 0.9 * Math.min(1, r / 0.34)), 0.006, 4, 10, Math.PI), MAT.gloss(0x8a7f70), [Math.cos(a) * r, 0.09, Math.sin(a) * r]).rotateY(-a)); }
  const nod = mesh(new THREE.SphereGeometry(0.45, 20, 12, 0, Math.PI * 2, 0, Math.PI / 2), stone, [0, 0.0, 0]); nod.scale.set(1, 0.2, 1); g.add(nod);
  return g;
}

export function create(ctx) {
  const { world, input, anim, sfx, ui, tools } = ctx;
  const tray = enamelTray(3.4, 1.4); tray.position.set(0, 0, 0.1); world.add(tray);
  const lens = createLens(ctx, { mag: 2.6, groundY: ctx.BENCH_Y + 0.08 });
  const objs = FOSSILS.map((f, i) => {
    let o;
    if (f.id === 'trilobite') o = trilobite(); else if (f.id === 'saligram') o = ammonite();
    else { o = new THREE.Group(); o.add(mesh(new THREE.BoxGeometry(0.62, 0.08, 0.62), [MAT.matte(0x9c8f78), MAT.matte(0x9c8f78), new THREE.MeshStandardMaterial({ map: slabTex(f.id), roughness: 0.9 }), MAT.matte(0x9c8f78), MAT.matte(0x9c8f78), MAT.matte(0x9c8f78)], [0, 0.04, 0])); }
    o.position.set(-1.32 + i * 0.66, 0.02, 0.1); o.rotation.y = (i % 2 ? 0.15 : -0.1); world.add(o);
    const t = tag(String(i + 1), { h: 0.08 }); t.position.set(-1.32 + i * 0.66, 0.35, 0.55); world.add(t);
    return Object.assign(o, { f });
  });
  const TRAY = S([0, 2.3, 2.3], [0, 0.1, 0.2], 4.0);
  const seen = new Set(); let dwellOn = null; let dwell = 0; const named = new Set(); let sh = null; let dz = null;
  const stepLens = {
    title: 'Examine the fossils', text: 'Hold the <b>hand lens</b> over each of the five fossils in turn and let it rest.', tool: 'lens', shot: TRAY,
    aim(p, out) { return input.planePoint(ctx.BENCH_Y + 0.1, out) || false; },
    skip() { objs.forEach((o) => seen.add(o.f.id)); },
    update(dt) {
      if (!lens.active) { dwell = 0; return; }
      const tip = tools.tip; const o = objs.find((q) => { const p = q.getWorldPosition(new THREE.Vector3()); return Math.hypot(p.x - tip.x, p.z - tip.z) < 0.3; });
      const id = o ? o.f.id : null; if (id && id === dwellOn) dwell += dt; else { dwellOn = id; dwell = 0; }
      if (id && dwell > 0.6 && !seen.has(id)) { seen.add(id); sfx.play('ok'); ctx.say(`<b>${objs.indexOf(o) + 1}.</b> ${DESCR[id]}`, 'good', 5200); ctx.progress(seen.size / 5); if (seen.size === 5) anim.wait(2.5, () => ctx.next()); }
    },
    handler: { down() { return ui.tool === 'lens'; } },
  };
  const DESCR = { trilobite: 'A flattened, segmented body divided lengthwise into three lobes, a head shield with eyes, a tail piece.', fish: 'An impression of a backbone with ribs, fin rays and a forked tail.', glosso: 'A tongue-shaped leaf with a midrib and a fine network of veins.', saligram: 'A black, polished stone with a tightly coiled, ribbed spiral shell; wavy lines (sutures) mark the chambers.', archae: 'A skeleton with feathered wings and a long feathered bony tail; the jaws have teeth and the wings clawed fingers.' };
  const stepName = {
    title: 'Name each fossil', text: 'Tap each fossil and choose its name.', tool: null, autoTool: 'hand', hideBelt: true, shot: TRAY,
    skip() { objs.forEach((o) => named.add(o.f.id)); },
    handler: { down(p) {
      const o = objs.find((q) => !named.has(q.f.id) && input.pick([q], true)); if (!o) return false;
      ui.choose(p.x, p.y, `Fossil ${objs.indexOf(o) + 1}`, FOSSILS.map((f) => ({ label: f.name, value: f.id })).sort(() => Math.random() - 0.5), (v) => {
        if (v !== o.f.id) { ctx.mistake('Look again at its shape: coiled shell, three lobes, leaf veins, feathers, or fins?', 2); return; }
        named.add(v); sfx.play('ok'); ctx.say(o.f.fact, 'good', 6000); ui.observe(`${objs.indexOf(o) + 1}. ${o.f.name}`, o.f.age); ctx.progress(named.size / 5); if (named.size === 5) anim.wait(2.2, () => ctx.next());
      });
      return true;
    } },
    exit() { ui.clearChooser(); },
  };
  const stepTime = {
    title: 'Place them on the geological time scale', text: 'Drag each fossil into the period of its rocks (or tap it, then the period). Oldest rocks are at the bottom.', tool: null, autoTool: 'hand', hideBelt: true, shot: TRAY,
    enter() {
      sh = sheet(ctx, { title: 'Geological time scale (Ma = million years ago)', cls: 'wide' });
      const rows = PERIODS.slice().reverse().map(([n, a]) => `<div style="display:flex;gap:6px;align-items:center"><span style="width:118px;font-size:.7rem"><b>${n}</b> ${a} Ma</span><div class="bh-slot" data-slot="${n}" style="flex:1;min-height:24px"></div></div>`).join('');
      sh.set(`<div class="bh-dtray"></div><div style="display:flex;flex-direction:column;gap:3px">${rows}</div>`);
      let n = 0;
      dz = chipDrop(ctx, sh.body.querySelector('.bh-dtray'), FOSSILS.map((f) => ({ id: f.id, html: `${f.name} <small>(${f.age})</small>` })), sh.body, (id, slot, chipEl, slotEl) => {
        const f = FOSSILS.find((q) => q.id === id); if (f.period !== slot) { ctx.mistake(`${f.name} is ${f.age} old. Find the period whose start and end bracket that age.`, 1); return false; }
        slotEl.appendChild(chipEl); n += 1; if (n === FOSSILS.length) anim.wait(0.8, () => ctx.next('Trilobites at the bottom, then fish, then seed ferns, then ammonites and the first birds.')); return true;
      });
    },
    skip() { },
    exit() { if (dz) dz.dispose(); if (sh) { sh.remove(); sh = null; } },
  };
  const stepEvidence = {
    title: 'What do the fossils tell us?', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: TRAY,
    enter() {
      ask(ctx, 'Archaeopteryx is called a connecting link because…', [{ label: 'It has both reptile (teeth, tail, claws) and bird (feathers, wings) characters', value: 'ok' }, { label: 'It is the oldest fossil', value: 'o' }, { label: 'It lived in the sea', value: 's' }], 'ok', {
        wrong: 'Look at its mix of characters.',
        then() { ask(ctx, 'Why are saligrams found high in the Himalaya?', [{ label: 'The rocks formed under the Tethys Sea and were lifted up as the Himalaya rose', value: 'ok' }, { label: 'Pilgrims carried them up', value: 'p' }, { label: 'Ammonites lived on mountains', value: 'm' }], 'ok', { delay: 0.3, ok: 'Fossils are palaeontological evidence of evolution: life in older rocks is simpler and different from today, groups appear in a sequence (fish → amphibians → reptiles → birds and mammals), connecting links show transitions, and marine fossils on mountains record great changes of Earth itself.', wrong: 'Ammonites were sea animals.' }); },
      });
    },
    exit() { ui.clearChooser(); },
  };
  const steps = [stepLens, stepName, stepTime, stepEvidence];
  ctx.debug = { objs };
  return {
    tools: ['hand', 'lens'],
    steps,
    update() { lens.update(); },
    result() { return { title: 'Fossils as evidence of evolution', rows: FOSSILS.map((f) => [f.name, `${f.period}, ${f.age}`]), conclusion: 'Fossils are the remains or impressions of past life preserved in sedimentary rock. Their order in the rocks shows life changing through time from simple to complex; transitional forms such as Archaeopteryx link major groups; and Nepal\'s saligrams — Jurassic ammonites from the Kali Gandaki — show that the Himalaya rose from the floor of the ancient Tethys Sea.' }; },
    dispose() { lens.dispose(); if (dz) dz.dispose(); if (sh) sh.remove(); ui.clearChooser(); },
  };
}
