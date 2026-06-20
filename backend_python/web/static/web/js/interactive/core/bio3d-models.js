import { THREE, makeLabelSprite } from './engine.js';

const MATERIAL_CACHE = new Map();

function mat(color, opts = {}) {
  const key = JSON.stringify([color, opts]);
  if (MATERIAL_CACHE.has(key)) return MATERIAL_CACHE.get(key);
  const m = new THREE.MeshStandardMaterial({
    color,
    roughness: opts.roughness ?? 0.55,
    metalness: opts.metalness ?? 0.05,
    transparent: opts.opacity !== undefined && opts.opacity < 1,
    opacity: opts.opacity ?? 1,
    emissive: opts.emissive ?? 0x000000,
    emissiveIntensity: opts.emissiveIntensity ?? 0,
    side: opts.side ?? THREE.FrontSide,
  });
  MATERIAL_CACHE.set(key, m);
  return m;
}
function glass(color = 0xbde3ff, opacity = 0.28) { return mat(color, { opacity, roughness: 0.08, metalness: 0.02, side: THREE.DoubleSide }); }
function metal(color = 0x94a3b8) { return mat(color, { roughness: 0.25, metalness: 0.72 }); }
function organic(color = 0x65a30d) { return mat(color, { roughness: 0.82, metalness: 0.0 }); }
function box(w, h, d, material, pos = [0, 0, 0]) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material); m.position.set(...pos); return m; }
function cyl(r1, r2, h, material, pos = [0, 0, 0], seg = 32) { const m = new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, seg), material); m.position.set(...pos); return m; }
function sphere(r, material, pos = [0, 0, 0], seg = 32) { const m = new THREE.Mesh(new THREE.SphereGeometry(r, seg, Math.max(12, Math.floor(seg / 2))), material); m.position.set(...pos); return m; }
function label(group, text, pos, opts = {}) { const s = makeLabelSprite(String(text), { scale: opts.scale || 0.28, fontSize: opts.fontSize || 34, bg: opts.bg, color: opts.color }); s.position.set(...pos); group.add(s); return s; }
function line(points, color = 0xe5e7eb, width = 1) {
  const geo = new THREE.BufferGeometry().setFromPoints(points);
  const material = new THREE.LineBasicMaterial({ color, linewidth: width, transparent: true, opacity: 0.88 });
  return new THREE.Line(geo, material);
}
function addBench(group) {
  group.add(box(8.8, 0.28, 5.2, mat(0x243244, { roughness: 0.76 }), [0, 0.56, 0]));
  group.add(box(9.2, 0.18, 5.55, mat(0x5b321c, { roughness: 0.82 }), [0, 0.37, 0]));
  for (let i = -4; i <= 4; i += 1) {
    const a = line([new THREE.Vector3(i, 0.715, -2.6), new THREE.Vector3(i, 0.715, 2.6)], 0xffffff);
    a.material.opacity = 0.055;
    const b = line([new THREE.Vector3(-4.4, 0.716, i * 0.58), new THREE.Vector3(4.4, 0.716, i * 0.58)], 0xffffff);
    b.material.opacity = 0.055;
    group.add(a, b);
  }
  label(group, 'NEB Biology 3D practical bench', [-2.8, 0.92, -2.15], { scale: 0.18, fontSize: 28, bg: 'rgba(0,0,0,.55)' });
}
function addTray(group, name = 'specimen tray') {
  group.add(box(3.9, 0.12, 2.25, mat(0xe5e7eb, { roughness: 0.65 }), [0, 0.82, 0]));
  group.add(box(4.05, 0.16, 0.10, mat(0x64748b), [0, 0.93, -1.14]));
  group.add(box(4.05, 0.16, 0.10, mat(0x64748b), [0, 0.93, 1.14]));
  group.add(box(0.10, 0.16, 2.3, mat(0x64748b), [-2.03, 0.93, 0]));
  group.add(box(0.10, 0.16, 2.3, mat(0x64748b), [2.03, 0.93, 0]));
  label(group, name, [-1.22, 1.13, -1.02], { scale: 0.14, fontSize: 24, bg: 'rgba(15,23,42,.7)' });
}
function addSlide(group, x = 0, z = 0, tint = 0xfbcfe8) {
  const slide = box(1.95, 0.025, 0.78, glass(0xdbeafe, 0.34), [x, 1.17, z]);
  group.add(slide);
  group.add(box(0.72, 0.028, 0.5, mat(tint, { opacity: 0.52 }), [x, 1.19, z]));
  group.add(box(0.84, 0.018, 0.6, glass(0xffffff, 0.22), [x, 1.215, z]));
  return slide;
}
function addMicroscope(group, state = {}, opts = {}) {
  const g = new THREE.Group();
  g.position.set(-1.6, 0.72, 0);
  g.add(box(1.55, 0.16, 1.15, metal(0x334155), [0, 0.16, 0]));
  g.add(cyl(0.16, 0.16, 1.65, metal(0x475569), [-0.48, 0.92, 0], 32));
  const arm = cyl(0.075, 0.075, 1.9, metal(0x64748b), [-0.18, 1.55, 0], 32); arm.rotation.z = -0.35; g.add(arm);
  const tube = cyl(0.16, 0.16, 1.15, metal(0x1f2937), [0.15, 2.32, 0], 32); tube.rotation.z = -0.35; g.add(tube);
  const eye = cyl(0.22, 0.18, 0.42, metal(0x0f172a), [0.36, 2.82, 0], 32); eye.rotation.z = -0.35; g.add(eye);
  const nose = cyl(0.26, 0.26, 0.16, metal(0x94a3b8), [0.04, 1.9, 0], 32); nose.rotation.z = Math.PI / 2; g.add(nose);
  for (let i = 0; i < 3; i++) { const o = cyl(0.07, 0.10, 0.5, metal(0xcbd5e1), [0.08 + i * 0.12, 1.68 - i * 0.03, -0.25 + i * 0.25], 24); o.rotation.x = Math.PI / 2; g.add(o); }
  g.add(box(1.25, 0.08, 1.0, metal(0x111827), [0.2, 1.05, 0]));
  addSlide(g, 0.2, 0, opts.tint || 0xf9a8d4);
  const light = sphere(0.18, mat(0xfef3c7, { emissive: 0xfacc15, emissiveIntensity: 0.45 }), [0.2, 0.6, 0], 24); g.add(light);
  const knobL = cyl(0.18, 0.18, 0.16, metal(0x94a3b8), [-0.72, 1.26, 0.48], 24); knobL.rotation.x = Math.PI / 2; g.add(knobL);
  const knobR = cyl(0.12, 0.12, 0.16, metal(0x94a3b8), [-0.72, 1.26, -0.48], 24); knobR.rotation.x = Math.PI / 2; g.add(knobR);
  label(g, 'compound microscope', [0.2, 3.25, 0], { scale: 0.16, fontSize: 26 });
  group.add(g);
  return g;
}
function addMicroscopeField(group, kind, state = {}) {
  const board = box(2.9, 1.9, 0.06, mat(0x020617, { opacity: 0.94 }), [1.88, 2.0, -0.88]);
  board.rotation.x = -0.05;
  group.add(board);
  const rim = cyl(0.78, 0.78, 0.035, metal(0xe5e7eb), [1.88, 2.03, -0.83], 80); rim.rotation.x = Math.PI / 2; group.add(rim);
  const field = cyl(0.735, 0.735, 0.038, mat(0xf8d7e8, { roughness: 0.82 }), [1.88, 2.04, -0.80], 80); field.rotation.x = Math.PI / 2; group.add(field);
  const count = kind.includes('mitosis') ? 38 : kind === 'stomata' ? 28 : 34;
  for (let i = 0; i < count; i++) {
    const a = Math.random() * Math.PI * 2;
    const r = Math.sqrt(Math.random()) * 0.63;
    const x = 1.88 + Math.cos(a) * r;
    const y = 2.04 + Math.sin(a) * r;
    let cell = sphere(0.035 + Math.random() * 0.018, mat(0xbe185d, { opacity: 0.78 }), [x, y, -0.735], 16);
    if (kind === 'stomata') {
      cell = new THREE.Group();
      cell.add(sphere(0.035, organic(0x16a34a), [-0.035, 0, 0], 16));
      cell.add(sphere(0.035, organic(0x16a34a), [0.035, 0, 0], 16));
      cell.add(box(0.025, 0.006, 0.006, mat(0x022c22), [0, 0, 0]));
      cell.position.set(x, y, -0.735); cell.rotation.z = Math.random() * Math.PI;
    } else if (kind.includes('mitosis')) {
      const colors = [0x7c3aed, 0xdb2777, 0x2563eb, 0xea580c, 0x16a34a];
      cell.material = mat(colors[i % colors.length], { opacity: 0.82 });
      cell.scale.set(1.0 + (i % 4) * 0.25, 0.75, 1.0);
    } else if (kind === 'animalTissue') {
      cell.material = mat(i % 3 === 0 ? 0xef4444 : 0xfca5a5, { opacity: 0.8 });
      cell.scale.set(i % 2 ? 1.4 : 0.8, 0.7, 1);
    } else if (kind === 'plasmolysis') {
      cell.material = mat(0x7c3aed, { opacity: 0.72 });
      cell.scale.set(0.72, 0.72, 1);
    }
    group.add(cell);
  }
  label(group, microscopeLabel(kind, state), [1.88, 3.15, -0.82], { scale: 0.15, fontSize: 24 });
}
function microscopeLabel(kind, state) {
  if (kind === 'mitosis' || kind === 'animalMitosis') return 'mitotic stages visible';
  if (kind === 'stomata') return `${state.surface || 'lower'} epidermis stomata`;
  if (kind === 'plasmolysis') return 'plasmolysed cells';
  if (kind === 'anatomyTS') return state.section || 'T.S. section';
  if (kind === 'frogDev') return state.stage || 'frog embryo';
  if (kind === 'animalTissue') return state.tissue || 'animal tissue';
  return 'focused microscope field';
}
function addFlower(group, state = {}) {
  addTray(group, 'flower dissection tray');
  const family = state.family || 'Solanaceae';
  const petalColor = family === 'Liliaceae' ? 0xf8fafc : family === 'Fabaceae' ? 0xec4899 : 0xa855f7;
  group.add(cyl(0.05, 0.06, 1.25, organic(0x15803d), [0, 1.25, 0], 20));
  for (let i = 0; i < 5; i++) {
    const a = (i / 5) * Math.PI * 2;
    const p = sphere(0.34, mat(petalColor, { roughness: 0.66 }), [Math.cos(a) * 0.52, 1.85 + Math.sin(a) * 0.05, Math.sin(a) * 0.52], 32);
    p.scale.set(0.7, 0.13, 1.28); p.rotation.y = -a; group.add(p);
  }
  for (let i = 0; i < 5; i++) { const a = i / 5 * Math.PI * 2; const s = sphere(0.2, organic(0x16a34a), [Math.cos(a) * 0.42, 1.55, Math.sin(a) * 0.42], 24); s.scale.set(0.65, 0.1, 1.1); s.rotation.y = -a; group.add(s); }
  for (let i = 0; i < 6; i++) { const a = i / 6 * Math.PI * 2; const filament = cyl(0.018, 0.018, 0.72, mat(0xfef3c7), [Math.cos(a) * 0.25, 1.82, Math.sin(a) * 0.25], 12); filament.rotation.z = Math.cos(a) * 0.15; group.add(filament); group.add(sphere(0.07, mat(0xf59e0b), [Math.cos(a) * 0.32, 2.17, Math.sin(a) * 0.32], 16)); }
  group.add(cyl(0.035, 0.045, 0.95, mat(0xfde68a), [0, 1.95, 0], 20)); group.add(sphere(0.09, mat(0xfacc15), [0, 2.46, 0], 20)); group.add(sphere(0.15, organic(0x22c55e), [0, 1.48, 0], 24));
  label(group, `${family}: whorls opened`, [0, 2.85, 0], { scale: 0.18, fontSize: 26 });
}
function addInflorescence(group, state = {}) {
  addTray(group, 'inflorescence comparison');
  const type = state.type || 'raceme';
  group.add(cyl(0.035, 0.045, 2.1, organic(0x15803d), [0, 1.75, 0], 18));
  const count = type === 'capitulum' ? 22 : 10;
  for (let i = 0; i < count; i++) {
    let x = 0, y = 1.0 + i * 0.15, z = 0;
    if (type === 'umbel') { const a = i / count * Math.PI * 2; x = Math.cos(a) * 0.82; z = Math.sin(a) * 0.82; y = 2.35; group.add(line([new THREE.Vector3(0, 1.55, 0), new THREE.Vector3(x, y, z)], 0x22c55e)); }
    else if (type === 'capitulum') { const a = i / count * Math.PI * 2; const r = 0.1 + (i % 5) * 0.08; x = Math.cos(a) * r; z = Math.sin(a) * r; y = 2.1 + (i % 3) * 0.02; }
    else if (type === 'spike') { x = 0.16 * (i % 2 ? 1 : -1); y = 1.05 + i * 0.16; }
    else if (type === 'cyme') { x = (i - 5) * 0.16; y = 2.45 - Math.abs(i - 5) * 0.08; z = (i % 2 - 0.5) * 0.4; }
    else { x = (i % 2 ? 0.36 : -0.36); y = 1.0 + i * 0.16; group.add(line([new THREE.Vector3(0, y, 0), new THREE.Vector3(x, y + 0.05, 0)], 0x22c55e)); }
    group.add(sphere(0.09, mat(0xf472b6), [x, y, z], 18));
  }
  label(group, `type: ${type}`, [0, 2.95, 0], { scale: 0.18 });
}
function addHerbarium(group, state = {}) {
  group.add(box(3.2, 0.04, 4.3, mat(0xf8fafc), [0, 0.9, 0]));
  group.add(box(1.1, 0.035, 0.62, mat(0xe2e8f0), [0.85, 0.94, 1.55]));
  group.add(line([new THREE.Vector3(-0.25, 0.98, -1.3), new THREE.Vector3(0, 0.99, -0.5), new THREE.Vector3(0.2, 0.99, 0.6)], 0x14532d));
  for (let i = 0; i < 9; i++) { const a = i / 9 * Math.PI * 2; const leaf = sphere(0.18, organic(0x166534), [Math.cos(a) * 0.42, 1.02, -0.35 + Math.sin(a) * 1.1], 16); leaf.scale.set(1.5, 0.05, 0.55); leaf.rotation.y = -a; group.add(leaf); }
  label(group, `dryness ${state.dryness || 82}%`, [-0.8, 1.35, -1.6], { scale: 0.16 });
}
function addMushroom(group, state = {}) {
  addTray(group, 'mushroom morphology');
  for (let i = 0; i < 4; i++) {
    const x = -1.2 + i * 0.8; const h = 0.55 + i * 0.08;
    group.add(cyl(0.1, 0.14, h, mat(0xf5e7c8), [x, 1.1 + h/2, 0], 24));
    const cap = sphere(0.32, mat(i === 2 && state.volva === 'yes' ? 0xef4444 : 0xb45309), [x, 1.45 + h, 0], 32); cap.scale.y = 0.35; group.add(cap);
    for (let g = 0; g < 7; g++) { const stripe = box(0.018, 0.02, 0.38, mat(0xffedd5), [x + (g-3)*0.05, 1.37 + h, 0]); group.add(stripe); }
    if (i === 2 && state.volva === 'yes') group.add(cyl(0.2, 0.28, 0.14, mat(0xf8fafc), [x, 1.04, 0], 24));
  }
  label(group, `spore print: ${state.sporePrint || 'brown'}`, [0, 2.7, 0], { scale: 0.17 });
}
function addCulture(group, state = {}) {
  addTray(group, 'soil culture plate');
  const plate = cyl(0.86, 0.86, 0.12, glass(0xffffff, 0.36), [0, 1.08, 0], 64); group.add(plate);
  group.add(cyl(0.79, 0.79, 0.025, mat(0xfef3c7, { opacity: 0.72 }), [0, 1.15, 0], 64));
  const colonies = Math.min(70, Math.max(10, state.colonies || 38));
  for (let i = 0; i < colonies; i++) { const a = Math.random()*Math.PI*2; const r = Math.sqrt(Math.random())*0.68; const c = [0xfde68a,0xfca5a5,0xd9f99d,0xf8fafc][i%4]; group.add(sphere(0.018+Math.random()*0.035, mat(c), [Math.cos(a)*r, 1.19, Math.sin(a)*r], 10)); }
  label(group, `${state.colonies || 54} colonies on dilution 10^-${state.dilution || 3}`, [0, 2.28, 0], { scale: 0.17 });
}
function addPond(group, state = {}, zoo = false) {
  const tray = cyl(1.75, 1.75, 0.25, mat(0x334155), [0, 0.92, 0], 64); group.add(tray);
  group.add(cyl(1.65, 1.65, 0.05, mat(0x0ea5e9, { opacity: 0.78, roughness: 0.25 }), [0, 1.08, 0], 64));
  for (let i = 0; i < 18; i++) { const a = Math.random()*Math.PI*2; const r = Math.sqrt(Math.random())*1.45; const plant = cyl(0.015, 0.035, 0.35+Math.random()*0.45, organic(0x16a34a), [Math.cos(a)*r, 1.28, Math.sin(a)*r], 8); plant.rotation.z = (Math.random()-.5)*0.3; group.add(plant); }
  for (let i = 0; i < (zoo ? 10 : 5); i++) { const fish = sphere(0.09, mat(0xf97316), [(Math.random()-.5)*2.2, 1.18, (Math.random()-.5)*2.2], 16); fish.scale.set(1.6,0.45,0.75); group.add(fish); }
  label(group, zoo ? `DO ${state.oxygen || 6.8} mg/L` : `pH ${state.pH || 7.2}, turbidity ${state.turbidity || 32} NTU`, [0, 2.38, 0], { scale: 0.18 });
}
function addQuadrat(group, state = {}, frequency = false) {
  group.add(box(4.8, 0.07, 3.2, organic(0x365314), [0, 0.82, 0]));
  for (let i = -2; i <= 2; i++) group.add(line([new THREE.Vector3(i*0.7,0.9,-1.55), new THREE.Vector3(i*0.7,0.9,1.55)], 0xf8fafc));
  for (let j = -2; j <= 2; j++) group.add(line([new THREE.Vector3(-1.75,0.91,j*0.7), new THREE.Vector3(1.75,0.91,j*0.7)], 0xf8fafc));
  const plants = frequency ? (state.hits || 7) * 4 : (state.plants || 22);
  for (let i = 0; i < plants; i++) { const x=(Math.random()-.5)*3.3; const z=(Math.random()-.5)*2.9; group.add(cyl(0.015,0.02,0.22+Math.random()*0.22,organic(0x22c55e),[x,1.02,z],8)); group.add(sphere(0.05, organic(0x84cc16), [x,1.22,z], 10)); }
  label(group, frequency ? `frequency ${Math.round((state.hits || 7)/(state.total || 10)*100)}%` : `density ${((state.plants || 22)/(state.area || 1)).toFixed(1)} plants/m2`, [0, 2.0, 0], { scale: 0.18 });
}
function addSoil(group, state = {}) {
  addTray(group, 'soil analysis station');
  const colors=[0x92400e,0x78350f,0xa16207];
  for (let i=0;i<3;i++){ const cup=cyl(0.38,0.32,0.42,glass(0xffffff,.25),[-1+i,1.12,0],32); group.add(cup); group.add(cyl(0.33,0.29,0.25,mat(colors[i]),[-1+i,1.13,0],32)); label(group,['sandy','loamy','clayey'][i],[-1+i,1.72,0],{scale:.1,fontSize:20}); }
  const moisture=((state.wetMass-state.dryMass)/state.dryMass*100)||29;
  label(group, `moisture ${moisture.toFixed(1)}%`, [0,2.15,0], { scale:.17 });
}
function addSpecimens(group, state = {}) {
  addTray(group, 'vegetation specimens');
  const names=['Bacteria','Spirogyra','Moss','Fern','Pine','Lichen'];
  names.forEach((n,i)=>{ const x=-1.5+i*.6; const jar=cyl(.22,.22,.7,glass(0xdbeafe,.28),[x,1.24,0],24); group.add(jar); group.add(sphere(.12,organic(i%2?0x16a34a:0x84cc16),[x,1.25,0],16)); label(group,n,[x,1.82,0],{scale:.08,fontSize:18}); });
  label(group, `selected: ${state.specimen || 'Spirogyra'}`, [0,2.45,0], { scale:.17 });
}
function addFossil(group, state={}) {
  addTray(group, 'fossil evidence');
  const shell = new THREE.Group();
  for(let i=0;i<12;i++){ const r=.12+i*.045; const a=i*.72; shell.add(sphere(r*.42, mat(0x78716c), [Math.cos(a)*r, 0, Math.sin(a)*r], 18)); }
  shell.position.set(0,1.15,0); shell.scale.set(1.7,.18,1.7); group.add(shell);
  label(group, `visible fossil chambers: ${state.chambers || 9}`, [0,2.05,0], { scale:.17 });
}
function addAnimals(group, state={}) {
  addTray(group, 'animal specimen rack');
  const animal=state.animal || 'Earthworm';
  for(let i=0;i<5;i++){ const x=-1.5+i*.75; const body=sphere(.22, mat([0xf97316,0x22c55e,0x38bdf8,0xfacc15,0xa78bfa][i]), [x,1.22,0], 20); body.scale.set(1.5,.45,.65); group.add(body); }
  if(animal==='Earthworm'||animal==='Leech'||animal==='Ascaris'){ for(let i=0;i<12;i++) group.add(sphere(.08, mat(0x9f1239), [-.55+i*.1,1.58,0], 12)); }
  else if(animal==='Honeybee'||animal==='Prawn'){ addCockroachLike(group, [0,1.55,0], 0.65, 0xf59e0b); }
  else if(['Frog','Lizard','Rabbit'].includes(animal)){ addVertebrate(group, animal); }
  label(group, `identify: ${animal}`, [0,2.55,0], { scale:.18 });
}
function addDissection(group, state={}) {
  addTray(group, 'guided dissection model');
  const model=state.model || 'Earthworm';
  const baseColor=model==='Rabbit'?0xd6d3d1:model==='Frog'?0x16a34a:0x9f1239;
  const body=sphere(.55, mat(baseColor,{opacity:.88}), [0,1.25,0], 40); body.scale.set(model==='Earthworm'?2.5:1.6,.42,.55); group.add(body);
  const opened=(state.opened||70)/100;
  group.add(box(1.9*opened,.025,.08,mat(0xfef3c7),[0,1.52,0]));
  ['mouth','crop','stomach','intestine','anus'].forEach((n,i)=>label(group,n,[-1.0+i*.5,1.75,(i%2-.5)*.45],{scale:.09,fontSize:18}));
  label(group, `${model} alimentary canal`, [0,2.35,0], { scale:.17 });
}
function addVertebrate(group, animal='Frog') { const y=1.55; group.add(sphere(.3, mat(animal==='Frog'?0x16a34a:0xd6d3d1), [0,y,0], 24)); group.add(sphere(.18, mat(animal==='Frog'?0x16a34a:0xd6d3d1), [.38,y+.05,0], 18)); for(let i=0;i<4;i++){ const leg=line([new THREE.Vector3((i<2?-.25:.25),y-.1,(i%2?-.2:.2)),new THREE.Vector3((i<2?-.75:.75),y-.35,(i%2?-.55:.55))],0xe5e7eb); group.add(leg); } }
function addConservation(group,state={}) { group.add(box(4.8,.08,3.2,organic(0x14532d),[0,.82,0])); for(let i=0;i<12;i++){ group.add(cyl(.04,.1,.45,organic(0x166534),[(Math.random()-.5)*4,1.05,(Math.random()-.5)*2.5],8)); } group.add(box(.55,.12,1.2,mat(0x94a3b8),[-1.5,.95,0])); group.add(box(.12,.12,3.0,mat(0xfacc15),[0,.96,0])); group.add(sphere(.16,mat(0xf97316),[1.4,1.16,.5],16)); label(group,`habitat ${state.habitat||62}% / corridor ${state.corridor||45}%`,[0,2.1,0],{scale:.16}); }
function addOsmosis(group,state={}) { addTray(group,'potato osmometer'); const potato=sphere(.72,mat(0xb45309),[0,1.18,0],40); potato.scale.y=.42; group.add(potato); const cup=cyl(.24,.28,.78,glass(0xfef3c7,.32),[0,1.55,0],32); group.add(cup); const rise=((state.sucrose||20)*(state.time||45)/1200); group.add(cyl(.18,.18,.25+rise,mat(0x38bdf8,{opacity:.68}),[0,1.35+rise/2,0],32)); label(group,`liquid rise ${rise.toFixed(2)} cm`,[0,2.35,0],{scale:.17}); }
function addPhysiology(group,state={},kind='respiration') { addTray(group, kind); if(kind==='transpiration'||kind==='suction'){ group.add(cyl(.035,.045,1.4,organic(0x166534),[-.55,1.45,0],12)); for(let i=0;i<8;i++){ const leaf=sphere(.16,organic(0x22c55e),[-.35+Math.random()*.6,1.4+Math.random()*.75,(Math.random()-.5)*.6],16); leaf.scale.set(1.4,.1,.65); group.add(leaf); } group.add(line([new THREE.Vector3(.15,1.1,0),new THREE.Vector3(1.2,1.1,0)],0x38bdf8)); }
  else if(kind==='respiration'||kind==='anaerobic'){ const flask=cyl(.55,.38,1.0,glass(0xdbeafe,.3),[-.7,1.28,0],48); group.add(flask); group.add(cyl(.4,.36,.35,mat(0xfde68a,{opacity:.6}),[-.7,1.05,0],48)); group.add(line([new THREE.Vector3(-.25,1.75,0),new THREE.Vector3(.9,1.9,0),new THREE.Vector3(1.3,1.2,0)],0xdbeafe)); const tube=cyl(.28,.28,.6,glass(0xdbeafe,.3),[1.35,1.15,0],32); group.add(tube); }
  else if(kind==='phototropism'){ group.add(box(2.8,.12,1.3,mat(0x78350f),[0,.9,0])); for(let i=0;i<6;i++){ const stem=cyl(.02,.025,.8,organic(0x22c55e),[-1.1+i*.42,1.25,0],8); stem.rotation.z=-0.32; group.add(stem); group.add(sphere(.09,organic(0x84cc16),[-.98+i*.42,1.65,0],12)); } group.add(sphere(.28,mat(0xfacc15,{emissive:0xfacc15,emissiveIntensity:.65}),[2.0,2.3,0],32)); }
  else if(kind==='apicalBud'){ for(let i=0;i<2;i++){ const x=-.6+i*1.2; group.add(cyl(.03,.04,1.2,organic(0x166534),[x,1.45,0],10)); for(let b=0;b<4;b++){ const br=line([new THREE.Vector3(x,1.3+b*.18,0),new THREE.Vector3(x+(i?-.35:.35),1.2+b*.25,.1)],0x22c55e); group.add(br); } if(i===0) group.add(sphere(.08,organic(0x84cc16),[x,2.1,0],12)); } }
  label(group, physiologyLabel(kind,state), [0,2.65,0], { scale:.17 }); }
function physiologyLabel(kind,state){ if(kind==='transpiration')return `${state.surface||'lower'} surface: ${(60/(state.time||75)).toFixed(2)} units/min`; if(kind==='suction')return `water movement ${(((state.leafArea||60)*(state.minutes||30))/1000).toFixed(2)} cm`; if(kind==='respiration')return `rate ${((state.movement||18)/(state.mass||20)).toFixed(2)} mm/g`; if(kind==='anaerobic')return `CO2 bubbling: ${Math.round((state.yeast||70)*(state.time||25)/100)} units`; if(kind==='phototropism')return `curvature ${Math.min(70,((state.light||70)*(state.hours||36)/90)).toFixed(0)} deg`; if(kind==='apicalBud')return `lateral growth ${(((100-(state.auxin||35))*(state.days||10))/100).toFixed(1)} cm`; return 'plant physiology setup'; }
function addGenetics(group,state={}){ addTray(group,'Mendelian seed tray'); const dom=state.dominant||90, rec=state.recessive||32; for(let i=0;i<dom+rec && i<150;i++){ const row=Math.floor(i/15), col=i%15; const color=i<dom?0xfacc15:0x16a34a; group.add(sphere(.045,mat(color),[-1.6+col*.23,1.05,-.9+row*.19],10)); } label(group,`ratio ${(dom/Math.max(rec,1)).toFixed(2)}:1`,[0,2.25,0],{scale:.17}); }
function addImbibition(group,state={}){ addTray(group,'imbibition seeds'); const init=state.initial||20, fin=state.final||32; for(let i=0;i<16;i++){ const big=i<8; const s=sphere(big?.11:.08, mat(0x92400e),[-1.1+(i%8)*.31,1.08,big?.35:-.35],16); s.scale.set(1.2,big?1.0:.75,1); group.add(s); } label(group,`water uptake ${(((fin-init)/init)*100).toFixed(1)}%`,[0,2.05,0],{scale:.17}); }
function addBiofertilizer(group,state={}){ addTray(group,'biofertilizer batch'); const bag=box(1.3,.7,1.0,mat(0x78350f,{opacity:.72}),[0,1.22,0]); group.add(bag); for(let i=0;i<26;i++)group.add(sphere(.035,organic(i%2?0x16a34a:0x84cc16),[(Math.random()-.5)*1,1.62,(Math.random()-.5)*.7],10)); label(group,`moisture ${state.moisture||45}% / day ${state.days||7}`,[0,2.25,0],{scale:.16}); }
function addFrogDev(group,state={}){ addMicroscope(group,state,{tint:0xfde68a}); addMicroscopeField(group,'frogDev',state); }
function addBiochemical(group,state={},kind='starchTest'){ addTray(group,kind); const samples=['control','sample','reagent']; samples.forEach((n,i)=>{ const x=-.8+i*.8; const positive=biochemPositive(kind,state); const color=i===1?(positive?biochemColor(kind,state):0x93c5fd):i===2?0xfacc15:0xe0f2fe; const tube=cyl(.18,.15,.95,glass(0xdbeafe,.28),[x,1.25,0],32); group.add(tube); group.add(cyl(.13,.12,.42,mat(color,{opacity:.72}),[x,1.04,0],32)); label(group,n,[x,1.95,0],{scale:.09,fontSize:18}); }); label(group,biochemLabel(kind,state),[0,2.45,0],{scale:.16}); }
function biochemPositive(kind,state){ if(kind==='starchTest')return ['potato','rice water'].includes(state.sample); if(kind==='proteinTest')return ['egg albumin','milk'].includes(state.sample); if(kind==='urine')return (state.intensity||0)>20; return true; }
function biochemColor(kind,state){ if(kind==='starchTest')return 0x111827; if(kind==='proteinTest')return 0x7c3aed; if(kind==='urine')return {urea:0xfacc15,sugar:0xb45309,albumin:0xf8fafc,'bile salts':0x22c55e}[state.test]||0xb45309; return 0xf97316; }
function biochemLabel(kind,state){ if(kind==='starchTest')return `${state.sample||'sample'}: ${biochemPositive(kind,state)?'blue-black positive':'brown negative'}`; if(kind==='proteinTest')return `${state.sample||'sample'}: ${biochemPositive(kind,state)?'violet positive':'blue negative'}`; if(kind==='urine')return `${state.test||'sugar'} test intensity ${state.intensity||55}%`; return 'biochemical test'; }
function addAmylase(group,state={}){ addBiochemical(group,state,'amylase'); const temp=state.temperature||37, pH=state.pH||7; const activity=Math.max(0,100-Math.abs(temp-37)*3-Math.abs(pH-7)*18); label(group,`amylase activity ${activity.toFixed(0)}%`,[0,2.75,0],{scale:.18}); }
function addBloodSugar(group,state={}){ addTray(group,'blood glucose strip'); group.add(box(2.4,.035,.38,mat(0xf8fafc),[0,1.05,0])); const g=state.glucose||96; const color=g<70?0x60a5fa:g<140?0x22c55e:g<200?0xf97316:0xef4444; group.add(box(.55,.04,.32,mat(color),[.55,1.09,0])); label(group,`${g} mg/dL`,[0,1.75,0],{scale:.19}); }
function addSkeleton(group, state = {}, health = false) {
  const bone = mat(0xf8fafc, { roughness: 0.65, metalness: 0.08 });
  const jointHighlightMat = mat(health ? 0xef4444 : 0x3b82f6, { opacity: 0.25, transparent: true });
  const activeHighlightMat = mat(health ? 0xef4444 : 0x60a5fa, { emissive: health ? 0xef4444 : 0x3b82f6, emissiveIntensity: 0.65, roughness: 0.3 });

  const angle = state.angle !== undefined ? state.angle : 110;
  const mobility = state.mobility !== undefined ? state.mobility : 72;
  
  let neckY = 0;
  let lShoulderZ = -0.15, rShoulderZ = 0.15;
  let lShoulderX = 0, rShoulderX = 0;
  let lElbowX = -0.2, rElbowX = -0.2;
  let lWristX = 0, rWristX = 0;
  let lHipX = 0, rHipX = 0;
  let lKneeX = 0.15, rKneeX = 0.15;
  
  let highlightNeck = false;
  let highlightShoulder = false;
  let highlightElbow = false;
  let highlightHip = false;
  let highlightKnee = false;
  let highlightWrist = false;
  let highlightSpine = false;
  
  if (!health) {
    const rad = angle * Math.PI / 180;
    if (state.joint === 'neck pivot') {
      neckY = (angle - 90) * Math.PI / 180;
      highlightNeck = true;
    } else if (state.joint === 'shoulder ball') {
      lShoulderZ = -rad;
      rShoulderZ = rad;
      highlightShoulder = true;
    } else if (state.joint === 'elbow hinge') {
      lElbowX = -rad;
      rElbowX = -rad;
      highlightElbow = true;
    } else if (state.joint === 'knee hinge') {
      lKneeX = rad * 0.8;
      rKneeX = rad * 0.8;
      highlightKnee = true;
    }
  } else {
    const stressAngle = (100 - mobility) * 0.015;
    if (state.joint === 'spine') {
      highlightSpine = true;
    } else if (state.joint === 'knee') {
      lKneeX = stressAngle;
      highlightKnee = true;
    } else if (state.joint === 'hip') {
      lHipX = -stressAngle * 0.5;
      highlightHip = true;
    } else if (state.joint === 'wrist') {
      lWristX = stressAngle * 0.6;
      highlightWrist = true;
    }
  }

  function makeBone(length, radius) {
    const boneGroup = new THREE.Group();
    const shaft = cyl(radius, radius, length - radius * 2.2, bone, [0, -length / 2, 0], 12);
    boneGroup.add(shaft);
    const top = sphere(radius * 1.5, bone, [0, -radius, 0], 12);
    top.scale.set(1.2, 0.8, 1);
    const bottom = sphere(radius * 1.5, bone, [0, -length + radius, 0], 12);
    bottom.scale.set(1.2, 0.8, 1);
    boneGroup.add(top, bottom);
    return boneGroup;
  }

  function makeDoubleBone(length, radius1, radius2) {
    const boneGroup = new THREE.Group();
    const shaft1 = cyl(radius1, radius1, length - radius1 * 2.2, bone, [-radius1 * 1.1, -length / 2, 0], 12);
    const top1 = sphere(radius1 * 1.4, bone, [-radius1 * 1.1, -radius1, 0], 12);
    const bottom1 = sphere(radius1 * 1.4, bone, [-radius1 * 1.1, -length + radius1, 0], 12);
    boneGroup.add(shaft1, top1, bottom1);

    const shaft2 = cyl(radius2, radius2, length - radius2 * 2.2, bone, [radius2 * 1.1, -length / 2, 0], 12);
    const top2 = sphere(radius2 * 1.4, bone, [radius2 * 1.1, -radius2, 0], 12);
    const bottom2 = sphere(radius2 * 1.4, bone, [radius2 * 1.1, -length + radius2, 0], 12);
    boneGroup.add(shaft2, top2, bottom2);
    return boneGroup;
  }

  function addJointHighlight(g, active, size = 0.08) {
    if (active) {
      const ring = new THREE.Mesh(new THREE.TorusGeometry(size * 1.4, size * 0.35, 8, 24), activeHighlightMat);
      ring.rotation.x = Math.PI / 2;
      g.add(ring);
    } else {
      const ball = sphere(size, jointHighlightMat, [0, 0, 0], 12);
      g.add(ball);
    }
  }

  const skullGroup = new THREE.Group();
  skullGroup.position.set(0, 2.50, 0);
  skullGroup.rotation.y = neckY;
  
  const cranium = sphere(0.16, bone, [0, 0.10, 0]);
  cranium.scale.set(1.0, 1.05, 1.15);
  skullGroup.add(cranium);
  
  const jaw = sphere(0.10, bone, [0, 0.03, 0.05]);
  jaw.scale.set(1.1, 0.6, 1.0);
  skullGroup.add(jaw);
  
  const eyeL = sphere(0.035, mat(0x0f172a, { roughness: 0.9 }), [-0.055, 0.10, 0.14]);
  const eyeR = sphere(0.035, mat(0x0f172a, { roughness: 0.9 }), [0.055, 0.10, 0.14]);
  skullGroup.add(eyeL, eyeR);
  
  const nose = box(0.02, 0.035, 0.02, mat(0x0f172a, { roughness: 0.9 }), [0, 0.065, 0.15]);
  skullGroup.add(nose);
  
  const sutureColor = (state.joint === 'skull suture' && !health) ? (health ? 0xef4444 : 0x60a5fa) : 0xd1d5db;
  const sutureMat = mat(sutureColor, { roughness: 0.5 });
  const coronal = new THREE.Mesh(new THREE.TorusGeometry(0.162, 0.005, 4, 16, Math.PI), sutureMat);
  coronal.position.set(0, 0.10, 0);
  coronal.rotation.y = Math.PI / 2;
  coronal.scale.set(1, 1.05, 1.15);
  skullGroup.add(coronal);
  
  const sagittal = new THREE.Mesh(new THREE.TorusGeometry(0.162, 0.005, 4, 16, Math.PI), sutureMat);
  sagittal.position.set(0, 0.10, 0);
  sagittal.rotation.x = Math.PI / 2;
  sagittal.rotation.y = Math.PI / 2;
  sagittal.scale.set(1.05, 1.0, 1.15);
  skullGroup.add(sagittal);

  addJointHighlight(skullGroup, highlightNeck, 0.055);
  group.add(skullGroup);

  const spineGroup = new THREE.Group();
  const spineStress = highlightSpine ? (100 - mobility) * 0.004 : 0;
  
  for (let i = 0; i < 12; i++) {
    const vertY = 2.36 - i * 0.062;
    const offsetZ = highlightSpine ? Math.sin((12 - i) / 12 * Math.PI) * spineStress * 0.5 : 0;
    const offsetX = highlightSpine ? Math.sin((12 - i) / 12 * Math.PI * 2) * spineStress * 0.4 : 0;
    
    const vertebra = cyl(0.055, 0.055, 0.026, bone, [offsetX, vertY, offsetZ], 12);
    spineGroup.add(vertebra);
    
    const disc = cyl(0.057, 0.057, 0.010, mat(0x94a3b8), [offsetX, vertY - 0.018, offsetZ], 12);
    spineGroup.add(disc);
    
    if (i >= 2 && i <= 9) {
      const ribIndex = i - 2;
      const rScale = 0.18 + Math.sin(ribIndex / 7 * Math.PI) * 0.06;
      
      const ribL = new THREE.Mesh(new THREE.TorusGeometry(rScale, 0.010, 6, 24, Math.PI * 0.75), bone);
      ribL.position.set(-rScale * 0.4, vertY - 0.015, 0.05);
      ribL.rotation.set(Math.PI / 2, 0.1, 0.2);
      spineGroup.add(ribL);
      
      const ribR = ribL.clone();
      ribR.position.x = -ribL.position.x;
      ribR.rotation.y = -ribL.rotation.y;
      ribR.rotation.z = -ribL.rotation.z;
      spineGroup.add(ribR);
    }
  }
  
  const sternumY = 2.10;
  const sternumZ = highlightSpine ? Math.sin(6 / 12 * Math.PI) * spineStress * 0.5 : 0;
  const sternumX = highlightSpine ? Math.sin(6 / 12 * Math.PI * 2) * spineStress * 0.4 : 0;
  const sternum = box(0.028, 0.32, 0.012, bone, [sternumX, sternumY, sternumZ + 0.18]);
  spineGroup.add(sternum);
  
  const clavL = cyl(0.010, 0.010, 0.26, bone, [-0.13, 2.32, 0.05]);
  clavL.rotation.z = Math.PI / 2;
  clavL.rotation.y = -0.2;
  spineGroup.add(clavL);
  
  const clavR = clavL.clone();
  clavR.position.x = -clavL.position.x;
  clavR.rotation.y = -clavL.rotation.y;
  clavR.rotation.z = -clavL.rotation.z;
  spineGroup.add(clavR);
  
  const pelvisY = 1.62;
  const pelvisL = sphere(0.09, bone, [-0.10, pelvisY, 0.02]);
  pelvisL.scale.set(1.4, 0.9, 0.3);
  pelvisL.rotation.set(0.1, 0.2, 0.1);
  spineGroup.add(pelvisL);
  
  const pelvisR = pelvisL.clone();
  pelvisR.position.x = -pelvisL.position.x;
  pelvisR.rotation.y = -pelvisL.rotation.y;
  pelvisR.rotation.z = -pelvisL.rotation.z;
  spineGroup.add(pelvisR);
  
  const sacrum = cyl(0.065, 0.022, 0.10, bone, [0, pelvisY - 0.03, -0.02], 12);
  spineGroup.add(sacrum);
  
  group.add(spineGroup);

  const leftShoulder = new THREE.Group();
  leftShoulder.position.set(-0.28, 2.32, 0);
  leftShoulder.rotation.z = lShoulderZ;
  leftShoulder.rotation.x = lShoulderX;
  addJointHighlight(leftShoulder, highlightShoulder, 0.055);
  
  const leftHumerus = makeBone(0.38, 0.025);
  leftShoulder.add(leftHumerus);
  
  const leftElbow = new THREE.Group();
  leftElbow.position.set(0, -0.38, 0);
  leftElbow.rotation.x = lElbowX;
  addJointHighlight(leftElbow, highlightElbow, 0.045);
  
  const leftForearm = makeDoubleBone(0.32, 0.016, 0.012);
  leftElbow.add(leftForearm);
  
  const leftWrist = new THREE.Group();
  leftWrist.position.set(0, -0.32, 0);
  leftWrist.rotation.x = lWristX;
  addJointHighlight(leftWrist, highlightWrist, 0.035);
  
  const leftHand = box(0.045, 0.07, 0.010, bone, [0, -0.035, 0]);
  leftWrist.add(leftHand);
  leftElbow.add(leftWrist);
  leftShoulder.add(leftElbow);
  group.add(leftShoulder);

  const rightShoulder = new THREE.Group();
  rightShoulder.position.set(0.28, 2.32, 0);
  rightShoulder.rotation.z = rShoulderZ;
  rightShoulder.rotation.x = rShoulderX;
  addJointHighlight(rightShoulder, highlightShoulder, 0.055);
  
  const rightHumerus = makeBone(0.38, 0.025);
  rightShoulder.add(rightHumerus);
  
  const rightElbow = new THREE.Group();
  rightElbow.position.set(0, -0.38, 0);
  rightElbow.rotation.x = rElbowX;
  addJointHighlight(rightElbow, highlightElbow, 0.045);
  
  const rightForearm = makeDoubleBone(0.32, 0.016, 0.012);
  rightElbow.add(rightForearm);
  
  const rightWrist = new THREE.Group();
  rightWrist.position.set(0, -0.32, 0);
  rightWrist.rotation.x = rWristX;
  addJointHighlight(rightWrist, highlightWrist, 0.035);
  
  const rightHand = box(0.045, 0.07, 0.010, bone, [0, -0.035, 0]);
  rightWrist.add(rightHand);
  rightElbow.add(rightWrist);
  rightShoulder.add(rightElbow);
  group.add(rightShoulder);

  const leftHip = new THREE.Group();
  leftHip.position.set(-0.14, 1.60, 0);
  leftHip.rotation.x = lHipX;
  addJointHighlight(leftHip, highlightHip, 0.065);
  
  const leftFemur = makeBone(0.46, 0.032);
  leftHip.add(leftFemur);
  
  const leftKnee = new THREE.Group();
  leftKnee.position.set(0, -0.46, 0);
  leftKnee.rotation.x = lKneeX;
  addJointHighlight(leftKnee, highlightKnee, 0.055);
  
  const leftPatella = sphere(0.026, bone, [0, 0, 0.035], 12);
  leftKnee.add(leftPatella);
  
  const leftShin = makeDoubleBone(0.40, 0.024, 0.012);
  leftKnee.add(leftShin);
  
  const leftAnkle = new THREE.Group();
  leftAnkle.position.set(0, -0.40, 0);
  
  const leftFoot = box(0.055, 0.018, 0.10, bone, [0, -0.009, 0.025]);
  leftAnkle.add(leftFoot);
  leftKnee.add(leftAnkle);
  leftHip.add(leftKnee);
  group.add(leftHip);

  const rightHip = new THREE.Group();
  rightHip.position.set(0.16, 1.60, 0);
  rightHip.rotation.x = rHipX;
  addJointHighlight(rightHip, highlightHip, 0.065);
  
  const rightFemur = makeBone(0.46, 0.032);
  rightHip.add(rightFemur);
  
  const rightKnee = new THREE.Group();
  rightKnee.position.set(0, -0.46, 0);
  rightKnee.rotation.x = rKneeX;
  addJointHighlight(rightKnee, highlightKnee, 0.055);
  
  const rightPatella = sphere(0.026, bone, [0, 0, 0.035], 12);
  rightKnee.add(rightPatella);
  
  const rightShin = makeDoubleBone(0.40, 0.024, 0.012);
  rightKnee.add(rightShin);
  
  const rightAnkle = new THREE.Group();
  rightAnkle.position.set(0, -0.40, 0);
  
  const rightFoot = box(0.055, 0.018, 0.10, bone, [0, -0.009, 0.025]);
  rightAnkle.add(rightFoot);
  rightKnee.add(rightAnkle);
  rightHip.add(rightKnee);
  group.add(rightHip);

  label(group, health ? `${state.joint || 'knee'} mobility ${state.mobility || 72}%` : `${state.joint || 'knee hinge'} angle ${state.angle || 110} deg`, [0, 2.9, 0], { scale: .17 });
}
function addCockroachLike(group,pos=[0,1.2,0],scale=1,color=0x92400e){ const g=new THREE.Group(); g.position.set(...pos); g.scale.setScalar(scale); g.add(sphere(.28,mat(color),[-.38,0,0],24)); g.add(sphere(.4,mat(color),[0,0,0],32)); g.add(sphere(.48,mat(color),[.55,0,0],32)); g.children.forEach((c)=>{c.scale.y=.36;c.scale.z=.58;}); for(let i=0;i<3;i++){ [-1,1].forEach(side=>{ const x=-.18+i*.3; const leg=line([new THREE.Vector3(x,0,side*.22),new THREE.Vector3(x+.15,0,side*.62),new THREE.Vector3(x+.38,0,side*.82)],0x111827); g.add(leg); }); } g.add(line([new THREE.Vector3(-.62,.05,.12),new THREE.Vector3(-1.15,.22,.48)],0x111827)); g.add(line([new THREE.Vector3(-.62,.05,-.12),new THREE.Vector3(-1.15,.22,-.48)],0x111827)); group.add(g); return g; }
function addCockroach(group,state={}){ addTray(group,'cockroach external morphology'); addCockroachLike(group,[0,1.32,0],1.4,0x92400e); ['head','thorax','abdomen','legs','antennae'].forEach((n,i)=>label(group,n,[-1.4+i*.7,2.25,(i%2-.5)*.5],{scale:.09,fontSize:18})); label(group,`view: ${state.view||'dorsal'} / focus ${state.zoomPart||'thorax'}`,[0,2.75,0],{scale:.16}); }

export function buildBiologyModel(root, config, state, actors = {}) {
  addBench(root);
  const kind = config.kind;
  if (['microscope','mitosis','plasmolysis','stomata','anatomyTS','animalTissue','animalMitosis'].includes(kind)) { addMicroscope(root, state, { tint: kind === 'stomata' ? 0xbbf7d0 : 0xf9a8d4 }); addMicroscopeField(root, kind, state); }
  else if (kind === 'microscopeParts') { addMicroscope(root, state); label(root,'eyepiece / objectives / stage / focus / light',[1.35,2.45,0],{scale:.14}); }
  else if (kind === 'flower') addFlower(root, state);
  else if (kind === 'inflorescence') addInflorescence(root, state);
  else if (kind === 'herbarium') addHerbarium(root, state);
  else if (kind === 'mushroom') addMushroom(root, state);
  else if (kind === 'culture') addCulture(root, state);
  else if (kind === 'pond') addPond(root, state, false);
  else if (kind === 'pondZoo') addPond(root, state, true);
  else if (kind === 'quadrat') addQuadrat(root, state, false);
  else if (kind === 'quadrat2') addQuadrat(root, state, true);
  else if (kind === 'soil') addSoil(root, state);
  else if (kind === 'specimens') addSpecimens(root, state);
  else if (kind === 'fossil') addFossil(root, state);
  else if (kind === 'animals') addAnimals(root, state);
  else if (kind === 'dissection') addDissection(root, state);
  else if (kind === 'conservation') addConservation(root, state);
  else if (kind === 'osmosis') addOsmosis(root, state);
  else if (['transpiration','respiration','anaerobic','phototropism','apicalBud','suction'].includes(kind)) addPhysiology(root, state, kind);
  else if (kind === 'genetics') addGenetics(root, state);
  else if (kind === 'imbibition') addImbibition(root, state);
  else if (kind === 'biofertilizer') addBiofertilizer(root, state);
  else if (kind === 'frogDev') addFrogDev(root, state);
  else if (['starchTest','proteinTest','urine'].includes(kind)) addBiochemical(root, state, kind);
  else if (kind === 'amylase') addAmylase(root, state);
  else if (kind === 'bloodSugar') addBloodSugar(root, state);
  else if (kind === 'skeleton') addSkeleton(root, state, false);
  else if (kind === 'skeletonHealth') addSkeleton(root, state, true);
  else if (kind === 'cockroach') addCockroach(root, state);
  else addSpecimens(root, state);
  label(root, config.title, [0, 3.28, -1.8], { scale: 0.18, fontSize: 26, bg: 'rgba(0,0,0,.66)' });
}

export function disposeBioMaterials() {
  MATERIAL_CACHE.forEach((m) => m.dispose && m.dispose());
  MATERIAL_CACHE.clear();
}
