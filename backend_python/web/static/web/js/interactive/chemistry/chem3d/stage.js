import { THREE, createEngine, createOrbitControls } from '../../core/engine.js';
import { buildRoom, BENCH_Y } from '../../core/lab3d-room.js';

export { THREE, BENCH_Y };

// A chemistry bench in the school lab (the same room as the hands-on practicals), an orbit camera
// round the apparatus, and tap/drag picking of named objects. World units are 10 cm; the bench top
// is at BENCH_Y and `world` sits on it.
export function createChemLab(stage, { title, aim = '', subject = 'chemistry', target = [0, 1.4, 0], camera = [0, 3.4, 7.2], minDistance = 2.5, maxDistance = 14 } = {}) {
  const engine = createEngine(stage, { lite: true, noise: true, envIntensity: 0.6, fov: 38, shadows: true, environment: true, exposure: 1.05 });
  if (!engine) return null;
  const { scene, quality, renderer } = engine;
  const cam = engine.camera;
  cam.near = 0.02; cam.updateProjectionMatrix();
  buildRoom(scene, { subject, title, subtitle: aim }, quality, renderer);
  if (quality.tier !== 'low') { renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; }
  const world = new THREE.Group(); world.position.y = BENCH_Y; scene.add(world);
  const t = new THREE.Vector3(target[0], target[1] + BENCH_Y, target[2]);
  cam.position.set(camera[0], camera[1] + BENCH_Y, camera[2]);
  const controls = createOrbitControls(cam, engine.canvas, { target: t, minDistance, maxDistance, minPolar: 0.25, maxPolar: 1.5, damping: 0.1 });

  const ray = new THREE.Raycaster(); const ndc = new THREE.Vector2();
  const targets = [];
  let down = null;
  function hitAt(e) {
    const r = engine.canvas.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, cam);
    const objs = targets.filter((x) => x.enabled !== false).map((x) => x.obj);
    const hit = ray.intersectObjects(objs, true)[0];
    if (!hit) return null;
    let o = hit.object;
    while (o && !targets.some((x) => x.obj === o)) o = o.parent;
    return targets.find((x) => x.obj === o) || null;
  }
  function onDown(e) { down = { x: e.clientX, y: e.clientY, t: performance.now() }; }
  function onUp(e) {
    if (!down) return;
    const moved = Math.hypot(e.clientX - down.x, e.clientY - down.y);
    down = null;
    if (moved > 8) return;
    const h = hitAt(e);
    if (h && h.onTap) h.onTap(h.obj);
  }
  function onMove(e) { if (down) return; const h = hitAt(e); engine.canvas.style.cursor = h ? 'pointer' : ''; }
  engine.canvas.addEventListener('pointerdown', onDown);
  engine.canvas.addEventListener('pointerup', onUp);
  engine.canvas.addEventListener('pointermove', onMove);

  return {
    engine, scene, camera: cam, controls, world, quality, renderer,
    tappable(obj, onTap) { const x = { obj, onTap }; targets.push(x); return x; },
    label(stage2) {
      const el = document.createElement('div');
      el.style.cssText = 'position:absolute;left:0;top:0;pointer-events:none;font:700 11px Poppins,system-ui,sans-serif;padding:3px 9px;border-radius:999px;background:rgba(15,23,42,0.82);color:#f8fafc;white-space:nowrap;z-index:2;will-change:transform';
      (stage2 || stage).appendChild(el);
      const v = new THREE.Vector3();
      return {
        el,
        at(p, dy = 0) {
          v.copy(p).project(cam);
          const vis = v.z < 1 && Math.abs(v.x) < 1.1 && Math.abs(v.y) < 1.1;
          el.style.opacity = vis ? '1' : '0';
          if (vis) el.style.transform = `translate(${((v.x + 1) / 2 * stage.clientWidth).toFixed(1)}px, ${((1 - v.y) / 2 * stage.clientHeight + dy).toFixed(1)}px) translate(-50%, -50%)`;
        },
        remove() { el.remove(); },
      };
    },
    dispose() {
      engine.canvas.removeEventListener('pointerdown', onDown);
      engine.canvas.removeEventListener('pointerup', onUp);
      engine.canvas.removeEventListener('pointermove', onMove);
      controls.dispose(); engine.dispose();
    },
  };
}

// A labelled reagent bottle: amber or clear glass, a screw cap and a printed label.
export function bottle(name, color, { glass = 0xd8e4ea, h = 1.3, r = 0.3 } = {}) {
  const g = new THREE.Group();
  const prof = [[0, 0], [r, 0], [r, h * 0.7], [r * 0.92, h * 0.78], [r * 0.4, h * 0.88], [r * 0.38, h]].map(([x, y]) => new THREE.Vector2(x, y));
  const body = new THREE.Mesh(new THREE.LatheGeometry(prof, 40), new THREE.MeshPhysicalMaterial({ color: glass, roughness: 0.08, transparent: true, opacity: 0.35, clearcoat: 1, depthWrite: false }));
  body.renderOrder = 4;
  const liquid = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.94, r * 0.94, h * 0.6, 32), new THREE.MeshPhysicalMaterial({ color, roughness: 0.15, transparent: true, opacity: 0.85, clearcoat: 0.6 }));
  liquid.position.y = h * 0.31; liquid.renderOrder = 3;
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.42, r * 0.42, h * 0.12, 24), new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.6 }));
  cap.position.y = h * 1.04;
  const c = document.createElement('canvas'); c.width = 256; c.height = 128;
  const x = c.getContext('2d');
  x.fillStyle = '#f8fafc'; x.fillRect(0, 0, 256, 128);
  x.fillStyle = typeof color === 'number' ? `#${color.toString(16).padStart(6, '0')}` : color; x.fillRect(0, 0, 256, 18);
  x.fillStyle = '#0f172a'; x.font = '700 30px Poppins, system-ui, sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle';
  x.fillText(name, 128, 70, 236);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const label = new THREE.Mesh(new THREE.CylinderGeometry(r * 1.005, r * 1.005, h * 0.32, 32, 1, true, -0.9, 1.8), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.7 }));
  label.position.y = h * 0.36;
  [body, liquid, cap, label].forEach((m) => { m.castShadow = true; });
  g.add(liquid, body, cap, label);
  return g;
}
