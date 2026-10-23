// Biodiversity conservation in Nepal, on a raised relief map. The student places threatened
// animals in the protected areas that hold them, sorts conservation measures into in-situ and
// ex-situ, matches each threat to a remedy, and works out how much Nepal's rhinos and tigers have
// recovered from census figures — then writes the conclusion of a conservation report.
import { THREE } from '../../engine.js';
import { ask, sheet, chipDrop, table } from '../bench.js';
import { mesh, MAT, canvasTexture, smooth } from '../kit.js';

const S = (pos, target, fit, fitH) => ({ pos: [pos[0], pos[1] + 0.8, pos[2]], target: [target[0], target[1] + 0.8, target[2]], fit, fitH });
const OUTLINE = [[80.06, 28.84], [80.25, 29.45], [80.55, 29.75], [80.95, 30.2], [81.25, 30.05], [81.55, 30.42], [82.1, 30.35], [82.7, 29.75], [83.35, 29.35], [83.8, 29.25], [84.25, 28.95], [84.85, 28.6], [85.2, 28.55], [85.75, 28.3], [86.1, 28.1], [86.55, 27.95], [87.1, 27.85], [87.7, 27.9], [88.15, 27.85], [88.2, 27.4], [88.05, 26.95], [88.15, 26.5], [87.85, 26.4], [87.25, 26.4], [86.7, 26.45], [86.05, 26.62], [85.55, 26.82], [85.15, 26.85], [84.65, 27.1], [84.2, 27.4], [83.8, 27.4], [83.3, 27.35], [82.75, 27.5], [82.1, 27.8], [81.7, 27.95], [81.25, 28.3], [80.8, 28.45], [80.4, 28.65]];
const PARKS = {
  chitwan: ['Chitwan NP', 84.4, 27.5], bardia: ['Bardia NP', 81.45, 28.45], sukla: ['Shuklaphanta NP', 80.3, 28.85], koshi: ['Koshi Tappu WR', 87.0, 26.65],
  sagar: ['Sagarmatha NP', 86.75, 27.95], lang: ['Langtang NP', 85.55, 28.15], shey: ['Shey-Phoksundo NP', 82.9, 29.2], rara: ['Rara NP', 82.08, 29.53],
  anna: ['Annapurna CA', 83.9, 28.65], kanch: ['Kanchenjunga CA', 87.9, 27.7], zoo: ['Central Zoo', 85.31, 27.67],
};
const SPECIES = [
  ['One-horned rhinoceros', ['chitwan', 'bardia', 'sukla'], 'Greater one-horned rhino: Chitwan holds most of Nepal\'s rhinos (translocated to Bardia and Shuklaphanta).'],
  ['Bengal tiger', ['bardia', 'chitwan', 'sukla'], 'Royal Bengal tiger: Chitwan, Bardia, Banke, Parsa and Shuklaphanta in the Terai Arc.'],
  ['Wild water buffalo (arna)', ['koshi'], 'Wild water buffalo: Nepal\'s last wild herd lives in Koshi Tappu Wildlife Reserve.'],
  ['Swamp deer (barasingha)', ['sukla'], 'Swamp deer: the largest herd is in the grasslands of Shuklaphanta.'],
  ['Red panda', ['rara', 'lang', 'kanch'], 'Red panda: bamboo forests of Rara, Langtang and Kanchenjunga.'],
  ['Snow leopard', ['shey', 'sagar', 'anna', 'kanch'], 'Snow leopard: high Himalaya — Shey-Phoksundo, Sagarmatha, Annapurna, Kanchenjunga.'],
  ['Gharial crocodile', ['chitwan'], 'Gharial: Narayani and Rapti rivers in Chitwan, restocked from the breeding centre at Kasara.'],
];

function mapTex() {
  return canvasTexture('nepal-relief', 1024, 512, (g, w, h) => {
    const X = (lon) => (lon - 79.9) / 8.4 * w; const Y = (lat) => (30.6 - lat) / 4.4 * h;
    g.clearRect(0, 0, w, h); g.save(); g.beginPath(); OUTLINE.forEach(([lo, la], i) => (i ? g.lineTo(X(lo), Y(la)) : g.moveTo(X(lo), Y(la)))); g.closePath(); g.clip();
    for (let y = 0; y < h; y += 2) { const lat = 30.6 - y / h * 4.4; const t = lat; for (let x = 0; x < w; x += 8) { const lon = 79.9 + x / w * 8.4; const n = Math.sin(lon * 7.1) * Math.cos(lat * 6.3) * 0.25; const north = t - (28.0 + (lon - 80) * -0.13); g.fillStyle = north > 0.9 + n ? '#f1f5f9' : north > 0.45 + n ? '#a8a29e' : north > -0.25 + n ? '#8a9a5b' : north > -0.75 + n ? '#5d8c3a' : '#9dbb5a'; g.fillRect(x, y, 8, 2); } }
    g.strokeStyle = 'rgba(59,130,246,0.75)'; g.lineWidth = 3; [[83.6, 29.2, 84.3, 27.6], [85.0, 28.4, 84.4, 27.6], [86.9, 28.0, 87.0, 26.6], [81.3, 29.6, 81.3, 28.4], [80.6, 29.8, 80.2, 28.9]].forEach(([a, b, c, d]) => { g.beginPath(); g.moveTo(X(a), Y(b)); g.quadraticCurveTo(X((a + c) / 2) + 15, Y((b + d) / 2), X(c), Y(d)); g.stroke(); });
    g.restore(); g.strokeStyle = '#7f1d1d'; g.lineWidth = 3; g.beginPath(); OUTLINE.forEach(([lo, la], i) => (i ? g.lineTo(X(lo), Y(la)) : g.moveTo(X(lo), Y(la)))); g.closePath(); g.stroke();
  });
}
const MW = 4.2; const MD = MW * 4.4 / 8.4;
const P2 = (lon, lat) => [(lon - 79.9) / 8.4 * MW - MW / 2, (30.6 - lat) / 4.4 * MD - MD / 2];
function elev(lon, lat) { const north = lat - (28.0 + (lon - 80) * -0.13); return 0.02 + smooth(-0.8, -0.2, north) * 0.06 + smooth(-0.2, 0.6, north) * 0.12 + smooth(0.5, 1.2, north) * 0.2 + Math.max(0, Math.sin(lon * 7.1) * Math.cos(lat * 6.3)) * 0.04 * smooth(0, 1, north); }

export function create(ctx) {
  const { world, anim, sfx, ui, input } = ctx;
  const geo = new THREE.PlaneGeometry(MW, MD, 168, 88); geo.rotateX(-Math.PI / 2);
  const p = geo.attributes.position; for (let i = 0; i < p.count; i++) { const x = p.getX(i); const z = p.getZ(i); const lon = 79.9 + (x + MW / 2) / MW * 8.4; const lat = 30.6 - (z + MD / 2) / MD * 4.4; p.setY(i, elev(lon, lat)); } geo.computeVertexNormals();
  const relief = mesh(geo, new THREE.MeshStandardMaterial({ map: mapTex(), transparent: true, alphaTest: 0.5, roughness: 0.8 }), [0, 0.06, 0.1]); world.add(relief);
  world.add(mesh(new THREE.BoxGeometry(MW + 0.3, 0.06, MD + 0.3), MAT.gloss(0x334155), [0, 0.03, 0.1]));
  const pins = {}; Object.entries(PARKS).forEach(([k, [, lon, lat]]) => { const [x, z] = P2(lon, lat); const y = 0.06 + elev(lon, lat); const pin = new THREE.Group(); pin.position.set(x, y, z + 0.1); pin.add(mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.14, 6), MAT.steel(), [0, 0.07, 0])); pin.add(mesh(new THREE.SphereGeometry(0.025, 10, 8), MAT.gloss(k === 'zoo' ? 0x7c3aed : 0xdc2626), [0, 0.15, 0])); world.add(pin); pins[k] = pin; });
  const layer = document.createElement('div'); layer.className = 'bh-jlayer'; ui.root.appendChild(layer);
  const pills = Object.entries(PARKS).map(([k, [name]]) => { const d = document.createElement('div'); d.className = 'bh-park'; d.dataset.slot = k; d.innerHTML = `<b>${name}</b><span></span>`; layer.appendChild(d); return [k, d]; });
  const v = new THREE.Vector3(); const MAP = S([0, 3.4, 3.0], [0.2, 0.1, 0.3], MW + 1.3, MD + 1.0);
  let sh = null; let dz = null; let dz2 = null;
  const stepSpecies = {
    title: 'Where do they live?', text: 'Drag each threatened animal onto a protected area that conserves it (or tap the animal, then the area).', tool: null, autoTool: 'hand', hideBelt: true, shot: MAP,
    enter() {
      layer.classList.add('on'); sh = sheet(ctx, { title: 'Threatened animals of Nepal', cls: 'left' }); sh.set('<div class="bh-dtray"></div>');
      let n = 0; dz = chipDrop(ctx, sh.body.querySelector('.bh-dtray'), SPECIES.map(([nm]) => ({ id: nm, html: nm })), layer, (id, slot, chipEl, slotEl) => {
        const sp = SPECIES.find((q) => q[0] === id); if (!sp[1].includes(slot)) { ctx.mistake(slot === 'zoo' ? 'The zoo is ex-situ; find the protected area where it lives in the wild.' : `Not ${PARKS[slot][0]}: think about the habitat — Terai grassland, wetland, mountain forest or high Himalaya?`, 2); return false; }
        slotEl.querySelector('span').textContent += `${slotEl.querySelector('span').textContent ? ', ' : ''}${id.split(' (')[0]}`; chipEl.remove(); n += 1; ctx.say(sp[2], 'good', 4200); ui.observe(id, PARKS[slot][0]); ctx.progress(n / SPECIES.length);
        if (n === SPECIES.length) anim.wait(1, () => ctx.next()); return true;
      });
    },
    skip() { SPECIES.forEach(([nm, parks]) => ui.observe(nm, PARKS[parks[0]][0])); },
    exit() { if (dz) dz.dispose(); if (sh) { sh.remove(); sh = null; } },
  };
  const MEAS = [['National parks and wildlife reserves', 'in'], ['Conservation areas (Annapurna, Kanchenjunga)', 'in'], ['Buffer-zone community forests', 'in'], ['Ramsar wetlands (Koshi Tappu, Rara)', 'in'], ['Central Zoo, Jawalakhel', 'ex'], ['National Botanical Garden, Godawari', 'ex'], ['Gharial breeding centre, Kasara', 'ex'], ['Seed and gene bank', 'ex'], ['Tissue culture of orchids', 'ex']];
  const stepSites = {
    title: 'In-situ or ex-situ?', text: 'Sort each conservation measure: in the natural habitat (in-situ) or outside it (ex-situ).', tool: null, autoTool: 'hand', hideBelt: true, shot: MAP,
    enter() {
      layer.classList.remove('on'); sh = sheet(ctx, { title: 'Conservation measures', cls: 'wide' });
      sh.set('<div class="bh-dtray"></div><div style="display:flex;gap:6px"><div style="flex:1"><b style="font-size:.72rem">In-situ</b><div class="bh-slot" data-slot="in" style="min-height:90px;align-content:flex-start"></div></div><div style="flex:1"><b style="font-size:.72rem">Ex-situ</b><div class="bh-slot" data-slot="ex" style="min-height:90px;align-content:flex-start"></div></div></div>');
      let n = 0; dz2 = chipDrop(ctx, sh.body.querySelector('.bh-dtray'), MEAS.map(([m]) => ({ id: m, html: m })), sh.body, (id, slot, chipEl, slotEl) => {
        const want = MEAS.find((q) => q[0] === id)[1]; if (want !== slot) { ctx.mistake(want === 'in' ? 'This protects species where they naturally live: in-situ.' : 'This keeps species or their genes away from their natural habitat: ex-situ.', 2); return false; }
        slotEl.appendChild(chipEl); n += 1; if (n === MEAS.length) anim.wait(0.8, () => ctx.next('In-situ conservation protects whole ecosystems; ex-situ is a back-up for species in danger.')); return true;
      });
    },
    exit() { if (dz2) dz2.dispose(); if (sh) { sh.remove(); sh = null; } },
  };
  const THREATS = [['Poaching of rhinos for their horn', 'Armed anti-poaching patrols and strict punishment'], ['Loss of forest corridors between parks', 'Restore corridors such as Barandabhar and Khata'], ['Crop raiding by wild animals', 'Buffer-zone programmes and compensation for losses'], ['Spread of the invasive Mikania vine', 'Uproot invasive plants from grasslands'], ['Illegal trade in pangolin scales', 'Enforce CITES and wildlife-trade laws']];
  let ti = 0;
  const stepThreats = {
    title: 'Threats and remedies', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: MAP,
    enter() { ti = 0; this.askOne(); },
    askOne() {
      const [t, a] = THREATS[ti]; const opts = THREATS.map((q) => q[1]).sort(() => Math.random() - 0.5);
      ask(ctx, `Threat: ${t}. Best action?`, opts.map((o) => ({ label: o, value: o })), a, { delay: 0.3, wrong: 'Choose the action that removes this particular threat.', then: () => { ui.observe(t.split(' ').slice(0, 4).join(' ') + '…', 'remedied'); ti += 1; if (ti < THREATS.length) stepThreats.askOne(); else ctx.next(); } });
    },
    exit() { ui.clearChooser(); },
  };
  const stepCensus = {
    title: 'Is conservation working?', text: '', tool: null, autoTool: 'hand', hideBelt: true, shot: MAP,
    enter() {
      sh = sheet(ctx, { title: 'National census counts' }); sh.set(table(['Species', 'Earlier count', 'Recent count'], [['One-horned rhino', '409 (2011)', '752 (2021)'], ['Bengal tiger', '121 (2010)', '355 (2022)']]));
      const right = Math.round((355 - 121) / 121 * 100);
      ask(ctx, 'Tigers increased by about…', [right, Math.round(355 / 121 * 100), Math.round((355 - 121) / 355 * 100), 234].map((x) => ({ label: `${x} %`, value: x })), right, {
        wrong: 'Increase % = (new − old) ÷ old × 100.',
        then() { ui.observe('Tiger increase', `${right} % (nearly tripled)`); ask(ctx, 'The best long-term strategy for Nepal\'s biodiversity is…', [{ label: 'Protected areas with community participation, corridors and law enforcement, backed by ex-situ programmes', value: 'ok' }, { label: 'Keeping every threatened animal in zoos', value: 'z' }, { label: 'Banning people from all forests', value: 'b' }], 'ok', { delay: 0.3, ok: 'Nepal\'s success comes from protected areas (about 24 % of the country), buffer zones and community forests that share benefits with local people, wildlife corridors, the army\'s anti-poaching work, and ex-situ breeding (gharial, vultures) as a back-up.', wrong: 'Zoos cannot keep whole ecosystems; excluding people loses their support.' }); },
      });
    },
    exit() { ui.clearChooser(); if (sh) { sh.remove(); sh = null; } },
  };
  const steps = [stepSpecies, stepSites, stepThreats, stepCensus];
  ctx.debug = { pins };
  void input; void sfx;
  return {
    tools: ['hand'],
    steps,
    update() {
      if (!layer.classList.contains('on')) return; const w = ctx.stage.clientWidth; const h = ctx.stage.clientHeight;
      pills.forEach(([k, d]) => { pins[k].getWorldPosition(v); v.y += 0.17; ctx.input.project(v, v, w, h); d.style.transform = `translate(${Math.round(v.x)}px, ${Math.round(v.y)}px)`; });
    },
    result() { return { title: 'Biodiversity conservation in Nepal', rows: [['Species placed', `${SPECIES.length}`], ['Measures sorted', `${MEAS.length} (in-situ / ex-situ)`], ['Tiger recovery', '121 → 355 (≈ 193 %)'], ['Rhino recovery', '409 → 752 (≈ 84 %)']], conclusion: 'Nepal conserves its biodiversity mainly in-situ — national parks, wildlife reserves, conservation areas, buffer zones, community forests and Ramsar wetlands — supported by ex-situ measures such as the zoo, botanical gardens, breeding centres and gene banks. Matching each threat with its remedy, and involving local communities, has let rhino and tiger numbers recover.' }; },
    dispose() { layer.remove(); if (dz) dz.dispose(); if (dz2) dz2.dispose(); if (sh) sh.remove(); ui.clearChooser(); },
  };
}
