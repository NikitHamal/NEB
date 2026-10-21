/**
 * Optics bench in 3D: a graduated metre rail on the physics bench with a burning candle, a lens (convex
 * or concave) or a spherical mirror (concave or convex) on a holder, and a white screen. Slide the
 * candle and the screen along the rail (drag them, or use the sliders) and change the focal length.
 * The three principal rays are traced exactly (paraxial, s' = s − y/f at the element), so they meet
 * where 1/f = 1/u + 1/v says the image is; the image stands there as a ghost candle (dashed rays lead
 * back to a virtual one), and a real image appears on the screen, sharp only at v.
 */
import { solve, describe, KINDS } from '../core/optics2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';
import { createChemLab, THREE } from '../chemistry/chem3d/stage.js';

const CM = 0.1; const AXIS = 1.6; const RAYC = [0xe5484d, 0x2563eb, 0x16a34a];
const fmt = (x, d = 0) => x.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

function candle() {
  const g = new THREE.Group();
  const wax = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 1, 24), new THREE.MeshStandardMaterial({ color: 0xf6f1e6, roughness: 0.6 })); g.add(wax);
  const wick = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.05, 6), new THREE.MeshStandardMaterial({ color: 0x111111 })); g.add(wick);
  const flameMat = new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 } },
    vertexShader: 'varying vec3 vP; uniform float uT; void main() { vP = position; vec3 p = position; p.x += sin(uT * 9.0 + p.y * 20.0) * 0.006 * (p.y + 0.05) * 10.0; gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0); }',
    fragmentShader: 'varying vec3 vP; void main() { float h = clamp((vP.y + 0.04) / 0.16, 0.0, 1.0); vec3 c = mix(vec3(1.0, 0.95, 0.75), vec3(1.0, 0.45, 0.08), h); c = mix(vec3(0.35, 0.55, 1.0), c, smoothstep(0.0, 0.18, h)); gl_FragColor = vec4(c * 2.2, 1.0); }',
  });
  const flame = new THREE.Mesh(new THREE.SphereGeometry(0.04, 16, 12), flameMat); flame.scale.set(1, 2.2, 1); g.add(flame);
  const light = new THREE.PointLight(0xffb366, 1.2, 6, 2); g.add(light);
  return { group: g, wax, wick, flame, flameMat, light };
}

export default function init(stage) {
  const S = createChemLab(stage, { title: 'Optics bench', aim: 'Images formed by lenses and mirrors', subject: 'physics', target: [0, AXIS, 0], camera: [1.0, 4.4, 9.6], minDistance: 3, maxDistance: 20 });
  if (!S) return null;
  const { engine, world, camera, controls } = S;
  const hud = createHud(stage);
  const badge = hud.badge('Drag the candle or the screen along the rail', '#2563eb');

  let kind = 'convex-lens'; let f = 20; let u = 45; const h = 8; let screenX = 40; let showScreen = true;
  const r = {};

  // the rail with a cm scale, the holder and the element
  const steel = new THREE.MeshStandardMaterial({ color: 0x9aa3ad, metalness: 0.85, roughness: 0.3 });
  const rail = new THREE.Mesh(new THREE.BoxGeometry(11, 0.12, 0.5), steel); rail.position.y = 0.3; world.add(rail);
  for (const x of [-5.3, 5.3]) { const foot = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.3, 0.9), steel); foot.position.set(x, 0.15, 0); world.add(foot); }
  const scale = (() => { const c = document.createElement('canvas'); c.width = 2048; c.height = 64; const g = c.getContext('2d'); g.fillStyle = '#f8fafc'; g.fillRect(0, 0, 2048, 64); g.fillStyle = '#0f172a'; g.font = '700 22px Poppins, system-ui, sans-serif'; g.textAlign = 'center'; for (let i = 0; i <= 100; i++) { const x = 24 + i / 100 * 2000; g.fillRect(x - 1, 0, 2, i % 10 === 0 ? 30 : i % 5 === 0 ? 20 : 12); if (i % 10 === 0) g.fillText(String(Math.abs(i - 50)), x, 56); } const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; })();
  const tape = new THREE.Mesh(new THREE.PlaneGeometry(10.24, 0.32), new THREE.MeshStandardMaterial({ map: scale, roughness: 0.6 })); tape.rotation.x = -Math.PI / 2; tape.position.set(0, 0.361, 0.05); world.add(tape);
  const post = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, AXIS - 0.36, 12), steel); post.position.set(0, (AXIS + 0.36) / 2, 0); world.add(post);
  const glass = new THREE.MeshPhysicalMaterial({ color: 0xdff2ff, roughness: 0.02, transparent: true, opacity: 0.35, clearcoat: 1, depthWrite: false, side: THREE.DoubleSide });
  const mirrorMat = new THREE.MeshStandardMaterial({ color: 0xe8eef5, metalness: 1, roughness: 0.04, side: THREE.DoubleSide });
  const element = new THREE.Group(); element.position.set(0, AXIS, 0); world.add(element);
  function buildElement() {
    while (element.children.length) element.remove(element.children[0]);
    const R = 0.75;
    if (KINDS[kind].lens) {
      const bulge = kind === 'convex-lens' ? 0.09 : -0.07;
      const pts = []; for (let i = 0; i <= 24; i++) { const t = i / 24; const y = t * R; const x = 0.03 + bulge * (1 - t * t); pts.push(new THREE.Vector2(y, Math.max(0.012, x))); }
      const lens = new THREE.Mesh(new THREE.LatheGeometry(pts.map((p) => new THREE.Vector2(p.x, p.y)), 48), glass);
      const lens2 = lens.clone(); lens2.scale.y = -1;
      const g = new THREE.Group(); g.add(lens, lens2); g.rotation.z = Math.PI / 2; element.add(g);
      const ring = new THREE.Mesh(new THREE.TorusGeometry(R + 0.02, 0.03, 10, 60), steel); ring.rotation.y = Math.PI / 2; element.add(ring);
    } else {
      const sign = kind === 'concave-mirror' ? 1 : -1;
      const cap = new THREE.Mesh(new THREE.SphereGeometry(2.2, 48, 16, 0, Math.PI * 2, 0, 0.35), mirrorMat);
      cap.rotation.z = sign > 0 ? -Math.PI / 2 : Math.PI / 2; cap.position.x = sign > 0 ? -2.2 : 2.2;
      element.add(cap);
      const back = new THREE.Mesh(new THREE.CylinderGeometry(0.78, 0.78, 0.04, 48), new THREE.MeshStandardMaterial({ color: 0x334155 })); back.rotation.z = Math.PI / 2; back.position.x = sign > 0 ? 0.08 : 0.2; element.add(back);
    }
  }
  buildElement();
  const C = candle(); world.add(C.group);
  const ghost = new THREE.Group(); world.add(ghost);
  const ghostWax = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 1, 20), new THREE.MeshBasicMaterial({ color: 0xffd9a0, transparent: true, opacity: 0.28, depthWrite: false }));
  const ghostFlame = new THREE.Mesh(new THREE.SphereGeometry(0.04, 12, 10), new THREE.MeshBasicMaterial({ color: 0xffa040, transparent: true, opacity: 0.6, depthWrite: false })); ghostFlame.scale.set(1, 2.2, 1);
  ghost.add(ghostWax, ghostFlame);
  // the screen: a white card whose picture is drawn from the optics (inverted flame, blurred off focus)
  const sc = document.createElement('canvas'); sc.width = 256; sc.height = 256; const sg = sc.getContext('2d');
  const sTex = new THREE.CanvasTexture(sc); sTex.colorSpace = THREE.SRGBColorSpace;
  const screen = new THREE.Group(); world.add(screen);
  const card = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.6), new THREE.MeshStandardMaterial({ map: sTex, roughness: 0.9, side: THREE.DoubleSide })); card.rotation.y = -Math.PI / 2; card.position.y = AXIS; screen.add(card);
  const sPost = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, AXIS - 0.36, 10), steel); sPost.position.y = (AXIS + 0.36) / 2; screen.add(sPost);
  const rays = RAYC.map((c) => {
    const mat = new THREE.MeshBasicMaterial({ color: c, toneMapped: false }); const dmat = new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: 0.5, toneMapped: false });
    const segs = [0, 1, 2].map(() => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 1, 6), mat); world.add(m); return m; });
    const dashes = Array.from({ length: 14 }, () => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 1, 5), dmat); world.add(m); return m; });
    return { segs, dashes };
  });
  const fMarks = [0, 1, 2, 3].map(() => { const m = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.14, 12), new THREE.MeshBasicMaterial({ color: 0x0f172a })); world.add(m); return m; });
  const lbl = { F: S.label(), F2: S.label(), img: S.label() };

  const panel = createPanel(stage, { title: 'Optics bench' });
  panel.chips({ label: 'Element', options: Object.keys(KINDS).map((key) => ({ value: key, label: KINDS[key].label })), value: kind, onChange: (v) => { kind = v; buildElement(); } });
  const fS = panel.slider({ label: 'Focal length |f|', min: 5, max: 40, step: 1, value: f, format: (v) => `${v} cm`, onChange: (v) => { f = v; } });
  const uS = panel.slider({ label: 'Candle distance u', min: 2, max: 50, step: 1, value: u, format: (v) => `${v} cm`, onChange: (v) => { u = v; } });
  const xS = panel.slider({ label: 'Screen position', min: 2, max: 50, step: 0.5, value: screenX, format: (v) => `${v} cm`, onChange: (v) => { screenX = v; } });
  panel.toggle({ label: 'Screen on the rail', value: true, onChange: (v) => { showScreen = v; } });
  const st = panel.stats([{ key: 'u', label: 'u' }, { key: 'v', label: 'v' }, { key: 'm', label: 'm = −v/u' }, { key: 'f', label: 'f (signed)' }]);
  const nature = panel.readout({ label: 'Image', value: '—' });
  const check = panel.readout({ label: '1/u + 1/v', value: '—' });
  panel.info('Real-is-positive: u, v and f are positive for real objects, real images and converging elements; a negative v means a virtual image. Put the candle inside F of a convex lens to make a magnifying glass.');

  // drag the candle or the screen along the rail
  const ray = new THREE.Raycaster(); const ndc = new THREE.Vector2(); const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0); const hit = new THREE.Vector3();
  let drag = null;
  const pick = (e) => { const rr = engine.canvas.getBoundingClientRect(); ndc.set(((e.clientX - rr.left) / rr.width) * 2 - 1, -((e.clientY - rr.top) / rr.height) * 2 + 1); ray.setFromCamera(ndc, camera); };
  engine.canvas.addEventListener('pointerdown', (e) => {
    pick(e);
    if (ray.intersectObject(C.group, true).length) drag = 'candle'; else if (showScreen && ray.intersectObject(screen, true).length) drag = 'screen'; else return;
    controls.enabled = false; e.stopImmediatePropagation();
  }, true);
  engine.canvas.addEventListener('pointermove', (e) => {
    if (!drag) return; pick(e); if (!ray.ray.intersectPlane(plane, hit)) return;
    const x = world.worldToLocal(hit.clone()).x / CM;
    if (drag === 'candle') { u = Math.max(2, Math.min(50, Math.round(-x))); uS.set(u); } else { screenX = Math.max(2, Math.min(50, Math.round(x * 2) / 2)); xS.set(screenX); }
  });
  const up = () => { if (drag) { drag = null; controls.enabled = true; } };
  engine.canvas.addEventListener('pointerup', up); engine.canvas.addEventListener('pointercancel', up);

  const A = new THREE.Vector3(); const B = new THREE.Vector3(); const Y = new THREE.Vector3(0, 1, 0); const D = new THREE.Vector3();
  function seg(m, a, b) { D.subVectors(b, a); const L = D.length(); m.visible = L > 1e-4; if (!m.visible) return; m.position.copy(a).addScaledVector(D, 0.5); m.scale.set(1, L, 1); m.quaternion.setFromUnitVectors(Y, D.normalize()); }
  const toW = (xcm, ycm) => new THREE.Vector3(xcm * CM, AXIS + ycm * CM, 0);
  function drawScreen(v, hi, real) {
    sg.fillStyle = '#f8fafc'; sg.fillRect(0, 0, 256, 256);
    sg.strokeStyle = 'rgba(15,23,42,0.08)'; sg.strokeRect(6, 6, 244, 244);
    if (!real || !isFinite(v) || !KINDS[kind].lens) { sTex.needsUpdate = true; return; }
    const defocus = Math.abs(screenX - v); const blur = Math.min(24, defocus * 1.2);
    const size = Math.min(110, Math.abs(hi) * 1.6 * 16 / 1.6 / 8 * 8);
    const k = 1 / (1 + defocus * 0.15);
    sg.save(); sg.filter = `blur(${blur.toFixed(1)}px)`; sg.translate(128, 128); sg.scale(1, -Math.sign(hi || -1));
    const grd = sg.createRadialGradient(0, size * 0.25, 1, 0, size * 0.1, size * 0.6); grd.addColorStop(0, `rgba(255,250,220,${k})`); grd.addColorStop(0.5, `rgba(255,170,60,${0.9 * k})`); grd.addColorStop(1, 'rgba(255,140,40,0)');
    sg.fillStyle = grd; sg.beginPath(); sg.ellipse(0, size * 0.25, size * 0.18, size * 0.45, 0, 0, Math.PI * 2); sg.fill();
    sg.fillStyle = `rgba(240,225,200,${0.8 * k})`; sg.fillRect(-size * 0.12, -size * 0.9, size * 0.24, size * 0.9);
    sg.restore(); sTex.needsUpdate = true;
  }

  let tick = 0;
  engine.setUpdate((dt, time) => {
    controls.update(dt);
    solve(kind, u, f, h, r);
    const lens = KINDS[kind].lens; const fold = lens ? 1 : -1;
    C.group.position.set(-u * CM, 0.36 + h * CM / 2, 0); C.wax.scale.y = h * CM; C.wax.position.y = 0; C.wick.position.y = h * CM / 2 + 0.02; C.flame.position.y = h * CM / 2 + 0.09; C.flameMat.uniforms.uT.value = time;
    C.light.position.y = h * CM / 2 + 0.1; C.light.intensity = 1 + Math.sin(time * 13) * 0.08;
    screen.visible = showScreen && lens; screen.position.x = screenX * CM;
    // principal rays from the flame tip, through the element, folded back for mirrors
    const sIns = [0, -h / u, Math.abs(r.F - u) > 1e-3 ? h / (r.F - u) : 0];
    const reach = 60;
    rays.forEach((R, i) => {
      const s = sIns[i]; const ym = h + s * u; const sOut = s - ym / r.F;
      seg(R.segs[0], A.copy(toW(-u, h)), B.copy(toW(0, ym)));
      const dEnd = r.real && !r.inf && r.v < reach ? Math.max(r.v + 8, 20) : reach;
      seg(R.segs[1], A.copy(toW(0, ym)), B.copy(toW(fold * dEnd, ym + sOut * dEnd)));
      R.segs[2].visible = false;
      const virt = !r.real && !r.inf;
      R.dashes.forEach((m, j) => {
        m.visible = virt;
        if (!virt) return;
        const d0 = r.v * j / R.dashes.length; const d1 = r.v * (j + 0.5) / R.dashes.length;
        seg(m, A.copy(toW(fold * d0, ym + sOut * d0)), B.copy(toW(fold * d1, ym + sOut * d1)));
      });
    });
    ghost.visible = !r.inf && Math.abs(r.v) < 120;
    if (ghost.visible) { const xi = fold * r.v; ghost.position.set(xi * CM, AXIS + r.hi * CM / 2, 0); ghost.scale.set(Math.min(3, Math.abs(r.m)) || 1, 1, 1); ghostWax.scale.y = Math.abs(r.hi) * CM; ghostFlame.position.y = Math.sign(r.hi) * (Math.abs(r.hi) * CM / 2 + 0.09); ghostFlame.scale.y = 2.2 * Math.sign(r.hi); }
    const marks = lens ? [Math.abs(f), 2 * Math.abs(f), -Math.abs(f), -2 * Math.abs(f)] : [-r.F, -2 * r.F];
    fMarks.forEach((m, i) => { const x = marks[i]; m.visible = x !== undefined && Math.abs(x) <= 50; if (m.visible) m.position.set(x * CM, 0.46, 0.22); });
    lbl.F.el.textContent = 'F'; lbl.F.at(A.set(fMarks[0].position.x, 0.8 + 0.62, 0.22)); lbl.F2.el.textContent = '2F'; lbl.F2.at(A.set(fMarks[1].position.x, 0.8 + 0.62, 0.22));
    if (!fMarks[1].visible) lbl.F2.el.style.opacity = '0';
    lbl.img.el.textContent = r.inf ? '' : `${r.real ? 'real' : 'virtual'} image`; if (ghost.visible) lbl.img.at(A.set(fold * r.v * CM, 0.8 + AXIS + r.hi * CM + 0.3 * Math.sign(r.hi || 1), 0)); else lbl.img.el.style.opacity = '0';
    if ((tick++ & 3) === 0) drawScreen(r.v, r.hi, r.real);
    st.u.set(`${fmt(u, 0)} cm`); st.v.set(r.inf ? '∞' : `${fmt(r.v, 1)} cm`); st.m.set(r.inf ? '∞' : fmt(r.m, 2)); st.f.set(`${fmt(r.F, 0)} cm`);
    check.set(r.inf ? '1/u = 1/f → v = ∞' : `${fmt(1 / u, 3)} + ${fmt(1 / r.v, 3)} = ${fmt(1 / u + 1 / r.v, 3)} = 1/${fmt(r.F, 1)}`);
    nature.set(describe(r));
    badge.set(lens && r.real && !r.inf && showScreen ? (Math.abs(screenX - r.v) < 0.8 ? `Sharp image on the screen at v = ${fmt(r.v, 1)} cm` : 'Slide the screen until the flame is sharp') : describe(r));
  });
  engine.start();

  stage.__optics = { set: (k2, ff, uu, sx) => { kind = k2; f = ff; u = uu; if (sx) screenX = sx; buildElement(); fS.set(ff); uS.set(uu); }, result: () => ({ ...r }) };
  return { dispose() { panel.dispose(); hud.dispose(); Object.values(lbl).forEach((l) => l.remove()); sTex.dispose(); S.dispose(); } };
}
